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

2. **Asynchronous Webhook Processing** ⚡
   - GitHub Webhooks are instantly received by the FastAPI backend and pushed to a **Redis Queue**.
   - A dedicated **ARQ Background Worker** picks up the jobs and processes the heavy LLM pipelines asynchronously, ensuring the API remains fast and resilient.

3. **Automated Remediation (Human-in-the-Loop)** 🛠️
   - When the pipeline detects a vulnerability, execution pauses for Human Review.
   - With a single click on the dashboard, the AI can securely rewrite the vulnerable code and automatically push the patch directly to your GitHub Pull Request.

4. **Context-Aware ChatBot** 💬
   - Ask questions about your security scan directly in the dashboard! The embedded ChatBot uses strict grounding rules to only answer based on the generated markdown report, eliminating hallucination.

5. **Interactive Analytics Dashboard** 📊
   - View historical scan reports in a stunning dark-mode React UI.
   - Includes interactive Donut and Bar charts powered by `recharts` to quickly understand risk distribution across tools and severity levels.

---

## 🏗️ Architecture

ReviewGuard AI is built with:

- **Backend:** FastAPI (Python), LangGraph (Agentic Workflow), SQLite (Checkpointer & History), ChromaDB (RAG).
- **Background Jobs:** Redis, ARQ (Python).
- **Frontend:** React, Vite, Tailwind CSS, Recharts.
- **LLM Provider:** Groq (Llama-3).
- **DevOps:** Docker, Docker Compose, Ngrok (Local Tunneling).
- **Documentation:**
  - [GitHub Actions Integration](docs/GITHUB_ACTIONS.md)
  - [Multi-Agent Architecture](docs/AGENTS.md)
  - [System Architecture & Production Roadmap](SYSTEM_DESIGN.md)

---

## 🐳 Quick Start with Docker

The fastest way to get ReviewGuard AI running. No Python, Node, or tool installations required!

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- A Groq API Key
- A GitHub Personal Access Token

### 1. Clone & Configure

```bash
git clone <repository-url>
cd reviewguard_ai

# Configure backend secrets
cp backend/.env.example backend/.env
# Edit backend/.env and set GROQ_API_KEY, GITHUB_TOKEN, NGROK_AUTHTOKEN, and REVIEWGUARD_API_KEY
```

### 2. Build & Run

```bash
docker compose up -d --build
```
*(This spins up the FastAPI Backend, ARQ Worker, Redis Database, React Frontend, and Ngrok tunnel).*

### 3. Open the Dashboard

- **Frontend:** [http://localhost](http://localhost)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **Ngrok Tunnel (For Webhooks):** [http://localhost:4040](http://localhost:4040)

To stop: `docker compose down`

---

## 🚀 Manual Setup (Without Docker)

### Prerequisites

- Node.js (v18+)
- Python (3.11+)
- Redis Server running on port 6379
- Git installed on your system

### 1. Setup the Backend

```bash
cd backend
uv sync # Or use venv and pip install -r requirements.txt

# Set up your environment variables
cp .env.example .env
```

### 2. Setup the Frontend

```bash
cd frontend
npm install

# Create a local environment file for the frontend
echo "VITE_API_KEY=your_secure_api_key_here" > .env.local
```

### 3. Run the Application

Open three terminal windows:

**Terminal 1 (Backend API):**
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (ARQ Worker):**
```bash
cd backend
uv run arq app.worker.WorkerSettings
```

**Terminal 3 (Frontend):**
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
