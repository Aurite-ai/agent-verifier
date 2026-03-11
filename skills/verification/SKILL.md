---
name: verification
description: Verify code against organizational policies, security requirements, and framework best practices. Use when asked to "verify", "review", "audit", "check compliance", or "validate" code.
---

# Agent Verifier

## Purpose

Verify code against business rules, security policies, and framework best practices. All analysis happens locally—code never leaves your machine.

## When to Use

Trigger this skill when the user asks to:
- "verify my code/agent"
- "review code"
- "check compliance"
- "audit my code"
- "check against rules"
- "validate implementation"

## Process

### Step 1: Detect Mode and Load Context

**Check for Kahuna integration** (`.kahuna/` directory exists):

If `.kahuna/` directory exists:
- Context is pre-loaded from `kahuna_prepare_context`
- Use `kahuna_ask` for additional queries
- Read `.kahuna/context-guide.md` for organizational rules and framework patterns

If `.kahuna/` directory does NOT exist (standalone mode):
- Scan for project configuration files
- Apply built-in best practices (see Step 1b)

### Step 1b: Standalone Context Discovery

When running without Kahuna, gather context from the project itself:

**Project configuration files:**
- `package.json`, `pyproject.toml`, `Cargo.toml` - Dependencies and project type
- `tsconfig.json`, `biome.json`, `.eslintrc*` - Linting/formatting rules
- `.env.example` - Expected environment variables

**Documentation:**
- `README.md` - Project overview
- `docs/`, `CONTRIBUTING.md`, `.github/CONTRIBUTING.md` - Guidelines
- `ARCHITECTURE.md`, `DESIGN.md` - Design decisions

**Detect language/framework from:**
- File extensions (`.py`, `.ts`, `.js`, `.go`, `.rs`)
- Dependencies in manifest files
- Directory structure patterns

### Step 2: Discover Files to Analyze

Locate implementation files in the project. Check these common locations:

**Directories:**
- `src/agent/`, `agent/`, `src/`, project root
- `lib/`, `app/`, `packages/`

**Key files to analyze:**
- `graph.py` - Workflow/graph definition (LangGraph)
- `tools.py` - Tool implementations
- `state.py` - State schema definitions
- `prompts.py` - Prompt templates
- `nodes.py` - Node function implementations
- `config.py`, `settings.py` - Configuration
- `*.ts`, `*.js` - TypeScript/JavaScript sources
- `*.go`, `*.rs` - Go/Rust sources

**AI Agent files to prioritize (when agent patterns detected):**
- `graph.py`, `graph.ts` - Agent workflow definitions
- `tools.py`, `tools.ts`, `tools/*.py`, `tools/*.ts` - Tool implementations
- `state.py`, `state.ts` - State schemas
- `prompts.py`, `prompts/*.md`, `system.md` - Prompt templates
- `agent.py`, `agent.ts` - Main agent logic
- `langgraph.json`, `crew.yaml` - Framework configurations

**Exclude from prompt size analysis:**
- `skills/` directory and all subdirectories — these are skill definition files (e.g. `SKILL.md`) loaded on demand by the coding agent, not static system prompts embedded in every LLM call. Flagging them for size would be a false positive.

Use `list_files` or equivalent to discover the actual structure, then read relevant files.

### Step 3: Verify Code Against Rules

Analyze code against all available rules:

**With Kahuna (enhanced mode):**
1. **Organizational rules** - Company policies from `.kahuna/context-guide.md`
2. **IT/Security rules** - Security requirements from knowledge base
3. **Framework best practices** - Patterns from surfaced context

**Standalone (built-in rules):**
1. **General code quality**
   - Clear naming conventions (descriptive, consistent)
   - Appropriate code organization and structure
   - Error handling patterns
   - No magic numbers/strings without constants

2. **Security basics**
   - No hardcoded secrets, API keys, or passwords
   - Input validation on external data
   - Proper error messages (no stack traces in production)
   - Secure defaults

3. **Language-specific (auto-detected):**

   *TypeScript/JavaScript:*
   - Type safety (prefer strict mode)
   - Async/await error handling
   - Dependency security (outdated/vulnerable packages)
   - No `any` types without justification

   *Python:*
   - Type hints on public functions
   - Docstrings for modules, classes, functions
   - Virtual environment usage
   - Requirements pinning

   *Go:*
   - Error handling (no ignored errors)
   - Context propagation
   - Proper package structure

