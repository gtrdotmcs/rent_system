# Phase 2: Core Layout & Authentication

## 🎯 Goal
Establish the "App Shell" and the secure entry point.

## ✅ Checklist
- [ ] **Mobile Base Template:** Create `templates/base_mobile.html` using Tailwind CSS.
    - Implement Bottom Navigation (Home, Payments, Profile).
    - Create a dynamic content area (`#app-content`) for JS injection.
- [ ] **API-Driven Login:** Create `templates/login_mobile.html`.
    - JavaScript logic to POST credentials to `/api/v1/token/`.
    - Store JWT in `localStorage`.
- [ ] **Role-Based Routing:** Logic to detect role from the `/me/` endpoint and redirect to the correct dashboard.

## 🛠 Implementation Details
- Create new HTML files in the `templates/` directory.
- Create a `static/js/auth.js` for handling tokens and redirects.
- Setup Tailwind CSS via CDN in the base template.
