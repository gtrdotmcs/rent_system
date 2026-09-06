# Modern Mobile-First Web UI Plan (API-Driven)

## 🎯 Objective
Transform the current server-side rendered (SSR) website into a modern, mobile-friendly Single Page Application (SPA) experience. The UI will act as a client that communicates with the existing Django REST API (DRF) via JSON, ensuring a consistent experience between the web and the future Android app.

## 🛠 Tech Stack Proposal
- **Frontend:** HTML5, Tailwind CSS (for mobile-first responsiveness), and Vanilla JavaScript (Fetch API) or Vue.js/React.
- **Communication:** REST API (`/api/v1/`) using JWT (JSON Web Tokens) for authentication.
- **Design Philosophy:** App-like experience (Bottom navigation for mobile, Sidebar for desktop).

---

## 🗺️ UI/UX Roadmap

### 1. Authentication Layer (Universal)
- **Login Page:** 
    - Clean, centered card layout.
    - Mobile-responsive input fields.
    - Stores JWT token in `localStorage` or `Secure Cookie` upon success.
    - Redirects user based on their assigned `Role`.

### 2. Role-Based Access Control (RBAC) Navigation
The system will detect the user role from the JWT payload or a `/api/v1/user/me/` endpoint to render the appropriate dashboard.

#### A. Tenant View (The User Experience)
- **Dashboard:** 
    - Current Lease status (Active/Expired).
    - Next payment due date and amount.
- **My Details Page:** 
    - Personal profile info.
    - Property address linked to their lease.
- **Payment Portal:** 
    - Form to submit a new payment.
    - History list of previous payments with status badges (Pending $\rightarrow$ Approved).

#### B. Owner View (The Management Experience)
- **Property Portfolio:** 
    - Grid view of properties owned by the user.
    - Quick stats (Total Units, Occupied vs. Vacant).
- **Property Detail View:** 
    - List of tenants currently leasing the property.
    - Option to create new leases.
- **Payment Approval Center:** 
    - List of "Pending" payments from all their properties.
    - One-click "Approve" or "Reject" buttons.

#### C. Super Admin View (The System Control)
- **Global Overview:** 
    - Total Owners, Total Tenants, and Total Properties across the system.
- **User Management:** 
    - Table of all Owners with ability to Create/Edit/Delete.
- **System Audit:** 
    - Ability to track all properties and lease agreements globally.

---

## 🚀 Implementation Phases

### Phase 1: API Alignment
- Ensure all required endpoints exist in `rentals/api.py` (e.g., `/me/` endpoint for profile details).
- Implement JWT refresh token logic for seamless mobile sessions.

### Phase 2: Core Layout & Auth
- Create `base_mobile.html` with a responsive navigation bar.
- Build the API-driven Login page.

### Phase 3: Role-Specific Modules
- Develop the Tenant Dashboard $\rightarrow$ Owner Portfolio $\rightarrow$ Admin Panel in sequence.

### Phase 4: Optimization
- Add "Loading" skeletons and "Toast" notifications for API responses.
- PWA (Progressive Web App) support for "Add to Home Screen" capability.
