# Software Requirements Specification (SRS) — Prospekt

| Field | Value |
| --- | --- |
| Product | Prospekt |
| Version | MVP + Beta |
| Releases | MVP — Mid-term, Beta — Final |
| Status | Draft |
| Related docs | [Product Requirements Document (PRD)](https://www.google.com/search?q=PRD.md), [Technical Design Document (TDD)](https://www.google.com/search?q=TDD.md) |

## 1. Introduction

### 1.1 Purpose

This document specifies the software requirements for Prospekt, covering the public MVP data API and interface, as well as the Beta administrative portal, authentication, and security hardening deployed on Vercel.

### 1.2 Scope

* **MVP:** Public access to university admission prospectus data, unit-based filtering, mark distributions, fees, seat info, dates, and search functionality. No user login or registration is required.
* **Beta:** Authenticated admin portal for content management, admin roles, profile management, and client-side productivity features (comparisons and bookmarks).

### 1.3 Definitions

| Term | Meaning |
| --- | --- |
| Prospectus | The official rulebook and information guide released by a university for admission applicants |
| Unit | An academic grouping (e.g., Unit A for Science, Unit B for Arts) with specific eligibility and exam rules |
| Mark Distribution | The breakdown of examination scoring (MCQ marks, written marks, negative marking penalties) |
| CRUD | Create, Read, Update, Delete operations |
| REST | Architectural style utilizing standard HTTP methods (GET, POST, PATCH, DELETE) |
| JWT | JSON Web Token used for authenticating administrators |
| RBAC | Role-Based Access Control restricting system access based on user roles (`admin`, `super_admin`) |

## 2. Overall Description

### 2.1 System Context

```
[Browser / Student] --(HTTPS Public GET)--> [Prospekt API: FastAPI on Vercel]
[Admin / Content Manager] --(HTTPS Auth POST/PATCH)--> [Prospekt API: FastAPI on Vercel]
[Prospekt API: FastAPI on Vercel] --(SQLModel)--> [(PostgreSQL: Supabase)]

```

### 2.2 User Roles & Access

| Role | Release | Authentication | Permissions |
| --- | --- | --- | --- |
| **Guest / Information Seeker** | MVP & Beta | None (Anonymous) | Access all public read endpoints, search, unit filtering, view mark distributions, dates, and fees. |
| **Admin / Content Provider** | Beta | Required (JWT login) | Manage university prospectus entries, create/update unit criteria, mark distributions, and schedules. |
| **Super Admin** | Beta | Required (JWT login) | Full administrative access, including managing other admin accounts and system configurations. |

### 2.3 Use Cases

**MVP (Public Access)**

* Browse Universities & Units
* Filter by Academic Background (Science / Arts / Commerce)
* View Mark Distribution & Negative Marking Rules
* Check Important Dates & Fees
* Search Prospectus Bits by Keyword
* Access Official Portal Links

**Beta (Admin Access)**

* Admin Login / Logout
* Manage Universities (Create, Update, Delete)
* Manage Units & Eligibility Rules
* Manage Mark Distributions & Penalties
* Manage Seats & Important Dates
* Manage Admin Accounts & Roles

## 3. Functional Requirements

### 3.1 Public Prospectus Data — MVP

| ID | Requirement | Release | Story |
| --- | --- | --- | --- |
| FR-01 | The system shall provide an endpoint to list all available universities and their academic sessions. | MVP | US-01 |
| FR-02 | The system shall allow clients to retrieve units associated with a university, filtered by background (Science, Arts, Commerce). | MVP | US-01 |
| FR-03 | The system shall return detailed eligibility criteria (minimum SSC/HSC GPA, combined GPA, second-time allowed, subject prerequisites) for any unit. | MVP | US-01 |
| FR-04 | The system shall return mark distribution details, including total marks, MCQ vs written breakdown, and negative marking penalties. | MVP | US-02 |
| FR-05 | The system shall return seat distribution statistics, including total seats and quota allocations (Freedom Fighter, Tribal, etc.). | MVP | US-02 |
| FR-06 | The system shall return important dates (application start/end, admit card download, exam date). | MVP | US-04 |
| FR-07 | The system shall return fee structures and payment gateway instructions (bKash, Nagad, Teletalk). | MVP | US-03 |
| FR-08 | The system shall support keyword search across university names, unit titles, and prospectus requirements. | MVP | US-05 |
| FR-09 | The system shall provide direct URLs to official university application portals. | MVP | US-06 |
| FR-10 | The system shall expose `GET /api/health` returning status `ok`. | MVP | US-07 |
| FR-11 | The system shall publish interactive OpenAPI documentation at `/api/docs`. | MVP | US-07 |

### 3.2 Admin Authentication & Management — Beta

| ID | Requirement | Release | Story |
| --- | --- | --- | --- |
| FR-12 | The system shall authenticate administrators using email and password, returning an access token and setting a secure refresh token cookie. | Beta | US-08 |
| FR-13 | The system shall issue new access tokens via the refresh token endpoint and rotate refresh tokens. | Beta | US-08 |
| FR-14 | The system shall allow administrators to log out, revoking active refresh tokens and clearing cookies. | Beta | US-08 |
| FR-15 | The system shall allow authenticated administrators to create, update, and delete university and unit prospectus records. | Beta | US-09 |
| FR-16 | The system shall restrict write operations (`POST`, `PATCH`, `DELETE`) strictly to authenticated admin users (`401` or `403` otherwise). | Beta | US-09, US-10 |
| FR-17 | Super admins shall be able to list, create, and modify other admin accounts. | Beta | US-10 |
| FR-18 | Administrators shall be able to view their profile and update their name or password. | Beta | US-11 |
| FR-19 | After 5 consecutive failed login attempts, the system shall lock the admin account for 15 minutes (`429 Too Many Requests`). | Beta | US-11 |

## 4. Non-Functional Requirements

| ID | Category | Requirement | Release |
| --- | --- | --- | --- |
| NFR-01 | Performance | 95% of public read requests shall respond in under 500 ms (excluding cold starts). | MVP |
| NFR-02 | Persistence | All prospectus data shall be stored in Supabase PostgreSQL and persist across redeploys. | MVP |
| NFR-03 | Security | All client-server communication shall use HTTPS enforced by Vercel. | MVP |
| NFR-04 | Security | Database credentials and secrets shall reside exclusively in Vercel environment variables. | MVP |
| NFR-05 | Security | Admin passwords shall be hashed using Argon2; plain passwords shall never be stored or logged. | Beta |
| NFR-06 | Maintainability | Database schema changes shall be managed via Alembic migrations. | Beta |
| NFR-07 | Usability | The user interface shall be fully responsive and optimized for mobile devices used by students. | MVP |

## 5. Acceptance Criteria

### MVP (Public Features)

* **AC-01: List Universities (FR-01)**
* Given active university records exist in the database, when a client sends `GET /api/v1/universities`, then the response is `200 OK` with a JSON list of universities.


* **AC-02: Unit Filtering (FR-02)**
* Given units exist for Science and Arts, when a client queries units with `background=Science`, then only Science units are returned.


* **AC-03: Public Read Access (FR-03 to FR-09)**
* When an anonymous client requests eligibility, mark distributions, dates, or search results, the system responds with `200 OK` without requiring any authentication token.



### Beta (Admin Features)

* **AC-04: Admin Login (FR-12)**
* Given valid admin credentials, when an admin posts to `/api/v1/admin/auth/login`, then a `200 OK` is returned with an `access_token` and an HttpOnly refresh cookie is set.


* **AC-05: Unauthorized Write Block (FR-16)**
* When an unauthenticated client attempts `POST /api/v1/admin/universities`, the system returns `401 Unauthorized`.


* **AC-06: Login Lockout (FR-19)**
* Given 5 failed login attempts for an admin email, when a login attempt is made within 15 minutes, the system returns `429 Too Many Requests`.



## 6. Traceability Matrix

| Story | Requirements | API Endpoint | Release |
| --- | --- | --- | --- |
| US-01 | FR-01, FR-02, FR-03 | `GET /api/v1/universities`, `GET /api/v1/units` | MVP |
| US-02 | FR-04, FR-05 | `GET /api/v1/units/{id}/marks`, `GET /api/v1/units/{id}/seats` | MVP |
| US-03 | FR-07 | `GET /api/v1/universities/{id}/fees` | MVP |
| US-04 | FR-06 | `GET /api/v1/universities/{id}/dates` | MVP |
| US-05 | FR-08 | `GET /api/v1/search` | MVP |
| US-06 | FR-09 | `GET /api/v1/units/{id}` (includes portal link) | MVP |
| US-07 | FR-10, FR-11 | `GET /api/health`, `/api/docs` | MVP |
| US-08 | FR-12, FR-13, FR-14 | `/api/v1/admin/auth/login`, `/refresh`, `/logout` | Beta |
| US-09 | FR-15, FR-16 | `POST/PATCH/DELETE /api/v1/admin/universities/*` | Beta |
| US-10 | FR-17 | `GET/POST /api/v1/admin/users` | Beta |
| US-11 | FR-18, FR-19 | `GET/PATCH /api/v1/admin/profile`, password endpoint | Beta |