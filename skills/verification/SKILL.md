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

#### Check Tiers

Every check in this skill is classified as one of two tiers. Apply them differently:

- **`[PATTERN]`** — Mechanical. The answer is objectively correct or incorrect based on code structure. Apply the rule exactly as written. Do not use judgment to soften or skip. A missing `stop=` parameter on `@retry` is always an ❌ Issue, regardless of context. Report these with high confidence.

- **`[HEURISTIC]`** — Judgment required. The rule describes a quality signal that requires interpretation. Apply it as a best-effort assessment. Mark these findings clearly so the reader knows they reflect analysis, not a deterministic check.

In the report, tag every finding with its tier: `[P]` for pattern, `[H]` for heuristic.

---

Analyze code against all available rules:

**With Kahuna (enhanced mode):**
1. **Organizational rules** - Company policies from `.kahuna/context-guide.md`
2. **IT/Security rules** - Security requirements from knowledge base
3. **Framework best practices** - Patterns from surfaced context

**Standalone (built-in rules):**

1. **`[HEURISTIC]` General code quality**
   - Clear naming conventions (descriptive, consistent)
   - Appropriate code organization and structure
   - Error handling patterns
   - No magic numbers/strings without constants

2. **Security basics** — mixed tier (see per-item labels below:)
   - `[PATTERN]` No hardcoded secrets — scan for assignments matching `API_KEY`, `SECRET`, `PASSWORD`, `TOKEN`, `PRIVATE_KEY` (case-insensitive) assigned to string literals. Flag any match as ❌ Issue.
   - `[HEURISTIC]` Input validation on external data
   - `[HEURISTIC]` Proper error messages (no stack traces in production)
   - `[HEURISTIC]` Secure defaults

3. **Language-specific (auto-detected):**

   *TypeScript/JavaScript:*
   - `[PATTERN]` Type safety — flag if `tsconfig.json` does not have `"strict": true`
   - `[HEURISTIC]` Async/await error handling
   - `[PATTERN]` No `any` types — flag unqualified `: any` annotations as ⚠️ Warning
   - `[HEURISTIC]` Dependency security (outdated/vulnerable packages)

   *Python:*
   - `[PATTERN]` Type hints — flag any `def` function in public scope (no leading `_`) that has parameters without type annotations, as ⚠️ Warning
   - `[HEURISTIC]` Docstrings for modules, classes, functions
   - `[PATTERN]` Requirements pinning — flag any line in `requirements.txt` / `pyproject.toml` dependencies using `>=`, `>`, or no version specifier (should use `==`), as ❌ Issue

   *Go:*
   - `[PATTERN]` No ignored errors — flag any `_ = ` assignments where the right-hand side is a function call returning `error`, as ❌ Issue
   - `[HEURISTIC]` Context propagation
   - `[HEURISTIC]` Proper package structure

