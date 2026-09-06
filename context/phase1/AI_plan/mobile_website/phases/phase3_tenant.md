# Phase 3: Tenant Module Implementation

## 🎯 Goal
Provide tenants with a self-service payment and lease portal.

## ✅ Checklist
- [ ] **Tenant Dashboard View:** 
    - Display current lease details (Address, Rent Amount).
    - Highlight "Next Payment Due" date.
- [ ] **Payment Submission Form:** 
    - Mobile-friendly form calling `POST /api/v1/payments/`.
    - Instant feedback upon submission.
- [ ] **Payment History List:** 
    - List of payments with status badges (Pending $\rightarrow$ Approved).

## 🛠 Implementation Details
- Create `static/js/tenant.js` to handle API calls for lease and payment data.
- Create HTML snippets for the dashboard and payment forms.
- Implement dynamic rendering into `#app-content`.
