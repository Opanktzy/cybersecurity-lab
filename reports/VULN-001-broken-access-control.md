# VULN-001 — Broken Access Control / IDOR Simulation

## 1. Summary

The `/users/{user_id}` endpoint allows a client to retrieve user objects by directly supplying an object identifier.

The application does not implement authorization checks before returning the requested user object.

This creates a Broken Access Control condition and simulates an Insecure Direct Object Reference (IDOR) scenario.

---

## 2. Scope

Target:

```text
http://127.0.0.1:8000
```

Endpoint:

```text
GET /users/{user_id}
```

Environment:

```text
Localhost / intentionally vulnerable security laboratory
```

This test was performed only against the locally owned laboratory application.

---

## 3. Discovery

Initial enumeration showed that the API exposes a user collection through:

```text
GET /users
```

The application returns multiple user objects containing identifiers.

Example:

```json
[
    {
        "id": 1,
        "username": "alice",
        "role": "user"
    },
    {
        "id": 2,
        "username": "bob",
        "role": "user"
    },
    {
        "id": 3,
        "username": "admin",
        "role": "admin"
    }
]
```

The presence of predictable numeric identifiers suggested that object-level authorization should be tested.

---

## 4. Proof of Concept

Request:

```http
GET /users/1
```

Response:

```json
{
    "id": 1,
    "username": "alice",
    "role": "user"
}
```

Changing the object identifier:

```http
GET /users/3
```

returns:

```json
{
    "id": 3,
    "username": "admin",
    "role": "admin"
}
```

The server does not verify whether the requester is authorized to access the requested object.

---

## 5. Automated Verification

A Python PoC was created:

```text
tests/test_idor.py
```

The script requests multiple object identifiers and records the HTTP responses.

Example result:

```text
GET /users/1 -> 200
GET /users/2 -> 200
GET /users/3 -> 200
```

---

## 6. Impact

In this laboratory application, the exposed information is intentionally non-sensitive.

In a real application, the same authorization weakness could allow users to access objects belonging to other users.

Depending on the exposed data, potential impact could include:

* Unauthorized data disclosure
* Access to another user's profile
* Exposure of confidential information
* Unauthorized modification of resources
* Privilege-related information disclosure

The actual severity depends on the sensitivity of the affected objects and the available operations.

---

## 7. Root Cause

The endpoint retrieves a user object based solely on the supplied `user_id`.

Conceptually:

```text
client-controlled ID
        ↓
database/object lookup
        ↓
object returned
```

There is no authorization decision between the object lookup and response.

---

## 8. Recommended Remediation

Implement server-side authorization checks before returning an object.

The application should verify:

```text
Authenticated user
        ↓
Requested object
        ↓
Authorization policy
        ↓
Allow / Deny
```

For example:

```python
if requested_user.id != current_user.id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden",
    )
```

Administrative access should be explicitly handled through an authorization policy rather than inferred from a user-controlled identifier.

---

## 9. Retest Plan

After remediation, repeat the same requests:

```text
GET /users/1
GET /users/2
GET /users/3
```

The application should only return objects that the authenticated user is authorized to access.

Unauthorized requests should return an appropriate response such as:

```text
403 Forbidden
```

---

## 10. Security Classification

Category:

```text
Broken Access Control
```

Related concept:

```text
Insecure Direct Object Reference (IDOR)
```

Primary weakness:

```text
Missing object-level authorization
```

---

## 11. Evidence

Evidence collected during testing:

```text
nmap service enumeration
curl HTTP requests
Python automated PoC
API responses
```

The complete test was performed against the local CyberLab environment.
