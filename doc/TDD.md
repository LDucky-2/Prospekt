# Technical Design Document (TDD) - Prospekt

| Field | Value |
|---|---|
| Product | Prospekt |
| Status | Current implementation |
| API framework | FastAPI |
| Frontend | React 19, TypeScript 7, Vite 8 |

## 1. Technology Stack

| Component | Technology | Role |
|---|---|---|
| Frontend | React, TypeScript, Vite | Public browsing and administration SPA |
| API | FastAPI | HTTP routing, validation, OpenAPI |
| ORM | SQLModel and SQLAlchemy | Models and persistence |
| Local database | SQLite | Development database |
| Production database | PostgreSQL-compatible SQL database | Persistent deployment storage |
| Password security | pwdlib Argon2 | Password hashing and verification |
| Access tokens | PyJWT, HS256 | Short-lived authentication |
| Refresh tokens | Opaque random token, SHA-256 hash | Revocable browser sessions |
| Testing | pytest, HTTPX | Backend tests |
| Hosting | Vercel | Frontend/API services and rewrites |

## 2. Architecture

```text
Browser
  |
  | HTTPS
  v
Vite React SPA
  |
  | /api/* JSON, Bearer access token, HttpOnly refresh cookie
  v
FastAPI application
  |
  | SQLModel
  v
SQLite locally / PostgreSQL in production
```

`vercel.json` routes `/api/*` to the FastAPI service and every other path to the Vite frontend. The frontend calls same-origin API paths and does not contain database credentials.

## 3. Backend Structure

```text
backend/
  main.py
  app/
    config.py
    database.py
    errors.py
    migrations.py
    activity/
    admin/
    auth/
    rbac/
    universities/
  migrations/
  tests/
```

* `main.py` configures FastAPI, CORS, security headers, routers, health, and initial-admin seeding.
* `app/universities` contains public read and protected content CRUD.
* `app/auth` contains login, refresh, logout, profile, password, and session logic.
* `app/admin` contains user management and activity-log endpoints.
* `app/rbac` contains permission constants and the reusable role check dependency.
* `app/activity` contains audit models, repository methods, and recording.
* `app/database.py` creates the SQLModel engine and database tables.

## 4. Frontend Structure

```text
frontend/src/
  App.tsx
  index.css
  main.tsx
  services/api.ts
```

All application state and UI are implemented in `App.tsx`. `services/api.ts` stores the access token in `sessionStorage`, stores expiry metadata, sends credentials and bearer headers, refreshes once after a 401, and exposes university/auth/admin operations.

## 5. Data Model

### Core entities

* `University`: identity, name, website, timestamps, and prospectuses.
* `Prospectus`: university foreign key, admissions session, overview, application/admit/exam dates, and units.
* `Unit`: prospectus foreign key, name, academic background, and total seats.
* `EligibilityRule`: one-to-one unit eligibility information.
* `MarkDistribution`: one-to-one unit mark details.
* `SeatInfo`: one-to-one unit seat/quota details.
* `ImportantDate`: one-to-one unit date details.
* `FeeStructure`: one-to-one unit fee/payment details.

All detailed unit relationships use cascade deletion and one-to-one ownership on the unit.

### Security entities

* `AppUser`: UUID, email, name, Argon2 password hash, editor/admin role, active status, login counters, lockout time, and timestamps.
* `RefreshToken`: UUID, user, session UUID, SHA-256 token hash, expiry, revocation time, timestamps, IP, and user-agent.
* `ActivityLog`: UUID, action, account and target identifiers, detail, IP, user-agent, and timestamp.

When an account is deleted, its historical activity rows retain the recorded email and other event details while their `account_id` reference is cleared. This keeps deletion compatible with the audit foreign key and preserves searchable history.

## 6. REST API

