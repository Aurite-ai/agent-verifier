---
name: verify-language
version: "1.0.0"
description: Language-specific verification for Python, TypeScript/JavaScript, and Go. Checks type safety, language idioms, and best practices. Use when asked to "verify language", "check types", or for language-specific checks.
---

# Language-Specific Verification

## Purpose

Verify code against language-specific best practices and idioms for Python, TypeScript/JavaScript, and Go. All analysis happens locally.

## When to Use

Trigger this skill when the user asks to:
- "verify agent language"
- "verify language"
- "check types"
- "check Python/TypeScript/Go code"

This skill is also auto-invoked by the main verification orchestrator based on detected language.

> **Note:** For full verification including security, patterns, and quality checks, tell the user to say **"verify agent"**.

## Process

### Step 1: Detect Language

Identify the primary language by checking:

| Indicator | Language |
|-----------|----------|
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python |
| `package.json`, `tsconfig.json` | TypeScript/JavaScript |
| `go.mod`, `go.sum` | Go |
| `Cargo.toml` | Rust |

Also check file extensions in `src/` or project root:
- `.py` → Python
- `.ts`, `.tsx`, `.js`, `.jsx` → TypeScript/JavaScript  
- `.go` → Go
- `.rs` → Rust

### Step 2: Run Language-Specific Checks

Apply checks based on detected language. Each section below is only applicable for its language.

---

## Python Checks

### `[PATTERN]` Type Hints on Public Functions

Flag any `def` function in public scope (no leading `_`) that has parameters without type annotations.

**Examples:**

```python
# ⚠️ Warning - Missing type hints
def get_user(user_id):
    return db.find_user(user_id)

def process_items(items, filter_fn):
    return [filter_fn(item) for item in items]

# ✅ Pass - Has type hints
def get_user(user_id: int) -> User:
    return db.find_user(user_id)

def process_items(items: list[Item], filter_fn: Callable[[Item], bool]) -> list[Item]:
    return [filter_fn(item) for item in items]
```

**Scope:**
- Public functions (no leading `_`)
- Class methods (except `__init__` can skip return type)
- Module-level functions

Severity: ⚠️ Warning

---

### `[HEURISTIC]` Docstrings

Check for missing docstrings:

| Location | Requirement |
|----------|-------------|
| Module | Top-level docstring explaining purpose |
| Class | Docstring explaining class responsibility |
| Public function | Docstring explaining args, returns, raises |

**Examples:**

```python
# ⚠️ Warning - Missing docstrings
class UserService:
    def get_user(self, user_id: int) -> User:
        return self.db.find(user_id)

# ✅ Pass - Documented
class UserService:
    """Service for user-related operations."""
    
    def get_user(self, user_id: int) -> User:
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            User object if found
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        return self.db.find(user_id)
```

Severity: ⚠️ Warning

---

### `[PATTERN]` Requirements Pinning

Check `requirements.txt` and `pyproject.toml` dependencies:

| Pattern | Severity |
|---------|----------|
| `package>=1.0` | ❌ Issue |
| `package>1.0` | ❌ Issue |
| `package` (no version) | ❌ Issue |
| `package==1.0.0` | ✅ Pass |
| `package~=1.0` | ✅ Pass |

**In `pyproject.toml`:**

```toml
# ❌ Issue
[project]
dependencies = [
    "langchain>=0.1.0",
    "openai",
]

# ✅ Pass
[project]
dependencies = [
    "langchain==0.1.0",
    "openai==1.12.0",
]
```

Severity: ❌ Issue

---

### `[HEURISTIC]` Python Idioms

Check for non-idiomatic patterns:

| Anti-pattern | Idiomatic |
|--------------|-----------|
| `if len(list) > 0:` | `if list:` |
| `if x == True:` | `if x:` |
| `list = list + [item]` | `list.append(item)` |
| `for i in range(len(list)):` | `for item in list:` or `enumerate()` |
| `dict.keys()` iteration | Direct dict iteration |

Severity: ⚠️ Warning

---

## TypeScript/JavaScript Checks

### `[PATTERN]` Strict Mode

Check `tsconfig.json` for strict type checking:

```json
// ❌ Issue - Not strict
{
  "compilerOptions": {
    "strict": false
  }
}

// ❌ Issue - Strict not set
{
  "compilerOptions": {
    "target": "ES2020"
  }
}

// ✅ Pass
{
  "compilerOptions": {
    "strict": true
  }
}
```

Severity: ❌ Issue (if `strict` is `false` or absent)

---

### `[PATTERN]` No `any` Types

Flag unqualified `: any` type annotations:

```typescript
// ⚠️ Warning
function process(data: any): any {
    return data.value;
}

const items: any[] = [];

// ✅ Pass - Specific types
function process(data: UserData): ProcessedData {
    return { value: data.value };
}

// ✅ Pass - Explicit unknown with narrowing
function process(data: unknown): ProcessedData {
    if (isUserData(data)) {
        return { value: data.value };
    }
    throw new Error("Invalid data");
}
```

