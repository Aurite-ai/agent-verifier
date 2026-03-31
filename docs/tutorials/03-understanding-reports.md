# Tutorial 3: Understanding Reports

This tutorial teaches you how to read verification reports, understand severity levels, and prioritize what to fix first.

**Time:** ~10 minutes  
**Prerequisites:** Completed [Tutorial 2](02-first-verification.md)

---

## What You'll Learn

1. Report structure and sections
2. Severity levels and what they mean
3. Check reliability indicators
4. How to prioritize findings
5. Walking through a real report

---

## Part 1: Report Anatomy

Every verification report follows this structure:

```markdown
# Agent Verification Report

**Project:** [name]
**Date:** [date]
**Mode:** [Standalone | Kahuna-enhanced]
**Language:** [Python | TypeScript | Go]
**Agent framework:** [detected framework]
**Files analyzed:** [count]

## Summary
## Security
## Agent Patterns (if agent detected)
## Quality
## Language ([detected language])
## Detailed Findings
## Recommendations
```

### Header Section

| Field | What it tells you |
|-------|-------------------|
| **Project** | Directory name or path analyzed |
| **Date** | When verification ran |
| **Mode** | Standalone (built-in rules) or Kahuna-enhanced (org rules) |
| **Language** | Primary language detected |
| **Agent framework** | LangGraph, CrewAI, AutoGen, LangChain, Custom, or None |
| **Files analyzed** | Total files checked |

### Summary Section

```markdown
## Summary

✅ 12 checks passed | ⚠️ 3 warnings | ❌ 1 issue

### By Category
| Category | Pass | Warn | Issue |
|----------|------|------|-------|
| Security | 5 | 0 | 1 |
| Patterns | 3 | 2 | 0 |
| Quality | 3 | 1 | 0 |
| Language | 1 | 0 | 0 |
```

This gives you a quick overview before diving into details.

---

## Part 2: Severity Levels

### ✅ Pass

The check found no problems. Your code follows best practices for that rule.

**Example:**
```markdown
- [x] No hardcoded secrets or API keys
- [x] All retry decorators have stop conditions
```

### ⚠️ Warning

A potential issue that deserves attention but isn't critical. Warnings often indicate code that *works* but could be improved.

**Common warnings:**
- Missing type hints on public functions
- System prompt approaching size limits
- Potential unbounded loop (but may have external termination)
- Naming inconsistencies

**Example:**
```markdown
- [ ] ⚠️ System prompt exceeds recommended size (6.2K tokens)
  - **Location:** prompts/system.md
  - **Suggestion:** Consider splitting into modular sections
```

### ❌ Issue

A definite problem that should be fixed. Issues represent security risks, missing safety checks, or violations of required patterns.

