# Phase 4: REST API Layer (Android Integration)

## Goal
Expose the system logic via a RESTful API using Django REST Framework (DRF) to support the Android mobile application. The API will be versioned (v1) to ensure backward compatibility for mobile clients.

---

## API Versioning Strategy
- **Method**: URL Path Versioning.
- **Pattern**: `/api/v1/<endpoint>/`
- **Reasoning**: Allows the Android app to continue using v1 while the backend evolves to v2, preventing app crashes on user devices.

---

## Step-by-Step Implementation Plan

### Step 1: DRF Setup, JWT Authentication & Versioning
**Objective:** Configure DRF, implement stateless JWT authentication, and set up the v1 URL routing.
- Install and configure `djangorestframework` and `djangorestframework-simplejwt`.
- Set up the authentication classes in `settings.py`.
- Create a versioned URL structure (`/api/v1/`).
- Create endpoints for obtaining and refreshing JWT tokens.

**Prompt for AI:**
> "Set up Django REST Framework (DRF) in the `rent_system` project. Configure `SimpleJWT` for authentication. Implement URL versioning by creating a separate URL configuration for `api/v1/`. Provide the updated `settings.py` and the URL configurations for the token obtain and refresh endpoints under the v1 prefix."

---

### Step 2: Property & Lease API Endpoints
**Objective:** Create API endpoints for viewing properties and leases.
- Implement Serializers for `Property` and `Lease` models.
- Create API views that enforce role-based access (e.g., Tenants can only see their own lease).

**Prompt for AI:**
> "Create DRF serializers and API views for the `Property` and `Lease` models. Implement endpoints that allow Tenants to retrieve their active lease details and Owners to list their properties. Ensure that the API enforces the same data isolation rules as the web portal. Provide the serializers, views, and URLs."

---

### Step 3: Payment Submission & Status API
**Objective:** Enable the Android app to submit payments and track their status.
- Implement a POST endpoint for submitting payments.
- Implement a GET endpoint for retrieving payment history.

**Prompt for AI:**
> "Implement API endpoints for the payment workflow. Create a POST endpoint for Tenants to submit a payment and a GET endpoint for Tenants to view their payment history and status. Ensure the endpoints are protected by JWT authentication. Provide the serializers, views, and URLs."

---

### Step 4: Owner Management API
**Objective:** Allow Owners to manage their properties and approve payments via the API.
- Create endpoints for updating property details.
- Create an endpoint for updating payment status (Approved/Rejected).

**Prompt for AI:**
> "Create API endpoints for Owners to manage their properties and approve/reject payments. The payment status endpoint should only be accessible to the owner of the property associated with the lease. Provide the serializers, views, and URLs."

---

## Summary of Phase 4
- **Auth**: JWT (Stateless)
- **Endpoints**: Properties, Leases, Payments (Role-restricted)
- **Client**: Android App $\rightarrow$ JSON $\rightarrow$ DRF

## API Usage

Install the dependencies in the project virtual environment:
```powershell
python -m pip install djangorestframework djangorestframework-simplejwt
```

Obtain a token with the user's username and password:
```http
POST /api/v1/token/
Content-Type: application/json

{"username": "api-tenant", "password": "password"}
```

Send the returned access token on protected requests:
```http
Authorization: Bearer <access-token>
```

Refresh an expired access token with `POST /api/v1/token/refresh/` and the refresh token.

## Role Access
- **OWNER**: Own properties, owner leases, and payment approval endpoints.
- **TENANT**: Own active lease and payment history/submission endpoints.
- **SUPER_ADMIN**: No Phase 4 mobile API endpoints are assigned yet; administration remains available through Django Admin and the web portal.
- Unauthenticated requests receive `401 Unauthorized`.
- Authenticated users with the wrong role receive `403 Forbidden`.
- An object outside the authenticated owner's or tenant's queryset behaves as not found (`404 Not Found`).

## Verification Command
Run the Django checks and test suite from the project root:
```powershell
python manage.py check
python manage.py test rentals.tests
```

## Implementation Progress

### Completed Steps
- **Step 1**: DRF Setup, JWT Authentication & Versioning
- **Step 2**: Property & Lease API Endpoints (v1)
- **Step 3**: Payment Submission & Status API
- **Step 4**: Owner Management API

### Implemented API Routes
- `POST /api/v1/token/` obtains access and refresh tokens.
- `POST /api/v1/token/refresh/` refreshes an access token.
- `GET|POST /api/v1/properties/` lists or creates owner properties.
- `GET|PATCH|PUT|DELETE /api/v1/properties/<id>/` manages an owner property.
- `GET /api/v1/owner/leases/` lists leases for the authenticated owner's properties.
- `GET /api/v1/tenant/lease/` returns the authenticated tenant's active leases.
- `GET|POST /api/v1/tenant/payments/` lists or submits tenant payments.
- `PATCH /api/v1/owner/payments/<id>/status/` approves or rejects an owned property's payment.

### Verification Notes
- DRF and SimpleJWT are installed and configured in `settings.py`.
- All API querysets enforce owner and tenant data isolation.
- Payment leases and `PENDING` status are assigned server-side.
- Django system checks pass and the touched Python files report no errors.
- API tests cover JWT issuance, role isolation, payment submission, and payment approval.
