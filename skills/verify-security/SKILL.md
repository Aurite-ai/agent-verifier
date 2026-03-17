---
name: verify-security
version: "1.0.0"
description: Verify code for security issues including hardcoded secrets, input validation, error exposure, and dependency vulnerabilities. Use when asked to "verify security", "check for secrets", or "scan for vulnerabilities".
---

# Security Verification

## Purpose

Verify code for security anti-patterns and vulnerabilities. All analysis happens locally—code never leaves your machine.

## When to Use

Trigger this skill when the user asks to:
- "verify agent security"
- "verify security"
- "check for secrets"
- "scan for vulnerabilities"
- "security audit"

> **Note:** For full verification including patterns, quality, and language-specific checks, tell the user to say **"verify agent"**.

## Process

### Step 1: Discover Files

Locate files to analyze:

**Configuration files:**
- `package.json`, `pyproject.toml`, `Cargo.toml` - Dependencies
- `.env`, `.env.example`, `.env.local` - Environment files
- `config.py`, `settings.py`, `config.ts` - Configuration

**Source files:**
- `*.py`, `*.ts`, `*.js`, `*.go`, `*.rs` - Source code
- Prioritize files with: `auth`, `api`, `client`, `secret`, `config` in name

**Exclude:**
- `node_modules/`, `.venv/`, `venv/`, `__pycache__/`
- `*.test.*`, `*.spec.*`, `*_test.go`

### Step 2: Run Security Checks

#### Check Tiers

- **`[PATTERN]`** — Mechanical check. Apply exactly as written.
- **`[HEURISTIC]`** — Judgment required. Mark findings clearly.

Tag every finding with `[P]` for pattern or `[H]` for heuristic.

---

#### 2.1 `[PATTERN]` Hardcoded Secrets

Scan for assignments matching these patterns (case-insensitive):

| Variable pattern | Fail condition |
|------------------|----------------|
| `API_KEY` | Assigned to string literal |
| `SECRET` | Assigned to string literal |
| `PASSWORD` | Assigned to string literal |
| `TOKEN` | Assigned to string literal |
| `PRIVATE_KEY` | Assigned to string literal |
| `AWS_ACCESS_KEY_ID` | Assigned to string literal |
| `AWS_SECRET_ACCESS_KEY` | Assigned to string literal |

**Examples of failures:**

```python
# ❌ Issue
API_KEY = "sk-abc123..."
password = "hunter2"
OPENAI_API_KEY = "sk-proj-..."

# ✅ Pass
API_KEY = os.environ["API_KEY"]
password = os.getenv("PASSWORD")
api_key = settings.API_KEY
```

**Also flag:**
- String literals matching known API key patterns:
  - `sk-...` (OpenAI)
  - `sk-ant-...` (Anthropic)
  - `AKIA...` (AWS)
  - `ghp_...` (GitHub)
  - `xoxb-...` (Slack)

Severity: ❌ Issue

---

#### 2.2 `[PATTERN]` Dependency Version Pinning

**Python (`requirements.txt`):**

| Pattern | Severity |
|---------|----------|
| `package>=1.0` | ❌ Issue |
| `package>1.0` | ❌ Issue |
| `package` (no version) | ❌ Issue |
| `package==1.0.0` | ✅ Pass |
| `package~=1.0` | ✅ Pass |

**Python (`pyproject.toml`):**

Check `[project.dependencies]` and `[tool.poetry.dependencies]`:
- Unpinned or `>=` versions → ❌ Issue
- Pinned with `==` or `^` or `~` → ✅ Pass

**JavaScript/TypeScript (`package.json`):**

| Pattern | Severity |
|---------|----------|
| `"package": "*"` | ❌ Issue |
| `"package": "latest"` | ❌ Issue |
| `"package": ">=1.0.0"` | ⚠️ Warning |
| `"package": "^1.0.0"` | ✅ Pass |
| `"package": "~1.0.0"` | ✅ Pass |
| `"package": "1.0.0"` | ✅ Pass |

---

#### 2.3 `[HEURISTIC]` Input Validation

