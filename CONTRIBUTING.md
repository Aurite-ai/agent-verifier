# Contributing to Agent Verifier

Thanks for your interest in improving Agent Verifier! This project lives or dies on community contributions, and we welcome bug reports, feature requests, new checks, and code fixes alike.

## Ways to contribute

- **Found a bug?** [Open an issue](https://github.com/Aurite-ai/agent-verifier/issues/new) with a clear description, the language/framework involved, and, if possible, a minimal reproduction.
- - **Want a new check?** [Open a feature request](https://github.com/Aurite-ai/agent-verifier/issues/new) describing the pattern you'd like caught, why it matters, and whether it's pattern-matched (mechanical) or heuristic (judgment-based) — see the README's "Check Reliability" section for that distinction.
  - - **Want to contribute code?** Open a pull request. Small, focused PRs are easier to review and land faster than large ones.
   
    - ## Development setup
   
    - 1. Fork and clone the repository.
      2. 2. Skills live under `skills/` — each verification domain (`verify-security`, `verify-patterns`, `verify-quality`, `verify-language`) is its own skill, with `verification` as the orchestrator.
         3. 3. Test fixtures live under `tests/fixtures/`. When adding or changing a check, add a fixture that demonstrates it firing (and, ideally, one that demonstrates it correctly staying silent).
            4. 4. Run the skill against the fixtures locally before opening a PR, the same way an end user would trigger it ("verify agent" or a focused variant like "verify agent security").
              
               5. ## Pull request guidelines
              
               6. - Reference the issue your PR addresses, if one exists.
                  - - Keep the change scoped to one concern — a new check, a bug fix, or a docs update, not several at once.
                    - - Update the README's check tables (Code Quality / Security / Language-Specific / AI Agent Patterns) if you're adding or changing a check, so the documentation stays accurate.
                      - - New pattern-matched checks should note their reliability tier ([P] pattern-matched vs [H] heuristic) consistent with the existing convention.
                       
                        - ## Reporting security issues
                       
                        - If you find a security issue in Agent Verifier itself (as opposed to something it should catch in other people's code), please avoid filing a public issue and instead reach out directly at info@aurite.ai.
                       
                        - ## Code of conduct
                       
                        - This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you're expected to uphold it.
                        - 
