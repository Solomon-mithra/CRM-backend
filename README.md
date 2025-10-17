
# Backend API Documentation

## Overview

This document describes the backend API for authentication, lead management, activities, and dashboard metrics. It consolidates the validated manual tests into clear references with example requests and responses.

### Tech and Runtime

- Framework: FastAPI
- Dev server: Uvicorn
- Start command:

```bash
venv/bin/uvicorn main:app --reload
```

### Authentication

- Scheme: Bearer token (JWT)
- Obtain token: Login with username and password to receive `access_token`
- Use token: Add header `Authorization: Bearer <access_token>` to protected requests

---

### Base URL

Use your local server base. The examples below reference the [localhost](http://localhost) routes used during testing.

---

### Endpoints Summary

- POST Register user: http://localhost:8000/api/users/register
- POST Login: http://localhost:8000/api/users/login
- GET Current user: http://localhost:8000/api/users/me
- POST Create lead: http://localhost:8000/api/leads
- GET List leads (active): http://0.0.0.0:8000/api/leads
- GET Lead by id: http://localhost:8000/api/leads/<lead_id>
    
    Example: http://localhost:8000/api/leads/1
    
- PUT Update lead: http://localhost:8000/api/leads/<lead_id>
    
    Example: http://localhost:8000/api/leads/1
    
- DELETE Soft delete lead: http://localhost:8000/api/leads/<lead_id>
    
    Example: http://localhost:8000/api/leads/1
    
- POST Create activity for a lead: http://localhost:8000/api/leads/<lead_id>/activities
    
    Example: http://localhost:8000/api/leads/1/activities
    
- GET List activities for a lead: http://localhost:8000/api/leads/<lead_id>/activities
    
    Example: http://localhost:8000/api/leads/1/activities
    
- GET Dashboard stats: http://localhost:8000/api/dashboard/statistics

---

### 1) Register User

- Method: POST
- URL: http://localhost:8000/api/users/register
- Auth: Not required
- Request (JSON):

```json
{
  "username": "testuser",
  "email": "[test@example.com](mailto:test@example.com)",
  "password": "password123",
  "first_name": "Test",
  "last_name": "User"
}
```

- Expected Response: 200 OK
    
    Body contains the created user details without password.
    

---

### 2) Login

- Method: POST
- URL: http://localhost:8000/api/users/login
- Auth: Not required
- Request (form):
    - username: testuser
    - password: password123
- Expected Response: 200 OK

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

- Note: Copy `access_token` and use it as Bearer token for protected endpoints.

---

### 3) Get Current User

- Method: GET
- URL: http://localhost:8000/api/users/me
- Auth: Bearer token required
- Expected Response: 200 OK

```json
{
  "id": 1,
  "username": "testuser",
  "email": "[test@example.com](mailto:test@example.com)",
  "first_name": "Test",
  "last_name": "User",
  "created_at": "2025-10-15T23:18:24"
}
```

---

### 4) Create Lead

- Method: POST
- URL: http://localhost:8000/api/leads
- Auth: Bearer token required
- Request (JSON):

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "[john.doe@example.com](mailto:john.doe@example.com)",
  "phone": "123-456-7890",
  "status": "new",
  "source": "website",
  "budget_min": 300000,
  "budget_max": 450000,
  "property_interest": "3BR house in suburban area"
}
```

- Expected Response: 200 OK

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "[john.doe@example.com](mailto:john.doe@example.com)",
  "phone": "123-456-7890",
  "status": "new",
  "source": "website",
  "budget_min": 300000,
  "budget_max": 450000,
  "property_interest": "3BR house in suburban area",
  "is_active": true,
  "created_at": "2025-10-15T23:35:58",
  "updated_at": "2025-10-15T23:35:58",
  "activity_count": 0
}
```

- Note: Save the returned `id` for subsequent operations.

---

### 5) List Leads (active)

- Method: GET
- URL: http://0.0.0.0:8000/api/leads
- Auth: Bearer token required
- Expected Response: 200 OK

```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "[john.doe@example.com](mailto:john.doe@example.com)",
    "phone": "123-456-7890",
    "status": "new",
    "source": "website",
    "budget_min": 300000,
    "budget_max": 450000,
    "property_interest": "3BR house in suburban area",
    "is_active": true,
    "created_at": "2025-10-15T23:35:58",
    "updated_at": "2025-10-15T23:35:58",
    "activity_count": 0
  }
]
```

---

### 6) Get Lead By ID

- Method: GET
- URL: http://localhost:8000/api/leads/<lead_id>
- Example: http://localhost:8000/api/leads/1
- Auth: Bearer token required
- Expected Response: 200 OK

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "[john.doe@example.com](mailto:john.doe@example.com)",
  "phone": "123-456-7890",
  "status": "new",
  "source": "website",
  "budget_min": 300000,
  "budget_max": 450000,
  "property_interest": "3BR house in suburban area",
  "is_active": true,
  "created_at": "2025-10-15T23:35:58",
  "updated_at": "2025-10-15T23:35:58",
  "activity_count": 0
}
```

---

### 7) Update Lead

- Method: PUT
- URL: http://localhost:8000/api/leads/<lead_id>
- Example: http://localhost:8000/api/leads/1
- Auth: Bearer token required
- Request (JSON):

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "[john.doe.updated@example.com](mailto:john.doe.updated@example.com)",
  "phone": "123-456-7890",
  "status": "contacted",
  "source": "website",
  "budget_min": 300000,
  "budget_max": 450000,
  "property_interest": "3BR house in suburban area"
}
```

