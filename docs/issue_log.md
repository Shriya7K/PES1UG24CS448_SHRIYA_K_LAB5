# Static Code Analysis Issue Log

## Overview

This document records the static analysis findings identified in `tower_maintenance.py` during Lab 5, detailing the diagnostic codes, affected lines, severity levels, remediation steps, and verification evidence.

---

## Issue Tracking Table

| Issue | Tool | Type | Original file and line | Modified file and line | Description | Severity | Fix applied | Verification |
| ----- | ---- | ---- | ---------------------- | ---------------------- | ----------- | -------- | ----------- | ------------ |
| **SQL Injection via String Formatting** | Bandit / Pylint | Security / Defect | `tower_maintenance.py:11` | `tower_maintenance.py:21-24` | `B608` / `C0209`: SQL query constructed using `%` string formatting (`INSERT INTO towers ... VALUES ('%s', %d, %d)`), exposing the database to SQL injection attacks. | Medium | Replaced string formatting with parameterized query placeholders `(?, ?, ?)` and passed variables as a tuple parameter to `conn.execute()`. | Bandit report: `B608` eliminated (0 medium issues). Pylint: `C0209` eliminated. Verified by `test_tower_maintenance.TestTowerMaintenance.test_add_and_snapshot`. |
| **Insecure Deserialization via Pickle** | Bandit | Security / Insecure Function | `tower_maintenance.py:1`, `tower_maintenance.py:43` | `tower_maintenance.py:53-55` | `B403` / `B301`: `snapshot()` serialized and deserialized in-memory SQLite results with `pickle.loads(pickle.dumps(...))`. Pickle deserialization can lead to arbitrary code execution on untrusted data and was completely redundant. | Medium / Low | Removed `import pickle` entirely. Replaced `pickle.loads(pickle.dumps(...))` with `list(conn.execute("SELECT * FROM towers").fetchall())`. | Bandit report: `B403` and `B301` eliminated. Verified by `test_tower_maintenance.TestTowerMaintenance.test_add_and_snapshot`. |
| **Hardcoded Password Credential** | Bandit | Security / CWE-259 | `tower_maintenance.py:6` | `tower_maintenance.py:14` | `B105`: Hardcoded credential literal (`NOC_PASSWORD = "tower-noc-77"`), risking secret leakage into source control. | Low | Replaced plaintext secret literal with runtime environment retrieval using `os.getenv("NOC_PASSWORD", "")`. | Bandit report: `B105` eliminated. Verified in `reports/after/bandit_report.txt`. |
| **Overly Broad Exception Handling** | Pylint | Code Quality / Bug Risk | `tower_maintenance.py:20` | `tower_maintenance.py:37` | `W0718`: `except Exception:` caught all exceptions indiscriminately, which can conceal syntax bugs, system interrupts, or unanticipated faults. | Warning | Restricted exception catching specifically to `sqlite3.Error`, allowing non-database exceptions and system signals to bubble up appropriately. | Pylint report: `W0718` eliminated. Verified in `reports/after/pylint_report.txt` and `test_service_tower`. |
| **Unnecessary Else Clause After Return** | Pylint | Code Quality / Complexity | `tower_maintenance.py:36-39` | `tower_maintenance.py:47-51` | `R1705`: `riskLevel` contained an redundant `else:` block immediately after an explicit `return "high"`, adding unnecessary branching depth. | Refactor | Removed the `else` block and de-indented `return "normal"`. Also added a safety check for `row is not None`. | Pylint report: `R1705` eliminated. Verified by `test_tower_maintenance.TestTowerMaintenance.test_risk_level`. |
| **Invalid Function and Variable Naming** | Pylint | Code Quality / Style | `tower_maintenance.py:7, 10, 15, 34` | `tower_maintenance.py:15, 17, 28, 45` | `C0103`: Functions `addTower`, `serviceTower`, and `riskLevel` violated PEP 8 snake_case conventions. Variable `service_count` at module scope violated constant uppercase rules and prompted global mutation (`W0603`). | Convention | Renamed functions to snake_case (`add_tower`, `service_tower`, `risk_level`). Replaced mutable global integer with a structured state dictionary `SERVICE_TRACKER = {"count": 0}`, removing `global` keyword. | Pylint report: `C0103` and `W0603` eliminated. Verified by `test_tower_maintenance.py`. |
| **Missing Module and Function Documentation** | Pylint | Documentation | `tower_maintenance.py:1, 10, 15, 25, 34, 42, 46` | `tower_maintenance.py:1, 18, 29, 40, 46, 54, 58` | `C0114` & `C0116`: The module and its six functions lacked docstrings explaining their purpose, parameters, and behaviors. | Convention | Added PEP 257-compliant docstrings to the module header and every function (`add_tower`, `service_tower`, `overdue`, `risk_level`, `snapshot`, `main`). | Pylint report: all `C0114` and `C0116` warnings resolved. Score improved to 10.00/10. |
| **Line Length and PEP 8 Formatting Violations** | Flake8 / Pylint | Style / Formatting | `tower_maintenance.py:5, 11, 18, 24, 35, 43, 50` | `tower_maintenance.py:6-12, 21-25, 32-35, 47-50, 61` | `E501`, `E303`, `E225`: Multiple lines exceeded 79 characters (up to 120 characters), triple blank lines before `overdue()`, and missing whitespace around the assignment operator `total=len(...)`. | Style | Broken SQL schema string and query executions across multiple lines within 79 characters; normalized blank lines to standard 2 between top-level functions; formatted operator spacing to `total = len(...)`. | Flake8 report: 0 violations reported. Clean exit with status 0. |

