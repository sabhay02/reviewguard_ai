import os
import subprocess
from app.graphs.state import ReviewState
from app.llm.groq import LLMClient
from app.utils.timer import measure
from app.utils.configs import settings
from collections import defaultdict

llm = LLMClient()

@measure("Auto-Remediation")
def remediation_node(state: ReviewState):
    print("\n>>> ENTERED AUTO-REMEDIATION NODE <<<")
    print(f"Total findings in state: {len(state['findings'])}")
    for f in state['findings']:
        print(f" - {f.file}: {f.severity}")
    
    # Filter for all actionable findings
    actionable_findings = [f for f in state["findings"] if f.severity.upper() in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]]
    print(f"Actionable findings count: {len(actionable_findings)}")
    
    if not actionable_findings:
        return {
            "summary": "## 🚀 Auto-Remediation Skipped\nNo actionable findings were found to remediate.\n\n" + state["summary"]
        }

    # Group findings by file
    findings_by_file = defaultdict(list)
    for finding in actionable_findings:
        findings_by_file[finding.file].append(finding)

    repo_path = state["repo_path"]
    
    # Iterate over files and rewrite them
    for filename, findings in findings_by_file.items():
        # Handle cases where the parser returned an absolute path or a path already prefixed with the temp directory
        if os.path.isabs(filename):
            file_path = filename
        elif filename.replace("\\", "/").startswith(repo_path.replace("\\", "/")):
            file_path = filename
        else:
            file_path = os.path.join(repo_path, filename)
            
        # Final fallback check
        if not os.path.exists(file_path) and os.path.exists(filename):
            file_path = filename
            
        print(f"[Auto-Remediation] Checking file: {filename}")
        print(f"[Auto-Remediation] Resolved full path: {file_path}")
        if not os.path.exists(file_path):
            print(f"[Auto-Remediation] SKIPPING: Path does not exist!")
            continue
            
        print(f"[Auto-Remediation] Found file! Proceeding to LLM rewrite...")
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        finding_descriptions = "\n".join([f"- Line {f.line}: {f.review.title} ({f.severity})\n  {f.review.summary}\n  Recommendation: {f.review.recommendation}" for f in findings])
        
        prompt = f"""
You are an expert security engineer and software developer.

I have a file `{filename}` with the following security vulnerabilities:
{finding_descriptions}

Here is the current source code of `{filename}`:
```
{content}
```

Please rewrite the ENTIRE file to securely fix these vulnerabilities while maintaining the original functionality. 
Ensure you apply the recommendations (e.g. use parameterized SQL queries instead of string concatenation, use safe hashing algorithms instead of MD5, use subprocess safely instead of shell injection).

OUTPUT ONLY THE RAW FIXED CODE. Do not include markdown code blocks (```), explanations, or any other text. Output exactly what should be written to the file.
"""
        
        fixed_content = llm.generate(prompt)
        # Clean up any potential markdown blocks if the LLM didn't listen
        if fixed_content.startswith("```"):
            lines = fixed_content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            fixed_content = "\n".join(lines)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)
            
        print(f"Rewrote {filename} to fix vulnerabilities. Content length: {len(fixed_content)}")

    # Git commit and push
    push_success = False
    
    owner = state.get("owner")
    repo_name = state.get("repo_name")
    
    if owner and repo_name:
        try:
            subprocess.run(["git", "config", "user.name", "ReviewGuard AI"], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "ai@reviewguard.dev"], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True, capture_output=True)
            
            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_path, capture_output=True, text=True)
            print(f"[Auto-Remediation] git status: '{status.stdout}'")
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", "🚀 Auto-Remediation: Fixed security vulnerabilities"], cwd=repo_path, check=True, capture_output=True)
                
                # Setup auth and push
                token = settings.github_token
                
                # Since the repo is cloned, we need to extract the current branch
                branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path, capture_output=True, text=True).stdout.strip()
                
                repo_url = f"https://{token}@github.com/{owner}/{repo_name}.git"
                subprocess.run(["git", "remote", "set-url", "origin", repo_url], cwd=repo_path, check=True, capture_output=True)
                subprocess.run(["git", "push", "origin", branch], cwd=repo_path, check=True, capture_output=True)
                push_success = True
        except subprocess.CalledProcessError as e:
            print(f"Git Command Failed: {e.cmd}")
            print(f"STDOUT: {e.stdout.decode('utf-8') if e.stdout else 'None'}")
            print(f"STDERR: {e.stderr.decode('utf-8') if e.stderr else 'None'}")
        except Exception as e:
            print(f"Error pushing auto-remediation commit: {e}")

        new_summary = "## 🚀 Auto-Remediation Complete\nI have successfully re-written the vulnerable files and pushed a commit to your branch! Please review the code changes on GitHub.\n\n" + state["summary"]
        if not push_success:
             new_summary = "## ⚠️ Auto-Remediation Failed to Push\nI successfully re-written the vulnerable files locally, but failed to push the commit to GitHub. Check the server logs.\n\n" + state["summary"]
    else:
        new_summary = "## 🚀 Local Auto-Remediation Complete\nI have successfully re-written the vulnerable files locally in your repository!\n\n" + state["summary"]

    return {
        "summary": new_summary,
        "action": "approve" # Reset action so it doesn't loop
    }
