Prospectus:

Prospectus solves the "wall-of-text" information overload in university admission prospectuses by extracting dense PDFs into bite-sized, unit-filtered, structured web data for candidates and guardians in Bangladesh.

Key Features
    - Remove irrelevent information depending on the candidates, who can select their background (Science/Arts/Commerce) and view only the specific rules and information that apply to them.
    - Showing important informations as structured tables for mark distributions, negative marking rules, and seat capacity.
    - Clear Breakdown of the important scheduled dates(application, exam)
    - Fast Search & Direct Links: Instantly query specific keywords or jump directly to official payment/application portals.


Tech Stack & Architecture

This repository is structured as a monorepo designed to compile and deploy seamlessly to Vercel as a single unified project using Vercel Serverless Functions.
    - Frontend: React, TypeScript, Vite
    - Backend: Python 3.11+, FastAPI


## Local Development

Run the backend and frontend in separate terminals. The frontend calls the backend through Vite's `/api` development proxy, so browser requests and database access still go through FastAPI.

**Terminal 1 — backend** (from the repository root):

```powershell
cd backend
fastapi dev main.py
```

FastAPI serves the API at `http://127.0.0.1:8000`.

**Terminal 2 — frontend** (from the repository root):

```powershell
cd frontend
npm run dev
```

Open the Vite URL shown in the terminal (usually `http://localhost:5173`). Keep both processes running while developing. The Vite proxy forwards `/api/*` to `http://127.0.0.1:8000`; do not connect the frontend directly to the database.


#