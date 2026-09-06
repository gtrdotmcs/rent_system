# Context for Phase 1: Database Schema & Custom User Model

## Project Overview
- **Project Name:** House Rent Management System (HRMS)
- **Tech Stack:** Django (Python), Django REST Framework (DRF), PostgreSQL.
- **Architecture:** Hybrid Monolith (Web Portal + REST API for Android).

## Phase 1 Goal
Establish the foundation of the system by implementing a custom user model for Role-Based Access Control (RBAC) and the core relational database schema.

## Core Entities & Relationships
1. **Custom User Model:**
   - Roles: `SUPER_ADMIN`, `OWNER`, `TENANT`.
   - Base: Extends `AbstractUser`.
2. **Property Model:**
   - Relationship: `Owner (User)` $\rightarrow$ `Property` (One-to-Many).
3. **Lease Model:**
   - Relationship: `Property` $\rightarrow$ `Lease` (One-to-Many).
   - Relationship: `Tenant (User)` $\rightarrow$ `Lease` (One-to-Many).
4. **Payment Model:**
   - Relationship: `Lease` $\rightarrow$ `Payment` (One-to-Many).

## Implementation Roadmap (Phase 1)
- [ ] **Step 1:** Project Init & PostgreSQL Config.
- [ ] **Step 2:** Custom User Model with Roles.
- [ ] **Step 3:** Property Model (Linked to Owner).
- [ ] **Step 4:** Lease Model (Linking Tenant to Property).
- [ ] **Step 5:** Payment Model (Tracking rent & approval status).
- [ ] **Step 6:** Migrations & Admin Verification.

## Key Constraints
- Data Isolation: Owners see only their properties; Tenants see only their leases.
- Payment Workflow: Tenant Submit $\rightarrow$ Pending $\rightarrow$ Owner Review $\rightarrow$ Approved/Rejected.

## Reference Files
- Detailed Guide: `i:\rent_system\phase1_db.md`
- Architecture: `i:\rent_system\High-Level Technical Architecture_teneat.txt`


Quick Recommendations to Fill the Gaps
Notifications – Add email (Django send_mail) and optional SMS (Twilio) for payment status changes and rent‑due reminders (cron/Celery beat).
Payment Gateway – Integrate Stripe/PayPal for real money handling; store only transaction IDs in Payment.
Background Tasks – Use Celery (or Django‑Q) for periodic reminders, overdue‑payment processing, and audit‑log writes.
Robust Permissions – Implement a reusable OwnerPermissionMixin for the web views, and finish the DRF custom permission classes (IsOwnerOfProperty, IsTenantOfLease).
Security Hardening – Enable CSRF, CSP, HSTS, secure cookies, and add password‑reset flows via Django’s built‑in auth views.
API Polish – Add throttling, versioned URLs (/api/v1/…), and generate an OpenAPI schema (drf-yasg or drf-spectacular).
Testing – Write unit tests for each model/serializer, view tests for permission edge‑cases, and integration tests for the full payment cycle.
Documentation & DevOps – Provide a README.md, Dockerfile, docker‑compose for dev, and CI pipeline (GitHub Actions) that runs linting, tests, and migrations.
Observability – Configure structured logging, integrate Sentry for error tracking, and expose basic health‑check endpoints.
