# Lab 5: Static Code Analysis — Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL Injection in Query Construction | Security / Vulnerability | 11 | `INSERT INTO towers` used `%s, %d, %d` string formatting, susceptible to SQL injection (Bandit B608). | Replace string formatting with parameterized query `(?, ?, ?)` in `conn.execute()`. |
| Insecure Deserialization via Pickle | Security / Vulnerability | 1, 43 | `pickle.loads(pickle.dumps(...))` used for snapshot copy, introducing unsafe deserialization (Bandit B403, B301). | Remove `pickle` import and replace call with direct list copy `list(conn.execute(...).fetchall())`. |
| Hardcoded Credentials | Security / Hardcoded Password | 6 | Plaintext password literal `NOC_PASSWORD = "tower-noc-77"` hardcoded in file (Bandit B105). | Use `os.getenv("NOC_PASSWORD", "")` to load credentials from the environment. |
| Overly Broad Exception Handling | Bug Risk / Quality | 20 | `except Exception:` catches all exceptions indiscriminately, hiding bugs (Pylint W0718). | Catch specific `sqlite3.Error` database exception instead. |
| Non-PEP 8 Function and Identifier Naming | Style / Code Quality | 7, 10, 15, 34 | CamelCase names `addTower`, `serviceTower`, `riskLevel` and global mutation of `service_count` (Pylint C0103, W0603). | Rename functions to snake_case (`add_tower`, `service_tower`, `risk_level`) and manage counter in state dictionary. |
| Redundant Else After Return | Code Quality / Complexity | 36-39 | `riskLevel` had an unnecessary `else:` after an explicit `return` (Pylint R1705). | Remove `else:` and un-indent default return, adding safety check for `None`. |
| Missing Module and Function Docstrings | Documentation | 1, 10, 15, 25, 34, 42, 46 | Module and all functions lacked docstrings (Pylint C0114, C0116). | Add descriptive PEP 257 docstrings for module and all functions. |
| PEP 8 Formatting & Line Length Violations | Formatting / Style | 5, 11, 18, 24, 35, 43, 50 | Lines exceeded 79 characters, excess blank lines, and missing operator whitespace (Flake8 E501, E303, E225). | Wrap long queries across lines, adjust blank lines to 2, format spacing around operators. |

*For full details, diagnostic codes, and before/after verification logs, see [docs/issue_log.md](docs/issue_log.md).*
