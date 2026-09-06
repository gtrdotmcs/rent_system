# Phase 5: Security & Validation (Hardening)

## Goal
Ensure strict data isolation, input validation, and system security to prevent unauthorized data access.

---

## Before Starting
- Treat the existing session-authenticated web portal and JWT-authenticated `/api/v1/` API as separate security surfaces.
- Preserve the current owner and tenant workflows while tightening access checks.
- Record every security change with a regression test before marking the related step complete.
- Do not rely on hidden form fields, URL IDs, or client-supplied owner, tenant, lease, or payment values for authorization.

## Security Acceptance Criteria
- A user cannot read, update, delete, approve, or reject an object outside their permitted relationship, even when its ID is guessed.
- Tenant payment creation always selects the authenticated tenant's active lease and forces `PENDING` status server-side.
- Owner payment status changes accept only `APPROVED` or `REJECTED`.
- Lease dates and payment amounts are validated consistently by models, forms, and serializers.
- Anonymous API requests return `401`; authenticated users with an incorrect role are denied; ownership violations do not reveal object data.
- The test suite covers both successful workflows and cross-owner/cross-tenant access attempts.

---

## Step-by-Step Implementation Plan

### Step 1: Strict Data Isolation Audit
**Objective:** Verify that no user can access data belonging to another user of the same role.
- Review all web views and `/api/v1/` endpoints to ensure `get_queryset` filters by the authenticated user's relationship.
- Check property, lease, and payment detail/update paths for IDOR vulnerabilities.
- Prefer queryset filtering and object-level permissions over a global middleware check, so authorization remains explicit at the owning view boundary.
- Verify that unauthorized object access does not expose object existence or fields.

**Prompt for AI:**
> "Audit the session-authenticated web views and the JWT-authenticated `/api/v1/` endpoints in the `accounts` and `rentals` apps. Test guessed property, lease, and payment IDs for cross-owner and cross-tenant access. Harden each affected `get_queryset`, form queryset, or object-level permission so unauthorized users cannot read or mutate data. Add regression tests for every finding and preserve the existing Phase 3 and Phase 4 workflows."

---

### Step 2: Advanced Input Validation
**Objective:** Prevent invalid data from entering the system.
- Implement model-level validation for lease date ranges and positive payment amounts.
- Apply equivalent validation in `LeaseForm`, `PaymentForm`, and DRF serializers.
- Reject duplicate payments for the same lease, month, and year unless the business rules explicitly allow them.
- Validate that payment years are within the supported business range and that an active lease is required for new tenant payments.

**Prompt for AI:**
> "Add consistent validation to the `Lease` and `Payment` models, forms, and DRF serializers. Require `end_date` to be after `start_date` when an end date exists, require a positive payment amount, validate month/year values, and prevent duplicate payments for one lease and billing period. Return clear form and JSON validation errors and add tests for valid and invalid input."

---

### Step 3: Permission Class Refinement
**Objective:** Move from simple role checks to robust Django Permission classes.
- Create reusable DRF permission classes for owner-property and tenant-lease relationships.
- Keep queryset filtering as the primary data-isolation boundary; use object permissions for detail mutations.
- Review the web decorators and replace duplicated role strings with shared role constants where practical.
- Confirm CSRF protection remains enabled for session-authenticated web forms.

**Prompt for AI:**
> "Refactor the Phase 4 API authorization into reusable DRF permissions. Implement `IsOwnerOfProperty` and `IsTenantOfLease` relationship checks, apply them to the relevant detail endpoints, and retain safe `get_queryset` filtering. Review the web decorators for equivalent owner and tenant checks, keep CSRF protection enabled for session forms, and add permission regression tests."

---

### Step 4: Final End-to-End Testing
**Objective:** Validate the entire workflow from Super Admin $\rightarrow$ Owner $\rightarrow$ Tenant $\rightarrow$ Payment.
- Cover model, form, serializer, web-view, and API-view validation.
- Test JWT authentication, role restrictions, IDOR attempts, invalid status changes, and CSRF-protected web submissions.
- Verify the web portal and `/api/v1/` API enforce the same ownership and tenant-isolation rules.
- Run `manage.py check` and the complete test suite before completion.

**Prompt for AI:**
> "Create end-to-end and security regression tests for the complete workflow: Super Admin creates Owner $\rightarrow$ Owner creates Property $\rightarrow$ Owner assigns Tenant $\rightarrow$ Tenant submits Payment $\rightarrow$ Owner approves or rejects Payment. Cover both the web portal and JWT `/api/v1/` endpoints, including anonymous requests, wrong-role requests, guessed IDs, cross-owner and cross-tenant access, invalid dates and amounts, duplicate billing periods, invalid payment statuses, and CSRF-protected POST requests. Run `manage.py check` and the full test suite."

---

## Summary of Phase 5
- **Security**: IDOR prevention, Custom Permission Classes
- **Validation**: Date and Amount constraints
- **Verification**: Full E2E Lifecycle Testing

## Implementation Progress

### ✅ Completed Steps
- **Step 1**: Strict Data Isolation Audit - Implemented `get_queryset` filtering and object-level permissions in API and Web views.
- **Step 2**: Advanced Input Validation - Added model-level and form-level validation for lease dates and duplicate payments.
- **Step 3**: Permission Class Refinement - Created `IsOwnerOfProperty` and `IsTenantOfLease` DRF permission classes.
- **Step 4**: Final End-to-End Testing - Added `SecurityRegressionTests` covering cross-tenant/owner access and validation logic.
