# Aurite Agent Verifier

A coding agent skill that verifies code against organizational policies, security requirements, and framework best practices.

## Installation

Install using the [skills CLI](https://github.com/vercel-labs/skills):

### From NPM Registry (Recommended)

```bash
# Install to all detected agents (Claude Code, Roo Code, Cursor, etc.)
npx skills add aurite-ai/agent-verifier

# Install to specific agents
npx skills add aurite-ai/agent-verifier -a claude-code -a roo

# Install globally (available in all projects)
npx skills add aurite-ai/agent-verifier -g
```

### From GitHub Repository

Install directly from a GitHub repo (public or private with access):

```bash
# From public GitHub repo
npx skills add github:aurite-ai/agent-verifier

# From a specific branch
npx skills add github:aurite-ai/agent-verifier#main

# From a specific tag/release
npx skills add github:aurite-ai/agent-verifier#v1.0.0

# From private repo (requires GitHub authentication)
npx skills add github:your-org/your-private-skill
```

### From Local Source

Install from a local directory during development:

```bash
# Install from local path (relative or absolute)
npx skills add ./path/to/agent-verifier

# Install from current directory
cd agent-verifier
npx skills add .

# Install with link (for development - changes reflect immediately)
npx skills link .
```

### Manual Installation

For agents that don't support the skills CLI, copy the skill files directly:

```bash
# For Roo Code
cp -r skills/verification ~/.roo/skills/

# For Claude Code
cp -r skills/verification ~/.claude/skills/

# For other agents, check their documentation for the skills directory location
```

## Updating Installed Skills

### From NPM Registry

Re-run the install command to get the latest published version:

```bash
# Update to latest version
npx skills add aurite-ai/agent-verifier -a claude-code

# Or specify a version
npx skills add aurite-ai/agent-verifier@1.2.0 -a claude-code
```

### From GitHub Repository

Re-run with the same source to pull latest changes:

```bash
# Update from default branch
npx skills add github:aurite-ai/agent-verifier -a claude-code

# Update from specific branch
npx skills add github:aurite-ai/agent-verifier#main -a claude-code

# Update to specific tag/release
npx skills add github:aurite-ai/agent-verifier#v1.2.0 -a claude-code
```

### From Local Source (Symlink)

If installed with symlink, changes reflect automatically. No action needed.

Check if you're using symlink:
```bash
# Check the skills-lock.json in your project
cat skills-lock.json  # Look for "method": "symlink"

# Or check the installed skill directly
ls -la .agents/skills/verification  # Should show -> pointing to source
```

### From Local Source (Copy)

Re-run the install command to update:

```bash
# Reinstall from source
npx skills add /path/to/agent-verifier -a claude-code

# Or force reinstall
npx skills add /path/to/agent-verifier -a claude-code --force
```

### Remove and Reinstall

```bash
# Remove the skill
npx skills remove verification

# Reinstall from any source
npx skills add aurite-ai/agent-verifier -a claude-code
```

### Manual Update

```bash
# Copy updated files directly
cp -r /path/to/agent-verifier/skills/verification ~/.claude/skills/
```

## Usage

Once installed, trigger the skill by asking your coding agent to:

- "verify my code"
- "review this implementation"
- "check compliance"
- "audit my agent"
- "validate against best practices"

## Features

### Dual-Mode Operation

**Standalone Mode** (default):
- Automatically detects project language and framework
- Applies built-in best practices for code quality and security
- Honors existing lint configs (ESLint, Biome, etc.)

**Kahuna-Enhanced Mode** (when [Kahuna](https://github.com/aurite-ai/kahuna) is installed):
- Loads organization-specific rules from knowledge base
- Uses `kahuna_ask` for deeper context queries
- Applies framework patterns surfaced by `kahuna_prepare_context`

### Verification Checks

The skill performs comprehensive verification across multiple categories:

#### 1. Code Quality

| Check | Description | Severity |
|-------|-------------|----------|
| Naming conventions | Clear, descriptive, consistent naming | ⚠️ Warning |
| Code organization | Appropriate structure and modularity | ⚠️ Warning |
| Error handling | Proper try/catch, error propagation | ❌ Issue |
| Magic values | No unexplained numbers/strings | ⚠️ Warning |
| Documentation | Comments for complex logic | ⚠️ Warning |

#### 2. Security

| Check | Description | Severity |
|-------|-------------|----------|
| Hardcoded secrets | No API keys, passwords in source | ❌ Issue |
| Input validation | Validate external data | ❌ Issue |
| Error exposure | No stack traces in production | ⚠️ Warning |
| Secure defaults | Safe default configurations | ⚠️ Warning |
| Dependency vulnerabilities | Known CVEs in dependencies | ❌ Issue |

#### 3. Language-Specific

**Python:**
| Check | Description |
|-------|-------------|
| Type hints | Public functions should have type annotations |
| Docstrings | Modules, classes, functions should be documented |
| Requirements pinning | Dependencies should specify versions |

**TypeScript/JavaScript:**
| Check | Description |
|-------|-------------|
| Type safety | Prefer strict mode, avoid `any` |
| Async handling | Proper error handling for promises |
| Dependency security | No outdated/vulnerable packages |

**Go:**
| Check | Description |
|-------|-------------|
| Error handling | No ignored errors (`_ = err`) |
| Context propagation | Pass context through call chains |

#### 4. AI Agent Patterns

**Loop Safety:**
| Pattern | Language | Severity |
|---------|----------|----------|
| `while True:` without `break` | Python | ⚠️ Warning |
| `while (true)` without break | TS/JS | ⚠️ Warning |
| `for { }` without break/return | Go | ⚠️ Warning |
| Recursive calls without depth limit | All | ⚠️ Warning |

**Retry Limits:**
| Pattern | Required Parameter | Severity |
|---------|-------------------|----------|
| `@retry` (tenacity) | `stop=stop_after_attempt(n)` | ❌ Issue |
| `@backoff.on_exception` | `max_tries=n` | ❌ Issue |
| `retry` (async-retry) | `retries: n` | ❌ Issue |
| `p-retry` | `retries: n` | ❌ Issue |

**Tool Registry:**
| Check | Description | Severity |
|-------|-------------|----------|
| Hallucinated tools | Tool references not in registry | ❌ Issue |
| Undocumented tools | Tools not listed in prompts | ⚠️ Warning |

**Context Management:**
| Content Type | Warning | Issue |
|--------------|---------|-------|
| System prompt | > 4,000 tokens (~16KB) | > 8,000 tokens (~32KB) |
| Single tool description | > 500 tokens (~2KB) | > 1,000 tokens (~4KB) |
| Total tool descriptions | > 2,000 tokens (~8KB) | > 4,000 tokens (~16KB) |

#### 5. Framework Detection

Automatically detects and applies framework-specific checks:

| Framework | Detection | Special Checks |
|-----------|-----------|----------------|
| LangGraph | `langgraph` in imports | State schema, node connectivity |
| CrewAI | `crewai` in imports | Agent roles, task dependencies |
| AutoGen | `autogen` in imports | Agent configuration |
| LangChain | `langchain` in imports | Chain composition, memory config |
| Custom | Direct SDK usage | General agent patterns |

## Testing the Skill

Test fixtures are provided in `tests/fixtures/` to validate the agent pattern detection:

```bash
# Navigate to a fixture directory and ask your agent to verify it
cd tests/fixtures/infinite_loop
# Then ask: "verify this code for agent patterns"

# Or verify all fixtures at once
cd tests/fixtures
# Then ask: "verify these test fixtures and report findings"
```

See [`tests/fixtures/README.md`](tests/fixtures/README.md) for expected results.

## Report Format

The skill generates a structured markdown report:

```markdown
# Verification Report

**Project:** my-project
**Date:** 2026-03-02
**Mode:** Standalone
**Files analyzed:** 12

## Summary

✅ 8 checks passed | ⚠️ 3 warnings | ❌ 1 issue

## Findings

### ✅ Passing
- Naming conventions: Consistent camelCase used throughout

### ⚠️ Warnings
- Missing type hints: `utils.py:45`
  - **Suggestion:** Add type hints to `process_data()` function

### ❌ Issues
- Hardcoded API key: `config.py:12`
  - **Rule:** No secrets in source code
  - **Fix:** Move to environment variable
```

## Supported Agents

This skill works with any agent supported by the [skills CLI](https://github.com/vercel-labs/skills), including:

- Claude Code
- Roo Code  
- Cursor
- Codex
- OpenCode
- Windsurf
- And [30+ more](https://github.com/vercel-labs/skills#supported-agents)

## Privacy

All code analysis happens locally. Your code never leaves your machine.

## Related Skills

- Coming soon: `aurite-ai/agent-documenter` - Documentation search
- Coming soon: `aurite-ai/agent-architect` - Architecture planning
- Coming soon: `aurite-ai/agent-implementer` - Plan execution

## License

MIT License - see [LICENSE](LICENSE)
