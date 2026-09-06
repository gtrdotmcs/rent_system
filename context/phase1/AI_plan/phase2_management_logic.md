# Phase 2: Super Admin & Owner Logic (The Management Side)

## Goal
Implement the administrative and ownership management layer, allowing Super Admins to manage Owners and Owners to manage their Properties and Tenants.

---

## Step-by-Step Implementation Plan

### Step 1: Super Admin Dashboard & Owner Management
**Objective:** Create the interface and logic for Super Admins to create and manage House Owner accounts.
- Implement views for listing, creating, updating, and deleting (CRUD) User accounts with the `OWNER` role.
- Ensure only users with `SUPER_ADMIN` role can access these views.
- Create Django templates for the Super Admin dashboard.

**Prompt for AI:**
> "In the `accounts` app, implement a set of views and templates for the Super Admin to manage House Owners. The Super Admin should be able to create, list, edit, and delete users who have the `OWNER` role. Use a custom decorator or Mixin to ensure only users with the `SUPER_ADMIN` role can access these views. Provide the views, URLs, and basic Bootstrap templates."

---

### Step 2: Owner Property Management
**Objective:** Allow House Owners to manage their own properties.
- Implement CRUD views for the `Property` model.
- **Crucial:** Filter all queries so an Owner can only see and edit properties they own.
- Create templates for adding and listing properties.

**Prompt for AI:**
> "In the `rentals` app, implement CRUD functionality for the `Property` model specifically for users with the `OWNER` role. Ensure that Owners can only view, edit, or delete properties where they are the assigned owner. Provide the views (using `LoginRequiredMixin` and role checks), URLs, and templates for the Owner's property management dashboard."

---

### Step 3: Tenant Assignment & Lease Creation
**Objective:** Enable Owners to link Tenants to their properties via the `Lease` model.
- Implement a view for Owners to create a `Lease`.
- The view should allow selecting a property (owned by the owner) and a user (with the `TENANT` role).
- Implement validation to ensure a property cannot have more than one active lease.

**Prompt for AI:**
> "In the `rentals` app, create a view that allows an Owner to assign a Tenant to one of their properties by creating a `Lease` record. The form should provide a dropdown of the Owner's properties and a dropdown of users with the `TENANT` role. Include server-side validation to prevent creating an active lease for a property that already has one. Provide the view, form, and template."

---

### Step 4: Owner's Rent Overview
**Objective:** Provide Owners with a high-level view of their properties and active leases.
- Create a dashboard view that lists all properties and their current lease status.
- Link to the payment history for each property.

**Prompt for AI:**
> "Create an 'Owner Overview' dashboard in the `rentals` app. This view should list all properties owned by the logged-in user, showing the current tenant (if any) and the monthly rent amount. Provide the view and the corresponding template."

---

## Summary of Phase 2
- **Super Admin** $\rightarrow$ Manages **Owners**
- **Owner** $\rightarrow$ Manages **Properties**
- **Owner** $\rightarrow$ Creates **Leases** (Links Property to Tenant)

## Implementation Progress

### ✅ Completed Steps
- **Step 1**: Super Admin Dashboard & Owner Management
- **Step 2**: Owner Property Management
- **Step 3**: Tenant Assignment & Lease Creation
- **Step 4**: Owner's Rent Overview
