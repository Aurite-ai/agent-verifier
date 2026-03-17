---
name: verify-patterns
version: "1.0.0"
description: Verify AI agent patterns including loop safety, retry limits, tool consistency, context size, and graph cycle analysis. Use when asked to "verify agent patterns", "check loops", "verify tools", or "check retry limits".
---

# Agent Pattern Verification

## Purpose

Verify AI agent code for common anti-patterns that can cause infinite loops, runaway retries, tool mismatches, and context overflow. All analysis happens locally.

## When to Use

Trigger this skill when the user asks to:
- "verify agent patterns"
- "check agent loops"
- "verify tools"
- "check retry limits"
- "verify agent safety"

> **Note:** For full verification including security, quality, and language-specific checks, tell the user to say **"verify agent"**.

## Process

### Step 1: Detect Agent Framework

Identify the agent framework by checking imports in Python/TypeScript files:

| Import Pattern | Framework |
|----------------|-----------|
| `from langgraph` or `import langgraph` | LangGraph |
| `from crewai` or `import crewai` | CrewAI |
| `from autogen` or `import autogen` | AutoGen |
| `from langchain` or `import langchain` | LangChain |
| Direct `openai`/`anthropic` SDK only | Custom |

Also check for framework config files: `langgraph.json`, `crew.yaml`.

### Step 2: Locate Agent Files

Find files to analyze:

**Priority files:**
- `graph.py`, `graph.ts` - Agent workflow definitions
- `tools.py`, `tools.ts`, `tools/*.py`, `tools/*.ts` - Tool implementations
- `state.py`, `state.ts` - State schemas
- `prompts.py`, `prompts/*.md`, `system.md` - Prompt templates
- `agent.py`, `agent.ts` - Main agent logic

**Directories to check:**
- `src/agent/`, `agent/`, `src/`, project root
- `lib/`, `app/`, `packages/`

**Exclude from analysis:**
- `skills/` directory — these are skill definitions, not agent system prompts

### Step 3: Run Pattern Checks

#### Check Tiers

- **`[PATTERN]`** — Mechanical check. Apply exactly as written.
- **`[HEURISTIC]`** — Judgment required. Mark findings clearly.

Tag every finding with `[P]` for pattern or `[H]` for heuristic.

---

#### 3.1 `[PATTERN]` Loop Safety

Apply mechanically. Do not pass a loop because it "looks like it might terminate."

| Pattern to find | Pass condition | Severity |
|-----------------|----------------|----------|
| `while True:` in Python | A `break` statement exists within the same block scope | ⚠️ Warning if absent |
| `for { }` in Go | A `break` or `return` exists within the block | ⚠️ Warning if absent |
| `while (true)` in TS/JS | A `break` or `return` exists within the block | ⚠️ Warning if absent |
| Function calls itself recursively | A non-recursive return path exists (base case), OR a depth/counter parameter is present | ⚠️ Warning if absent |

**`[HEURISTIC]` Fallback: Unrecognized Loop Patterns**

After applying the pattern table, also scan for:
- Loops where termination depends entirely on external/runtime state with no timeout
- Generator functions that `yield` indefinitely without documented exit
- Event/polling loops without timeout parameters
- Recursive call chains across multiple functions without depth tracking

Flag as ⚠️ Warning: *"Potential unbounded loop not matching known patterns — verify termination condition manually"*

---

#### 3.2 `[PATTERN]` Retry Limit Enforcement

Apply mechanically. If required parameter is absent, flag as ❌ Issue.

**Python — Decorator-based:**

| Library/Pattern | Required parameter | Fail condition |
|-----------------|-------------------|----------------|
| `@retry` (tenacity) | `stop=stop_after_attempt(n)` or `stop=stop_after_delay(n)` | `stop=` absent |
| `@backoff.on_exception` | `max_tries=n` | `max_tries=` absent |

**Python — HTTP client retry:**

| Library/Pattern | Required parameter | Fail condition |
|-----------------|-------------------|----------------|
| `urllib3.Retry(...)` | `total=n` where n > 0 | `total=` absent or `total=0` |
| `HTTPAdapter(max_retries=Retry(...))` | Retry object must have `total=n` | `total=` absent |
| `httpx.HTTPTransport(retries=n)` | `retries=n` where n > 0 | `retries=` absent or `retries=0` |

