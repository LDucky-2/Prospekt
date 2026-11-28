# Product Requirements Document (PRD) - Prospekt

| Field | Value |
|---|---|
| Product | Prospekt |
| Status | Implementation complete for the current repository build |
| Audience | Students, guardians, content editors, and administrators |
| Platform | React + TypeScript SPA and FastAPI REST API |
| Hosting | Vercel monorepo deployment |

## 1. Purpose

Prospekt makes university admission prospectus information easier to browse. It presents admission sessions, units, eligibility rules, marks, seats, dates, fees, and official websites as structured web data instead of dense PDF text.

## 2. Problem Statement

Admission prospectuses combine rules for several academic units and admissions sessions. Users currently need to search and interpret long documents manually, while administrators need a controlled way to keep structured admission data current.

## 3. Target Users

| Role | User | Main tasks | Restrictions |
|---|---|---|---|
| Visitor | Student or guardian | Browse universities and sessions, filter content, view unit details and official links | Cannot change data or manage accounts |
| Editor | Authenticated content maintainer | Create, update, and delete prospectus and unit data | Cannot create a university or manage users/logs |
| Admin | Authenticated administrator | Manage all prospectus content and manage editor/admin accounts and logs | Cannot change its own account through the account-management actions |

## 4. Goals and Success Measures

| ID | Goal | Measurable success criterion |
|---|---|---|
| G-1 | Make public prospectus data accessible | Anonymous requests to university and prospectus endpoints return 200 responses |
| G-2 | Preserve admissions sessions and nested unit data | One university can contain multiple sessions; each session can contain multiple units |
| G-3 | Protect content changes | Missing or invalid credentials return 401; insufficient permissions return 403 |
| G-4 | Secure administrative sessions | Argon2 password hashing, short-lived JWT access tokens, HttpOnly refresh cookies, and refresh rotation are active |
| G-5 | Provide account accountability | Login, logout, account, role, status, password, university, and prospectus actions are written to the activity log |
| G-6 | Support reliable deployment | The Vite build and backend test suite complete successfully |

## 5. Scope

### In scope

* Public university and prospectus browsing.
* Multiple academic sessions per university.
* Multiple units per prospectus.
* Eligibility, mark distribution, seat, date, and fee data.
* Academic background fields for unit filtering in the UI.
* University and prospectus creation, editing, and deletion.
* Admin and editor roles.
* Editor account creation, role/status changes, deletion, search, and filters.
* Login, logout, refresh, profile update, password change, and session management endpoints.
* Activity logs with search, action, and IP filters.
* Login lockout after five failed attempts.
* Responsive React interface and OpenAPI documentation.

### Not implemented in the current repository

* PDF upload or automated PDF extraction.
* Student registration or public user accounts.
* Group or group-ownership features.
* Unit comparison and browser bookmarks.
* CSV export.
* Bulk account or content actions.
* Automated CI/CD workflow configuration.
* Public signup or password reset.

### Assumptions and constraints

* SQLite is used for local development; PostgreSQL is intended for production.
* A production database provider and Vercel environment variables must be configured by the project owner.
* The initial administrator is created from environment variables.
* Text values such as marks and GPA fields accept non-numeric text because source prospectuses vary in format.

## 6. Functional Features

| ID | Feature | Priority | Implementation status |
|---|---|---|---|
| F-1 | Public university/prospectus browsing | Must | Implemented |
| F-2 | Academic background filtering | Must | Implemented in the UI data model |
| F-3 | Structured unit admission details | Must | Implemented |
| F-4 | Admin/editor authentication | Must | Implemented |
| F-5 | Refresh-token rotation and logout | Must | Implemented |
| F-6 | Account lockout | Must | Implemented |
| F-7 | Prospectus CRUD | Must | Implemented |
| F-8 | Account role/status management | Must | Implemented |
| F-9 | Activity logs | Should | Implemented |
| F-10 | Session list/revoke API | Should | Implemented |
| F-11 | PDF extraction | Could | Not implemented |
| F-12 | Bookmarks/comparison | Could | Not implemented |

## 7. User Stories

* US-01: As a visitor, I want to browse universities so that I can identify relevant admissions information.
* US-02: As a visitor, I want to open a session and view its units so that I can see only relevant admission data.
* US-03: As a visitor, I want to view eligibility, marks, seats, dates, and fees so that I can prepare.
* US-04: As a visitor, I want to open an official website so that I can access the source portal.
* US-05: As an editor, I want to log in so that I can update prospectus records.
* US-06: As an editor, I want to create or update prospectuses so that published data stays accurate.
* US-07: As an editor, I want to delete content only when authorized so that accidental or unauthorized deletion is prevented.
* US-08: As an admin, I want to create editor accounts so that maintainers can update content.
* US-09: As an admin, I want to change account roles and statuses so that access remains controlled.
* US-10: As an admin, I want to filter and search the activity log so that I can audit account and content actions.
* US-11: As an administrator, I want refreshable sessions so that I do not lose access unnecessarily.
* US-12: As a user, I want to change my password or profile so that I can maintain my account.

## 8. Success Metrics

* 8 backend tests pass.
* Frontend TypeScript/Vite production build succeeds.
* Public reads do not require authentication.
* Editor accounts can manage prospectus content.
* Admin accounts can manage users and logs.
* Deactivated accounts are rejected and refreshes are revoked.
* `GET /api/health` returns `{"status":"ok"}`.
* `/api/docs` exposes the live OpenAPI schema.
