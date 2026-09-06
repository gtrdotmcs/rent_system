# Phase 1: API Enrichment & Foundation

## 🎯 Goal
Ensure the backend provides all the data necessary for a dynamic frontend without page reloads.

## ✅ Checklist
- [ ] **User Profile Endpoint:** Implement `GET /api/v1/user/me/` to return the current user's role, full name, and email.
- [ ] **Owner Summary Endpoint:** Implement `GET /api/v1/owner/dashboard/` to return total properties and a count of pending payments.
- [ ] **Tenant Summary Endpoint:** Implement `GET /api/v1/tenant/dashboard/` to return active lease status and next payment due date.
- [ ] **Admin Global Stats:** Implement `GET /api/v1/admin/stats/` for system-wide totals (Owners, Tenants, Properties).
- [ ] **JWT Optimization:** Ensure refresh token logic is working for seamless mobile sessions.

## 🛠 Implementation Details
- Edit `rentals/api.py` to add new views.
- Create necessary serializers in `rentals/serializers.py`.
- Update `rent_system/urls_api_v1.py` to expose these endpoints.
