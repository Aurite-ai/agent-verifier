---
name: verify-quality
version: "1.0.0"
description: Verify code quality including naming conventions, organization, documentation, and general best practices. Use when asked to "verify quality", "check code quality", or "review code organization".
---

# Code Quality Verification

## Purpose

Verify code for quality anti-patterns including poor naming, missing documentation, magic values, and organizational issues. All analysis happens locally.

## When to Use

Trigger this skill when the user asks to:
- "verify agent quality"
- "verify quality"
- "check code quality"
- "review code organization"
- "check naming conventions"

> **Note:** For full verification including security, patterns, and language-specific checks, tell the user to say **"verify agent"**.

## Process

### Step 1: Discover Files

Locate files to analyze:

**Source files:**
- `*.py`, `*.ts`, `*.js`, `*.go`, `*.rs` - Source code
- Focus on main implementation files, not tests

**Directories to check:**
- `src/`, `lib/`, `app/`, project root
- `agent/`, `tools/`, `utils/`

**Exclude:**
- `node_modules/`, `.venv/`, `venv/`, `__pycache__/`
- Test files (`*.test.*`, `*.spec.*`, `*_test.go`)
- Generated files, migrations

### Step 2: Run Quality Checks

All checks in this skill are **`[HEURISTIC]`** — they require judgment. Tag findings with `[H]`.

---

#### 2.1 `[HEURISTIC]` Naming Conventions

**Check for:**

| Issue | Examples |
|-------|----------|
| Single-letter variables (except loops) | `x = get_data()`, `d = {}` |
| Unclear abbreviations | `proc_usr_req()`, `calc_val()` |
| Inconsistent casing | Mixing `camelCase` and `snake_case` in same file |
| Names that don't describe purpose | `data`, `temp`, `result`, `info` |
| Boolean names without is/has/can | `enabled = check()` vs `is_enabled = check()` |

**Good naming:**

```python
# ✅ Clear, descriptive
user_profile = get_user_profile(user_id)
is_authenticated = check_authentication(token)
max_retry_attempts = 3

# ⚠️ Unclear
x = get_up(uid)
auth = check(t)
n = 3
```

Severity: ⚠️ Warning

---

#### 2.2 `[HEURISTIC]` Code Organization

**Check for:**

| Issue | Description |
|-------|-------------|
| Large files | > 500 lines for a single module |
| Large functions | > 50 lines for a single function |
| Deep nesting | > 4 levels of indentation |
| Mixed concerns | Business logic mixed with I/O in same function |
| God objects | Classes with > 10 public methods or > 20 attributes |

**Example issues:**

```python
# ⚠️ Warning - Deep nesting
def process(data):
    if condition1:
        if condition2:
            for item in items:
                if condition3:
                    if condition4:  # Too deep
                        ...

# ⚠️ Warning - Mixed concerns
def save_user(user):
    # Validation
    if not user.email:
        raise ValueError("...")
    # Business logic
    user.created_at = datetime.now()
    # Database I/O
    db.session.add(user)
    db.session.commit()
    # Email sending
    send_welcome_email(user)  # Multiple concerns
```

Severity: ⚠️ Warning

---

#### 2.3 `[HEURISTIC]` Magic Numbers and Strings

**Check for:**
- Numeric literals in code without constants
- String literals repeated multiple times
- Configuration values hardcoded in logic

**Examples:**

```python
# ⚠️ Warning - Magic numbers
if retry_count > 3:  # What does 3 mean?
    ...
time.sleep(60)  # Why 60?

# ⚠️ Warning - Repeated strings
if status == "pending":
    ...
elif status == "pending":  # Typo risk
    ...

# ✅ Good - Named constants
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60
STATUS_PENDING = "pending"

if retry_count > MAX_RETRIES:
    ...
time.sleep(RETRY_DELAY_SECONDS)
```

Severity: ⚠️ Warning

---

#### 2.4 `[HEURISTIC]` Documentation

**Check for:**

