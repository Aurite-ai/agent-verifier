# Tutorial 2: First Verification

This tutorial guides you through running your first verification and saving the results. You'll learn what happens during verification and how to practice with test fixtures.

**Time:** ~10 minutes  
**Prerequisites:** Agent Verifier installed ([Tutorial 1](01-installation.md))

---

## What You'll Learn

1. Run a full verification on your project
2. Understand what happens during verification
3. Save reports to files
4. Practice with test fixtures

---

## Part 1: Run Your First Verification

### Step 1: Open your project

Navigate to any AI agent project in your coding agent. If you don't have one handy, you can use the test fixtures (see [Part 4](#part-4-practice-with-test-fixtures)).

### Step 2: Trigger verification

In your coding agent, say:

```
"verify agent"
```

Alternative trigger phrases that also work:
- `"verify my agent"`
- `"audit agent"`
- `"full verification"`

### Step 3: Watch the verification process

The agent will work through several stages:

```
1. Context Discovery
   ├── Detecting project language...
   ├── Checking for agent framework...
   └── Looking for Kahuna integration...

2. Running Security Checks...
3. Running Pattern Checks...
4. Running Quality Checks...
5. Running Language-Specific Checks...
6. Consolidating Report...
```

### Step 4: Review the summary

At the end, you'll see a summary like:

```
✅ 12 checks passed | ⚠️ 3 warnings | ❌ 1 issue
```

---

## Part 2: Understanding the Verification Process

Agent Verifier runs four skill checks in sequence:

### 1. Security Checks (`verify-security`)

Scans for:
- Hardcoded API keys and secrets
- Unpinned dependencies
- Missing input validation
- Error messages that expose internals

### 2. Pattern Checks (`verify-patterns`)

Validates agent-specific patterns:
- **Loop safety:** Do loops have termination conditions?
- **Retry limits:** Are retry mechanisms bounded?
- **Tool consistency:** Do prompts reference tools that exist?
- **Context size:** Is the system prompt within token limits?

### 3. Quality Checks (`verify-quality`)

Reviews code quality:
- Naming conventions
- Code organization
- Documentation coverage
- Magic numbers/strings

### 4. Language Checks (`verify-language`)

Applies language-specific rules:
- **Python:** Type hints, docstrings, requirements pinning
- **TypeScript:** Strict mode, no `any` types, async error handling
- **Go:** Error handling, context propagation

---

## Part 3: Saving Reports

After verification completes, the agent will ask:

> Would you like to save this verification report to a file?

### Saving to default location

Say **"yes"** to save. The report is saved to:

```
reports/verification/YYYY-MM-DD_HH-MM-SS.md
```

Example: `reports/verification/2026-03-27_14-30-45.md`

### Custom save location

You can specify a custom path:

```
"Save the report to docs/audit-report.md"
```

### Report contents

The saved report includes:
- Project metadata (name, date, language, framework)
- Summary counts (pass/warn/issue)
- Category breakdown table
- Detailed findings with file locations
- Prioritized recommendations

---

## Part 4: Practice with Test Fixtures

Agent Verifier includes test fixtures to help you understand what it detects.

### Navigate to fixtures

```bash
cd tests/fixtures
```

### Run verification on all fixtures

In your coding agent:

```
"verify agent"
```

### Expected results

The fixtures demonstrate various patterns:

| Fixture | What it tests | Expected result |
|---------|---------------|-----------------|
| `infinite_loop/` | Loop termination detection | ⚠️ Warnings for unbounded loops |
| `retry_limits/` | Retry limit enforcement | ❌ Issues for missing limits |
| `tool_registry/` | Tool consistency | ❌ Issue for hallucinated tool |
| `prompt_size/` | Context size awareness | ✅ Pass (within limits) |
| `langgraph_cycles/` | Graph cycle analysis | ❌ Issue for infinite cycle |

### Test individual categories

For focused testing:

```bash
cd tests/fixtures/retry_limits
```

Then say:
```
"verify agent patterns"
```

This runs only the pattern checks on the retry limit fixtures.

---

## Part 5: Quick Reference

### Trigger phrases

| Phrase | What it runs |
|--------|--------------|
| `"verify agent"` | Full verification (all 4 checks) |
| `"verify my agent"` | Full verification |
| `"audit agent"` | Full verification |
| `"verify agent security"` | Security checks only |
| `"verify agent patterns"` | Pattern checks only |
| `"verify agent quality"` | Quality checks only |
| `"verify agent language"` | Language checks only |

### What gets detected automatically

- **Language:** Python, TypeScript/JavaScript, Go
- **Framework:** LangGraph, CrewAI, AutoGen, LangChain, or custom
- **Kahuna:** Organizational rules if `.kahuna/` directory exists

---

## Common Questions

### How long does verification take?

Depends on project size:
- Small projects (< 20 files): 30 seconds - 1 minute
- Medium projects (20-100 files): 1-3 minutes
- Large projects (100+ files): 3-5 minutes

### Can I run verification on specific files?

Not directly, but you can:
1. Move to a subdirectory and run verification there
2. Use focused checks for faster feedback

### What if verification finds nothing?

If you see `✅ All checks passed`, your code follows best practices. The report will still contain the passing checks for documentation.

### Does verification modify my code?

No. Agent Verifier only reads and analyzes—it never modifies files. All suggested fixes are recommendations for you to implement.

---

## Next Steps

Now that you've run your first verification, learn how to interpret the results:

[Tutorial 3: Understanding Reports →](03-understanding-reports.md)
