# Python Code Quality Rules

## Imports

- Group imports in this order (separated by blank lines):
  1. Standard library
  2. Third-party packages
  3. Local modules
- Use `isort` ordering within each group.
- Never use wildcard imports: `from module import *` is forbidden.

## Error Handling

- Always use specific exception types. Never catch bare `except:`.
- Log errors with context before raising: `logger.error(f"Failed to ...: {e}")`.
- Use `logging` module — never use bare `print()` for debug output in production code.

## Functions & Methods

- Each function should do ONE thing.
- Maximum function length: 40 lines. If longer, refactor into smaller helpers.
- All parameters must have type hints. Return type must be annotated.

## Example of correct function style:

```python
import logging

logger = logging.getLogger(__name__)

def calculate_remaining_seconds(total: int, elapsed: int) -> int:
    """Calculate remaining seconds in the current session.

    Args:
        total: Total session duration in seconds.
        elapsed: Elapsed time in seconds.

    Returns:
        Remaining seconds, clamped to 0 if overdue.
    """
    return max(0, total - elapsed)
```
