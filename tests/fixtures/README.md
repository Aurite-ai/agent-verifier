# Test Fixtures for Agent Pattern Detection

These fixtures validate the agent observability pattern checks defined in Phase 1 of the implementation guide.

## Fixture Structure

```
tests/fixtures/
├── README.md                # This file
├── infinite_loop/           # Loop safety pattern detection
├── retry_limits/            # Retry limit validation
├── tool_registry/           # Tool registry consistency
└── prompt_size/             # Context size awareness
```

## How to Test

### Option 1: Test Individual Fixture Categories

Ask your coding agent to verify a specific fixture directory:

```
cd tests/fixtures/infinite_loop
```

Then say to the agent:
> "Verify this code for agent loop safety patterns"

### Option 2: Test All Fixtures

From the project root:
```
cd tests/fixtures
```

Then say to the agent:
> "Run verification on these test fixtures and generate a report"

### Option 3: Use the Skill Trigger Phrases

Any of these will work:
- "verify my code"
- "audit this agent code"
- "check compliance"
- "validate against best practices"

---

## Expected Results

### Infinite Loop Detection (`infinite_loop/`)

| File | Expected | Pattern Detected |
|------|----------|------------------|
| `while_true_no_break.py` | ⚠️ Warning | `while True:` at lines 16, 26 without visible break in scope |
| `while_true_with_break.py` | ✅ Pass | `while True:` has explicit break conditions |
| `recursive_no_base.py` | ⚠️ Warning | Recursive calls without depth limits at lines 28, 45, 62 |

### Retry Limit Validation (`retry_limits/`)

| File | Expected | Pattern Detected |
|------|----------|------------------|
| `retry_no_limit.py` | ❌ Issue | `@retry` at lines 16, 30, 45 without `stop` parameter |
| `retry_with_limit.py` | ✅ Pass | All `@retry` decorators have `stop_after_attempt` or `stop_after_delay` |
| `backoff_no_limit.py` | ❌ Issue | `@backoff.on_exception` at lines 13, 27, 45 without `max_tries` |

### Tool Registry Consistency (`tool_registry/`)

| File | Expected | Pattern Detected |
|------|----------|------------------|
| `tools.py` | ✅ Pass | Defines tools: `search_docs`, `write_file`, `run_tests` |
| `prompt.md` | ❌ Issue | References `execute_sql` (lines 19, 26, 33, 48) - not in registry |

**Cross-reference result:** 
- Registered tools: `search_docs`, `write_file`, `run_tests`
- Referenced tools: `search_docs`, `write_file`, `execute_sql`, `run_tests`
- Hallucinated: `execute_sql` (4 references)

### Prompt Size Warnings (`prompt_size/`)

| File | Size | Tokens (est.) | Expected |
|------|------|---------------|----------|
| `small_prompt.md` | 314 bytes | ~78 tokens | ✅ Pass |
| `large_prompt.md` | 12,847 bytes | ~3,212 tokens | ✅ Pass (under 4K threshold) |

**Note:** The large_prompt.md is actually ~3.2K tokens, below the 4K warning threshold. For a true warning test, a prompt would need to exceed ~16KB.

---

## Sample Verification Report

When running verification on all fixtures, expect a report like:

```markdown
# Verification Report

**Project:** tests/fixtures
**Date:** 2026-03-04
**Mode:** Standalone
**Files analyzed:** 10
**Agent type detected:** Custom

## Summary

✅ 4 checks passed | ⚠️ 3 warnings | ❌ 5 issues

### By Category
| Category | Pass | Warn | Issue |
|----------|------|------|-------|
| Code Quality | 2 | 0 | 0 |
| Security | 0 | 0 | 0 |
| Agent Patterns | 2 | 3 | 5 |

## Agent Pattern Analysis

### Loop Safety
- [ ] ⚠️ `while_true_no_break.py:16` - `while True:` without break in scope
- [ ] ⚠️ `while_true_no_break.py:26` - `while True:` without break in scope
- [x] `while_true_with_break.py` - All loops have explicit termination
- [ ] ⚠️ `recursive_no_base.py:28` - Recursive call without depth limit

### Retry Limits
- [ ] ❌ `retry_no_limit.py:16` - `@retry` without stop parameter
- [ ] ❌ `retry_no_limit.py:30` - `@retry` without stop parameter
- [ ] ❌ `retry_no_limit.py:45` - `@retry` without stop parameter
- [x] `retry_with_limit.py` - All retry decorators have explicit limits
- [ ] ❌ `backoff_no_limit.py:13` - `@backoff.on_exception` without max_tries

### Tool Consistency
- [x] Tool registry found: 3 tools defined
- [ ] ❌ Hallucinated tool: `execute_sql` referenced in prompt.md

### Context Management
- [x] `small_prompt.md` - 78 tokens (under threshold)
- [x] `large_prompt.md` - ~3,212 tokens (under 4K threshold)

## Findings

### ✅ Passing
- Loop termination: `while_true_with_break.py` has explicit break conditions
- Retry limits: `retry_with_limit.py` all decorators have stop parameters

### ⚠️ Warnings
- Potential infinite loop: `while_true_no_break.py:16, 26`
- Recursive without depth: `recursive_no_base.py:28, 45, 62`

### ❌ Issues
- Missing retry limit: `retry_no_limit.py:16, 30, 45`
- Missing max_tries: `backoff_no_limit.py:13, 27, 45`
- Hallucinated tool: `execute_sql` in `prompt.md`

## Recommendations

1. **Add break conditions** to while loops in `while_true_no_break.py`
2. **Add stop parameter** to retry decorators: `stop=stop_after_attempt(3)`
3. **Add depth limits** to recursive functions

## Agent-Specific Recommendations

1. **Loop Safety:** Add explicit `MAX_ITERATIONS` constants and break conditions
2. **Tool Registry:** Remove `execute_sql` reference or implement the tool
3. **Context Management:** All prompts within recommended limits ✓
```

---

## Token Estimation

The skill uses this heuristic: **~4 characters = 1 token**

| Threshold | Characters | Bytes (approx) |
|-----------|------------|----------------|
| 4,000 tokens (warning) | 16,000 | ~16KB |
| 8,000 tokens (issue) | 32,000 | ~32KB |

---

## Adding New Test Cases

To add a new fixture:

1. Create the test file in the appropriate directory
2. Add a docstring explaining:
   - What pattern it tests
   - Expected result (Pass/Warning/Issue)
   - Why it should pass or fail
3. Update the expected results table in this README

### Example Fixture Template

```python
"""
Test fixture: [Description of what this tests]
Expected: [✅ Pass | ⚠️ Warning | ❌ Issue] - [Reason]

This pattern is [acceptable/problematic] because [explanation].
"""

# Your test code here
```
