# Aurite Agent Verifier

A coding agent skill that verifies code against organizational policies, security requirements, and framework best practices.

## Installation

Install using the [skills CLI](https://github.com/vercel-labs/skills):

```bash
# Install to all detected agents (Claude Code, Roo Code, Cursor, etc.)
npx skills add aurite-ai/agent-verifier

# Install to specific agents
npx skills add aurite-ai/agent-verifier -a claude-code -a roo

# Install globally (available in all projects)
npx skills add aurite-ai/agent-verifier -g
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

### Built-in Checks

**General Code Quality:**
- Clear naming conventions
- Appropriate code organization
- Error handling patterns
- No magic numbers/strings

**Security Basics:**
- No hardcoded secrets or API keys
- Input validation
- Secure error handling
- Safe defaults

**Language-Specific:**
- TypeScript/JavaScript: Type safety, async patterns, dependency security
- Python: Type hints, docstrings, virtual environments
- Go: Error handling, context propagation
- And more...

**AI Agent-Specific:**
- State schema validation
- Tool error handling
- Prompt injection considerations

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
