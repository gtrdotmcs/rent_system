# Implementation Roadmap: Mobile-First API Web UI

This document breaks down the implementation of the modern, mobile-friendly web interface into actionable phases. Each phase must be completed and tested before moving to the next.

---

## 📅 Phase 1: API Enrichment & Foundation
**Goal:** Ensure the backend provides all the data necessary for a dynamic frontend without page reloads.

- [ ] **User Profile Endpoint:** Implement `GET /api/v1/user/me/` to return the current user's role, full name, and email.
- [ ] **Owner Summary Endpoint:** Implement `GET /api/v1/owner/dashboard/` to return total properties and a count of pending payments.
- [ ] **Tenant Summary Endpoint:** Implement `GET /api/v1/tenant/dashboard/` to return active lease status and next payment due date.
- [ ] **Admin Global Stats:** Implement `GET /api/v1/admin/stats/` for system-wide totals (Owners, Tenants, Properties).
- [ ] **JWT Optimization:** Ensure refresh token logic is working for seamless mobile sessions.

---

## 📅 Phase 2: Core Layout & Authentication
**Goal:** Establish the "App Shell" and the secure entry point.

- [ ] **Mobile Base Template:** Create `templates/base_mobile.html` using Tailwind CSS.
    - Implement Bottom Navigation (Home, Payments, Profile).
    - Create a dynamic content area (`#app-content`) for JS injection.
- [ ] **API-Driven Login:** Create `templates/login_mobile.html`.
    - JavaScript logic to POST credentials to `/api/v1/token/`.
    - Store JWT in `localStorage`.
- [ ] **Role-Based Routing:** Logic to detect role from the `/me/` endpoint and redirect to the correct dashboard.

---

## 📅 Phase 3: Tenant Module Implementation
**Goal:** Provide tenants with a self-service payment and lease portal.

- [ ] **Tenant Dashboard View:** 
    - Display current lease details (Address, Rent Amount).
    - Highlight "Next Payment Due" date.
- [ ] **Payment Submission Form:** 
    - Mobile-friendly form calling `POST /api/v1/payments/`.
    - Instant feedback upon submission.
- [ ] **Payment History List:** 
    - List of payments with status badges (Pending $\rightarrow$ Approved).

---

## 📅 Phase 4: Owner Module Implementation
**Goal:** Empower owners to manage their portfolio and approve payments.

- [ ] **Property Portfolio Grid:** 
    - Display a responsive grid of owned properties.
    - Quick stats at the top (Occupied vs Vacant).
- [ ] **Property Detail View:** 
    - List of tenants linked to a specific property.
    - Lease management options.
- [ ] **Payment Approval Center:** 
    - A dedicated view for all "Pending" payments across all properties.
    - Quick "Approve" or "Reject" actions via API.

---

## 📅 Phase 5: Super Admin Module Implementation
**Goal:** Provide global system oversight and user management.

- [ ] **Global Dashboard:** 
    - Visual cards for system-wide totals.
- [ ] **Owner Management Table:** 
    - Ability to create, edit, and delete Owner accounts via API.
- [ ] **System-Wide Audit:** 
    - View all active leases and property distributions.

---

## 📅 Phase 6: Polishing & PWA Transition
**Goal:** Finalize the user experience and make it installable.

- [ ] **UI/UX Enhancements:**
    - Add "Loading Skeletons" while waiting for API responses.
    - Implement "Toast" notifications for API errors/success.
- [ ] **State Sync:** Ensure UI updates automatically after actions (e.g., approving a payment updates the count).
- [ ] **PWA Integration:** 
    - Add `manifest.json` and Service Worker for "Add to Home Screen" capability.
- [ ] **Cross-Device Testing:** Final validation on iOS, Android, and Desktop browsers.