4. **AI Agent-specific (if detected):**
   - State schema validation
   - Tool error handling
   - Prompt injection considerations
   - Rate limiting awareness

   **Agent Observability Patterns (NEW):**

   5. **Loop Safety**
      - All `while True` patterns must have explicit break conditions
      - Retry decorators must specify max attempts
      - Agent loops must have iteration counters
      - Recursive functions must have termination conditions

      | Pattern | Language | Detection | Severity |
      |---------|----------|-----------|----------|
      | `while True:` without `break` in scope | Python | Regex + scope analysis | ⚠️ Warning |
      | `for { }` without break/return | Go | Regex | ⚠️ Warning |
      | `while (true)` without break | TS/JS | Regex | ⚠️ Warning |
      | Recursive call without termination check | All | Call graph analysis | ⚠️ Warning |
      | `@retry` without `max_retries` or `stop` | Python | Decorator inspection | ❌ Issue |
      | `retryable()` without limit config | TS/JS | Function call inspection | ❌ Issue |

   6. **Retry Limit Enforcement**
      - Retry decorators must specify max attempts
      - Backoff strategies must have maximum delay caps

      | Library/Pattern | Required Parameter | Language |
      |-----------------|-------------------|----------|
      | `@retry` (tenacity) | `stop=stop_after_attempt(n)` | Python |
      | `@backoff.on_exception` | `max_tries=n` | Python |
      | `retry` (async-retry) | `retries: n` | Node.js |
      | `p-retry` | `retries: n` | Node.js |
      | Custom `while` retry | Counter with max check | All |

   7. **Tool Registry Consistency**
      - All tool references must exist in tool definitions
      - Tool names in prompts must match registered tools
      - No undefined tool calls in agent code

      *Detection approach:*
      1. Build tool inventory from definitions (`@tool`, `@function_tool`, schema `name:`)
      2. Find tool references in code and prompts
      3. Flag any reference not in the inventory

   8. **Context Size Awareness**
      - System prompts should not exceed recommended limits
      - Large file inclusions should be flagged

      | Content Type | Warning Threshold | Issue Threshold |
      |--------------|-------------------|-----------------|
      | System prompt | > 4,000 tokens (~16KB) | > 8,000 tokens (~32KB) |
      | Single tool description | > 500 tokens (~2KB) | > 1,000 tokens (~4KB) |
      | Total tool descriptions | > 2,000 tokens (~8KB) | > 4,000 tokens (~16KB) |

      *Token estimation:* Use heuristic of ~4 characters per token for English text.

   9. **Explicit Tool Listing**
      - System prompts should list available tools
      - Tool capabilities should be clearly described
      - Agents should know their boundaries

      *Detection:* Check for tool listing sections (headers like "Available Tools", "You have access to")

For each check, determine:
- ✅ **Pass** - Code complies with the rule
- ⚠️ **Warning** - Potential concern worth reviewing
- ❌ **Issue** - Clear violation that needs fixing

### Step 3b: Agent Pattern Analysis (if AI agent detected)

If the project appears to be an AI agent (LangGraph, CrewAI, AutoGen, LangChain, or custom), perform additional analysis:

**Framework Detection:**
- `langgraph` in imports → LangGraph agent
- `crewai` in imports → CrewAI agent
- `autogen` in imports → AutoGen agent
- `langchain` in imports → LangChain agent
- Custom patterns → Custom agent framework

**Analysis Steps:**

1. **Build tool registry**
   - Scan tool definition files (`tools.py`, `tools.ts`, `tools/*.py`)
   - Extract tool names from decorators (`@tool`, `@function_tool`)
   - Extract from schema definitions (`name: "tool_name"`)
   - Note tool count and complexity

2. **Analyze agent loops**
   - Find main execution loops
   - Check for termination conditions (break, return, max iterations)
   - Verify retry limits on all retry mechanisms

3. **Analyze prompts**
   - Measure prompt sizes (estimate tokens)
   - Check for tool listings in system prompts
   - Verify tool references against registry
   - **Exclude `skills/` directories** — files under `skills/` (e.g. `SKILL.md`) are skill definitions loaded on demand, not static system prompts. Do not flag them for context size.

4. **Cross-reference**
   - Tools in prompts vs registry (flag mismatches)
   - State fields vs usage
   - Config vs implementation

