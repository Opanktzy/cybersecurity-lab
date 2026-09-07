# Cybersecurity Lab — Architecture

## 1. Overview

Cybersecurity Lab is a local security research environment designed to demonstrate a complete application security workflow:

> Discover → Exploit → Remediate → Test → Automate → Detect → Document

The project uses an intentionally vulnerable FastAPI application as the primary target. All security testing is performed against the local lab environment.

The project is designed for educational and portfolio purposes and is not intended for production deployment.

---

## 2. Architecture

```text
                         ┌─────────────────────────┐
                         │    Cybersecurity Lab    │
                         └────────────┬────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
       ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
       │  Web Security  │    │   Automation   │    │   Detection    │
       │      Lab       │    │                │    │   Engineering  │
       └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
               │                     │                     │
               ▼                     ▼                     ▼
          FastAPI API          Python Scanner        Log Analyzer
               │                     │                     │
       ┌───────┼────────┐      ┌─────┴─────┐         ┌─────┴─────┐
       ▼       ▼        ▼      ▼           ▼         ▼           ▼
      IDOR    SQLi    Cmd      Recon      Web      Rules       Alerts
                       Injection Scanner   Scanner
               │
               ▼
       ┌────────────────┐
       │   Remediation  │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ Security Tests  │
       │     Pytest      │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ GitHub Actions  │
       │      CI         │
       └────────────────┘
```

---

## 3. Web Security Lab

The web security component is implemented using FastAPI.

The application intentionally contains security weaknesses for controlled research and demonstration.

### Target endpoints

| Endpoint           | Purpose                       |
| ------------------ | ----------------------------- |
| `/`                | Application status            |
| `/health`          | Health check                  |
| `/login`           | Lab authentication simulation |
| `/users`           | User listing                  |
| `/users/me`        | Current-user information      |
| `/users/{user_id}` | User object access            |
| `/products`        | Product search                |
| `/ping`            | Host connectivity test        |

### Vulnerabilities studied

#### VULN-001 — Broken Access Control

The application initially allowed users to access other users' objects without proper authorization.

The vulnerability was reproduced using a local authenticated request and subsequently remediated using object-level authorization.

Expected behavior:

```text
Alice → /users/1 → 200 OK
Alice → /users/2 → 403 Forbidden
Admin → /users/2 → 200 OK
```

---

#### VULN-002 — SQL Injection

The product search endpoint initially constructed SQL queries using untrusted user input.

The vulnerability was demonstrated in the local lab using a controlled SQL injection payload.

The remediation uses parameterized SQL queries:

```python
query = """
    SELECT id, name, category, price
    FROM products
    WHERE name LIKE ?
"""
```

User input is supplied separately from the SQL statement.

---

#### VULN-003 — OS Command Injection

The `/ping` endpoint was initially vulnerable to command injection because user-controlled input was passed to a shell command.

The vulnerable implementation was replaced with:

```python
subprocess.run(
    ["ping", "-c", "1", host],
    capture_output=True,
    text=True,
    timeout=5,
)
```

Input validation is also performed using Python's `ipaddress` module.

---

## 4. Security Automation

The automation layer contains lightweight Python security utilities.

### Reconnaissance Scanner

`automation/recon.py`

Responsibilities:

* Check selected TCP ports
* Identify reachable local services
* Generate a reconnaissance report
* Demonstrate basic socket-based security automation

This tool is intentionally lightweight and is not intended to replace professional scanners such as Nmap.

### Web Security Scanner

`automation/vuln_scanner.py`

The scanner performs basic checks against the local API.

Current checks include:

* Content Security Policy
* X-Content-Type-Options
* X-Frame-Options
* HTTP Strict Transport Security
* Known lab endpoints

The scanner is designed as a learning exercise in automated security assessment.

---

## 5. Detection Engineering

The detection component simulates a small security monitoring workflow.

```text
Access Logs
     │
     ▼
Log Analyzer
     │
     ▼
Detection Rules
     │
     ▼
Security Alerts
     │
     ▼
Incident Report
```

### Detection rules

Current rules detect patterns associated with:

* SQL injection
* Command injection
* Forbidden access
* Repeated HTTP 403 responses

The analyzer processes application access logs and generates security alerts.

---

## 6. Incident Response

Detected activity is documented in an incident report.

The workflow is:

```text
Suspicious Request
       ↓
Log Analysis
       ↓
Detection Rule
       ↓
Alert
       ↓
Investigation
       ↓
Incident Documentation
```

This demonstrates the transition from vulnerability research into defensive security and incident analysis.

---

## 7. Security Regression Testing

The project uses `pytest` to ensure previously remediated vulnerabilities remain fixed.

The test suite verifies:

* Application health
* Object-level authorization
* Administrative access
* SQL injection remediation
* Command injection prevention

Example:

```python
def test_user_cannot_access_other_user_profile():
    response = client.get(
        "/users/2",
        headers={"X-Token": "alice-token"},
    )

    assert response.status_code == 403
```

This prevents future code changes from silently reintroducing known vulnerabilities.

---

## 8. CI/CD

GitHub Actions is used to automatically execute the security regression suite.

The intended workflow is:

```text
Developer
    │
    ▼
git push
    │
    ▼
GitHub Actions
    │
    ▼
Install Dependencies
    │
    ▼
Run Pytest
    │
    ├───────────────┐
    ▼               ▼
  PASS             FAIL
    │               │
    ▼               ▼
Continue         Block/Investigate
```

This provides a basic DevSecOps workflow where security tests become part of the development lifecycle.

---

## 9. Repository Structure

```text
cybersecurity-lab/
│
├── automation/
│   ├── recon.py
│   └── vuln_scanner.py
│
├── detection/
│   ├── logs/
│   ├── rules/
│   └── log_analyzer.py
│
├── docs/
│   └── architecture.md
│
├── reports/
│   ├── VULN-001-broken-access-control.md
│   ├── VULN-002-sql-injection.md
│   ├── VULN-003-command-injection.md
│   ├── INCIDENT-001-suspicious-web-activity.md
│   └── recon-002-automated-scan.md
│
└── web-security/
    └── lab-target/
        ├── app/
        ├── tests/
        ├── requirements.txt
        └── pytest.ini
```

---

## 10. Security Scope

This project is intentionally limited to a local security research environment.

Testing should only be performed against systems that are owned by the researcher or where explicit authorization has been provided.

The intentionally vulnerable API should not be exposed to the public internet.

The authentication mechanism and vulnerabilities are intentionally simplified for educational purposes and should not be considered production-ready security implementations.

---

## 11. Skills Demonstrated

This project demonstrates practical experience with:

* Web application security
* Broken access control
* SQL injection
* Command injection
* Secure coding
* Python security automation
* TCP reconnaissance
* HTTP security analysis
* Detection engineering
* Log analysis
* Incident documentation
* Security regression testing
* Pytest
* CI/CD
* Git and GitHub
* Linux-based security workflows

---

## 12. Security Engineering Workflow

The complete project follows:

```text
             ┌──────────────┐
             │   Discover   │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │     PoC      │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │  Remediate   │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │     Test     │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │   Automate   │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │    Detect    │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │  Document    │
             └──────────────┘
```

The goal is not to build a production security platform, but to demonstrate understanding of the security engineering lifecycle through a reproducible local laboratory.
