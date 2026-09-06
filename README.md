# House Rent Management System (HRMS)

A comprehensive Django-based system for managing rental properties, leases, and payments with a secure REST API for mobile integration.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL Database
- Virtual Environment (venv)

### Installation
1. **Clone the repository**
2. **Set up a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install django djangorestframework djangorestframework-simplejwt psycopg2
   ```
4. **Configure Database:**
   Update `rent_system/settings.py` with your PostgreSQL credentials.
5. **Run Migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create Superuser:**
   ```powershell
   python manage.py createsuperuser
   ```
7. **Start Server:**
   ```powershell
   python manage.py runserver
   ```

---

## 📊 Seeding Dummy Data

The system includes a custom management command to populate the database for testing.

**Run the seed command:**
```powershell
python manage.py seed_data
```
*This will create test Owners, Tenants, Properties, and Leases.*

---

## 🧪 Testing

### Running Backend Tests
Run the complete test suite to verify business logic and security boundaries:
```powershell
python manage.py test rentals.tests
```

### Manual Verification
1. **Super Admin:** Login to `/admin` to manage Owners.
2. **Owner:** Login to the web portal to create Properties and assign Tenants via Leases.
3. **Tenant:** Login to the tenant dashboard to submit rent payments.

---

## 📱 API Testing (REST API v1)

The API is secured using **JWT (JSON Web Tokens)**. All endpoints are prefixed with `/api/v1/`.

### 1. Authentication
Obtain an access token by sending a POST request to `/api/v1/token/`:
**Request:**
```http
POST /api/v1/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```
**Response:**
```json
{
    "refresh": "...",
    "access": "<your_access_token>"
}
```

### 2. Using the Token
Include the access token in the `Authorization` header for all protected requests:
`Authorization: Bearer <your_access_token>`

### 3. Key Endpoints
| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/api/schema/swagger-ui/` | GET | Any | **Interactive API Documentation (Swagger)** |
| `/api/schema/redoc/` | GET | Any | **Alternative API Documentation (Redoc)** |
| `/api/v1/properties/` | GET/POST | Owner | List or Create properties |
| `/api/v1/leases/` | GET | Tenant/Owner | View active leases |
| `/api/v1/payments/` | GET/POST | Tenant | View history or Submit payment |
| `/api/v1/payments/<id>/` | PATCH | Owner | Approve/Reject a payment |

---

## 🛡️ Security Features
- **RBAC:** Role-Based Access Control (Super Admin, Owner, Tenant).
- **Data Isolation:** Users cannot access or modify data belonging to others (IDOR protection).
- **Validation:** Strict server-side validation for payment amounts and lease date ranges.
- **Stateless Auth:** JWT implementation for mobile clients.