4. **AI Agent-specific (if detected):**
   - `[HEURISTIC]` State schema validation
   - `[HEURISTIC]` Tool error handling
   - `[HEURISTIC]` Prompt injection considerations
   - `[HEURISTIC]` Rate limiting awareness

   **Agent Observability Patterns:**

   5. **`[PATTERN]` Loop Safety**

      Apply mechanically. Do not pass a loop because it "looks like it might terminate."

      | Pattern to find | Pass condition | Severity |
      |-----------------|----------------|----------|
      | `while True:` in Python | A `break` statement exists within the same block scope | ⚠️ Warning if absent |
      | `for { }` in Go | A `break` or `return` exists within the block | ⚠️ Warning if absent |
      | `while (true)` in TS/JS | A `break` or `return` exists within the block | ⚠️ Warning if absent |
      | Function calls itself recursively | A non-recursive return path exists (base case), OR a depth/counter parameter is present | ⚠️ Warning if absent |

   6. **`[PATTERN]` Retry Limit Enforcement**

      Apply mechanically. Check each decorator or call against the table below. If the required parameter is absent, flag as ❌ Issue regardless of other parameters present.

      **Decorator-based (Python):**

      | Library/Pattern | Required parameter | Fail condition |
      |-----------------|-------------------|----------------|
      | `@retry` (tenacity) | `stop=stop_after_attempt(n)` or `stop=stop_after_delay(n)` | `stop=` absent |
      | `@backoff.on_exception` | `max_tries=n` | `max_tries=` absent |

      **HTTP client retry configuration (Python):**

      | Library/Pattern | Required parameter | Fail condition |
      |-----------------|-------------------|----------------|
      | `urllib3.Retry(...)` | `total=n` where n > 0 | `total=` absent or `total=0` |
      | `HTTPAdapter(max_retries=Retry(...))` | The `Retry` object must have `total=n` | `total=` absent in the `Retry` object passed to `max_retries=` |
      | `httpx.HTTPTransport(retries=n)` | `retries=n` where n > 0 | `retries=` absent or `retries=0` |

      **AWS SDK (Python/boto3):**

      | Library/Pattern | Required parameter | Fail condition |
      |-----------------|-------------------|----------------|
      | `Config(retries={...})` (botocore) | `max_attempts` key with value > 1 | `max_attempts` absent, or `max_attempts: 0` or `max_attempts: 1` (no retries) |

      > Note: boto3 clients without any explicit `Config(retries=...)` use the SDK default (3 attempts, standard mode) — do **not** flag the absence of retry config as an issue. Only flag when retry config is present but disables retries.

      **JavaScript/TypeScript:**

      | Library/Pattern | Required parameter | Fail condition |
      |-----------------|-------------------|----------------|
      | `retry(...)` (async-retry) | `retries: n` in options object | `retries:` absent |
      | `pRetry(...)` (p-retry) | `retries: n` in options object | `retries:` absent |

      **Custom retry loops (all languages):**

      A `while True:` / `while (true)` / `for {}` block that contains a `try/except` (or `try/catch`) with a `continue` or a re-invocation of the same call is a manual retry loop. Apply the same rule as Loop Safety: a bounded counter must be present.

      | Pattern to find | Pass condition | Fail condition |
      |-----------------|----------------|----------------|
      | Loop + `try/except` + `continue` | An integer counter is declared before the loop and incremented inside it, with a conditional check against a max | No counter present → ❌ Issue |

   7. **`[PATTERN]` Tool Registry Consistency**

      Apply mechanically:
      1. Collect all tool names from definition files. A tool name is defined by:
         - `@tool` or `@function_tool` decorator on a function → the function name
         - A dict/object with a `"name":` or `name:` key at the top level of a tools file
      2. Collect all tool name references from prompt files (`.md`, `.txt`, `prompts.py`). A reference is any backtick-quoted identifier or string that names a capability the agent is told it can use.
      3. Flag every reference not in the definition list as ❌ Issue (hallucinated tool).
      4. Flag every defined tool not mentioned in any prompt as ⚠️ Warning (undocumented tool).
      5. **`[HEURISTIC]` Tools never bound to LLM** — Find where tools are defined (any list, registry, or decorated set of functions intended as agent tools). Then find where the LLM is invoked (the call that sends messages to the model). Check whether the tools are passed to that invocation point. If a tools collection exists but is never connected to the LLM call, flag as ❌ Issue: the LLM has no knowledge of these tools and cannot invoke them — the tool-calling architecture is broken or incomplete.

         The connection can take many forms depending on the framework (e.g. a `tools=` argument, a bind method, a plugin registration API, an agent constructor parameter). Do not look for any specific method name — reason about whether the defined tools actually reach the LLM invocation. Example of the broken pattern: tools decorated with `@tool` and collected in `ALL_TOOLS`, but the LLM call never receives `ALL_TOOLS` in any form.

   8. **`[PATTERN]` Context Size Awareness**

      Apply mechanically using the formula: `token_estimate = len(file_content_chars) / 4`

      | Content | ⚠️ Warning threshold | ❌ Issue threshold |
      |---------|----------------------|-------------------|
      | System prompt file | > 4,000 tokens | > 8,000 tokens |
      | Single tool description block | > 500 tokens | > 1,000 tokens |
      | All tool descriptions combined | > 2,000 tokens | > 4,000 tokens |

      Exclude `skills/` directories from this check (see Step 2).

   9. **`[HEURISTIC]` Explicit Tool Listing**
      - System prompts should list available tools
      - Tool capabilities should be clearly described

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

   Scan all tool definition files: `tools.py`, `tools.ts`, `tools/*.py`, `tools/*.ts`, and any file whose name or content suggests it defines agent tools. Extract tool names using the patterns below. A name found by **any** pattern counts as a registered tool.

   **Python — decorator patterns:**

   | Pattern | How to extract name |
   |---------|---------------------|
   | `@tool` (LangChain) on a `def` | Function name immediately below the decorator |
   | `@function_tool` (OpenAI Agents SDK) on a `def` | Function name immediately below the decorator |
   | `@tool(name="...")` with explicit name arg | Use the `name=` argument value, not the function name |

   **Python — dict/list patterns:**

   | Pattern | How to extract name |
   |---------|---------------------|
   | `{"type": "function", "function": {"name": "..."}}` (OpenAI function calling) | Value of the `"name"` key inside `"function"` |
   | `{"name": "...", "input_schema": {...}}` (Anthropic tool use) | Value of the top-level `"name"` key |
   | `{"name": "...", "description": "...", "parameters": {...}}` (generic schema) | Value of the top-level `"name"` key |
   | `ToolNode([func1, func2, ...])` (LangGraph) | Each function name in the list — these must already be registered via decorator or schema above |
   | `tools = [func1, func2]` / `TOOLS = [...]` list assigned to a variable | Each identifier in the list — resolve to function names already found by other patterns |

   **TypeScript/JavaScript — patterns:**

   | Pattern | How to extract name |
   |---------|---------------------|
   | `{ type: "function", function: { name: "..." } }` (OpenAI) | Value of `name:` inside `function:` |
   | `tool({ description: "...", parameters: z.object({...}) })` assigned to a `const name =` (Vercel AI SDK) | The `const` variable name |
   | `new DynamicTool({ name: "...", ... })` (LangChain.js) | Value of `name:` |
   | `zodFunction({ name: "...", ... })` | Value of `name:` |

   After collecting all names, note the total count and source format for the report.

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

