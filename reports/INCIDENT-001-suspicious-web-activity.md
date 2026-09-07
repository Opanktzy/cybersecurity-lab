# INCIDENT-001 — Suspicious Web Activity

## 1. Incident Summary

The CyberLab detection engine identified multiple suspicious HTTP requests against the intentionally vulnerable local API.

Detected activity included:

* SQL Injection pattern
* Command Injection pattern
* Repeated HTTP 403 responses

All events occurred within the local CyberLab environment.

---

## 2. Detection Source

Detection engine:

```text
detection/log_analyzer.py
```

Input:

```text
detection/logs/access.log
```

Detection rules:

```text
detection/rules/rules.txt
```

---

## 3. Detected Activity

### SQL Injection

Detected pattern:

```text
' OR 1=1
```

Associated endpoint:

```text
/products
```

Classification:

```text
Injection / SQL Injection
```

---

### Command Injection

Detected pattern:

```text
; id
```

Associated endpoint:

```text
/ping
```

Classification:

```text
OS Command Injection
```

---

### Repeated Authorization Failures

Multiple requests returned:

```text
HTTP 403
```

Affected endpoint:

```text
/users/{user_id}
```

The repeated authorization failures may indicate an attempt to access objects without sufficient authorization.

---

## 4. Timeline

```text
12:01:10  SQL Injection pattern detected
12:01:11  Command Injection pattern detected
12:01:12  Authorization failure
12:01:13  Authorization failure
```

---

## 5. Analysis

The events demonstrate how application security vulnerabilities can generate detectable signals in application logs.

The SQL Injection and Command Injection patterns were detected using known indicators.

The repeated HTTP 403 responses were detected as potentially suspicious authorization activity.

---

## 6. Severity

Laboratory severity:

```text
MEDIUM
```

The severity is intentionally limited because the activity occurred against a local training environment containing non-sensitive sample data.

In a production environment, severity would depend on:

* affected assets
* data sensitivity
* attacker privileges
* successful exploitation
* business impact

---

## 7. Response

Recommended defensive actions:

1. Investigate the originating IP address.
2. Review surrounding application logs.
3. Verify whether exploitation was successful.
4. Validate authorization controls.
5. Validate SQL query parameterization.
6. Validate command execution controls.
7. Preserve relevant evidence.

---

## 8. Lessons Learned

This exercise demonstrates a basic detection engineering workflow:

```text
Application Event
        ↓
Log Collection
        ↓
Rule Matching
        ↓
Alert
        ↓
Investigation
        ↓
Incident Report
```

---

## 9. Scope

All testing and simulated malicious activity were performed against the local CyberLab environment owned and controlled by the researcher.
