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

## Final deployment setup

The application uses a hosted PostgreSQL database in production and SQLite only for local development.

Set these values in Vercel:

- `DATABASE_URL` or `POSTGRES_URL`: hosted PostgreSQL connection string
- `JWT_SECRET`: long random signing secret
- `PASSWORD_PEPPER`: long random password pepper
- `ACCESS_TOKEN_MINUTES`: access-token lifetime, recommended value `15`
- `REFRESH_TOKEN_DAYS`: refresh-session lifetime
- `INITIAL_ADMIN_EMAIL`: email of the first admin account
- `INITIAL_ADMIN_PASSWORD`: password of the first admin account
- `INITIAL_ADMIN_NAME`: name of the first admin account
- `FRONTEND_URL`: exact deployed frontend origin

Never commit real values or the `.env` file.

### Local test commands

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

```powershell
cd frontend
npm run build
```

### Vercel smoke test

1. Open the deployed frontend.
2. Log in with the initial admin account.
3. Confirm public prospectuses are readable.
4. Confirm the admin Users and Logs pages work.
5. Create and delete a test editor account.
6. Create a test university only as admin.
7. Open `/api/docs` and confirm it loads.
8. Reload a deep link and verify the React page remains accessible.




Public - private key pair