5. **LangGraph graph cycle analysis** *(only when LangGraph is detected)*

   LangGraph agents define control flow as a directed graph of nodes and edges, not `while` loops. A cycle in the graph is intentional (the agent loops between "agent" and "tools" nodes), but **every cycle must have at least one conditional edge that can route to `END`**. A cycle with no reachable `END` is an infinite loop at the graph level.

   **Detection steps:**

   a. Find the graph file (`graph.py`, `graph.ts`, or file containing `StateGraph`/`MessageGraph`)

   b. Build an edge map by scanning for:
      - `workflow.add_edge(source, dest)` — unconditional edge
      - `workflow.add_conditional_edges(source, fn, mapping)` — conditional edges; extract all destination values from the mapping dict

   c. Identify cycles: find any node that is reachable from itself by following edges

   d. For each cycle, check if `END` (or `"__end__"`) is reachable from any node in the cycle via a conditional edge mapping

   e. Flag accordingly:

   | Condition | Severity |
   |-----------|----------|
   | Cycle exists, `END` reachable via conditional edge | ✅ Pass |
   | Cycle exists, no path to `END` from any node in cycle | ❌ Issue |
   | Graph has no `END` node at all | ❌ Issue |
   | Node has no outgoing edges and is not `END` | ⚠️ Warning (dead-end node) |

   **Example — infinite cycle (❌ Issue):**
   ```python
   workflow.add_edge("agent", "tools")
   workflow.add_edge("tools", "agent")  # cycle, but no path to END
   ```

   **Example — cycle with exit (✅ Pass):**
   ```python
   workflow.add_conditional_edges("agent", should_continue, {
       "continue": "tools",
       "end": END          # END is reachable → cycle is safe
   })
   workflow.add_edge("tools", "agent")
   ```

   **Note:** The check inspects the *static structure* of `add_edge` / `add_conditional_edges` calls. It does not evaluate the routing function itself (`should_continue`) — that is runtime behaviour. If the mapping dict contains `END` as a possible destination, the check passes.

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
- [ ] ❌ `[H]` Tools defined but never connected to LLM invocation — LLM cannot invoke tools
- [ ] ⚠️ Z tools not documented in system prompt

### Context Management
- [x] System prompt within limits (~X tokens)
- [ ] ⚠️ System prompt exceeds recommended size (~X tokens)
- [x] Tool descriptions within limits

## Findings

> `[P]` = pattern-matched (structurally reliable) · `[H]` = heuristic (best-effort judgment)

### ✅ Passing
- `[P]` [Check name]: [Brief confirmation of compliance]

### ⚠️ Warnings
- `[P|H]` [Check name]: [Description of concern]
  - **Location:** [file:line if applicable]
  - **Suggestion:** [How to address]

### ❌ Issues
- `[P|H]` [Check name]: [Description of violation]
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
- **Respect tier discipline:** `[PATTERN]` checks must be applied exactly as specified — do not use judgment to pass something the rule says should fail. `[HEURISTIC]` checks require judgment — apply them thoughtfully and mark findings clearly so the reader understands the confidence level.