**Python — AWS SDK (boto3):**

| Library/Pattern | Required parameter | Fail condition |
|-----------------|-------------------|----------------|
| `Config(retries={...})` | `max_attempts` > 1 | `max_attempts` absent or ≤ 1 |

> Note: boto3 without explicit retry config uses SDK defaults (3 attempts) — do not flag absence.

**JavaScript/TypeScript:**

| Library/Pattern | Required parameter | Fail condition |
|-----------------|-------------------|----------------|
| `retry(...)` (async-retry) | `retries: n` in options | `retries:` absent |
| `pRetry(...)` (p-retry) | `retries: n` in options | `retries:` absent |

**Custom retry loops (all languages):**

| Pattern to find | Pass condition | Fail condition |
|-----------------|----------------|----------------|
| Loop + `try/except` + `continue` | Integer counter with max check | No counter → ❌ Issue |

**`[HEURISTIC]` Fallback: Unrecognized Retry Patterns**

After applying pattern tables, scan for:
- Functions/decorators with "retry" in name not in tables above
- Imported modules with "retry" in package name (e.g. `stamina`, `aiohttp_retry`)
- Loops with sleep + exception handling + re-invocation without visible counter
- Config keys like `max_retries`, `retry_count`, `attempts`

Flag as ⚠️ Warning: *"Potential retry pattern not matching known libraries — verify retry bounds manually"*

---

#### 3.3 `[PATTERN]` Tool Registry Consistency

**Step 1: Collect defined tools**

Scan tool definition files. A name found by any pattern counts as registered.

*Python — decorator patterns:*

| Pattern | How to extract name |
|---------|---------------------|
| `@tool` (LangChain) on `def` | Function name below decorator |
| `@function_tool` (OpenAI Agents SDK) on `def` | Function name below decorator |
| `@tool(name="...")` | Use `name=` argument value |

*Python — dict/list patterns:*

| Pattern | How to extract name |
|---------|---------------------|
| `{"type": "function", "function": {"name": "..."}}` (OpenAI) | Value of `"name"` inside `"function"` |
| `{"name": "...", "input_schema": {...}}` (Anthropic) | Top-level `"name"` |
| `{"name": "...", "description": "...", "parameters": {...}}` | Top-level `"name"` |
| `ToolNode([func1, func2, ...])` (LangGraph) | Each function name in list |
| `tools = [func1, func2]` / `TOOLS = [...]` | Each identifier in list |

*TypeScript/JavaScript:*

| Pattern | How to extract name |
|---------|---------------------|
| `{ type: "function", function: { name: "..." } }` (OpenAI) | `name:` inside `function:` |
| `tool({ description: "...", parameters: z.object({...}) })` | The `const` variable name |
| `new DynamicTool({ name: "...", ... })` (LangChain.js) | Value of `name:` |
| `zodFunction({ name: "...", ... })` | Value of `name:` |

**Step 2: Collect tool references from prompts**

Scan `.md`, `.txt`, `prompts.py` for backtick-quoted identifiers naming capabilities.

**Step 3: Cross-reference**

| Finding | Severity |
|---------|----------|
| Reference not in definition list | ❌ Issue (hallucinated tool) |
| Defined tool not in any prompt | ⚠️ Warning (undocumented tool) |

**`[HEURISTIC]` Tools never bound to LLM**

Find where tools are defined and where LLM is invoked. If tools exist but are never connected to the LLM call, flag as ❌ Issue: *"Tools defined but never connected to LLM invocation"*

**`[HEURISTIC]` Fallback: Unrecognized Tool Definitions**

Scan for tool-like structures:
- Dicts with both `"description"` and `"parameters"` keys
- Functions with structured docstrings (name, params, return)
- Variables named `tools`, `tool_list`, `available_tools`, `functions`
- Classes with `run()`, `execute()`, or `__call__()` methods

Include in count and note: *"Tool detected via heuristic — verify this is an intended agent tool."*

---

#### 3.4 `[PATTERN]` Context Size Awareness

