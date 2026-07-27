from app.graphs.state import ReviewState

from app.agents.security_agent import SecurityAgent
from app.agents.quality_agent import QualityAgent

from app.agents.testgap_agent import TestGapAgent
from app.report.risk_score import RiskScorer
from app.report.executive_summary import ExecutiveSummaryGenerator
from app.report.markdown import MarkdownReportGenerator
from app.utils.findings import deduplicate_findings
from app.utils.timer import measure
summary_generator = ExecutiveSummaryGenerator()


risk_scorer = RiskScorer()
security_agent = SecurityAgent()
quality_agent = QualityAgent()

testgap_agent = TestGapAgent()

report = MarkdownReportGenerator()
from app.report.statistics import RepositoryStatistics

stats_generator = RepositoryStatistics()

from app.agents.documentation_agent import DocumentationAgent

documentation_agent = DocumentationAgent()

@measure("Documentation")
def documentation_node(state: ReviewState):
    
    if "documentation" not in state["enabled_agents"]:
        print(">>> Skipping Documentation Agent")
        return {}

    print(">>> Documentation")

    findings = documentation_agent.analyze(state["repo_path"],state["changed_files"],)
   

    return {
        "findings": findings,
       
    }
@measure("Statistics")
def statistics_node(state):

    findings = deduplicate_findings(state["findings"])

    stats = stats_generator.generate(findings)

    return {
        "stats": stats,
    }

@measure("Report")
def report_node(state):
    print("Before dedup:", len(state["findings"]))
    generator = MarkdownReportGenerator()
    findings = deduplicate_findings(state["findings"])

    markdown = generator.generate(
        findings=findings,
        score={
            "score": state["score"],
            "grade": state["grade"],
            "risk": state["risk"],
        },
        stats=state["stats"],
        executive_summary=state["summary"],
    )

    # Unique path per review — prevents concurrent reviews overwriting each other
    review_id = state.get("review_id", "unknown")
    report_path = f"reports/{review_id}.md"
    generator.save(markdown, report_path)

    return {
         "report_path": report_path,
    "score": state["score"],
    "grade": state["grade"],
    "risk": state["risk"],
    "summary": state["summary"],
    "human_approved": state["human_approved"],
    "reviewer_feedback": state["reviewer_feedback"],
       
    }

@measure("Summary")
def summary_node(state):

    findings = deduplicate_findings(state["findings"])

    summary = summary_generator.generate(
        findings=findings,
        score={
            "score": state["score"],
            "grade": state["grade"],
            "risk": state["risk"],
        },
    )

    return {
        "summary": summary,
    }

@measure("Risk")
def risk_node(state):

    findings = deduplicate_findings(state["findings"])

    result = risk_scorer.calculate(findings)

    return {
        "score": result["score"],
        "grade": result["grade"],
        "risk": result["risk"],
    }

@measure("Security")
def security_node(state: ReviewState):
    
    if "security" not in state["enabled_agents"]:
        print(">>> Skipping Security Agent")
        return {}

    print(">>> Security")

    findings = security_agent.analyze(state["repo_path"],state["changed_files"])
  

    return {
        "findings": findings,
        
    }

@measure("Quality")
def quality_node(state: ReviewState):
    
    if "quality" not in state["enabled_agents"]:
        print(">>> Skipping Quality Agent")
        return {}

    print(">>> Quality")

    findings = quality_agent.analyze(state["repo_path"], state["changed_files"],)
   

    print("Quality findings:", len(findings))

    return {
        "findings": findings,
  
    }

@measure("TestGap")
def testgap_node(state: ReviewState):
  
    if "testgap" not in state["enabled_agents"]:
        print(">>> Skipping TestGap Agent")
        return {}

    print(">>> TestGap")

    findings = testgap_agent.analyze(state["repo_path"],state["changed_files"])
   

    print("TestGap findings:", len(findings))

    return {
        "findings": findings,
       
    }

def merge_node(state):
    return {
        "report_path": state["report_path"]
    }