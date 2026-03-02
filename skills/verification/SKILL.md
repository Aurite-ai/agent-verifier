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

For each check, determine:
- ✅ **Pass** - Code complies with the rule
- ⚠️ **Warning** - Potential concern worth reviewing
- ❌ **Issue** - Clear violation that needs fixing

### Step 4: Generate Report

Output a structured verification report:

```markdown
# Verification Report

**Project:** [project name or path]
**Date:** [current date]
**Mode:** [Kahuna-enhanced | Standalone]
**Files analyzed:** [list of files]

## Summary

✅ X checks passed | ⚠️ Y warnings | ❌ Z issues

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

1. [Priority recommendation based on findings]
2. [Additional improvements]
```

### Step 5: Export Report (Optional)

After presenting the report, ask the user:

> Would you like to save this verification report to a file?

If confirmed, save to:
```
reports/verification/YYYY-MM-DD_HH-MM-SS.md
```

## Notes

- **Privacy first:** All code analysis happens locally. Nothing is sent to external services.
- **Kahuna enhances, not requires:** The skill works standalone with built-in rules. Kahuna adds organization-specific knowledge.
- **Be specific:** Include file names and line numbers when reporting issues.
- **Explain the "why":** Help developers understand why each rule matters.
- **Honor existing configs:** Respect project's existing lint rules, `.editorconfig`, etc.