Severity: ⚠️ Warning

---

### `[HEURISTIC]` Async/Await Error Handling

Check that async functions handle errors:

```typescript
// ⚠️ Warning - No error handling
async function fetchUser(id: string): Promise<User> {
    const response = await fetch(`/users/${id}`);
    return response.json();
}

// ✅ Pass - Has error handling
async function fetchUser(id: string): Promise<User> {
    try {
        const response = await fetch(`/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    } catch (error) {
        logger.error("Failed to fetch user", { id, error });
        throw new UserFetchError(id, error);
    }
}
```

Severity: ⚠️ Warning

---

### `[HEURISTIC]` Promise Handling

Check for common Promise anti-patterns:

| Anti-pattern | Issue |
|--------------|-------|
| Missing `.catch()` | Unhandled rejection |
| `new Promise()` with async executor | Anti-pattern |
| Fire-and-forget promises | No await, no handling |

```typescript
// ⚠️ Warning - No catch
fetchData().then(process);

// ⚠️ Warning - Async executor
new Promise(async (resolve) => {
    const data = await fetchData();
    resolve(data);
});

// ✅ Pass
fetchData().then(process).catch(handleError);

// ✅ Pass - Using async/await
const data = await fetchData();
process(data);
```

Severity: ⚠️ Warning

---

## Go Checks

### `[PATTERN]` No Ignored Errors

Flag any `_ = ` assignments where the right-hand side returns `error`:

```go
// ❌ Issue - Ignored error
_ = file.Close()
_ = json.Unmarshal(data, &result)
result, _ := db.Query(sql)

// ✅ Pass - Error handled
if err := file.Close(); err != nil {
    log.Printf("failed to close file: %v", err)
}

result, err := db.Query(sql)
if err != nil {
    return nil, fmt.Errorf("query failed: %w", err)
}
```

Severity: ❌ Issue

---

### `[HEURISTIC]` Context Propagation

Check that context.Context is passed through call chains:

```go
// ⚠️ Warning - Context not passed
func ProcessData(data []byte) error {
    result, err := externalAPI.Call(data)  // No context
    return err
}

// ✅ Pass - Context propagated
func ProcessData(ctx context.Context, data []byte) error {
    result, err := externalAPI.Call(ctx, data)
    return err
}
```

**Check for:**
- HTTP handlers that don't use `r.Context()`
- Functions that call external services without context
- Long-running operations without context cancellation support

Severity: ⚠️ Warning

---

### `[HEURISTIC]` Proper Package Structure

Check Go project structure:

| Issue | Description |
|-------|-------------|
| `package main` with many files | Should split into packages |
| Circular imports | Package A imports B, B imports A |
| Internal packages exposed | Internal code in public packages |
| Missing `internal/` | Shared code that shouldn't be public |

Severity: ⚠️ Warning

---

### `[HEURISTIC]` Go Idioms

Check for non-idiomatic patterns:

| Anti-pattern | Idiomatic |
|--------------|-----------|
| `if err != nil { return err }` repeatedly | Consider helper or wrap |
| Naked returns in long functions | Explicit returns |
| `interface{}` without type assertions | Use generics or specific types |
| Getters named `GetX()` | Just `X()` |

Severity: ⚠️ Warning

---

## Step 3: Generate Report

```markdown
# Language Verification Report

**Project:** [name or path]
**Date:** [current date]
**Language detected:** [Python | TypeScript | JavaScript | Go]
**Files analyzed:** [count]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

## Type Safety

- [x] Types properly defined
- [ ] ⚠️ Missing type hints at `[file:line]`
- [ ] ❌ Strict mode not enabled in `tsconfig.json`

## Language Idioms

- [x] Code follows language best practices
- [ ] ⚠️ Non-idiomatic pattern at `[file:line]`

## Error Handling

- [x] Errors properly handled
- [ ] ❌ Ignored error at `[file:line]`

## Findings

> `[P]` = pattern-matched · `[H]` = heuristic

### ✅ Passing
- `[P]` [Check]: [confirmation]

### ⚠️ Warnings
- `[P|H]` [Check]: [description]
  - **Location:** [file:line]
  - **Language rule:** [which idiom/pattern]
  - **Suggestion:** [how to fix]

### ❌ Issues
- `[P]` [Check]: [description]
  - **Location:** [file:line]
  - **Rule:** [which rule violated]
  - **Fix:** [specific remediation]

## Language-Specific Recommendations

### Python
1. Add type hints to public functions
2. Include docstrings for classes and functions

### TypeScript
1. Enable strict mode in tsconfig.json
2. Replace `any` with specific types

### Go
1. Handle all returned errors
2. Propagate context through call chains
```

---

*For full verification including security, patterns, and quality checks, say "verify agent".*