**Example findings:**

```markdown
### ⚠️ Warnings
- Potential infinite loop: `agent/loop.py:45`
  - **Pattern:** `while True:` without visible break condition
  - **Suggestion:** Add explicit max iteration counter: `for i in range(MAX_ITERATIONS):`

- Large system prompt: `prompts/system.md`
  - **Size:** ~6,200 tokens (estimated)
  - **Threshold:** 4,000 tokens (warning)
  - **Risk:** May cause context overflow with long conversations
  - **Suggestion:** Consider splitting into base prompt + dynamic sections

### ❌ Issues
- Missing retry limit: `tools/api_client.py:23`
  - **Pattern:** `@retry` decorator without `stop` parameter
  - **Rule:** All retry mechanisms must have explicit bounds
  - **Fix:** Add `@retry(stop=stop_after_attempt(3))` or use `tenacity.stop_after_attempt(3)`

- Hallucinated tool reference: `prompts/system.md:34`
  - **Reference:** `execute_sql_query`
  - **Available tools:** search_docs, write_file, run_tests
  - **Rule:** Tool references must match registered tools
  - **Fix:** Either add tool definition or remove reference from prompt
```

### Step 4: Generate Report

Output a structured verification report with agent-specific sections when applicable:

```markdown
# Verification Report

**Project:** [project name or path]
**Date:** [current date]
**Mode:** [Kahuna-enhanced | Standalone]
**Files analyzed:** [count]
**Agent type detected:** [LangGraph | CrewAI | AutoGen | LangChain | Custom | None]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

### By Category
| Category | Pass | Warn | Issue |
|----------|------|------|-------|
| Code Quality | X | X | X |
| Security | X | X | X |
| Agent Patterns | X | X | X |

## Agent Pattern Analysis

*(Include this section only when Agent type detected ≠ None)*

### Loop Safety
- [x] All retry mechanisms have explicit limits
- [ ] ⚠️ Potential unbounded loop at `[file:line]`
- [ ] ❌ Missing retry limit at `[file:line]`

### Tool Consistency
- [x] Tool registry found: X tools defined
- [ ] ❌ Y hallucinated tool references in prompts
- [ ] ⚠️ Z tools not documented in system prompt

### Context Management
- [x] System prompt within limits (~X tokens)
- [ ] ⚠️ System prompt exceeds recommended size (~X tokens)
- [x] Tool descriptions within limits

## Findings

### ✅ Passing
- [Check name]: [Brief confirmation of compliance]

### ⚠️ Warnings
- [Check name]: [Description of concern]
  - **Location:** [file:line if applicable]
  - **Suggestion:** [How to address]

### ❌ Issues
- [Check name]: [Description of violation]
  - **Location:** [file:line]
  - **Rule:** [Which rule this violates]
  - **Fix:** [Specific remediation steps]

## Recommendations

*(Generic recommendations for all projects)*

1. [Priority recommendation based on findings]
2. [Additional improvements]

## Agent-Specific Recommendations

*(Include this section only when Agent type detected ≠ None)*

1. **Loop Safety:** [Add iteration limits / Add retry bounds]
2. **Tool Registry:** [Remove or define hallucinated tools]
3. **Context Management:** [Split large prompts / Add tool documentation]
```

### Step 5: Export Report (Optional)

After presenting the report, ask the user:

> Would you like to save this verification report to a file?

If confirmed:

1. Create the reports directory if it doesn't exist:
   ```bash
   mkdir -p reports/verification
   ```

2. Generate filename with **actual current timestamp** (not zeros):
   ```
   reports/verification/YYYY-MM-DD_HH-MM-SS.md
   ```
   
   **Example:** `reports/verification/2026-03-04_16-48-21.md`
   
   Use the current time from the system, not placeholder values.
   The format is: `{year}-{month}-{day}_{hour}-{minute}-{second}.md`

3. Save the complete report to that file.

## Notes

- **Privacy first:** All code analysis happens locally. Nothing is sent to external services.
- **Kahuna enhances, not requires:** The skill works standalone with built-in rules. Kahuna adds organization-specific knowledge.
- **Be specific:** Include file names and line numbers when reporting issues.
- **Explain the "why":** Help developers understand why each rule matters.
- **Honor existing configs:** Respect project's existing lint rules, `.editorconfig`, etc.
