# Tutorial 4: Focused Checks

This tutorial teaches you how to use individual verification skills for faster, targeted feedback. You'll learn when to use each skill and how to combine them for custom workflows.

**Time:** ~10 minutes  
**Prerequisites:** Completed [Tutorial 3](03-understanding-reports.md)

---

## What You'll Learn

1. When to use focused vs full verification
2. Each verification skill and what it checks
3. How to combine skills for custom workflows
4. Tips for efficient verification

---

## Part 1: Full vs Focused Verification

### Full verification (`"verify agent"`)

Runs all four check categories:
- Security → Patterns → Quality → Language

**Use when:**
- Starting a new project audit
- Before major releases
- Comprehensive code reviews
- First-time verification of a codebase

**Trade-off:** More complete, but slower

### Focused verification (`"verify agent [category]"`)

Runs only one check category.

**Use when:**
- You know what you're looking for
- Quick feedback during development
- Following up on specific findings
- CI/CD pipelines with time constraints

**Trade-off:** Faster, but may miss issues in other categories

---

## Part 2: The Four Verification Skills

### Security: `"verify agent security"`

**What it checks:**

| Check | Severity | Example |
|-------|----------|---------|
| Hardcoded secrets | ❌ Issue | `API_KEY = "sk-abc123..."` |
| Unpinned dependencies | ❌ Issue | `requests>=2.0` without upper bound |
| Missing input validation | ⚠️ Warning | User input passed directly to API |
| Error message exposure | ⚠️ Warning | Stack traces in production responses |
| Insecure defaults | ⚠️ Warning | `verify=False` in requests |

**When to use:**
- Before committing API integration code
- Reviewing authentication flows
- Checking dependency updates
- Security-focused code reviews

**Example output:**
```markdown
## Security

- [x] No hardcoded secrets
- [ ] ❌ `[P]` Unpinned dependency: anthropic>=0.18 in requirements.txt
  - **Fix:** Pin to specific version: anthropic==0.18.1
- [ ] ⚠️ `[H]` Input validation: Consider validating user_query at handlers.py:45
```

---

### Patterns: `"verify agent patterns"`

**What it checks:**

| Check | Severity | Example |
|-------|----------|---------|
| Unbounded loops | ⚠️ Warning | `while True:` without `break` |
| Missing retry limits | ❌ Issue | `@retry` without `stop=` |
| Hallucinated tools | ❌ Issue | Prompt references `execute_sql` but no tool exists |
| Large system prompts | ⚠️/❌ | > 4K tokens (warn), > 8K tokens (issue) |
| LangGraph infinite cycles | ❌ Issue | Cycle with no path to END |

**When to use:**
- Building new agent workflows
- Adding retry logic
- Modifying prompts or tools
- Debugging agent behavior issues

**Example output:**
```markdown
## Agent Patterns

### Loop Safety
- [x] All loops have termination conditions

### Retry Limits
- [ ] ❌ `[P]` Missing retry limit at services/llm.py:34
  - **Pattern:** `@retry` decorator without stop parameter
  - **Fix:** Add `stop=stop_after_attempt(3)`

### Tool Consistency
- [x] Tool registry: 5 tools defined
- [x] All prompt tool references found in registry

### Context Size
- [x] System prompt: 2.4K tokens (within limits)
- [ ] ⚠️ `[P]` Tool descriptions: 3.8K tokens (approaching 4K warning)
```

---

### Quality: `"verify agent quality"`

**What it checks:**

| Check | Severity | Example |
|-------|----------|---------|
| Naming inconsistencies | ⚠️ Warning | Mix of `camelCase` and `snake_case` |
| Poor organization | ⚠️ Warning | 500+ line files, mixed concerns |
| Magic numbers | ⚠️ Warning | `if retries > 5` without named constant |
| Missing documentation | ⚠️ Warning | Public functions without docstrings |
| Error handling | ❌ Issue | Bare `except:` clauses |

**When to use:**
- Code reviews
- Refactoring sprints
- Onboarding new team members
- Enforcing team standards

**Example output:**
```markdown
## Quality

### Naming
- [x] Consistent snake_case in Python files

### Organization
- [ ] ⚠️ `[H]` Large module: agent/graph.py (420 lines)
  - **Suggestion:** Consider extracting node definitions

### Documentation
- [x] All public functions have docstrings
- [ ] ⚠️ `[H]` Module docstring missing: utils/helpers.py

### Error Handling
- [x] No bare except clauses
```

---

### Language: `"verify agent language"`

Runs language-specific checks based on detected language.

#### Python checks

| Check | Severity | Example |
|-------|----------|---------|
| Missing type hints | ⚠️ Warning | `def process(data):` without annotations |
| Missing docstrings | ⚠️ Warning | Functions without `"""docstring"""` |
| Unpinned requirements | ❌ Issue | `langchain>=0.1` in requirements.txt |

