![][image1]

**Independent University, Bangladesh**  
**CSE309 Web Application & Internet**

**Final Project Submission Report**  
Submitted by:  
**Name**: Write your full name here  
**Student ID**: Write your IUB ID here  
**Section**: Write your section here  
**Team Number**: Write the team number assigned by the instructor here

**Project Title**: Write your project title here  
**Vercel URL**: Paste your Vercel deployment link here  
**GitHub Repository**: Paste your GitHub repository link here

**Submitted To**:  
**Sayef Reyadh**  
Adjunct Lecturer  
Department of Computer Science & Engineering  
Independent University, Bangladesh

Semester: Autumn 2026  
Date of Submission: Write the submission date here

# **How to use this report (Delete This Part)**

This document shows the sections your final report must have and what each section must contain. Keep the headings and numbering. Replace the grey guidance text with your own content. Blue italic lines show where a diagram, table or screenshot goes: replace them with the real figure and a caption that says what it proves. Write about your finished project, not about plans.

The same template is available as a Markdown file, with the same sections and numbering: [https\://github.com/sayef-reyadh-labs/smarter-todo/blob/main/docs/FINAL\_REPORT.md](https://www.google.com/url?q=https://www.google.com/url?q%3Dhttps://www.google.com/url?q%253Dhttps://www.google.com/url?q%25253Dhttps://www.google.com/url?q%2525253Dhttps://github.com/sayef-reyadh-labs/smarter-todo/blob/main/docs/FINAL_REPORT.md%25252526sa%2525253DD%25252526source%2525253Deditors%25252526ust%2525253D1795033502492832%25252526usg%2525253DAOvVaw1dn9X-HzYYX-H_NJC1arO0%252526sa%25253DD%252526source%25253Deditors%252526ust%25253D1795034810634129%252526usg%25253DAOvVaw1teT4_gSGUR3m6nsl4BzMi%2526sa%253DD%2526source%253Deditors%2526ust%253D1795035855591136%2526usg%253DAOvVaw1owLYikzk-orAKvJeMHi8u%26sa%3DD%26source%3Deditors%26ust%3D1795036711142675%26usg%3DAOvVaw3unLoKHjFe1guBNpBtpT1L&sa=D&source=editors&ust=1795037239204850&usg=AOvVaw0BIlcEQL1pCKBd-cKcb5tt) (copy it into your repository docs folder as FINAL\_REPORT.md and fill it in).

> * Write in your own words. Every statement must match your running application.  
> * Number every diagram, table and screenshot (Figure 1, Table 1, S1) and refer to them in the text.  
> * Use the same requirement IDs (FR-AUTH-01 and so on) in the requirements, the tests and the screenshots.  
> * Never show real passwords, secret keys or full tokens in screenshots or text (blur or mask them).  
> * Do not write test account user IDs and passwords in the Markdown file, and never write passwords anywhere in the repository: GitHub flags them. Put them only in the PDF report (Appendix).  
> * Submit the report twice: FINAL\_REPORT.md in the repository and a PDF with the screenshots.

# **Table of Contents**

Insert an automatic table of contents (Insert, Table of contents). Add a List of Figures and Screenshots with the number, caption and page of each.

*\[Table of contents\]*

*\[List of figures and screenshots\]*

# **1\. Executive Summary**

Length: one page. A reader who reads only this page must understand the project.

## **1.1 Project overview**

Project name, one paragraph on what the system does and for whom, and the stack in one line (React with TypeScript, FastAPI, database, Vercel).

## **1.2 What was built since the mid assessment**

One sentence for each major addition, named as it appears in the app:

> * JWT authentication with refresh and logout  
> * Role based access control (roles, ownership, group permissions)  
> * Admin dashboard (users, content, activity log, security view, exports)  
> * Audit logging, brute-force protection, deployment on Vercel

## **1.3 Live links**

A table with: GitHub repository, Vercel frontend, API, API docs and video demo. Do not put the test account user IDs and passwords here: write them in the PDF report (Appendix), because GitHub flags passwords committed to a repository.

*\[Table 1: links\]*

# **Part A. Product Requirements (PRD)**

Length: two to three pages. This part says what the product is for, not how it is built.

## **A1. Problem Statement**

One or two paragraphs: who has the problem, how they cope today, and why it matters. Do not describe your solution here.

## **A2. Users and Roles**

A table with one row per role: Visitor, User, Group member or owner (if you have groups), Admin.

Columns: role, who they are, main tasks, what they must never be able to do.

*\[Table 2: users and roles\]*

## **A3. Goals and Success Measures**

Four to six goals. Each has a measurable, testable measure (a number, a time limit or a yes or no check). Include at least two security goals, for example: no user can read another user's data, sessions are short-lived and revocable.

*\[Table 3: goal and measure\]*

## **A4. Scope and Non-Goals**

Three lists: in scope (authentication, RBAC, groups, admin dashboard, audit log, deployment and your domain features), out of scope (what you decided not to build and why), and assumptions and constraints (browser support, hosting limits, time).

## **A5. User Stories**

At least ten stories in the form: As a (role) I want (action) so that (benefit). Give each an ID (US-01). Cover every role: at least two for authentication, three for RBAC or groups, three for the admin.

*\[Table 4: user stories\]*

# **Part B. Software Requirements (SRS)**

Length: four to six pages. This part says exactly what the system shall do. Every requirement is numbered and testable.

## **B1. Introduction**

Purpose of the document, intended readers, a short definitions table (JWT, access token, refresh token, RBAC, role, permission, audit log) and the references you used (for example RFC 7519, OWASP ASVS, FastAPI documentation).

## **B2. Functional Requirements**

Tables grouped by area, each requirement written as one sentence beginning 'The system shall' and having a unique ID. Cover at least:

> * FR-AUTH: signup, login, password hashing and pepper, access token claims and lifetime, refresh and rotation, logout, session list and revoke, lockout, profile update, password change  
> * FR-RBAC: roles, server-side checks, ownership rules, group permissions (create, update, assign), owner-only actions, admin self-protection, banned user rejected on the next request  
> * FR-ADM: statistics, user list with search and filters, user detail, ban and unban, role change, session revoke, bulk actions, content moderation, activity log with filters, security view, CSV exports  
> * FR-DOMAIN: the features of your own resource

*\[Table 5 to Table 8: functional requirements by area\]*

## **B3. Non-Functional Requirements**

Measurable requirements in a table: security (secrets in environment variables, generic login errors), performance (pagination limits, response time target), usability (responsive, loading and error states), reliability (data persists after a restart) and maintainability (one RBAC module, automated tests).

*\[Table 9: non-functional requirements\]*

## **B4. Roles and Permission Matrix**

This must match your implementation exactly. Give three tables:

> * Endpoint groups against roles (Visitor, User, Group member, Group owner, Admin) with yes, no or own  
> * Group permissions: what create, update and assign each allow, and what only the owner can do  
> * Admin rules: what an admin cannot do (change own role, ban another admin) and what extra rights a system admin has inside a group (none, if so)

*\[Table 10: endpoint groups by roles\]*

*\[Table 11: group permissions\]*

*\[Table 12: admin rules\]*

## **B5. Use Cases**

At least six use cases: log in and refresh, create a record, change a member's permissions, a denied action, ban a user, read the audit log. For each: actor, preconditions, main flow as numbered steps, alternative and error flows (with status codes), postconditions.

*\[Diagram: use case diagram with the actors and the use cases\]*

*\[Table 13: use case descriptions\]*

## **B6. Acceptance Criteria**

Given, When, Then for every critical requirement. Cover at least: token expiry returns 401, a tampered token is rejected, a user cannot read another user's record, a member without a permission gets 403, a banned user is rejected on the next request, an admin cannot ban another admin.

*\[Table 14: acceptance criteria\]*

## **B7. Traceability Matrix**

One table linking each requirement to the endpoint or screen that implements it, the automated test that checks it and the screenshot that shows it. Every requirement must appear.

*\[Table 15: requirement, endpoint or screen, test, screenshot\]*

# **Part C. Technical Design (TDD)**

Length: six to nine pages. This part says how the system is built. A reader must be able to rebuild it from this part.

## **C1. Technology Stack**

A table: component, technology, version, reason for choosing it (frontend, UI library, backend, database, ORM, password hashing, JWT library, testing, hosting).

*\[Table 16: technology stack\]*

## **C2. System Architecture**

A diagram of the browser, the Vercel frontend, the Vercel API, the database and the audit log, with arrows for the requests, the access token header and the refresh cookie. Then two sentences for every arrow.

*\[Diagram: system architecture\]*

## **C3. Backend and Frontend Structure**

The folder tree of both projects (two levels), and a short explanation of where each thing lives: routes, services, repositories, models, the authentication code, the RBAC module and the admin code on the backend; pages, components, the API client, the authentication context and the route guards on the frontend.

*\[Folder tree of the backend\]*

*\[Folder tree of the frontend\]*

## **C4. Data Model**

An ER diagram with every table. For each table, a short table of columns, types, keys, constraints and indexes. Explain how roles, bans, sessions or refresh tokens, group membership with permissions, and the activity log are stored.

*\[Diagram: ER diagram\]*

*\[Table 17 and onward: tables and columns\]*

## **C5. API Design**

A table of every endpoint: method and path, authentication needed, required role or permission, request body, success status and error statuses. State the error response format and the API version prefix.

*\[Table: endpoint list\]*

## **C6. JWT Authentication Design**

Explain, with a diagram, how login, a protected request, token expiry, refresh, logout and reuse of an old refresh token work. Also cover:

> * Token claims (user id, role, issued at, expiry), the signing algorithm and where the secret comes from  
> * Lifetimes of the access and refresh tokens and why you chose them  
> * Where the tokens are stored in the browser (memory, localStorage or httpOnly cookie), the risks of that choice (XSS, CSRF) and what you did about them  
> * What the server checks on every request (signature, expiry, user exists, user not banned)  
> * What the frontend does on a 401 (refresh once, then log out)

*\[Diagram: JWT sequence diagram for login, request, expiry, refresh and logout\]*

*\[Table: token claims\]*

## **C7. RBAC Design**

Explain how a request is authorised, in order: token, user, role check, ownership check, group permission check, handler. Cover:

> * The list of roles and permission constants  
> * The one reusable check (dependency or decorator) with a short code excerpt (10 to 20 lines)  
> * How ownership is enforced in queries (filtering by the owner id, not only checking afterwards)  
> * How a new role or permission would be added  
> * The special rules for admins and banned users

*\[Diagram: authorisation flow for one request\]*

*\[Code excerpt: the reusable permission check\]*

## **C8. Admin Dashboard Design**

Describe every admin page, the endpoints it calls, its filters and pagination, its actions, and the audit events each action writes. Explain how bulk actions report how many items were affected and skipped, and how CSV export respects the filters.

*\[Diagram: admin pages and the endpoints they call\]*

*\[Table: page, endpoints, filters, actions, audit events\]*

## **C9. Security Design and Threats**

A table of threats, the defence and where it is in the code. Cover at least: password database leak, stolen access token, stolen refresh token, brute-force login, privilege escalation, access to another user's record, cross-site scripting, cross-site request forgery, CORS misuse, secrets in the repository, SQL injection and over-posting of fields.

*\[Table: threat, defence, file or module\]*

## **C10. Deployment on Vercel**

Describe the Vercel projects (frontend and API), the build settings and rewrites, how the frontend finds the API, the hosted database, and the names of all environment variables (never the values). Explain how to redeploy.

*\[Diagram: deployment layout\]*

*\[Table: environment variable names and what each is for\]*

## **C11. Testing**

The test strategy (automated API tests, manual tests on the live site), how to run the tests, and a results table: test name, requirement it checks, result. Include the tests for token expiry and tampering, ownership, the group permission matrix, the admin rules and lockout.

*\[Table: tests and results\]*

# **Part D. Evidence: Screenshots of the Running Application**

Take every screenshot on the deployed Vercel URL, with the address bar visible and the logged-in user shown. Crop to the relevant area. Give each a number, a caption saying what it proves and the requirement ID. Mask passwords and tokens.

## **D1. User Side**

Each screenshot below is required:

*\[S1: signup and login page, with a validation error shown (for example a weak password)\]*

*\[S2: the main feature page of a logged-in user, showing only that user's records\]*

*\[S3: profile page and the change password form, with the wrong current password rejected\]*

*\[S4: the sessions list with the revoke action\]*

*\[S5: a group page showing members and their permissions\]*

*\[S6: an action denied by RBAC, showing the message in the app and the 403 response in the browser network tab\]*

## **D2. Security Behaviour**

Use the browser developer tools:

*\[S7: network tab showing the Authorization header (token masked) and an expired token returning 401\]*

*\[S8: the refresh request returning a new access token, and the httpOnly cookie in the application tab\]*

*\[S9: a banned user rejected on the next request\]*

## **D3. Admin Dashboard**

Show real data and the matching result of each action:

*\[S10: overview statistics\]*

*\[S11: users list with search, filters and pagination\]*

*\[S12: user detail with sessions and recent activity\]*

*\[S13: the ban dialog with a reason, and the banned state afterwards\]*

*\[S14: records and groups moderation list with filters and a bulk action\]*

*\[S15: activity log with filters, showing the events caused by the steps above\]*

*\[S16: security view with failed logins by IP and by account\]*

*\[S17: a CSV export downloaded and opened\]*

## **D4. Deployment**

Show that it is live and configured:

*\[S18: the Vercel frontend project with the production deployment and domain\]*

*\[S19: the Vercel API project with the environment variable names (values hidden)\]*

*\[S20: the live API documentation page\]*

## **D5. Tests**

The output of the automated tests:

*\[S21: test run output showing all tests and the result\]*

# **Part E. Project Management and Conclusion**

## **E1. How to Run and Test**

Step by step: prerequisites, the environment file (variable names with example values), and the commands for the backend, frontend and tests. End with how to log in with the test accounts: name the roles (admin and user) and say that the user IDs and passwords are in the PDF report (Appendix), never in this file. Someone who has never seen the project must be able to follow it.

## **E2. GitHub Work**

A table of the issues and pull requests for each major feature (JWT, RBAC, admin dashboard and others): link, title and what it delivered. Say which commits are yours and how the work was divided over time.

*\[Table: issue, pull request, what it delivered\]*

## **E3. Limitations**

An honest list: what is missing or only partly done, known bugs, and security risks you did not cover. Hiding a problem is worse than reporting it.

## **E4. Future Work**

What you would build or fix next, in priority order, with one line of reason each.

## **E5. Sources, Libraries and Tools**

A table of every library, tutorial, document and tool you used (name, version or link, what for). If you used any AI tool, say which one, for which part, and what you checked or changed yourself.

*\[Table: sources, libraries and tools\]*

## **Appendix. Test Accounts and Video Demo**

The link to the video demo (5 to 8 minutes on the deployed URL). Test accounts: add them only in the PDF report. Write the user ID, password and role of every demo account (at least 2 admins and 3 normal users) and the group with mixed permissions (group name, owner and each member's permissions) in the Appendix of the PDF. Never write the user IDs or passwords in this Markdown file, and never write passwords in the README or anywhere else in the repository: GitHub flags them as leaked credentials. Use demo data only.

[image1]: <data:image/png;base64,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>