# 🔐 Cybersecurity Lab

> A local cybersecurity research laboratory demonstrating vulnerability discovery, secure remediation, security automation, detection engineering, regression testing, and CI/CD.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Pytest](https://img.shields.io/badge/Pytest-Security%20Testing-orange)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-red)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

---

## 🎯 Overview

**Cybersecurity Lab** is a controlled, local security research environment built to demonstrate practical application security and defensive security workflows.

The project intentionally uses a vulnerable FastAPI application as a local target. Vulnerabilities are reproduced in a controlled environment, remediated using secure coding practices, and verified through automated security regression tests.

The project follows this workflow:

```text
Discover
   ↓
PoC
   ↓
Remediate
   ↓
Retest
   ↓
Automate
   ↓
Detect
   ↓
Document
```

The goal is to demonstrate **security engineering methodology**, rather than simply collecting security tools or vulnerability examples.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │  Cybersecurity Lab    │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │ Web Security│       │ Automation  │       │  Detection  │
      │     Lab     │       │             │       │ Engineering │
      └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
             │                     │                     │
             ▼                     ▼                     ▼
          FastAPI              Python Tools         Log Analyzer
             │                     │                     │
       ┌─────┼─────┐          ┌────┴────┐          ┌─────┴─────┐
       ▼     ▼     ▼          ▼         ▼          ▼           ▼
      IDOR  SQLi  Cmd       Recon      Web        Rules      Alerts
                  Injection  Scanner   Scanner
       │
       ▼
   Remediation
       │
       ▼
  Security Tests
     Pytest
       │
       ▼
 GitHub Actions
```

Detailed architecture documentation:

[`docs/architecture.md`](docs/architecture.md)

---

# 🔎 Web Security Research

The lab currently covers three application security vulnerabilities.

## VULN-001 — Broken Access Control / IDOR

### Scenario

The application initially allowed an authenticated user to access another user's object without proper object-level authorization.

### Example

```text
Alice → /users/1 → 200 OK
Alice → /users/2 → 403 Forbidden
Admin → /users/2 → 200 OK
```

### Remediation

Object-level authorization was implemented to verify whether the authenticated user is authorized to access the requested object.

Report:

[`reports/VULN-001-broken-access-control.md`](reports/VULN-001-broken-access-control.md)

---

## VULN-002 — SQL Injection

### Scenario

The product search functionality was initially vulnerable to SQL injection because user input was incorporated directly into a SQL query.

### Remediation

The vulnerable query was replaced with a parameterized SQL statement.

```python
query = """
    SELECT id, name, category, price
    FROM products
    WHERE name LIKE ?
"""
```

User-controlled input is supplied separately as a SQL parameter.

Report:

[`reports/VULN-002-sql-injection.md`](reports/VULN-002-sql-injection.md)

---

## VULN-003 — OS Command Injection

### Scenario

The `/ping` endpoint initially passed user-controlled input into a shell command.

### Remediation

The implementation was changed to execute the command using an argument list instead of shell interpretation.

```python
subprocess.run(
    ["ping", "-c", "1", host],
    capture_output=True,
    text=True,
    timeout=5,
)
```

Input is additionally validated as an IP address before execution.

Report:

[`reports/VULN-003-command-injection.md`](reports/VULN-003-command-injection.md)

---

# 🤖 Security Automation

The project includes lightweight Python security automation.

## Reconnaissance Scanner

```text
automation/recon.py
```

Capabilities:

* TCP connectivity checks
* Selected port reconnaissance
* Local service discovery
* Automated reconnaissance report generation

This is intentionally a lightweight learning tool and is **not intended to replace Nmap or enterprise security scanners**.

---

## Basic Web Security Scanner

```text
automation/vuln_scanner.py
```

The scanner performs basic checks against the local API, including:

* Content Security Policy
* X-Content-Type-Options
* X-Frame-Options
* HTTP Strict Transport Security
* Known lab endpoints

The purpose is to demonstrate how security checks can be automated using Python.

---

# 🛡️ Detection Engineering

The project also demonstrates a basic defensive security workflow.

```text
Access Log
    │
    ▼
Log Analyzer
    │
    ▼
Detection Rules
    │
    ▼
Security Alert
    │
    ▼
Incident Investigation
    │
    ▼
Incident Report
```

Current detection rules identify patterns associated with:

* SQL injection
* Command injection
* Forbidden access
* Repeated HTTP 403 responses

Components:

```text
detection/
├── logs/
├── rules/
└── log_analyzer.py
```

Incident report:

[`reports/INCIDENT-001-suspicious-web-activity.md`](reports/INCIDENT-001-suspicious-web-activity.md)

---

# 🧪 Security Regression Testing

The project uses **Pytest** to verify that previously remediated vulnerabilities remain fixed.

Current tests cover:

* Application health
* User authorization
* Administrative authorization
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

Current local test result:

```text
6 passed
```

Security regression testing helps prevent previously fixed vulnerabilities from being accidentally reintroduced during future development.

---

# ⚙️ CI/CD

GitHub Actions is used to automatically execute the security regression suite.

```text
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
    ├──────────────┐
    ▼              ▼
  PASS            FAIL
    │              │
    ▼              ▼
 Continue      Investigate
```

This introduces a basic **DevSecOps workflow** by integrating security testing into the development lifecycle.

---

# 📂 Repository Structure

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

# 🛠️ Technologies

### Programming

* Python

### Web Security

* FastAPI
* HTTP
* REST APIs
* Access Control
* SQL Injection
* Command Injection

### Security Automation

* Python `socket`
* HTTP security checks
* Automated reconnaissance

### Defensive Security

* Log analysis
* Detection rules
* Alert generation
* Incident documentation

### Secure Development

* Secure coding
* Security regression testing
* Pytest
* GitHub Actions

### Environment

* Linux
* Git
* GitHub

---

# 🚀 Running the Lab

## 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd cybersecurity-lab
```

## 2. Create the virtual environment

```bash
cd web-security/lab-target

python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the API

```bash
uvicorn app.main:app --reload
```

The application should be available locally at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Run Security Tests

From:

```text
web-security/lab-target
```

run:

```bash
pytest -v
```

The tests verify the security controls implemented in the application.

---

# 📊 Reports

Security research findings are documented in the `reports/` directory.

Each vulnerability report follows a structured process:

```text
Description
     ↓
Impact
     ↓
Affected Component
     ↓
Proof of Concept
     ↓
Root Cause
     ↓
Remediation
     ↓
Retest
```

This documentation approach is intended to demonstrate the ability to communicate technical security findings clearly.

---

# 🎓 Skills Demonstrated

This project demonstrates practical exposure to:

* Web Application Security
* Vulnerability Assessment
* Broken Access Control
* SQL Injection
* Command Injection
* Secure Coding
* Python Security Automation
* TCP Reconnaissance
* HTTP Security Analysis
* Detection Engineering
* Log Analysis
* Incident Response Documentation
* Security Regression Testing
* Pytest
* CI/CD
* DevSecOps
* Linux
* Git/GitHub

---

# ⚠️ Security Disclaimer

This project intentionally contains vulnerable application components for educational security research.

All testing is designed to be performed against the local laboratory environment.

Do **not** expose the intentionally vulnerable application to the public internet or test systems without explicit authorization.

The authentication mechanism and vulnerable components are simplified for educational purposes and should not be considered production-ready security implementations.

---

# 👨‍💻 About

Built as a cybersecurity learning and portfolio project to demonstrate practical understanding of:

> **Offensive Security → Secure Development → Automation → Detection → DevSecOps**

The project emphasizes understanding the complete security lifecycle rather than relying solely on individual security tools.

---

## Project Status

**Status: Completed**

```text
[✓] Web Security Lab
[✓] Vulnerability Research
[✓] Vulnerability Remediation
[✓] Security Automation
[✓] Detection Engineering
[✓] Incident Documentation
[✓] Security Regression Testing
[✓] Architecture Documentation
[✓] Professional README
[ ] GitHub Actions CI
```

GitHub Actions is the final CI component planned for the project.