| Method | Path | Authorization | Success |
|---|---|---|---|
| GET | `/api/v1/universities` | Public | 200 |
| GET | `/api/v1/universities/{id}` | Public | 200 |
| POST | `/api/v1/universities` | Admin university:create | 201 |
| PUT | `/api/v1/universities/{id}` | Prospectus update permission | 200 |
| DELETE | `/api/v1/universities/{id}` | Prospectus delete permission | 204 |
| POST | `/api/v1/universities/{id}/prospectuses` | Prospectus create permission | 201 |
| PUT | `/api/v1/universities/{id}/prospectuses/{id}` | Prospectus update permission | 200 |
| DELETE | `/api/v1/universities/{id}/prospectuses/{id}` | Prospectus delete permission | 204 |
| POST | `/api/v1/auth/login` | Public | 200 |
| POST | `/api/v1/auth/refresh` | Refresh cookie | 200 |
| POST | `/api/v1/auth/logout` | Authenticated | 204 |
| GET | `/api/v1/auth/me` | Authenticated | 200 |
| PATCH | `/api/v1/auth/me` | Authenticated | 200 |
| POST | `/api/v1/auth/password` | Authenticated | 204 |
| GET | `/api/v1/auth/sessions` | Authenticated | 200 |
| DELETE | `/api/v1/auth/sessions/{id}` | Authenticated | 204 |
| GET/PATCH/POST/DELETE | `/api/v1/admin/users*` | Admin user permissions | 200/201/204 |
| GET | `/api/v1/admin/logs` | Admin log permission | 200 |
| GET | `/api/health` | Public | 200 |

Errors use `{"detail":"message"}` JSON responses; request validation can return an array of issue objects in `detail`, which the frontend formats into readable messages. Editor-creation passwords must be at least eight characters, with a matching client-side check.

## 7. Authentication Design

### Login and access token

1. The client posts email and password.
2. The server verifies Argon2 plus the configured password pepper.
3. A 15-minute HS256 JWT is issued with `sub`, `role`, `iat`, and `exp`.
4. The JWT secret comes from `JWT_SECRET`.

### Refresh

1. The login creates an opaque 48-byte random token.
2. Only a SHA-256 token hash is persisted.
3. The raw token is stored in an HttpOnly, Strict refresh cookie.
4. Refresh revokes the used record and creates a new record/token.
5. If a revoked token is reused, the server revokes all refresh sessions for that user.

### Frontend behavior

* Access token and expiry are kept in `sessionStorage`.
* Refresh cookie is managed by the browser and cannot be read by JavaScript.
* On 401, one refresh is attempted and the original request is retried once.
* If refresh fails, local access-token state is cleared.

## 8. RBAC Design

The permission module defines prospectus, university, user, and log permissions. The dependency resolves `CurrentUser`, looks up the role's permissions, and raises 403 for a missing permission.

```python
def require_permission(permission: Permission) -> Callable[..., AppUser]:
    def check(user: CurrentUser) -> AppUser:
        if permission not in ROLE_PERMISSIONS.get(user.role, set()):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return check
```

Editors receive prospectus create/update/delete permissions. Admins receive those permissions plus university creation and account/log permissions.

## 9. Security Threat Defenses

| Threat | Defence |
|---|---|
| Password database leak | Argon2 hash plus server pepper |
| Stolen access token | 15-minute lifetime; signature and expiry verification |
| Refresh-token database leak | Only SHA-256 hashes are persisted |
| Refresh-token reuse | Revoke all user sessions on reuse |
| Brute-force login | Five failures cause a 15-minute account lock |
| Privilege escalation | Server-side role/permission dependencies |
| Account access after ban/deactivation | Refresh and protected authentication checks active status |
| XSS | Refresh token is HttpOnly |
| CSRF | SameSite=Strict refresh cookie and same-origin API usage |
| CORS misuse | Explicit allowed origins |
| SQL injection | SQLModel/SQLAlchemy parameterized queries |
| Repository secrets | Production secrets are environment variables |

## 10. Deployment

`vercel.json` declares FastAPI and Vite services and rewrites. The intended production database is PostgreSQL. SQLite is the fallback local database.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` or `POSTGRES_URL` | PostgreSQL or SQLite database URL |
| `JWT_SECRET` | Access-token signing secret |
| `PASSWORD_PEPPER` | Extra password-hashing secret |
| `ACCESS_TOKEN_MINUTES` | Access-token lifetime |
| `REFRESH_TOKEN_DAYS` | Refresh-session lifetime |
| `INITIAL_ADMIN_EMAIL` | Initial admin email |
| `INITIAL_ADMIN_PASSWORD` | Initial admin password |
| `INITIAL_ADMIN_NAME` | Initial admin display name |
| `FRONTEND_URL` | Allowed deployed frontend origin |
| `VERCEL` | Set by Vercel to enable production-secret validation |

## 11. Testing

Run the backend suite:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

Build the frontend:

```powershell
cd frontend
npm run build
```

Verified result:

* Backend: 9 tests passed.
* Frontend: TypeScript/Vite production build passed.
