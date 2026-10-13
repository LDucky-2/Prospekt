# Product Requirements Document (PRD) — Prospekt

| Field | Value |
| --- | --- |
| Product | Prospekt |
| Version | MVP + Beta |
| Releases | MVP — Mid-term, Beta — Final |
| Status | Draft |
| Related docs | [Software Requirements Specification (SRS)](https://www.google.com/search?q=SRS.md), [Technical Design Document (TDD)](https://www.google.com/search?q=TDD.md) |

This document covers **both releases**. Every goal, feature, and user story has a **Release** column to distinguish between what is built for the mid-term MVP and what is added for the final Beta.

## 0. Release Plan

| Release | When | Focus |
| --- | --- | --- |
| **MVP** | Mid-term | Core public data API, unit filtering, structured mark and seat tables, important dates, and fast search deployed on Vercel. End users access everything without any account or login. |
| **Beta** | Final | Admin authentication and portal for uploading and managing prospectus data, admin profile and RBAC, client-side unit comparison and bookmarks, and security hardening. |

## 1. Purpose

University admission prospectuses in Bangladesh are dense documents that mix requirements across multiple academic units into lengthy formats, forcing students to sift through irrelevant information. Prospekt solves this information overload by extracting dense PDFs into bite-sized, unit-filtered, structured web data.

To ensure a seamless experience, Prospekt is developed in two clear phases:

1. **MVP (mid-term):** A completely public web platform and REST API where students and guardians can instantly view, filter, and search prospectus data by academic unit without needing to register or log in.
2. **Beta (final):** An authenticated Admin Portal allowing authorized content managers and administrators to input, update, and manage prospectus bits, alongside client-side features like bookmarks and unit comparisons.

## 2. Problem Statement

University admissions in Bangladesh rely on PDF prospectuses containing information about deadlines, procedures, fees, exam details, mark distributions, and more. This format is difficult to navigate on mobile devices, leading to information overload where students miss critical eligibility rules or deadlines because the documents are densely packed with data for every subject and unit, preventing students from reading them fully.

## 3. Goals

| ID | Goal | Release |
| --- | --- | --- |
| G-1 | Provide a public REST API and clean interface for viewing prospectus data filtered by unit. | MVP |
| G-2 | Store university and unit data in a persistent relational database (Supabase PostgreSQL). | MVP |
| G-3 | Expose automatic interactive API documentation at `/api/docs`. | MVP |
| G-4 | Deploy automatically to Vercel on every push to `main`. | MVP |
| G-5 | Implement secure admin authentication (JWT access and refresh tokens) for content management. | Beta |
| G-6 | Provide an authenticated Admin Portal to create, update, and manage prospectus data bits. | Beta |
| G-7 | Support global admin roles (`admin`, `super_admin`) with strict permission controls. | Beta |
| G-8 | Enable client-side unit comparison and bookmarking using local browser storage. | Beta |

## 4. Target Users

| User | Description & Need | Release | Access Model |
| --- | --- | --- | --- |
| Information Seeker (Student / HSC Candidate) | Needs to quickly find unit-specific eligibility, mark distribution, seat info, and dates on mobile without hassle. | MVP & Beta | Public (No login required) |
| Information Seeker (Guardian / Parent) | Needs to check application fees, payment gateway instructions, and hard deadlines. | MVP & Beta | Public (No login required) |
| Information Seeker (Admission Mentor) | Needs a reliable quick-reference tool to verify complex rule variations across universities. | MVP & Beta | Public (No login required) |
| Information Provider (Admin / Maintainer) | Needs a secure portal to input, modify, and publish prospectus data deconstructed from source documents. | Beta | Authenticated (Admin Login) |

## 5. Scope

### In scope — MVP (mid-term)

* Public viewing of universities, units, eligibility rules, mark distributions, seat info, important dates, and fee structures.
* Unit-based filtering (Science, Arts, Commerce) so students only see relevant information.
* Structured tables for mark distributions, negative marking rules, and seat capacity.
* Fast keyword search across prospectus data bits.
* Direct links to official payment and application portals.
* Health check endpoint and interactive OpenAPI documentation at `/api/docs`.
* Automated deployment on Vercel.

### In scope — Beta (final)

* **Admin Authentication:** Secure admin sign-in, token refresh, and logout using JWT and HttpOnly cookies.
* **Admin Portal:** Secure CRUD interface for administrators to manage universities, units, and prospectus details.
* **Admin Profile & RBAC:** View admin profile, change password, and enforce role-based permissions (`admin` vs `super_admin`).
* **Client-Side Enhancements:** Unit comparison tables and bookmarked/saved units utilizing browser local storage.
* **Security Hardening:** Password hashing with Argon2, login lockout mechanisms, and security headers.

### Out of scope this semester

* Automated test suites and CI/CD pipelines (GitHub Actions, branch protection) — planned for later.
* Public user accounts, student sign-up, or student login (end users remain completely unauthenticated).
* Automated PDF scraping or AI-driven PDF parsing (admin data entry is managed via the structured portal).

## 6. Features and Priority (MoSCoW)

| ID | Feature | Release | Priority |
| --- | --- | --- | --- |
| F-1 | Public API endpoint for listing and filtering universities and units | MVP | Must |
| F-2 | Unit-filtered view (Science / Arts / Commerce) | MVP | Must |
| F-3 | Structured display of mark distributions and negative marking rules | MVP | Must |
| F-4 | Important dates and application deadline countdown | MVP | Must |
| F-5 | Fee breakdown and payment method details | MVP | Must |
| F-6 | Keyword search across prospectus data bits | MVP | Should |
| F-7 | Direct links to official application portals | MVP | Should |
| F-8 | Health check endpoint and `/api/docs` | MVP | Must |
| F-9 | Admin login and session refresh | Beta | Must |
| F-10 | Admin Portal for creating and updating prospectus records | Beta | Must |
| F-11 | Admin RBAC (`admin` / `super_admin`) and permission checks | Beta | Must |
| F-12 | Admin profile management (change name and password) | Beta | Should |
| F-13 | Client-side unit comparison tool | Beta | Could |
| F-14 | Client-side bookmarks / saved units (local storage) | Beta | Could |
| F-15 | Security hardening (Argon2 hashing, login lockout, security headers) | Beta | Must |

## 7. User Stories

### MVP (Public Features — No Login Required)

* **US-01:** As a student, I want to select my academic background (Science/Arts/Commerce), so I can view only the units and rules applicable to me.
* **US-02:** As a student, I want to view structured tables of exam mark distributions and negative marking rules, so I can prepare effectively without reading dense paragraphs.
* **US-03:** As a guardian, I want to check application fees and mobile banking payment instructions (bKash/Nagad), so I can manage financial preparation accurately.
* **US-04:** As a student, I want to see a clear breakdown of important dates (application window, admit card download, exam date), so I never miss a deadline.
* **US-05:** As a student, I want to search for specific keywords within the prospectus data, so I can locate information instantly.
* **US-06:** As a student, I want direct links to official payment and application portals, so I can avoid unorganized website navigation.
* **US-07:** As a maintainer, I want a health check endpoint and OpenAPI documentation, so I can verify the deployment status and API schema.

### Beta (Admin & Enhanced Features)

* **US-08:** As an administrator, I want to securely log in with my credentials, so I can access the backend management portal.
* **US-09:** As an administrator, I want to add, edit, or remove university prospectus entries through an interface, so the platform data stays accurate and up-to-date.
* **US-10:** As a super admin, I want to manage other administrator accounts and roles, so access is strictly controlled.
* **US-11:** As an administrator, I want my password stored securely and repeated unauthorized login attempts blocked, so the admin portal remains secure against breaches.
* **US-12:** As a student, I want to compare two university units side-by-side in my browser, so I can evaluate my options easily.
* **US-13:** As a student, I want to bookmark my favorite university units locally on my device, so I can access them quickly on subsequent visits.

## 8. Success Metrics

### MVP

* All public core GET endpoints respond successfully on the production Vercel URL.
* Prospectus data persists reliably in Supabase PostgreSQL across redeploys.
* `/api/docs` accurately documents all public endpoints with clear request/response schemas.

### Beta

* Unauthorized clients attempting to access admin mutation endpoints (`POST`, `PATCH`, `DELETE`) receive `401 Unauthorized` or `403 Forbidden`.
* Admin passwords are stored exclusively as secure Argon2 hashes.
* Brute-force login attempts are successfully locked out after 5 consecutive failures.

## 9. Assumptions and Constraints

* Hosted on Vercel as a monorepo combining the Vite + React frontend and FastAPI backend (`vercel.json`).
* Serverless execution environment requires an external relational database (Supabase PostgreSQL) rather than local file storage.
* End users do not require accounts, simplifying privacy and compliance requirements.
* The initial administrator account is provisioned directly in the database table editor.

## 10. Milestones

### MVP — Mid-term

* **M1 — Docs:** PRD, SRS, and TDD approved.
* **M2 — Data layer:** Database models and connection established with Supabase PostgreSQL.
* **M3 — Public API & UI:** Public CRUD/read endpoints implemented and integrated with the React frontend.
* **M4 — Mid demo:** MVP deployed live on Vercel, tagged `v0.1.0`.

### Beta — Final

* **M1 — Admin Auth:** Admin login, token refresh, and password hashing implemented with Alembic migrations.
* **M2 — Admin Portal & RBAC:** Administrative endpoints and UI panels established for managing prospectus content.
* **M3 — Client Enhancements:** Unit comparison and local bookmarking features added to the frontend.
* **M4 — Security Hardening:** Login lockout, security headers, and permission checks finalized.
* **M5 — Final demo:** Beta deployed live on Vercel, tagged `v0.2.0`.