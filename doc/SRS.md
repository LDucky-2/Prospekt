# Software Requirements Specification (SRS) - Prospekt

| Field | Value |
|---|---|
| Product | Prospekt |
| Status | Current implementation |
| API prefix | `/api/v1` |
| Authentication | JWT access token plus HttpOnly refresh cookie |

## 1. Introduction

This specification describes the implemented Prospekt public prospectus interface and protected administration functions.

### 1.1 Definitions

| Term | Meaning |
|---|---|
| Visitor | Anonymous browser user |
| Editor | Authenticated account allowed to manage university prospectuses |
| Admin | Authenticated account allowed to manage prospectuses, accounts, and logs |
| Prospectus | One admissions session belonging to a university |
| Unit | Admissions unit with eligibility, marks, seats, dates, and fee details |
| JWT | JSON Web Token used as a short-lived access credential |
| Refresh session | Server-recorded opaque refresh token stored in an HttpOnly cookie |
| RBAC | Server-side role/permission authorization |
| Activity log | Security and administration event history |

## 2. Functional Requirements

### Public prospectus requirements

| ID | Requirement |
|---|---|
| FR-DOM-01 | The system shall list universities through `GET /api/v1/universities`. |
| FR-DOM-02 | The system shall return a selected university and nested prospectuses through `GET /api/v1/universities/{id}`. |
| FR-DOM-03 | The system shall represent multiple prospectus sessions for each university. |
| FR-DOM-04 | The system shall represent multiple units for each prospectus. |
| FR-DOM-05 | The system shall expose eligibility, marks, seats, important dates, and fee structures as nested unit data. |
| FR-DOM-06 | The system shall accept textual values for GPA and mark fields to preserve source wording. |
| FR-DOM-07 | The system shall provide a health response at `GET /api/health`. |
| FR-DOM-08 | The system shall provide interactive OpenAPI documentation at `/api/docs`. |

### Content authorization requirements

| ID | Requirement |
|---|---|
| FR-CONT-01 | An editor or admin shall be able to create, update, and delete prospectuses and units. |
| FR-CONT-02 | An admin shall be allowed to create universities. |
| FR-CONT-03 | An editor shall not be allowed to create universities. |
| FR-CONT-04 | Every unauthorized mutation shall be rejected by server-side RBAC. |
| FR-CONT-05 | University, prospectus, and account actions shall be written to the activity log. |

### Authentication requirements

| ID | Requirement |
|---|---|
| FR-AUTH-01 | The system shall authenticate email and password against Argon2 password hashes. |
| FR-AUTH-02 | The system shall return a 401 response for invalid credentials. |
| FR-AUTH-03 | The system shall reject inactive accounts with 403. |
| FR-AUTH-04 | The system shall issue a short-lived HS256 access token containing `sub`, `role`, `iat`, and `exp`. |
| FR-AUTH-05 | The default access-token lifetime shall be 15 minutes. |
| FR-AUTH-06 | The system shall store refresh sessions as SHA-256-hashed opaque tokens in the database. |
| FR-AUTH-07 | The refresh cookie shall be HttpOnly, Strict, and Secure in Vercel deployments. |
| FR-AUTH-08 | The system shall rotate the refresh token on refresh. |
| FR-AUTH-09 | The system shall revoke all sessions when refresh-token reuse is detected. |
| FR-AUTH-10 | The system shall clear or revoke refresh sessions on logout. |
| FR-AUTH-11 | The system shall list and revoke the authenticated user's sessions. |
| FR-AUTH-12 | The system shall allow profile-name updates and password changes. |
| FR-AUTH-13 | The system shall lock an account for 15 minutes after five failed login attempts. |
| FR-AUTH-14 | The system shall return 423 while a login lockout is active. |

### Account and audit requirements

| ID | Requirement |
|---|---|
| FR-ADM-01 | An admin shall be able to list users with search, role, status, offset, and limit filters. |
| FR-ADM-02 | An admin shall be able to create editor accounts. |
| FR-ADM-03 | An admin shall be able to promote or demote editor/admin accounts. |
| FR-ADM-04 | An admin shall be able to activate or deactivate accounts. |
| FR-ADM-05 | An admin shall be able to delete other accounts. |
| FR-ADM-06 | An admin shall not be able to change or delete its own account through account-management routes. |
| FR-ADM-07 | Deactivating an account shall revoke all of that account's refresh sessions. |
| FR-ADM-08 | An admin shall be able to list filtered activity logs. |

## 3. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Security | Database, JWT, and pepper values shall come from environment variables in production |
| NFR-02 | Security | Password values shall not be stored or logged in plaintext |
| NFR-03 | Security | CORS shall allow only local development origins and the configured frontend origin |
| NFR-04 | Security | Browser responses shall include no-sniff, frame-denial, referrer, and permissions-policy headers |
| NFR-05 | Persistence | Local development shall support SQLite and production shall support PostgreSQL |
| NFR-06 | Usability | The interface shall remain usable at desktop and mobile widths |
| NFR-07 | API usability | API errors shall use JSON detail responses and appropriate HTTP status codes |
| NFR-08 | Maintainability | Authorization constants and checks shall remain centralized in the RBAC module |
| NFR-09 | Testing | Automated tests shall cover migrations, RBAC, token rejection, and nested prospectus data |
| NFR-10 | Performance | Public list requests shall use server JSON responses and no mandatory authentication round trip |

## 4. Role and Permission Matrix

| Permission | Visitor | Editor | Admin |
|---|---:|---:|---:|
| View public universities/prospectuses | Yes | Yes | Yes |
| Create university | No | No | Yes |
| Create/update/delete prospectus | No | Yes | Yes |
| View users | No | No | Yes |
| Manage users | No | No | Yes |
| View logs | No | No | Yes |

### Account self-protection

* An admin cannot change its own role.
* An admin cannot change its own status.
* An admin cannot delete itself.

## 5. Acceptance Criteria

| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | The backend is running | `GET /api/health` is requested | Status is 200 and the body is `{"status":"ok"}` |
| AC-02 | No credentials are supplied | A public university request is made | Status is 200 |
| AC-03 | An editor is logged in | An university-create request is made | Status is 403 |
| AC-04 | An admin is logged in | A valid university-create request is made | Status is 201 |
| AC-05 | A token has expired or is tampered | A protected request is made | The request is rejected |
| AC-06 | Five failed logins occur | Another login is attempted during lockout | Status is 423 |
| AC-07 | A refresh token is reused | A refresh request is made | The session family is revoked and status is 401 |
| AC-08 | An account is deactivated | It makes a protected request or refreshes | It is rejected |

## 6. Traceability

| Requirement | Endpoint or screen | Automated test | Status |
|---|---|---|---|
| FR-DOM-03, FR-DOM-04 | University detail response | `test_university_contains_multiple_prospectuses_with_nested_units` | Pass |
| FR-AUTH-04, FR-AUTH-05 | `/api/v1/auth/login` | `test_expired_access_token_is_rejected` | Pass |
| FR-AUTH-01 | Authentication service | Password and security tests | Pass |
| FR-CONT-03 | University create route | `test_editor_cannot_create_universities` | Pass |
| FR-ADM-01 | Users page and `/api/v1/admin/users` | RBAC tests | Implementation present |
| FR-CONT-04 | Protected mutation routes | `test_editor_has_prospectus_permissions_but_not_account_permissions` | Pass |
| FR-DOM-06 | Prospectus/unit schemas | `test_string_fields_accept_non_numeric_text` | Pass |