---

## Summary of Major Improvements

1. **Elimination of Security Vulnerabilities**:
   - Resolved SQL injection risk by migrating from unsafe string interpolation to native SQLite parameterized binding (`?`).
   - Removed insecure `pickle` deserialization which posed an arbitrary code execution vector.
   - Replaced hardcoded credentials with safe runtime environment variable loading via `os.getenv`.
2. **Defensive Error Handling and Robustness**:
   - Replaced broad `Exception` trapping with granular `sqlite3.Error` catching, preventing silent failure of system interrupts.
   - Added `None` check on database `fetchone()` queries in `risk_level` to prevent `TypeError` when queried tower IDs do not exist.
3. **Architecture and State Management**:
   - Removed unsafe `global` state mutation (`service_count`), encapsulating counter state within `SERVICE_TRACKER`.
4. **Code Quality and PEP 8 Compliance**:
   - Replaced non-standard camelCase function names with PEP 8-compliant snake_case identifiers.
   - Added complete PEP 257 docstrings for the module and all functions.
   - Enforced 79-character line limits, proper operator spacing, and standard blank-line spacing.

---

## Unresolved Findings and Rationale

- **None**. All findings reported by Pylint, Bandit, and Flake8 were investigated and resolved with genuine code fixes.
- No findings were left unaddressed.

---

## Justified False Positives and Suppressions

- **None**. No suppression comments (`# nosec`, `# pylint: disable`, `# noqa`) or configuration file overrides were introduced. Every finding was resolved directly in application logic and formatting.

---

## Final Results Summary

| Analysis Tool | Baseline Metric | Final Metric | Delta / Status |
| ------------- | --------------- | ------------ | -------------- |
| **Pylint** | 5.14 / 10 (17 diagnostic warnings) | **10.00 / 10** (0 diagnostic warnings) | +4.86 rating improvement, strictly > 9.5 target met |
| **Bandit** | 4 issues (2 Medium, 2 Low) | **0 issues** | 100% security issues resolved |
| **Flake8** | 7 style violations | **0 violations** | Clean PEP 8 compliance |
| **Unit Tests** | Not present | **4 passed** in 0.000s | Verified behavior, zero regressions |
| **Program Output** | `['Ridge-A'] high 2 1` | `['Ridge-A'] high 2 1` | Identical functional output preserved |
