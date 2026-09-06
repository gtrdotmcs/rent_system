# Phase 3: Tenant Portal & Payment Workflow (The User Side)

## Goal
Implement the tenant-facing interface and the end-to-end rent payment submission and approval process.

---

## Step-by-Step Implementation Plan

### Step 1: Tenant Lease Dashboard
**Objective:** Allow Tenants to view their active lease details.
- Implement a view that retrieves the active lease for the logged-in `TENANT`.
- Display property address, monthly rent, start date, and end date.

**Prompt for AI:**
> "In the `rentals` app, create a 'My Lease' dashboard for users with the `TENANT` role. The view should fetch the active lease associated with the logged-in user and display the property details and rent terms. Provide the view and template."

---

### Step 2: Rent Payment Submission
**Objective:** Enable Tenants to submit a payment record for a specific month and year.
- Create a form for submitting `Payment` details (amount, date, month, year).
- Ensure the payment is linked to the tenant's active lease.
- Default the payment status to `PENDING`.

**Prompt for AI:**
> "Implement a 'Submit Payment' feature in the `rentals` app. Create a form where a Tenant can enter the amount paid, payment date, and the month/year the payment is for. The system should automatically link this payment to the tenant's active lease and set the status to `PENDING`. Provide the view, form, and template."

---

### Step 3: Payment Tracking & History
**Objective:** Allow Tenants to track the status of their submitted payments.
- Create a view listing all payments made by the tenant.
- Display the status (`Pending`, `Approved`, `Rejected`) clearly.

**Prompt for AI:**
> "Create a 'Payment History' view for Tenants. It should list all payments they have submitted, showing the month, year, amount, and the current approval status. Use different Bootstrap badges for Pending, Approved, and Rejected statuses. Provide the view and template."

---

### Step 4: Owner Payment Approval Workflow
**Objective:** Allow Owners to review and update the status of pending payments.
- Create a view for Owners to see all `PENDING` payments for their properties.
- Implement a simple action (button/link) to mark a payment as `APPROVED` or `REJECTED`.

**Prompt for AI:**
> "In the `rentals` app, implement the payment approval workflow for Owners. Create a view that lists all pending payments for the Owner's properties. Add functionality to allow the Owner to change the status of a payment to either 'Approved' or 'Rejected'. Provide the views, URLs, and templates."

---

## Summary of Phase 3
- **Tenant** $\rightarrow$ Views **Lease** $\rightarrow$ Submits **Payment** $\rightarrow$ Tracks **Status**
- **Owner** $\rightarrow$ Reviews **Pending Payments** $\rightarrow$ Updates **Status**

## Implementation Progress

### ✅ Completed Steps
- **Step 1**: Tenant Lease Dashboard
- **Step 2**: Rent Payment Submission
- **Step 3**: Payment Tracking & History
- **Step 4**: Owner Payment Approval Workflow