Formula: `token_estimate = len(file_content_chars) / 4`

| Content | ⚠️ Warning threshold | ❌ Issue threshold |
|---------|----------------------|-------------------|
| System prompt file | > 4,000 tokens | > 8,000 tokens |
| Single tool description | > 500 tokens | > 1,000 tokens |
| All tool descriptions combined | > 2,000 tokens | > 4,000 tokens |

**Exclude:** `skills/` directories (loaded on demand, not embedded)

**`[HEURISTIC]` Fallback: Borderline and Non-Standard**

- Estimates within 20% of threshold → flag with tokenizer recommendation
- Dynamic prompts (f-strings, `.format()`) → flag if template alone is large
- Multiple concatenated prompts → estimate combined size
- Prompts with includes → note effective size may be larger

---

#### 3.5 `[HEURISTIC]` Explicit Tool Listing

Check system prompts for:
- Headers like "Available Tools", "You have access to"
- Tool capability descriptions

Flag if tools are defined but not documented in system prompt.

---

#### 3.6 `[PATTERN]` LangGraph Graph Cycle Analysis

*(Only when LangGraph is detected)*

**Detection steps:**

a. Find graph file (`graph.py`, `graph.ts`, or file with `StateGraph`/`MessageGraph`)

b. Build edge map:
   - `workflow.add_edge(source, dest)` — unconditional edge
   - `workflow.add_conditional_edges(source, fn, mapping)` — extract destinations from mapping

c. Identify cycles: nodes reachable from themselves

d. For each cycle, check if `END` (or `"__end__"`) is reachable via conditional edge

| Condition | Severity |
|-----------|----------|
| Cycle exists, `END` reachable via conditional | ✅ Pass |
| Cycle exists, no path to `END` | ❌ Issue |
| Graph has no `END` node | ❌ Issue |
| Node has no outgoing edges and is not `END` | ⚠️ Warning (dead-end) |

**Example — infinite cycle (❌ Issue):**
```python
workflow.add_edge("agent", "tools")
workflow.add_edge("tools", "agent")  # no path to END
```

**Example — cycle with exit (✅ Pass):**
```python
workflow.add_conditional_edges("agent", should_continue, {
    "continue": "tools",
    "end": END
})
workflow.add_edge("tools", "agent")
```

**`[HEURISTIC]` Fallback: Non-LangGraph Graphs**

Scan for graph-like control flow:
- State machines with transition tables
- Custom routing with implicit cycles
- LangGraph.js (camelCase methods)
- CrewAI/AutoGen agent handoffs
- Adjacency lists without termination path

Flag as ⚠️ Warning: *"Potential cyclic control flow — verify termination condition exists"*

---

### Step 4: Generate Report

```markdown
# Agent Pattern Verification Report

**Project:** [name or path]
**Date:** [current date]
**Framework detected:** [LangGraph | CrewAI | AutoGen | LangChain | Custom | None]
**Files analyzed:** [count]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

## Loop Safety

- [x] All loops have termination conditions
- [ ] ⚠️ Potential unbounded loop at `[file:line]`

## Retry Limits

- [x] All retry mechanisms have explicit limits
- [ ] ❌ Missing retry limit at `[file:line]`

## Tool Consistency

- [x] Tool registry found: X tools defined
- [ ] ❌ Y hallucinated tool references
- [ ] ⚠️ Z undocumented tools

## Context Size

- [x] System prompt within limits (~X tokens)
- [ ] ⚠️ System prompt exceeds recommended size

## Findings

> `[P]` = pattern-matched · `[H]` = heuristic

### ✅ Passing
- `[P]` [Check]: [confirmation]

### ⚠️ Warnings
- `[P|H]` [Check]: [description]
  - **Location:** [file:line]
  - **Suggestion:** [how to fix]

### ❌ Issues
- `[P|H]` [Check]: [description]
  - **Location:** [file:line]
  - **Rule:** [which rule violated]
  - **Fix:** [specific remediation]

## Recommendations

1. [Priority recommendation]
2. [Additional improvements]
```

---

*For full verification including security, quality, and language-specific checks, say "verify agent".*
