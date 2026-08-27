# Policy Search tool: An Architectural Monorepo Case Study

An end-to-end, full-stack demonstration combining deterministic local context extraction with modern API boundaries, engineered to match digital delivery standards.

## System Architecture
This repository is organised as a decoupled monorepo to isolate service boundaries cleanly:
* **/backend** — asynchronous text processing layer powered by Python and FastAPI.
* **/frontend** — static presentation layer engineered with Astro, utilising a hydrated Svelte island for reactive client state transitions.

## Automated Quality Engineering
The backend features a fully asynchronous integration test suite using **Pytest** and **HTTPX (`ASGITransport`)**. This enables executing full end-to-end API lifecycle evaluation entirely in-memory—completely isolating the network state and eliminating port leakage.

### To Run Backend Tests:
```bash
cd backend
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest -v
```

### To Run the Applications Locally:
* **Backend API server:** `cd backend && uvicorn main:app --reload`
* **Frontend dashboard client:** `cd frontend && npm install && npm run dev`