- Expected Response: 200 OK

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "[john.doe.updated@example.com](mailto:john.doe.updated@example.com)",
  "phone": "123-456-7890",
  "status": "contacted",
  "source": "website",
  "budget_min": 300000,
  "budget_max": 450000,
  "property_interest": "3BR house in suburban area",
  "is_active": true,
  "created_at": "2025-10-15T23:35:58",
  "updated_at": "2025-10-15T23:43:39",
  "activity_count": 0
}
```

---

### 8) Create Activity for a Lead

- Method: POST
- URL: http://localhost:8000/api/leads/<lead_id>/activities
- Example: http://localhost:8000/api/leads/1/activities
- Auth: Bearer token required
- Request (JSON):

```json
{
  "activity_type": "call",
  "title": "Initial contact call",
  "notes": "Discussed property preferences.",
  "duration": 15,
  "activity_date": "2025-10-15"
}
```

- Expected Response: 200 OK

```json
{
  "id": 4,
  "lead_id": 1,
  "user_id": 1,
  "activity_type": "call",
  "title": "Initial contact call",
  "notes": "Discussed property preferences.",
  "duration": 15,
  "activity_date": "2025-10-15",
  "created_at": "2025-10-15T23:54:37",
  "user_name": "testuser"
}
```

---

### 9) List Activities for a Lead

- Method: GET
- URL: http://localhost:8000/api/leads/<lead_id>/activities
- Example: http://localhost:8000/api/leads/1/activities
- Auth: Bearer token required
- Expected Response: 200 OK

```json
[
  { "id": 1, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:46:26", "user_name": "testuser" },
  { "id": 2, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:46:58", "user_name": "testuser" },
  { "id": 3, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:53:22", "user_name": "testuser" },
  { "id": 4, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:54:37", "user_name": "testuser" }
]
```

---

### 10) Soft Delete Lead

- Method: DELETE
- URL: http://localhost:8000/api/leads/<lead_id>
- Example: http://localhost:8000/api/leads/1
- Auth: Bearer token required
- Expected Response: 200 OK
    
    Body should return the lead with `is_active: false`.
    
- Observed Sample Response when id not found:

```json
{ "detail": "Lead not found" }
```

---

### 11) Dashboard Statistics

- Method: GET
- URL: http://localhost:8000/api/dashboard/statistics
- Auth: Bearer token required
- Expected Response: 200 OK

```json
{
  "total_leads": 0,
  "new_leads_this_week": 1,
  "closed_leads_this_month": 0,
  "total_activities": 4,
  "leads_by_status": [ { "status": "contacted", "count": 1 } ],
  "recent_activities": [
    { "id": 4, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:54:37", "user_name": "testuser" },
    { "id": 3, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:53:22", "user_name": "testuser" },
    { "id": 2, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:46:58", "user_name": "testuser" },
    { "id": 1, "lead_id": 1, "user_id": 1, "activity_type": "call", "title": "Initial contact call", "notes": "Discussed property preferences.", "duration": 15, "activity_date": "2025-10-15", "created_at": "2025-10-15T23:46:26", "user_name": "testuser" }
  ]
}
```

---

### Status Codes

- 200 OK: Successful request
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation error

### Data Models (observed)

- User: id, username, email, first_name, last_name, created_at
- Lead: id, first_name, last_name, email, phone, status, source, budget_min, budget_max, property_interest, is_active, created_at, updated_at, activity_count
- Activity: id, lead_id, user_id, activity_type, title, notes, duration, activity_date, created_at, user_name

### cURL Examples

Login and capture token:

```bash
curl -X POST \
  -F "username=testuser" -F "password=password123" \
  http://localhost:8000/api/users/login
```

Get current user:

```bash
curl -H "Authorization: Bearer <JWT>" http://localhost:8000/api/users/me
```

Create a lead:

```bash
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "[john.doe@example.com](mailto:john.doe@example.com)",
    "phone": "123-456-7890",
    "status": "new",
    "source": "website",
    "budget_min": 300000,
    "budget_max": 450000,
    "property_interest": "3BR house in suburban area"
  }' \
  http://localhost:8000/api/leads
```

List leads:

```bash
curl -H "Authorization: Bearer <JWT>" http://0.0.0.0:8000/api/leads
```

Create an activity:

```bash
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
  -d '{
    "activity_type": "call",
    "title": "Initial contact call",
    "notes": "Discussed property preferences.",
    "duration": 15,
    "activity_date": "2025-10-15"
  }' \
  http://localhost:8000/api/leads/1/activities
```