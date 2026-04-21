# StockPilot
A Secure Inventory &amp; Purchase Order Management System with Integrated Role-Based Access Control. One cockpit for controlling your inventory operations, procurement workflow, and user access - built with Django, DRF, Celery, and PostgreSQL.

---

## Tech Stack

- Python 3.12
- Django 5
- Django REST Framework
- django-filter
- Pillow
- SQLite (development)
- Session Authentication + CSRF protection

---

## Current Project Status

### Completed Phases

#### Phase 0 — Project Setup
- Virtual environment setup
- Modular Django project structure
- Environment-based settings split (`base.py`, `dev.py`, `prod.py`)
- `.env` configuration
- Git and repository initialization

#### Phase 1 — Users, Custom Auth, and RBAC
- Custom `User` model with email-based login
- Role-based access control (RBAC)
- Roles implemented:
  - Admin
  - Inventory Manager
  - Procurement Officer
  - Auditor
- Session-based authentication APIs
- CSRF endpoint for Postman/testing
- User admin integration
- Auth test coverage

#### Phase 2 — Inventory Module
- Inventory app setup
- Category and Product models
- Product image upload support
- Stock movement tracking
- Product filtering, searching, and pagination
- Inventory admin customization
- DRF CRUD APIs for categories and products
- RBAC enforcement for inventory operations
- Inventory tests

#### Phase 3 — Suppliers Module
- Suppliers app setup
- Supplier model implementation
- Many-to-many relationship between suppliers and products
- Supplier admin integration
- DRF CRUD APIs for suppliers
- RBAC enforcement for supplier operations
- Supplier tests

---

## Features Implemented

- Custom email-based authentication
- Role-based access control
- Session login/logout/me endpoints
- CSRF-aware API testing support
- Category management
- Product management
- Supplier management
- Product-supplier linking
- Stock tracking and low-stock detection
- Stock movement history
- Admin panel support
- API filtering, search, and pagination
- Automated test coverage for core modules

---

## Project Structure

```bash
stockpilot/
├── apps/
│   ├── users/
│   ├── inventory/
│   └── suppliers/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
├── media/
├── static/
├── requirements/
├── manage.py
└── README.md

## Authentication Endpoints

### Auth APIs
- `GET /api/auth/csrf/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

### Inventory APIs
- `GET /api/categories/`
- `POST /api/categories/`
- `GET /api/products/`
- `POST /api/products/`

### Supplier APIs
- `GET /api/suppliers/`
- `POST /api/suppliers/`

---

## Roles and Access

### Admin
- Full access to all modules

### Inventory Manager
- Full access to inventory-related operations

### Procurement Officer
- Full access to supplier-related operations

### Auditor
- Read-only access where permitted

---

## Filtering and Query Support

### Products

Supports:
- category filtering
- active/inactive filtering
- creator filtering
- min/max price filtering
- low-stock filtering
- search
- ordering
- pagination