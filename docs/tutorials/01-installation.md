# Tutorial 1: Installation

This tutorial walks you through installing Agent Verifier on your system. By the end, you'll have the verification skill ready to use in your coding agent.

**Time:** ~5 minutes  
**Prerequisites:** Node.js v18+, a supported coding agent

---

## Choose Your Installation Method

| Method | Best for | Difficulty |
|--------|----------|------------|
| [NPM Registry](#option-1-npm-registry-recommended) | Most users | Easy |
| [GitHub Repository](#option-2-github-repository) | Custom branches, private forks | Easy |
| [Local Source](#option-3-local-source) | Development, testing changes | Medium |
| [Manual Copy](#option-4-manual-installation) | Agents without CLI support | Medium |

---

## Option 1: NPM Registry (Recommended)

The simplest way to install—pulls the latest stable release.

### Step 1: Check available skills

```bash
npx skills add aurite-ai/agent-verifier --list
```

You'll see:
```
Available skills in aurite-ai/agent-verifier:
  - verification (full verification suite)
  - verify-security
  - verify-patterns
  - verify-quality
  - verify-language
```

### Step 2: Install to your coding agents

**Install to all detected agents:**
```bash
npx skills add aurite-ai/agent-verifier --all
```

**Or install to specific agents:**
```bash
# Single agent
npx skills add aurite-ai/agent-verifier -a claude-code

# Multiple agents
npx skills add aurite-ai/agent-verifier -a claude-code -a roo
```

**Or install specific skills only:**
```bash
npx skills add aurite-ai/agent-verifier --skill verification verify-security
```

### Step 3: Verify installation

Open your coding agent and say:
```
"verify agent"
```

If installed correctly, the agent will begin analyzing your project.

---

## Option 2: GitHub Repository

Install directly from GitHub—useful for specific branches, tags, or private forks.

### From the main branch

```bash
npx skills add github:aurite-ai/agent-verifier --all
```

### From a specific branch

```bash
npx skills add github:aurite-ai/agent-verifier#main --all
```

### From a specific release tag

```bash
npx skills add github:aurite-ai/agent-verifier#v1.0.0 --all
```

### From a private fork

```bash
# Requires GitHub authentication
npx skills add github:your-org/your-private-fork --all
```

---

## Option 3: Local Source

Install from a local directory—ideal for development or testing modifications.

### Clone and install

```bash
# Clone the repository
git clone https://github.com/aurite-ai/agent-verifier.git
cd agent-verifier

# Install to your agents
npx skills add . --all
```

### Development mode (symlink)

For active development, use symlink so changes reflect immediately:

```bash
npx skills link .
```

Changes to skill files take effect without reinstalling.

### Verify symlink is active

```bash
# Check skills-lock.json in your project
cat skills-lock.json  # Look for "method": "symlink"

# Or check the installed skill
ls -la .agents/skills/verification  # Shows -> pointing to source
```

---

## Option 4: Manual Installation

For agents that don't support the skills CLI, copy files directly.

### For Roo Code

```bash
cp -r skills/* ~/.roo/skills/
```

### For Claude Code

```bash
cp -r skills/* ~/.claude/skills/
```

### For other agents

Check your agent's documentation for the skills directory location, then copy the `skills/` folder contents there.

---

## Global vs Local Installation

| Type | Flag | Scope | Use case |
|------|------|-------|----------|
| **Local** | (default) | Current project only | Per-project verification |
| **Global** | `-g` | All projects | Organization-wide policies |

### Install globally

```bash
npx skills add aurite-ai/agent-verifier -g --all
```

Global installation makes the skill available in all projects without per-project setup.

---

## Troubleshooting

### "Command not found: npx"

**Cause:** Node.js not installed or not in PATH

**Fix:** Install Node.js v18+ from [nodejs.org](https://nodejs.org)

### "No agents detected"

**Cause:** The skills CLI couldn't find supported coding agents

**Fix:** Specify the agent explicitly:
```bash
npx skills add aurite-ai/agent-verifier -a claude-code
```

### "Permission denied"

**Cause:** File system permissions on the skills directory

**Fix:** Check permissions on your agent's skills directory:
```bash
ls -la ~/.claude/skills/  # or ~/.roo/skills/
```

### Skill not recognized by agent

**Cause:** Installation succeeded but agent can't find the skill

**Fix:**
1. Restart your coding agent
2. Check the skill directory exists:
   ```bash
   ls ~/.claude/skills/verification/  # or your agent's skills dir
   ```
3. Verify `SKILL.md` exists in the directory

### Wrong version installed

**Cause:** Cached version or incorrect source

**Fix:** Force reinstall:
```bash
npx skills add aurite-ai/agent-verifier --all --force
```

---

## Next Steps

Installation complete! Continue to [Tutorial 2: First Verification →](02-first-verification.md)
