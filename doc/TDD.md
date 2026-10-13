# Technical Design Document (TDD) — Prospekt

| Field | Value |
| --- | --- |
| Product | Prospekt |
| Version | MVP + Beta |
| Releases | MVP — Mid-term, Beta — Final |
| Status | Draft |
| Related docs | [Product Requirements Document (PRD)](https://www.google.com/search?q=PRD.md), [Software Requirements Specification (SRS)](https://www.google.com/search?q=SRS.md) |

## 1. Overview

* **MVP:** A FastAPI REST API backed by Supabase PostgreSQL (SQLite locally) providing public read endpoints for universities, units, eligibility criteria, mark distributions, seat data, important dates, and fee structures. Deployed on Vercel alongside the Vite + React frontend.
* **Beta:** Adds admin authentication (JWT + HttpOnly refresh cookies, Argon2 hashing), admin RBAC, an administrative CRUD portal for managing prospectus data, and Alembic database migrations.

## 2. Tech Stack

| Layer | Choice | Why | Release |
| --- | --- | --- | --- |
| API Framework | FastAPI | Automatic OpenAPI docs, robust data validation, and high performance | MVP |
| ORM / Models | SQLModel | Combines Pydantic validation with SQLAlchemy relational modeling | MVP |
| Production DB | PostgreSQL on Supabase | Managed Postgres, robust web table editor, and built-in transaction pooling for serverless | MVP |
| Local DB | SQLite | Zero-configuration local file database for development | MVP |
| Database Driver | `psycopg[binary]` | Standard connection driver for PostgreSQL | MVP |
| Frontend | Vite + React + TypeScript | Responsive, modern UI framework | MVP |
| Hosting | Vercel | Unified static frontend and serverless backend hosting (`vercel.json`) | MVP |
| Migrations | Alembic | Version-controlled database schema changes | Beta |
| JWT Handling | PyJWT | Secure encoding and decoding of admin access tokens | Beta |
| Password Hashing | `pwdlib[argon2]` | Industry-standard Argon2 hashing for admin passwords | Beta |

## 3. Architecture

```
[Browser / Frontend] --(GET /api/v1/*)--> [FastAPI Backend on Vercel]
[Admin Portal] --(POST/PATCH /api/v1/admin/*)--> [FastAPI Backend on Vercel]
[FastAPI Backend on Vercel] --(SQLModel Queries)--> [(Supabase PostgreSQL)]

```

Routing configuration in `vercel.json` directs all requests matching `/api/*` to the FastAPI backend service and all other requests to the frontend static build. Consequently, backend routes begin with `/api/v1`. API documentation is served at `/api/docs`:

```python
app = FastAPI(title="Prospekt API", docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None)

```

### 3.1 Request Flow (Public Read — MVP)

```
[Client / Browser] --(GET /api/v1/universities)--> [FastAPI Router]
[FastAPI Router] --(fetch_universities)--> [Service / DB Session]
[Service / DB Session] --(SELECT * FROM university)--> [Supabase PostgreSQL]
[Supabase PostgreSQL] --(University records)--> [Service / DB Session]
[Service / DB Session] --(List of universities)--> [FastAPI Router]
[FastAPI Router] --(200 OK JSON)--> [Client / Browser]

```

### 3.2 Admin Authentication & Mutation Flow (Beta)

```
[Admin Client] --(POST /api/v1/admin/auth/login)--> [Auth Router]
[Auth Router] --(Verify credentials)--> [Supabase PostgreSQL]
[Supabase PostgreSQL] --(Admin verified)--> [Auth Router]
[Auth Router] --(200 OK + Set-Cookie refresh_token)--> [Admin Client]
[Admin Client] --(POST /api/v1/admin/universities + Bearer Token)--> [Auth Router]
[Auth Router] --(Verify JWT & admin role)--> [Auth Router]
[Auth Router] --(Insert record)--> [Supabase PostgreSQL]
[Supabase PostgreSQL] --(Success)--> [Auth Router]
[Auth Router] --(201 Created)--> [Admin Client]

```

## 4. Project Structure

```
backend/
  main.py              # FastAPI app setup, router inclusion, health check, static file mounting
  app/
    config.py          # Environment settings (DATABASE_URL, JWT settings)
    database.py        # SQLModel engine, session dependency (`SessionDep`)
    security.py        # (Beta) Argon2 hashing, JWT verification, refresh token hashing
    universities/      # University domain folder
      router.py        # Public university & unit endpoints
      models.py        # University, Unit, Eligibility, MarkDistribution, SeatInfo, Date, Fee models
      schemas.py       # Pydantic request/response schemas
      service.py       # Business logic and queries
    admin/             # (Beta) Admin management domain
      router.py        # Admin CRUD endpoints for prospectus data
      auth_router.py   # Admin login, refresh, logout
      dependencies.py  # `get_current_admin`, role verification
  alembic/             # (Beta) Migration scripts
  alembic.ini
  requirements.txt
frontend/
  src/
    App.tsx            # Routes, layout, and theme configuration
    pages/             # Public Home, UniversityDetail, UnitDetail, AdminLogin, AdminDashboard
    components/        # UnitFilter, MarkDistributionTable, DateCountdown, UnitComparator
    services/          # API client fetch wrappers
docs/
  PRD.md
  SRS.md
  TDD.md

```

## 5. Data Model & ERD

### 5.1 Core Tables (MVP)

* **`university`**: `id` (PK), `name` (varchar), `session` (varchar), `website_url` (varchar), `created_at`, `updated_at`.
* **`unit`**: `id` (PK), `university_id` (FK), `unit_name` (varchar, e.g. "A Unit"), `background` (varchar: Science/Arts/Commerce), `total_seats` (int).
* **`eligibility_rule`**: `id` (PK), `unit_id` (FK), `min_ssc_gpa` (float), `min_hsc_gpa` (float), `combined_gpa` (float), `second_time_allowed` (bool), `second_time_penalty_marks` (float), `subject_requirements` (text).
* **`mark_distribution`**: `id` (PK), `unit_id` (FK), `total_marks` (int), `mcq_marks` (int), `written_marks` (int), `negative_marking_penalty` (float), `pass_mark_total` (float), `subject_breakout` (json).
* **`seat_info`**: `id` (PK), `unit_id` (FK), `general_seats` (int), `quota_breakdown` (json).
* **`important_date`**: `id` (PK), `university_id` (FK), `application_start` (datetime), `application_end` (datetime), `admit_card_start` (datetime), `exam_date` (datetime).
* **`fee_structure`**: `id` (PK), `unit_id` (FK), `application_fee` (float), `payment_methods` (text).

### 5.2 Admin Tables (Beta)

* **`admin_user`**: `id` (PK), `email` (varchar, unique), `name` (varchar), `password_hash` (varchar), `role` (varchar: `admin`, `super_admin`), `failed_login_count` (int), `locked_until` (datetime), `created_at`, `updated_at`.
* **`refresh_token`**: `id` (PK), `admin_id` (FK), `token_hash` (char 64), `expires_at` (datetime), `revoked_at` (datetime).

## 6. REST API Design

Base path: `/api/v1`. All payloads and responses use JSON.

### 6.1 Public Endpoints (MVP)

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/v1/universities` | List all universities and active sessions | Public |
| `GET` | `/api/v1/universities/{id}` | Get university details and important dates | Public |
| `GET` | `/api/v1/units` | List units (supports query params `university_id`, `background`) | Public |
| `GET` | `/api/v1/units/{id}` | Get full unit details (eligibility, marks, seats, fees, portal link) | Public |
| `GET` | `/api/v1/search` | Search universities, units, and requirements by keyword | Public |
| `GET` | `/api/health` | System health check | Public |

### 6.2 Admin Endpoints (Beta)

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `POST` | `/api/v1/admin/auth/login` | Admin login | Public (Guest Admin) |
| `POST` | `/api/v1/admin/auth/refresh` | Refresh access token via cookie | Refresh Cookie |
| `POST` | `/api/v1/admin/auth/logout` | Revoke refresh token | Admin |
| `GET` | `/api/v1/admin/profile` | Get logged-in admin profile | Admin |
| `PATCH` | `/api/v1/admin/profile` | Update admin name or password | Admin |
| `POST` | `/api/v1/admin/universities` | Create a new university record | Admin |
| `PATCH` | `/api/v1/admin/universities/{id}` | Update university details | Admin |
| `DELETE` | `/api/v1/admin/universities/{id}` | Delete university and associated units | Super Admin |
| `POST` | `/api/v1/admin/units` | Create a unit and its criteria | Admin |
| `PATCH` | `/api/v1/admin/units/{id}` | Update unit criteria, marks, or seats | Admin |
| `DELETE` | `/api/v1/admin/units/{id}` | Delete a unit | Admin |

## 7. Configuration & Deployment

* **Environment Variables:**
* `DATABASE_URL`: Connection string for Supabase PostgreSQL (transaction pooler port `6543`) or local SQLite.
* `JWT_SECRET`: Secure cryptographic secret for signing admin JWT tokens (minimum 32 bytes).
* `ACCESS_TOKEN_MINUTES`: Access token expiration (default: `15`).
* `REFRESH_TOKEN_DAYS`: Refresh token lifetime (default: `7`).


* **Supabase Integration:** Configured via Vercel environment variables using Supavisor transaction pooling with `NullPool` in SQLAlchemy to manage serverless connection lifecycles efficiently.
* **Deployment Pipeline:** Automatic deployments on pushes to `main` via the Vercel GitHub integration. Database migrations via Alembic are executed prior to pushing schema updates.

## 8. Security

* **Password Hashing:** Argon2 hashing via `pwdlib` for all administrator accounts.
* **Token Security:** Short-lived JWT access tokens paired with HttpOnly, Secure, SameSite=Strict refresh cookies restricted to the `/api/v1/admin/auth` path.
* **Brute-Force Protection:** Account lockout mechanism triggering `429 Too Many Requests` after 5 failed login attempts within 15 minutes.
* **Security Headers:** Enforced globally via `vercel.json` (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`).