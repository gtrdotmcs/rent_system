# Phase 1: Database Schema & Custom User Model Implementation Guide

This document outlines the step-by-step implementation of the foundation for the House Rent Management System (HRMS).

## Goal
Establish a robust database schema with a custom user model to support Role-Based Access Control (RBAC) for Super Admin, House Owners, and Tenants.

---

## Step-by-Step Implementation Plan

### Step 1: Project Initialization & Environment Setup
**Objective:** Set up the Django project and configure the database.
- Initialize Django project.
- Configure PostgreSQL database settings.
- Create the core application (e.g., `accounts` and `rentals`).

**Prompt for AI:**
> "Initialize a Django project named `rent_system`. Configure it to use PostgreSQL. Create two apps: `accounts` (for user management) and `rentals` (for properties, leases, and payments). Set up the basic folder structure and ensure the database connection is working."

---

### Step 2: Custom User Model Implementation
**Objective:** Create a flexible user model that supports different roles.
- Extend `AbstractUser`.
- Add a `Role` field with choices: `SUPER_ADMIN`, `OWNER`, `TENANT`.
- Update `AUTH_USER_MODEL` in `settings.py`.

**Prompt for AI:**
> "In the `accounts` app, implement a custom user model extending `AbstractUser`. Add a field `role` using a TextChoice with options: `SUPER_ADMIN`, `OWNER`, and `TENANT`. Update the `settings.py` to use this custom user model. Provide the code for `models.py` and the necessary migrations."

---

### Step 3: Property Model Implementation
**Objective:** Define how properties are stored and linked to owners.
- Create `Property` model in the `rentals` app.
- Link `Property` to the Custom User (Owner) via a ForeignKey.
- Include fields: address, property type, number of rooms, etc.

**Prompt for AI:**
> "In the `rentals` app, create a `Property` model. It should have a ForeignKey relationship to the custom User model (specifically for users with the `OWNER` role). Include fields for property name, address, city, and a description. Ensure the relationship is defined so one owner can have multiple properties."

---

### Step 4: Lease/Agreement Model Implementation
**Objective:** Link tenants to properties and define rent terms.
- Create `Lease` model.
- Link to `Property` and `User` (Tenant).
- Include fields: start date, end date, monthly rent amount, and status.

**Prompt for AI:**
> "In the `rentals` app, implement a `Lease` model. This model should link a `Property` to a `User` (the tenant). Add fields for `start_date`, `end_date`, `monthly_rent`, and a `status` field (e.g., Active, Expired, Terminated). Ensure that a property can only have one active lease at a time."

---

### Step 5: Payment Model Implementation
**Objective:** Track rent payments and their approval status.
- Create `Payment` model.
- Link to `Lease`.
- Include fields: amount, payment date, month/year of rent, and status (Pending, Approved, Rejected).

**Prompt for AI:**
> "In the `rentals` app, create a `Payment` model linked to the `Lease` model. It should track the `amount_paid`, `payment_date`, the `month` and `year` the payment is for, and a `status` field with choices: `Pending`, `Approved`, and `Rejected`. Default status should be `Pending`."

---

### Step 6: Database Migration & Verification
**Objective:** Apply all changes to the database and verify the schema.
- Run `makemigrations` and `migrate`.
- Create a superuser.
- Use Django Admin to verify the models.

**Prompt for AI:**
> "Provide the commands to run migrations for all apps. Then, show me how to create a superuser and how to register these models in `admin.py` so I can verify the database structure through the Django Admin panel."


---

## Summary of Model Relationships
- **User (Custom)** $\rightarrow$ **Property**: One-to-Many (Owner $\rightarrow$ Properties)
- **Property** $\rightarrow$ **Lease**: One-to-Many (Property $\rightarrow$ Leases over time)
- **User (Custom)** $\rightarrow$ **Lease**: One-to-Many (Tenant $\rightarrow$ Leases)
- **Lease** $\rightarrow$ **Payment**: One-to-Many (Lease $\rightarrow$ Monthly Payments)

---

## Implementation Progress

### ✅ Completed Steps
- **Step 1**: Project Initialization & Environment Setup
- **Step 2**: Custom User Model Implementation
- **Step 3**: Property Model Implementation
- **Step 4**: Lease/Agreement Model Implementation
- **Step 5**: Payment Model Implementation
- **Step 6**: Database Migration & Verification
