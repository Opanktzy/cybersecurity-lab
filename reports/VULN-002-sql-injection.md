# VULN-002 — SQL Injection

## 1. Summary

The `/products` search endpoint was found to be vulnerable to SQL Injection.

User-controlled input was directly concatenated into a SQL query, allowing SQL syntax to alter the intended database query.

---

## 2. Scope

Target:

```text
http://127.0.0.1:8000
```

Endpoint:

```text
GET /products?search=
```

Database:

```text
SQLite
```

Environment:

```text
Local CyberLab intentionally vulnerable application
```

---

## 3. Vulnerable Code

The original implementation constructed the SQL query using string interpolation:

```python
query = f"""
    SELECT id, name, category, price
    FROM products
    WHERE name LIKE '%{search}%'
"""
```

Because `search` is controlled by the client, SQL syntax can be injected into the query.

---

## 4. Proof of Concept

Normal request:

```text
GET /products?search=Laptop
```

Result:

```text
1 product
```

SQL Injection payload:

```text
' OR 1=1 --
```

The resulting SQL condition can become logically true for all rows.

The application subsequently returned all available products.

---

## 5. Impact

In this laboratory application, the database contains intentionally non-sensitive sample data.

In a real application, SQL Injection could potentially allow an attacker to:

* Read unauthorized database records
* Modify database information
* Delete records
* Bypass application logic
* Access sensitive application data

The actual impact depends on database permissions and the privileges available to the application.

---

## 6. Root Cause

The root cause was unsafe construction of SQL statements through direct string concatenation.

The application treated user-controlled input as part of the SQL statement instead of as a query parameter.

---

## 7. Remediation

The vulnerable query was replaced with a parameterized query:

```python
query = """
    SELECT id, name, category, price
    FROM products
    WHERE name LIKE ?
"""

parameter = f"%{search}%"

products = connection.execute(
    query,
    (parameter,),
).fetchall()
```

The database driver now handles the user input as a value rather than executable SQL syntax.

---

## 8. Retest

The original SQL Injection payload was executed again after remediation:

```text
' OR 1=1 --
```

The application no longer returned all database records.

Normal product searches continued to function correctly.

---

## 9. Automated Test

A Python security test was created:

```text
tests/test_sqli.py
```

The test verifies both:

1. Normal search functionality
2. SQL Injection behavior

---

## 10. Security Classification

Category:

```text
Injection
```

Vulnerability:

```text
SQL Injection
```

Primary cause:

```text
Unsafe SQL string construction
```

Remediation:

```text
Parameterized SQL queries
```

---

## 11. Evidence

Evidence collected:

```text
Normal HTTP request
SQL Injection PoC
Python automated security test
Vulnerable SQL implementation
Remediated SQL implementation
Retest result
```

All testing was performed against the local CyberLab environment.
