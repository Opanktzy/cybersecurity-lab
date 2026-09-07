# VULN-003 — OS Command Injection

## 1. Summary

The `/ping` endpoint was intentionally implemented with unsafe operating system command construction.

User-controlled input was concatenated directly into a shell command and executed with `shell=True`.

This created an OS Command Injection vulnerability.

---

## 2. Scope

Target:

```text
http://127.0.0.1:8000
```

Endpoint:

```text
GET /ping?host=
```

Environment:

```text
Local CyberLab intentionally vulnerable application
```

---

## 3. Vulnerable Implementation

The original implementation constructed a command using user-controlled input:

```python
command = f"ping -c 1 {host}"

subprocess.run(
    command,
    shell=True,
)
```

The application therefore allowed the supplied value to become part of a shell command.

---

## 4. Proof of Concept

Normal input:

```text
127.0.0.1
```

The resulting command was:

```text
ping -c 1 127.0.0.1
```

A harmless command-injection test was then performed using:

```text
127.0.0.1; id
```

The resulting command became conceptually:

```text
ping -c 1 127.0.0.1; id
```

The additional `id` command was executed by the shell.

This confirmed that user-controlled input could influence shell command execution.

---

## 5. Impact

OS Command Injection can be a critical vulnerability because successful exploitation may allow arbitrary operating system commands to execute with the privileges of the vulnerable application.

Potential impact includes:

* Unauthorized system information access
* Access to application files
* Modification or deletion of files
* Execution of additional programs
* Potential system compromise

The actual impact depends on the privileges of the application process and the surrounding system.

---

## 6. Root Cause

The root cause was unsafe shell command construction.

The application combined trusted command syntax and untrusted user input into one shell string.

The use of:

```python
shell=True
```

increased the risk because shell metacharacters could be interpreted as commands.

---

## 7. Remediation

The implementation was changed to pass command arguments directly to `subprocess.run()`:

```python
subprocess.run(
    ["ping", "-c", "1", host],
    capture_output=True,
    text=True,
)
```

Shell execution was removed.

Input validation was also added using Python's `ipaddress` module.

Only valid IP addresses are accepted.

---

## 8. Retest

The original harmless injection payload was tested again:

```text
127.0.0.1; id
```

The application rejected the input as an invalid IP address.

Normal requests such as:

```text
127.0.0.1
```

continued to work.

---

## 9. Automated Verification

A Python PoC was created:

```text
tests/test_command_injection.py
```

The test covers:

1. Normal ping functionality
2. Command injection behavior

---

## 10. Security Classification

Category:

```text
Injection
```

Vulnerability:

```text
OS Command Injection
```

Primary cause:

```text
Unsafe shell command construction
```

Remediation:

```text
Avoid shell execution
+
Use argument arrays
+
Validate input
```

---

## 11. Evidence

Evidence collected:

```text
Normal request
Command Injection PoC
Automated Python test
Vulnerable implementation
Remediated implementation
Retest result
```

All testing was performed against the local CyberLab environment.