#### TypeScript/JavaScript checks

| Check | Severity | Example |
|-------|----------|---------|
| Using `any` type | ⚠️ Warning | `function process(data: any)` |
| Strict mode disabled | ⚠️ Warning | `strict: false` in tsconfig.json |
| Unhandled promises | ⚠️ Warning | `fetchData()` without await or .catch() |

#### Go checks

| Check | Severity | Example |
|-------|----------|---------|
| Ignored errors | ❌ Issue | `_ = someFunc()` where func returns error |
| Missing context | ⚠️ Warning | Functions not propagating context.Context |

**When to use:**
- Language-specific code reviews
- Enforcing typing standards
- Preparing for type checker integration
- Learning language best practices

**Example output (Python):**
```markdown
## Language (Python)

### Type Safety
- [x] Public functions have type hints
- [ ] ⚠️ `[P]` Missing return type: `process_message` at handlers.py:34

### Documentation
- [x] All modules have docstrings

### Dependencies
- [ ] ❌ `[P]` Unpinned: openai>=1.0 in pyproject.toml
  - **Fix:** Pin to openai==1.12.0
```

---

## Part 3: Combining Skills

### Sequential checks

Run multiple focused checks in order:

```
"verify agent security"
```
*(review results)*

```
"verify agent patterns"
```
*(review results)*

This is useful when you want to address one category at a time.

### Comparison: Full vs Sequential

| Approach | Command | Use case |
|----------|---------|----------|
| Full | `"verify agent"` | Complete audit, consolidated report |
| Sequential | Run each skill separately | Address categories one at a time |
| Single | `"verify agent [category]"` | Quick check of specific concern |

### Common workflows

#### Pre-commit check (fast)
```
"verify agent security"
```
Catches secrets and obvious security issues quickly.

#### Feature branch review
```
"verify agent patterns"
```
Then:
```
"verify agent quality"
```
Ensures new agent code follows patterns and quality standards.

#### Release readiness
```
"verify agent"
```
Full verification before shipping.

#### After adding retry logic
```
"verify agent patterns"
```
Confirms retry limits are properly configured.

#### After updating dependencies
```
"verify agent security"
```
Then:
```
"verify agent language"
```
Checks for vulnerabilities and pinning issues.

---

## Part 4: Tips for Efficient Verification

### 1. Start narrow, expand if needed

```
"verify agent security"
```

If issues found, fix them. If clean, run the next category.

### 2. Use test fixtures for learning

```bash
cd tests/fixtures/retry_limits
```

```
"verify agent patterns"
```

See exactly what patterns are detected.

### 3. Save reports for comparison

After each verification:
> "Save the report"

Compare reports over time to track improvement.

### 4. Know your priorities

| Situation | Start with |
|-----------|------------|
| Security audit | `verify agent security` |
| Debugging agent loops | `verify agent patterns` |
| Code review | `verify agent quality` |
| Type safety push | `verify agent language` |

### 5. Understand check limitations

**Pattern-matched `[P]` checks** are reliable but may have edge cases:
- `while True` flagged even if termination is in called function
- Retry limits must be in the decorator, not runtime config

**Heuristic `[H]` checks** require judgment:
- "Large module" depends on context
- "Poor organization" is subjective

---

## Part 5: Quick Reference

### All verification commands

| Command | Category | Speed |
|---------|----------|-------|
| `"verify agent"` | All | Slowest |
| `"verify agent security"` | Security | Fast |
| `"verify agent patterns"` | Agent patterns | Fast |
| `"verify agent quality"` | Code quality | Fast |
| `"verify agent language"` | Language-specific | Fast |

### What each skill catches (summary)

| Skill | Key checks |
|-------|-----------|
| **security** | Secrets, dependencies, input validation |
| **patterns** | Loops, retries, tools, context size, LangGraph |
| **quality** | Naming, organization, docs, magic values |
| **language** | Types, idioms, language-specific rules |

### Legacy trigger phrases

These run the **full** verification suite:
- `"audit this agent code"`
- `"check compliance"`
- `"validate against best practices"`
- `"review this implementation"`

---

## Summary

You've learned how to:
- ✅ Choose between full and focused verification
- ✅ Use each of the four verification skills
- ✅ Combine skills for custom workflows
- ✅ Work efficiently with targeted checks

---

## What's Next?

You've completed the core tutorials! Here are ways to continue:

- **[Main README](../../README.md)** — Full technical reference
- **[Test Fixtures](../../tests/fixtures/README.md)** — Practice with example code
- **[Contribute](https://github.com/aurite-ai/agent-verifier/pulls)** — Found a bug or want to add a check? Open a PR!

---

## Need Help?

- **Questions?** [Open an issue](https://github.com/aurite-ai/agent-verifier/issues)
- **Enterprise support?** Contact [info@aurite.ai](mailto:info@aurite.ai)
