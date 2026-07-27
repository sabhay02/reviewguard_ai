# 🛡️ ReviewGuard AI

**ReviewGuard AI** is an intelligent, agent-based DevSecOps platform designed to automatically scan, analyze, and optionally auto-remediate vulnerabilities in your GitHub repositories and Pull Requests.

Powered by a LangGraph AI workflow, ReviewGuard AI orchestrates multiple static analysis tools, aggregates the findings using LLMs, and presents a beautiful, interactive dashboard for engineering and security teams.

---

## ✨ Key Features

1. **Multi-Agent Pipeline with RAG Support** 🤖
   - ReviewGuard orchestrates a team of specialized AI Agents using **LangGraph**:
     - **Security Agent:** Hunts for critical vulnerabilities, hardcoded secrets, and injection flaws (via Bandit, Semgrep, Gitleaks).
     - **Quality Agent:** Analyzes cyclomatic complexity, code smells, performance bottlenecks, and enforces PEP8 compliance (via Pylint and Ruff).
     - **Test Gap Agent:** Identifies missing unit tests and code paths lacking coverage to ensure robust deployments.
     - **Documentation Agent:** Reviews inline comments, docstrings, and READMEs to ensure code is easily maintainable.
     - **Supervisor Agent:** Aggregates findings from all sub-agents, deduplicates overlapping issues, and formats the final markdown report.
   - **Retrieval-Augmented Generation (RAG):** Integrates ChromaDB to index repository code and security knowledge bases, providing the AI agents with deep, contextual awareness of your specific codebase when generating reports and fixes.

2. **Interactive Analytics Dashboard** 📊
   - View historical scan reports in a stunning dark-mode UI.
   - Includes interactive Donut and Bar charts powered by `recharts` to quickly understand risk distribution across tools and severity levels.

3. **Automated Remediation** ⚡
   - With a single click, AI can generate and apply code fixes for identified vulnerabilities.
   - Automatically commits and pushes the fixes to your GitHub Pull Request.

4. **Context-Aware ChatBot** 💬
   - Ask questions about your security scan directly in the dashboard! The embedded ChatBot has full context of the markdown report.

5. **Robust Security Architecture** 🔒
   - **API Authentication:** Backend endpoints are fully secured by an API Key to prevent unauthorized access.
   - **CORS Lockdown:** Strict Cross-Origin policies.
   - **Anti-SSRF:** URL validation to prevent Server-Side Request Forgery.
   - **Anti-Injection:** Hardened `subprocess` execution to prevent command injection.

---

## 🏗️ Architecture

ReviewGuard AI is built with:

- **Backend:** FastAPI (Python), LangGraph (Agentic Workflow), SQLite (Checkpointer & History), ChromaDB (RAG).
- **Frontend:** React, Vite, Tailwind CSS, Recharts.
- **LLM Provider:** Groq (Llama-3).

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.10+)
- Git installed on your system
- A Groq API Key
- GitHub Personal Access Token (for PR comments and Auto-Fix pushes)

### 1. Clone the repository

```bash
git clone repository
cd reviewguard_ai
```

### 2. Setup the Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate`

pip install -r requirements.txt

# Set up your environment variables
cp .env.example .env
# Edit .env and add GROQ_API_KEY, GITHUB_TOKEN, and REVIEWGUARD_API_KEY
```

### 3. Setup the Frontend

```bash
cd frontend
npm install

# Create a local environment file for the frontend
echo "VITE_API_KEY=your_secure_api_key_here" > .env.local
```

> **Note:** Make sure that `REVIEWGUARD_API_KEY` in the backend `.env` matches `VITE_API_KEY` in the frontend `.env.local` so the dashboard can authenticate with the API!

### 4. Run the Application

Open two terminal windows:

**Terminal 1 (Backend):**

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**

```bash
cd frontend
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

---

## 🔒 Security Notice

Do **NOT** expose the backend port (`8000`) directly to the public internet without implementing API Authentication (e.g., JWT or API Keys). The backend has the ability to clone repositories and execute code, which requires strict access controls in a production environment.

## 📄 License

MIT License
