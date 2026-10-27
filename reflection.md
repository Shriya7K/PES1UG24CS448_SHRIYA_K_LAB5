# Lab 5: Static Code Analysis — Reflection Report

See the full reflection report in [docs/reflection.md](docs/reflection.md).

## Summary of Answers

### 1. What is static code analysis, and why is it useful?
Static code analysis analyzes source code without executing it, identifying bugs, security vulnerabilities, and style violations early in development to reduce technical debt and defect repair costs.

### 2. What is the difference between Pylint, Bandit, and Flake8?
- **Pylint**: Deep code quality analyzer and linter checking design patterns, logical errors, docstrings, and naming conventions with a 10.0-point scoring scale.
- **Bandit**: Dedicated AST-based security vulnerability scanner for Python checking against CWE security risks (SQL injection, unsafe pickle, hardcoded passwords).
- **Flake8**: Fast, lightweight style enforcer combining `pycodestyle` (PEP 8), `pyflakes` (syntax/import errors), and `mccabe` (complexity).

### 3. What issues were discovered in the assigned program?
- **Bandit**: SQL injection (`B608`), unsafe pickle deserialization (`B301`, `B403`), and hardcoded password (`B105`).
- **Pylint**: Overly broad `except Exception:` (`W0718`), mutable global state (`W0603`), camelCase naming (`C0103`), redundant else clause (`R1705`), missing docstrings (`C0114`, `C0116`).
- **Flake8**: Lines exceeding 79 characters (`E501`), excessive blank lines (`E303`), missing operator whitespace (`E225`).

### 4. How were the identified issues fixed?
- Parameterized SQL queries using `(?, ?, ?)`.
- Replaced `pickle` with direct list copies and removed `import pickle`.
- Retrieved passwords from the environment using `os.getenv()`.
- Caught specific `sqlite3.Error` instead of broad `Exception`.
- Renamed functions to snake_case and encapsulated counters in a state dictionary.
- Added comprehensive docstrings and formatted code to conform with PEP 8.

### 5. What did the before-and-after reports reveal?
- Pylint score jumped from **5.14/10** to **10.00/10**.
- Bandit issues dropped from **4** to **0**.
- Flake8 violations dropped from **7** to **0**.
- Program functionality and outputs remained 100% verified and identical (`['Ridge-A'] high 2 1`).

### 6. What challenges were encountered while fixing the findings?
Navigating tool interactions (such as Pylint's f-string recommendation vs Bandit's SQL injection warning), handling global state cleanly without `global`, and wrapping multi-line SQL queries under 79 characters without harming readability.

### 7. How does static analysis improve code quality, security, and maintainability?
It prevents defects prior to deployment, systematically audits for vulnerability patterns, and standardizes code style for team-wide readability and maintainability.

### 8. What are the limitations of static analysis?
It lacks runtime context, cannot verify semantic/business logic correctness, can yield false positives or false negatives, and must be accompanied by dynamic unit and integration testing.