| Missing | Where expected |
|---------|----------------|
| Module docstring | Top of `.py` files |
| Class docstring | After `class` definition |
| Function docstring | After `def` for public functions |
| README | Project root |
| Type hints | Public function parameters/returns |

**Examples:**

```python
# ⚠️ Warning - Missing docstrings
def calculate_score(user, items, weights):
    total = 0
    for item, weight in zip(items, weights):
        total += item.value * weight
    return total

# ✅ Good - Documented
def calculate_score(user: User, items: list[Item], weights: list[float]) -> float:
    """
    Calculate weighted score for a user's items.
    
    Args:
        user: The user to calculate score for
        items: List of items to score
        weights: Weight multipliers for each item
        
    Returns:
        Total weighted score
    """
    ...
```

Severity: ⚠️ Warning

---

#### 2.5 `[HEURISTIC]` Error Handling

**Check for:**

| Issue | Description |
|-------|-------------|
| Bare except | `except:` without specific exception |
| Silent failures | `except: pass` |
| Generic exceptions raised | `raise Exception("...")` |
| No error handling | Functions that can fail but don't handle errors |

**Examples:**

```python
# ⚠️ Warning - Bare except
try:
    process_data()
except:
    pass

# ⚠️ Warning - Generic exception
raise Exception("Something went wrong")

# ✅ Good - Specific handling
try:
    process_data()
except ValueError as e:
    logger.warning(f"Invalid data: {e}")
    return default_value
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise ServiceUnavailableError from e
```

Severity: ⚠️ Warning

---

#### 2.6 `[HEURISTIC]` Code Duplication

**Check for:**
- Identical or near-identical code blocks (> 5 lines)
- Copy-pasted functions with minor variations
- Repeated patterns that could be abstracted

**Example:**

```python
# ⚠️ Warning - Duplication
def get_user_by_id(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None

def get_order_by_id(order_id):
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    if response.status_code == 200:
        return response.json()
    return None

# ✅ Good - Abstracted
def get_resource(resource_type: str, resource_id: str):
    response = requests.get(f"{BASE_URL}/{resource_type}/{resource_id}")
    if response.status_code == 200:
        return response.json()
    return None
```

Severity: ⚠️ Warning

---

#### 2.7 `[HEURISTIC]` Commented-Out Code

**Check for:**
- Large blocks of commented-out code (> 5 lines)
- TODO comments that are stale (months old if dates present)
- FIXME comments indicating known issues

**Examples:**

```python
# ⚠️ Warning - Commented code should be removed
# def old_implementation():
#     for item in items:
#         process_item(item)
#     return results

# ⚠️ Warning - Stale TODO
# TODO: Fix this before launch (added 2024-01-15)

# ✅ Acceptable - Brief explanatory comment
# Note: Using legacy API format for backwards compatibility
```

Severity: ⚠️ Warning

---

### Step 3: Generate Report

```markdown
# Code Quality Verification Report

**Project:** [name or path]
**Date:** [current date]
**Files analyzed:** [count]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

## Naming

- [x] Naming conventions consistent
- [ ] ⚠️ Unclear names at `[file:line]`

## Organization

- [x] Code well-organized
- [ ] ⚠️ Large function at `[file:line]` ([X] lines)

## Documentation

- [x] Key functions documented
- [ ] ⚠️ Missing docstring at `[file:line]`

## Error Handling

- [x] Errors properly handled
- [ ] ⚠️ Bare except at `[file:line]`

## Findings

> `[H]` = heuristic (all quality checks require judgment)

### ✅ Passing
- `[H]` Consistent naming conventions throughout
- `[H]` Functions are well-scoped and focused

### ⚠️ Warnings
- `[H]` [Check]: [description]
  - **Location:** [file:line]
  - **Impact:** [why this matters]
  - **Suggestion:** [how to improve]

## Recommendations

1. [Priority recommendation]
2. [Additional improvements]
```

---

*For full verification including security, patterns, and language-specific checks, say "verify agent".*