**Common issues:**
- Hardcoded API keys or secrets
- Retry decorators without limits
- Hallucinated tool references (tools in prompts that don't exist)
- LangGraph cycles with no path to END

**Example:**
```markdown
- [ ] ❌ Missing retry limit
  - **Location:** services/api.py:45
  - **Rule:** All retry mechanisms must have explicit bounds
  - **Fix:** Add `stop=stop_after_attempt(3)` to `@retry` decorator
```

---

## Part 3: Check Reliability Indicators

Not all checks are equally reliable. Agent Verifier tags each finding with a reliability indicator:

### `[P]` Pattern-Matched (High Reliability)

These checks use mechanical pattern matching—the rule is applied exactly as specified to code structure.

**Same answer every run.** If the pattern exists, it's flagged.

**Examples of pattern-matched checks:**
| Check | What it looks for |
|-------|------------------|
| Retry limits | `@retry` without `stop=` parameter |
| Loop safety | `while True` without `break` in scope |
| Tool registry | Tool names in prompts not in definitions |
| Context size | `len(prompt) / 4` vs token thresholds |
| Hardcoded secrets | Assignments to `API_KEY`, `SECRET`, etc. |
| LangGraph cycles | Graph cycles with no `END` reachable |

### `[H]` Heuristic (Best-Effort)

These checks require judgment about intent or quality. Results may vary between runs.

**Examples of heuristic checks:**
| Check | Why it needs judgment |
|-------|----------------------|
| Code organization | "Appropriate structure" depends on context |
| Naming conventions | Consistency requires understanding project conventions |
| Input validation | Sufficiency depends on threat model |
| Docstring quality | Presence is checkable; usefulness is not |

### Reading tagged findings

```markdown
## Detailed Findings

### ✅ Passing
- `[P]` No hardcoded secrets or API keys
- `[P]` All retry decorators have stop conditions
- `[H]` Code organization follows best practices

### ⚠️ Warnings
- `[H]` Code organization: Consider splitting large module
  - **Location:** services/agent.py
  - **Suggestion:** Extract LLM interactions to separate file

### ❌ Issues
- `[P]` Missing retry limit
  - **Location:** services/api.py:45
  - **Rule:** All retry mechanisms must have explicit bounds
  - **Fix:** Add `stop=stop_after_attempt(3)` to `@retry` decorator
```

**Prioritize `[P]` issues first**—they're definite problems with clear fixes.

---

## Part 4: Category Breakdown

### Security Section

```markdown
## Security

- [x] No hardcoded secrets
- [x] Dependencies pinned
- [ ] ⚠️ Input validation: User input at api/handlers.py:23 not validated
- [ ] ❌ Hardcoded API key at config.py:12
```

**What to look for:**
- Secret exposure (API keys, passwords, tokens)
- Dependency vulnerabilities
- Missing input validation
- Error messages exposing internals

### Agent Patterns Section

```markdown
## Agent Patterns

### Loop Safety
- [x] All loops have termination conditions
- [ ] ⚠️ Potential unbounded loop at agent/loop.py:45

### Retry Limits
- [x] Tenacity retries: 3 decorators, all have limits
- [ ] ❌ Backoff retry at services/llm.py:67 missing max_tries

### Tool Consistency
- [x] Tool registry: 5 tools defined
- [ ] ❌ Hallucinated tool: `execute_sql` in prompts/main.md

### Context Size
- [x] System prompt: 2.1K tokens (within limits)
- [ ] ⚠️ Tool descriptions: 3.8K tokens (approaching 4K limit)
```

**What to look for:**
- Infinite loop risks
- Unbounded retry attempts
- Tools referenced but not defined
- Prompts approaching token limits

### Quality Section

```markdown
## Quality

- [x] Naming conventions consistent
- [x] Code well-organized
- [ ] ⚠️ Magic number at utils.py:34: `if retries > 5`
- [ ] ⚠️ Missing docstring: process_response() in handlers.py
```

**What to look for:**
- Inconsistent naming
- Poor organization
- Unexplained constants
- Missing documentation

### Language Section

```markdown
## Language (Python)

- [x] Type hints on public functions
- [ ] ⚠️ Missing type hints: internal helper at utils.py:12
- [ ] ❌ Unpinned dependency: requests>=2.0 in requirements.txt
```

**What to look for:**
- Missing type annotations
- Language-specific anti-patterns
- Dependency management issues

---

## Part 5: How to Prioritize Findings

### Priority Matrix

| Severity | Reliability | Priority | Action |
|----------|-------------|----------|--------|
| ❌ Issue | `[P]` | **Highest** | Fix immediately |
| ❌ Issue | `[H]` | High | Review and likely fix |
| ⚠️ Warning | `[P]` | Medium | Fix when convenient |
| ⚠️ Warning | `[H]` | Lower | Consider for improvement |

### Recommended workflow

1. **Start with `❌ [P]` issues** — These are definite problems with clear fixes
2. **Review `❌ [H]` issues** — Use judgment, but these often need attention
3. **Address `⚠️ [P]` warnings** — Patterns that could become problems
4. **Consider `⚠️ [H]` warnings** — Opportunities for improvement

### Example prioritization

Given this report:
```
❌ [P] Hardcoded API key at config.py:12
❌ [P] Missing retry limit at services/api.py:45
❌ [H] Insufficient input validation at handlers.py:23
⚠️ [P] System prompt at 6.2K tokens (limit: 8K)
⚠️ [H] Consider splitting agent.py (450 lines)
```

**Fix order:**
1. `config.py:12` — Security risk, clear fix (use env var)
2. `services/api.py:45` — Safety issue, clear fix (add stop param)
3. `handlers.py:23` — Review validation requirements
4. System prompt — Not urgent but worth monitoring
5. `agent.py` split — Nice to have, schedule for refactor

---

## Part 6: Example Report Walkthrough

Here's a complete report with annotations:

```markdown
# Agent Verification Report

**Project:** my-langgraph-agent
**Date:** 2026-03-27
**Mode:** Standalone
**Language:** Python
**Agent framework:** LangGraph          # ← Framework detected from imports
**Files analyzed:** 15

## Summary

✅ 8 checks passed | ⚠️ 2 warnings | ❌ 2 issues

### By Category
| Category | Pass | Warn | Issue |
|----------|------|------|-------|
| Security | 4 | 0 | 1 |       # ← One security issue to fix
| Patterns | 2 | 1 | 1 |       # ← One pattern issue (likely retry)
| Quality | 2 | 1 | 0 |
| Language | 0 | 0 | 0 |

## Security

- [x] No hardcoded secrets
- [x] Dependencies pinned
- [x] Error messages don't expose internals
- [ ] ❌ `[P]` Hardcoded OpenAI key      # ← Pattern-matched, fix first
  - **Location:** agent/config.py:8
  - **Fix:** Move to OPENAI_API_KEY environment variable

## Agent Patterns

### Loop Safety
- [x] All graph nodes have termination paths

### Retry Limits
- [ ] ❌ `[P]` Missing retry limit        # ← Pattern-matched, fix second
  - **Location:** agent/llm.py:34
  - **Pattern:** `@retry` without stop parameter
  - **Fix:** Add `stop=stop_after_attempt(3)`

### Tool Consistency
- [x] Tool registry: 4 tools defined, all referenced

### Context Size
- [ ] ⚠️ `[P]` System prompt: 5.8K tokens  # ← Approaching limit, monitor
  - **Location:** prompts/system.md
  - **Threshold:** Warning at 4K, Issue at 8K

## Quality

- [x] Naming conventions consistent
- [ ] ⚠️ `[H]` Large module                # ← Heuristic, lower priority
  - **Location:** agent/graph.py (380 lines)
  - **Suggestion:** Consider extracting node definitions

## Recommendations

1. **Move API key to environment variable** — Security risk
2. **Add retry limit to LLM calls** — Prevents infinite retry loops
3. **Monitor system prompt size** — Currently at 73% of warning threshold
```

---

## Quick Reference

### Severity at a glance

| Icon | Meaning | Action |
|------|---------|--------|
| ✅ | Passing | No action needed |
| ⚠️ | Warning | Review, fix if appropriate |
| ❌ | Issue | Should be fixed |

### Reliability at a glance

| Tag | Meaning | Confidence |
|-----|---------|------------|
| `[P]` | Pattern-matched | High — deterministic |
| `[H]` | Heuristic | Best-effort — may vary |

---

## Next Steps

Now that you understand reports, learn to run targeted checks:

[Tutorial 4: Focused Checks →](04-focused-checks.md)
