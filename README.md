# Policy Search Tool — Full-Stack Asynchronous RAG Monorepo

[![Frontend Deployment](https://github.com/sigilmancer/policy-search-tool/blob/main/.github/workflows/frontend-deploy.yml/badge.svg)](https://github.com/sigilmancer/policy-search-tool/blob/main/.github/workflows/frontend-deploy.yml)  

[![Backend CI](https://github.com/sigilmancer/policy-search-tool/blob/main/.github/workflows/backend-ci.yml/badge.svg)](https://github.com/sigilmancer/policy-search-tool/blob/main/.github/workflows/backend-ci.yml)

A full-stack RAG (Retrieval-Augmented Generation) tool built to parse, index, and query policies. 

This project is structured as a decoupled monorepo and features automated CI/CD workflows for testing and deployment, completely separated by workspace paths.

 **Live Frontend Website:** [https://sigilmancer.github.io/policy-search-tool/](https://sigilmancer.github.io/policy-search-tool/)  
 **Interactive API Docs:** [https://policy-search-api.onrender.com/docs](https://policy-search-api.onrender.com/docs)

---

## System Architecture

The project is split cleanly into frontend and backend directories to isolate service boundaries and simplify local development:

### Asynchronous Backend (`/backend`)
*   **Framework:** Built with **Python 3.11** and **FastAPI** utilising async/await endpoints for speed.
*   **CORS Configuration:** Setup with strict `CORSMiddleware` parameters to securely allow requests from the GitHub Pages frontend domain.
*   **Cloud Hosting:** Deployed as a web service on **Render**, locked into a stable Python environment to guarantee dependency compatibility (`pydantic`).

### Frontend UI (`/frontend`)
*   **Framework:** Built with **Astro 5.x** for fast static generation, using **Svelte** islands to handle interactive state transitions on the client side.
*   **Styling:** Compiled using the **Tailwind CSS Vite plugin** for quick, responsive utility styling.
*   **Cloud Hosting:** Hosted for free on **GitHub Pages**, using explicit `.nojekyll` flags to prevent default platform compilation overrides.

---

## CI/CD & Automated DevOps Workflow

The repository relies on custom GitHub Actions workflows to automate code quality and deployment:

1.  **Path-Isolated Workflows:** Using `paths:` filters, changes inside `/frontend` only trigger Node 22 frontend builds, while changes inside `/backend` only trigger Python test runners.
2.  **Automated Issue Tracking:** If an integration test fails during a push to `main`, a native GitHub CLI (`gh`) step automatically opens a new bug report under the **Issues** tab and assigns it straight to the committer.
3.  **Clean History Management:** Practiced Git squashing to compress experimental trial commits into clean, professional feature checkpoints.

---

## Testing & Quality Assurance

The backend features an asynchronous integration test suite using **Pytest** and **HTTPX (ASGITransport)**. This allows testing of the entire API lifecycle in-memory—completely isolating the network state and avoiding local port leaks.

### Run Backend Tests Locally:
```bash
cd backend
# Windows: .\venv\Scripts\Activate.ps1 | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
pytest -v
```

---

## Local Setup & Execution

To run the full stack locally, execute the following commands in separate terminal windows:

### 1. Start the Backend API
```bash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1 | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Start the Frontend Client
```bash
cd frontend
npm install
npm run dev
```
