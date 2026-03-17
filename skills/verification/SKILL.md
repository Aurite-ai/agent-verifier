---
name: verification
version: "1.0.0"
description: Full agent verification suite. Runs security, patterns, quality, and language-specific checks. Use when asked to "verify agent", "verify my agent", "audit agent", or "full verification".
---

# Agent Verifier

## Purpose

Run comprehensive verification on AI agent code. This orchestrator invokes focused verification skills and consolidates results into a unified report. All analysis happens locally—code never leaves your machine.

## When to Use

Trigger this skill when the user asks to:
- **"verify agent"** (primary invocation)
- "verify my agent"
- "audit agent"
- "full verification"
- "verify my code" (when agent patterns are detected)
- "check compliance"

## Available Verification Modes

| Command | Skill | What it checks |
|---------|-------|----------------|
| **"verify agent"** | This skill | Full suite (all below) |
| "verify agent security" | verify-security | Secrets, dependencies, input validation |
| "verify agent patterns" | verify-patterns | Loops, retries, tools, context size |
| "verify agent quality" | verify-quality | Naming, organization, documentation |
| "verify agent language" | verify-language | Type hints, idioms, language best practices |

## Process

### Step 1: Context Discovery

Scan the project to identify:

1. **Primary language:**
   - Check for `pyproject.toml`, `package.json`, `go.mod`
   - Look at file extensions in `src/` or project root

2. **Agent framework (if any):**
   - `langgraph` in imports → LangGraph
   - `crewai` in imports → CrewAI
   - `autogen` in imports → AutoGen
   - `langchain` in imports → LangChain
   - Direct SDK usage → Custom agent

3. **Kahuna integration:**
   - Check if `.kahuna/` directory exists
   - If yes, read `.kahuna/context-guide.md` for organizational rules

Record the detected context for reporting.

### Step 2: Run Security Checks

Load the **verify-security** skill and execute its process.

This checks for:
- Hardcoded secrets and API keys
- Dependency version pinning
- Input validation patterns
- Error message exposure
- Secure defaults

Record all findings.

### Step 3: Run Pattern Checks

Load the **verify-patterns** skill and execute its process.

This checks for:
- Loop safety (termination conditions)
- Retry limit enforcement
- Tool registry consistency
- Context size awareness
- LangGraph cycle analysis (if applicable)

Record all findings.

### Step 4: Run Quality Checks

Load the **verify-quality** skill and execute its process.

This checks for:
- Naming conventions
- Code organization
- Magic numbers/strings
- Documentation
- Error handling patterns

Record all findings.

### Step 5: Run Language-Specific Checks

Based on detected language, load the **verify-language** skill and execute its process.

**Python checks:**
- Type hints on public functions
- Docstrings
- Requirements pinning
- Python idioms

**TypeScript/JavaScript checks:**
- Strict mode enabled
- No `any` types
- Async/await error handling
- Promise handling

**Go checks:**
- No ignored errors
- Context propagation
- Package structure
- Go idioms

Record all findings.

### Step 6: Consolidate Report

Combine all findings from Steps 2-5 into a unified verification report.

#### Report Format

```markdown
# Agent Verification Report

**Project:** [project name or path]
**Date:** [current date]
**Mode:** [Kahuna-enhanced | Standalone]
**Language:** [Python | TypeScript | JavaScript | Go]
**Agent framework:** [LangGraph | CrewAI | AutoGen | LangChain | Custom | None]
**Files analyzed:** [count]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

### By Category
| Category | Pass | Warn | Issue |
|----------|------|------|-------|
| Security | X | X | X |
| Patterns | X | X | X |
| Quality | X | X | X |
| Language | X | X | X |

## Security

*(Summary from verify-security)*

- [x] No hardcoded secrets
- [x] Dependencies pinned
- [ ] ⚠️ [finding]
- [ ] ❌ [finding]

## Agent Patterns

*(Summary from verify-patterns — include only if agent detected)*

### Loop Safety
- [x] All loops have termination conditions
- [ ] ⚠️ Potential unbounded loop at `[file:line]`

### Retry Limits
- [x] All retry mechanisms have explicit limits
- [ ] ❌ Missing retry limit at `[file:line]`

### Tool Consistency
- [x] Tool registry found: X tools defined
- [ ] ❌ Hallucinated tool reference at `[file:line]`
- [ ] ⚠️ Undocumented tool: `[name]`

### Context Size
- [x] System prompt within limits (~X tokens)
- [ ] ⚠️ System prompt exceeds recommended size

## Quality

*(Summary from verify-quality)*

- [x] Naming conventions consistent
- [x] Code well-organized
- [ ] ⚠️ [finding]

## Language ([Python/TypeScript/Go])

*(Summary from verify-language)*

- [x] Type safety enforced
- [ ] ⚠️ [finding]
- [ ] ❌ [finding]

## Detailed Findings

> `[P]` = pattern-matched (structurally reliable) · `[H]` = heuristic (best-effort judgment)

### ✅ Passing
- `[P]` No hardcoded secrets or API keys
- `[P]` All retry decorators have stop conditions
- `[H]` Code organization follows best practices

### ⚠️ Warnings
- `[P|H]` [Check name]: [Description]
  - **Location:** [file:line]
  - **Category:** [Security | Patterns | Quality | Language]
  - **Suggestion:** [How to address]

### ❌ Issues
- `[P|H]` [Check name]: [Description]
  - **Location:** [file:line]
  - **Category:** [Security | Patterns | Quality | Language]
  - **Rule:** [Which rule this violates]
  - **Fix:** [Specific remediation steps]

## Recommendations

1. **[Highest priority]** - [Specific action]
2. **[Second priority]** - [Specific action]
3. [Additional improvements]

---

*Report generated by Agent Verifier v1.0.0*
```

### Step 7: Export Report (Optional)

After presenting the report, ask the user:

> Would you like to save this verification report to a file?

If confirmed:

1. Create the reports directory if it doesn't exist:
   ```bash
   mkdir -p reports/verification
   ```

2. Generate filename using the **current date and time** (NOT placeholders):
   - Get the actual current timestamp from your environment context
   - Format: `reports/verification/{date}_{time}.md`
   - Date format: `YYYY-MM-DD` (e.g., `2026-03-17`)
   - Time format: `HH-MM-SS` (e.g., `08-15-42` for 8:15:42 AM)
   
   **IMPORTANT:** Use the real current time, not zeros or placeholders. Check your system context for "Current Time" information.
   
   **Example:** If the current time is March 17, 2026 at 1:05:30 AM PST, the filename should be:
   `reports/verification/2026-03-17_01-05-30.md`

3. Save the complete report to that file.

## Check Tier Discipline

Throughout all verification steps, maintain tier discipline:

- **`[PATTERN]` checks** — Apply exactly as written. A rule says "flag X" → flag X. No judgment.
- **`[HEURISTIC]` checks** — Apply with judgment. Mark findings clearly with `[H]`.

Tag every finding in the report with `[P]` or `[H]` so readers understand confidence level.

## Notes

- **Privacy first:** All code analysis happens locally. Nothing is sent to external services.
- **Kahuna enhances, not requires:** The skill works standalone with built-in rules. Kahuna adds organization-specific knowledge.
- **Be specific:** Include file names and line numbers when reporting issues.
- **Explain the "why":** Help developers understand why each rule matters.
- **Honor existing configs:** Respect project's existing lint rules, `.editorconfig`, etc.
