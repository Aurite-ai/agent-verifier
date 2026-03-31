# Getting Started with Agent Verifier

Agent Verifier catches security issues, enforces coding standards, and validates AI agent patterns before your code ships. It works with Claude Code, Roo Code, Cursor, Windsurf, and [30+ other coding agents](https://github.com/vercel-labs/skills#supported-agents).

All analysis happens locally—your code never leaves your machine.

---

## Quick Start

Get from zero to first verification in under 2 minutes.

### 1. Install the skill

**Install to specific agents:**
```bash
# Single agent
npx skills add aurite-ai/agent-verifier -a claude-code

# Multiple agents
npx skills add aurite-ai/agent-verifier -a claude-code -a roo -a <your_favorite_coding_agent>
```

**Or install to all detected agents:**
```bash
npx skills add aurite-ai/agent-verifier --all
```

> **💡 Tip:** Add `-g` for global installation across all projects: `npx skills add aurite-ai/agent-verifier -g --all`

### 2. Run verification

In your coding agent, say:

```
"verify agent"
```

### 3. Review the report

The agent generates a markdown report showing:
- ✅ **Passing checks** — What's working well
- ⚠️ **Warnings** — Potential issues to review
- ❌ **Issues** — Problems that need fixing

That's it! For detailed guidance, continue to the [tutorials](tutorials/).

### 4. Add custom rules with Kahuna MCP (optional)

For project-specific or organizational policies, Agent Verifier integrates with [Kahuna MCP](https://github.com/aurite-ai/kahuna):

1. Set up Kahuna in your project with a `.kahuna/` directory
2. Add custom rules to `.kahuna/context-guide.md`
3. Agent Verifier automatically loads these rules during verification

---

## Enterprise Features

Looking for team and organizational capabilities?

- **Centralized policy management** — Define and enforce rules across all projects
- **Shared context pools** — Consistent verification context for your organization
- **Administrative controls** — Manage skills and policies at scale
- **CI/CD integration support** — Run verification in your pipelines
- **Custom integrations** — Tailored solutions for your workflow

Contact [info@aurite.ai](mailto:info@aurite.ai) to learn more about enterprise options.

---

## What Gets Checked?

Agent Verifier runs four types of checks:

| Category | What it checks | Command |
|----------|----------------|---------|
| **Security** | Hardcoded secrets, dependency vulnerabilities, input validation | `"verify agent security"` |
| **Patterns** | Loop safety, retry limits, tool consistency, context size | `"verify agent patterns"` |
| **Quality** | Naming conventions, code organization, documentation | `"verify agent quality"` |
| **Language** | Python type hints, TypeScript strict mode, Go error handling | `"verify agent language"` |

The full suite (`"verify agent"`) runs all four. Use individual commands for faster, focused checks.

---

## Supported Languages & Frameworks

**Languages:** Python, TypeScript/JavaScript, Go

**Agent frameworks:** LangGraph, CrewAI, AutoGen, LangChain, or custom agents using direct SDK calls

Agent Verifier automatically detects your project's language and framework.

---

## Next Steps

- **[Tutorial 1: Installation](tutorials/01-installation.md)** — Detailed installation options and troubleshooting
- **[Tutorial 2: First Verification](tutorials/02-first-verification.md)** — Run your first verification with guided walkthrough
- **[Tutorial 3: Understanding Reports](tutorials/03-understanding-reports.md)** — Learn to interpret and prioritize findings
- **[Tutorial 4: Focused Checks](tutorials/04-focused-checks.md)** — Use individual skills for targeted verification

---

## Need Help?

- **Questions?** [Open an issue](https://github.com/aurite-ai/agent-verifier/issues)
- **Found a bug?** [Open a PR](https://github.com/aurite-ai/agent-verifier/pulls)
- **Enterprise support?** Contact [info@aurite.ai](mailto:info@aurite.ai)
