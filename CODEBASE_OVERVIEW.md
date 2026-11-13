# Codebase Overview & System Architecture

This document serves as the persistent reference across AI pair-programming and developer sessions for the **House Rent Management System (HRMS)**.

---

## 1. System Summary & Tech Stack

- **Framework**: Django & Django REST Framework (DRF)
- **Authentication**:
  - **Web Portal**: Session-based authentication with CSRF protection.
  - **REST API (`/api/v1/`)**: JWT authentication via `djangorestframework-simplejwt`.
- **Database**: PostgreSQL (configured in `rent_system/settings.py`)
- **Key Python Packages**: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `drf-spectacular`, `psycopg2`.

---

## 2. User Roles & Permission Model

Defined in [`accounts/models.py`](file:///i:/rent_system/accounts/models.py):

- **Custom User Model**: `accounts.User` extending `AbstractUser`.
- **Roles (`User.Role`)**:
  - `SUPER_ADMIN`: Administrative control (creates owners, manages system).
  - `OWNER`: Manages properties, creates leases, reviews/approves tenant payments.
  - `TENANT`: Views assigned active lease, submits rent payments, views payment history.
- **View Decorators (Web)**: Defined in [`rentals/views.py`](file:///i:/rent_system/rentals/views.py) and [`accounts/decorators.py`](file:///i:/rent_system/accounts/decorators.py):
  - `@owner_required`: Enforces `user.role == 'OWNER'`.
  - `@tenant_required`: Enforces `user.role == 'TENANT'`.
- **DRF Permission Classes (API)**: Defined in [`rentals/api.py`](file:///i:/rent_system/rentals/api.py):
  - `IsOwner`: Validates owner role.
  - `IsTenant`: Validates tenant role.
  - `IsOwnerOfProperty`: Object-level ownership check.
  - `IsTenantOfLease`: Object-level tenant check.

---

## 3. Core Models & Business Constraints

Defined in [`rentals/models.py`](file:///i:/rent_system/rentals/models.py):

### `Property`
- ForeignKey: `owner` (`settings.AUTH_USER_MODEL`, `related_name="properties"`).
- Fields: `name`, `address`, `city`, `description`.

### `Lease`
- ForeignKeys: `property` (`related_name="leases"`), `tenant` (`related_name="leases"`).
- Statuses: `ACTIVE`, `EXPIRED`, `TERMINATED`.
- **Constraint**: `one_active_lease_per_property` (`UniqueConstraint` on `property` where `status='ACTIVE'`).
- Validation: `end_date` must be after `start_date` if provided.

### `Payment`
- ForeignKey: `lease` (`related_name="payments"`).
- Fields: `amount_paid` (decimal > 0), `payment_date`, `month` (1-12), `year`, `status`.
- Statuses: `PENDING` (default), `APPROVED`, `REJECTED`.
- **Business Rule**: Tenants submit payments (forced to `PENDING`). Only property owners can switch status to `APPROVED` or `REJECTED`.
- Validation: Duplicate payments for the same lease, month, and year are rejected.

---

## 4. API Endpoints (`/api/v1/`)

Defined in [`rent_system/urls_api_v1.py`](file:///i:/rent_system/rent_system/urls_api_v1.py):

| Endpoint | Method | Permission | Description |
|---|---|---|---|
| `/api/v1/token/` | POST | AllowAny | Obtain JWT pair (access + refresh) |
| `/api/v1/token/refresh/` | POST | AllowAny | Refresh access token |
| `/api/v1/me/` | GET | IsAuthenticated | Current user profile |
| `/api/v1/properties/` | GET, POST | IsOwner | List/create owner properties |
| `/api/v1/properties/<int:pk>/` | GET, PUT, PATCH, DELETE | IsOwner, IsOwnerOfProperty | Detail view for property |
| `/api/v1/owner/leases/` | GET | IsOwner | List all leases belonging to owner's properties |
| `/api/v1/tenant/lease/` | GET | IsTenant | Retrieve active lease for authenticated tenant |
| `/api/v1/tenant/payments/` | GET, POST | IsTenant | List tenant payments / submit new pending payment |
| `/api/v1/owner/payments/pending/` | GET | IsOwner | List all pending payments across owner's properties |
| `/api/v1/owner/payments/<int:pk>/status/` | PATCH | IsOwner, IsOwnerOfProperty | Approve or reject a payment (`APPROVED`/`REJECTED`) |

---

## 5. Implementation Roadmap Status

Located in `context/phase1/AI_plan/`:
- **Phase 1**: DB Schema & Core Models (Completed)
- **Phase 2**: Management Logic & Owner Dashboard (Completed)
- **Phase 3**: Tenant Dashboard & Payment Submissions (Completed)
- **Phase 4**: REST API with JWT Auth (Completed)
- **Phase 5**: Security & Validation Hardening (IDOR, permissions, input validation) (Active / Completed)
- **Mobile Website Plan**: Located at `context/phase1/AI_plan/mobile_website/` — multi-phase plan for mobile-first UI using `/api/v1/`.

---

## 6. Known Audit Findings & Action Items

During codebase inspection, the following issues were identified that require fixes:

1. **Import Error in `rentals/serializers.py` (Line 4)**:
   ```python
   # CURRENT (BROKEN):
   from .models import Lease, Payment, Property, User
   # FIX:
   from django.contrib.auth import get_user_model
   from .models import Lease, Payment, Property
   User = get_user_model()
   ```

2. **Missing `class Meta` in `rentals/forms.py`**:
   `LeaseForm` and `PaymentForm` contain placeholder comments (`# ...existing code...`) and lack their inner `class Meta: model = ...; fields = ...`. Instantiating either form will crash with `ValueError: ModelForm has no model class specified`.

3. **URL Name Discrepancies in `rentals/tests.py`**:
   `SecurityRegressionTests` uses old URL route names:
   - `owner-property-detail` $\rightarrow$ should be `api-v1-property-detail`
   - `tenant-lease-list` $\rightarrow$ should be `api-v1-tenant-lease`
   - `owner-payment-status` $\rightarrow$ should be `api-v1-owner-payment-status`

---

## 7. Common Development Commands

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Django sanity check
.\.venv\Scripts\python.exe manage.py check

# Run test suite
.\.venv\Scripts\python.exe manage.py test rentals.tests

# Seed database
.\.venv\Scripts\python.exe manage.py seed_data

# Run server
.\.venv\Scripts\python.exe manage.py runserver
```