Check for external data handling:

**Look for:**
- HTTP request handlers (`@app.route`, `router.get`, etc.)
- User input processing (`request.body`, `req.params`, `input()`)
- File uploads
- Database queries with user input

**Flag if:**
- User input is passed directly to database queries without sanitization
- File paths are constructed from user input without validation
- JSON parsing without schema validation on external data

Severity: ⚠️ Warning

**Example patterns to flag:**

```python
# ⚠️ Warning - SQL without parameterization
query = f"SELECT * FROM users WHERE id = {user_id}"

# ⚠️ Warning - Path traversal risk
file_path = os.path.join(base_dir, user_filename)

# ✅ Pass - Parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

---

#### 2.4 `[HEURISTIC]` Error Message Exposure

Check error handling for information leakage:

**Flag if:**
- Stack traces returned in HTTP responses
- Database error messages exposed to users
- Internal paths or system info in error messages
- Debug mode enabled in production code

**Look for:**

```python
# ⚠️ Warning
except Exception as e:
    return {"error": str(e)}  # Exposes internal details

# ⚠️ Warning
app = Flask(__name__)
app.debug = True  # Debug in production

# ✅ Pass
except Exception as e:
    logger.error(f"Error: {e}")
    return {"error": "An error occurred"}
```

Severity: ⚠️ Warning

---

#### 2.5 `[HEURISTIC]` Secure Defaults

Check configuration for insecure defaults:

| Setting | Insecure | Secure |
|---------|----------|--------|
| CORS | `*` (allow all) | Specific origins |
| SSL verification | `verify=False` | `verify=True` or omitted |
| Debug mode | `debug=True` | `debug=False` |
| Cookie security | `secure=False` | `secure=True` |
| CSRF | Disabled | Enabled |

**Examples:**

```python
# ⚠️ Warning
requests.get(url, verify=False)
app.config["SESSION_COOKIE_SECURE"] = False
CORS(app, origins="*")

# ✅ Pass
requests.get(url)  # verify=True is default
app.config["SESSION_COOKIE_SECURE"] = True
CORS(app, origins=["https://example.com"])
```

Severity: ⚠️ Warning

---

#### 2.6 `[HEURISTIC]` Sensitive Data Logging

Check logging statements for sensitive data:

**Flag if logging includes:**
- Passwords or tokens
- API keys
- Personal identifiable information (PII)
- Credit card numbers
- Session tokens

**Look for:**

```python
# ⚠️ Warning
logger.info(f"User login: {username} with password {password}")
print(f"API response: {response.json()}")  # May contain tokens

# ✅ Pass
logger.info(f"User login: {username}")
logger.debug(f"Request to {url}")  # No sensitive data
```

Severity: ⚠️ Warning

---

### Step 3: Generate Report

```markdown
# Security Verification Report

**Project:** [name or path]
**Date:** [current date]
**Files analyzed:** [count]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

## Secrets

- [x] No hardcoded secrets found
- [ ] ❌ Hardcoded secret at `[file:line]`

## Dependencies

- [x] All dependencies pinned
- [ ] ❌ Unpinned dependencies in `[file]`

## Input Validation

- [x] External input properly validated
- [ ] ⚠️ Potential injection at `[file:line]`

## Error Handling

- [x] Errors properly sanitized
- [ ] ⚠️ Information leakage at `[file:line]`

## Findings

> `[P]` = pattern-matched · `[H]` = heuristic

### ✅ Passing
- `[P]` No hardcoded API keys or secrets
- `[P]` Dependencies properly pinned

### ⚠️ Warnings
- `[H]` [Check]: [description]
  - **Location:** [file:line]
  - **Risk:** [what could go wrong]
  - **Suggestion:** [how to fix]

### ❌ Issues
- `[P]` [Check]: [description]
  - **Location:** [file:line]
  - **Rule:** [which rule violated]
  - **Fix:** [specific remediation]

## Recommendations

1. [Priority recommendation]
2. [Additional improvements]
```

---

*For full verification including patterns, quality, and language-specific checks, say "verify agent".*
