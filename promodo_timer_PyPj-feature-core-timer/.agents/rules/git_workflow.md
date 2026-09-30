# Git Workflow Rules

## Branching

- `main` branch is protected. Never commit directly to `main`.
- Branch naming format:
  - New features: `feature/<short-description>` (e.g., `feature/notification-sound`)
  - Bug fixes: `fix/<short-description>` (e.g., `fix/timer-not-stopping`)
  - Maintenance: `chore/<short-description>` (e.g., `chore/update-deps`)

## Commit Messages

Follow **Conventional Commits** format: `<type>: <short summary>`

| Type | When to use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `chore:` | Dependency updates, tooling |
| `docs:` | Documentation only |
| `test:` | Adding or updating tests |
| `refactor:` | Code change that is not a fix or feature |
| `style:` | Formatting, whitespace (no logic change) |

**Example**: `feat: add desktop notification on session end`

## Before Every Push

1. Run `pytest tests/` — all tests must pass.
2. Check for leftover debug `print()` statements.
3. Ensure no secrets or API keys are committed.

## AI Agent Instructions

When helping with Git tasks:
- Always suggest creating a new branch before implementing a feature or fix.
- Propose commit messages following the Conventional Commits format above.
- Remind developers to run tests before pushing.
