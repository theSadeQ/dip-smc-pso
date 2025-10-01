#==========================================================================================\
#================================ .dev_tools/session_manager.py ===========================\
#==========================================================================================\

"""Session continuity manager for zero-effort account switching.

This module provides utilities for maintaining session state across Claude Code account
switches when token limits are reached. It enables completely automatic context handoff
without requiring manual prompt writing.

Usage:
    # Check if there's a recent session to continue
    if has_recent_session():
        state = load_session()
        print(f"Continuing: {state['context']['current_task']}")

    # Update session state during work
    update_session_context(current_task="Implementing feature X", phase="testing")
    add_completed_todo("Write unit tests")
    add_decision("Use pytest for testing framework")

    # Prepare for token limit
    mark_token_limit_approaching()
    finalize_session("Completed feature X implementation")
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any


# Configuration
SESSION_FILE = Path(__file__).parent / "session_state.json"
AUTO_LOAD_THRESHOLD_HOURS = 24
SESSION_AUTO_SAVE_ENABLED = False  # Set to True to enable auto-save session functionality


def load_session() -> Optional[Dict[str, Any]]:
    """Load the current session state from disk.

    Returns:
        Dictionary containing session state, or None if file doesn't exist
        or is malformed.

    Example:
        >>> state = load_session()
        >>> if state:
        ...     print(f"Task: {state['context']['current_task']}")
    """
    try:
        if not SESSION_FILE.exists():
            return None

        with open(SESSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, KeyError) as e:
        print(f"Warning: Could not load session state: {e}")
        return None


def save_session(state: Dict[str, Any]) -> bool:
    """Save session state to disk.

    Args:
        state: Complete session state dictionary

    Returns:
        True if save was successful, False otherwise

    Example:
        >>> state = load_session() or get_default_state()
        >>> state['context']['current_task'] = "New task"
        >>> save_session(state)
    """
    # Check if auto-save is enabled
    if not SESSION_AUTO_SAVE_ENABLED:
        return False

    try:
        # Update timestamp
        state['last_updated'] = datetime.now().isoformat(timespec='seconds')

        # Ensure parent directory exists
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Write atomically using temporary file
        temp_file = SESSION_FILE.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp_file.replace(SESSION_FILE)
        return True

    except (IOError, OSError) as e:
        print(f"Error: Could not save session state: {e}")
        return False


def has_recent_session(threshold_hours: int = AUTO_LOAD_THRESHOLD_HOURS) -> bool:
    """Check if there's a recent session that should be auto-loaded.

    Args:
        threshold_hours: Maximum age in hours for auto-loading (default: 24)

    Returns:
        True if session exists and is within threshold, False otherwise

    Example:
        >>> if has_recent_session():
        ...     print("Continuing from previous session...")
        ... else:
        ...     print("Starting fresh session...")
    """
    # If auto-save is disabled, don't auto-load sessions
    if not SESSION_AUTO_SAVE_ENABLED:
        return False

    state = load_session()
    if not state:
        return False

    try:
        last_updated = datetime.fromisoformat(state['last_updated'])
        age = datetime.now() - last_updated
        return age < timedelta(hours=threshold_hours)
    except (ValueError, KeyError):
        return False


def get_session_summary() -> str:
    """Get a human-readable summary of the current session.

    Returns:
        Formatted string summarizing session state, or error message

    Example:
        >>> print(get_session_summary())
        Continuing from previous session (2 hours ago):
        Task: Implementing automated backup system
        Phase: completed
        Last commit: c8c9c64

        Completed: 5 items
        In progress: 1 item
        Pending: 2 items
    """
    state = load_session()
    if not state:
        return "No active session found."

    try:
        last_updated = datetime.fromisoformat(state['last_updated'])
        age = datetime.now() - last_updated

        if age < timedelta(hours=1):
            age_str = f"{int(age.total_seconds() / 60)} minutes ago"
        elif age < timedelta(days=1):
            age_str = f"{int(age.total_seconds() / 3600)} hours ago"
        else:
            age_str = f"{int(age.days)} days ago"

        context = state.get('context', {})
        todos = state.get('todos', {})

        summary = f"""Continuing from previous session ({age_str}):
Task: {context.get('current_task', 'Unknown')}
Phase: {context.get('phase', 'Unknown')}
Last commit: {context.get('last_commit', 'Unknown')}

Completed: {len(todos.get('completed', []))} items
In progress: {len(todos.get('in_progress', []))} items
Pending: {len(todos.get('pending', []))} items"""

        # Add next actions if present
        next_actions = state.get('next_actions', [])
        if next_actions:
            summary += f"\n\nNext actions:\n"
            for i, action in enumerate(next_actions[:3], 1):
                summary += f"{i}. {action}\n"

        return summary

    except (ValueError, KeyError) as e:
        return f"Error reading session: {e}"


def update_session_context(**kwargs) -> bool:
    """Update specific fields in the session context.

    Args:
        **kwargs: Key-value pairs to update in context

    Returns:
        True if update was successful, False otherwise

    Example:
        >>> update_session_context(
        ...     current_task="Implementing feature X",
        ...     phase="testing",
        ...     last_commit="abc1234"
        ... )
    """
    state = load_session()
    if not state:
        state = get_default_state()

    if 'context' not in state:
        state['context'] = {}

    state['context'].update(kwargs)
    return save_session(state)


def add_completed_todo(todo: str) -> bool:
    """Mark a todo item as completed.

    Args:
        todo: Description of completed todo

    Returns:
        True if update was successful

    Example:
        >>> add_completed_todo("Create PowerShell backup script")
    """
    state = load_session()
    if not state:
        state = get_default_state()

    if 'todos' not in state:
        state['todos'] = {'completed': [], 'in_progress': [], 'pending': []}

    # Remove from in_progress if present
    if todo in state['todos'].get('in_progress', []):
        state['todos']['in_progress'].remove(todo)

    # Add to completed
    if todo not in state['todos'].get('completed', []):
        state['todos']['completed'].append(todo)

    return save_session(state)


def add_decision(decision: str) -> bool:
    """Record an important decision made during the session.

    Args:
        decision: Description of the decision

    Returns:
        True if update was successful

    Example:
        >>> add_decision("Task Scheduler frequency: 1 minute")
    """
    state = load_session()
    if not state:
        state = get_default_state()

    if 'decisions' not in state:
        state['decisions'] = []

    if decision not in state['decisions']:
        state['decisions'].append(decision)

    return save_session(state)


def add_next_action(action: str) -> bool:
    """Add an action that should be taken next.

    Args:
        action: Description of the next action

    Returns:
        True if update was successful

    Example:
        >>> add_next_action("Register Task Scheduler job")
    """
    state = load_session()
    if not state:
        state = get_default_state()

    if 'next_actions' not in state:
        state['next_actions'] = []

    if action not in state['next_actions']:
        state['next_actions'].append(action)

    return save_session(state)


def mark_token_limit_approaching() -> bool:
    """Mark that token limit is approaching (triggers final state save).

    Returns:
        True if update was successful

    Example:
        >>> mark_token_limit_approaching()
    """
    state = load_session()
    if not state:
        return False

    state['token_limit_approaching'] = True
    state['status'] = 'token_limit_handoff'
    return save_session(state)


def finalize_session(summary: str) -> bool:
    """Finalize session before account switch.

    Args:
        summary: Brief summary of what was accomplished

    Returns:
        True if finalization was successful

    Example:
        >>> finalize_session("Completed automated backup system implementation")
    """
    state = load_session()
    if not state:
        return False

    state['status'] = 'finalized'
    state['finalization_summary'] = summary
    state['finalization_time'] = datetime.now().isoformat(timespec='seconds')

    # Increment session count for account switch tracking
    if 'metadata' in state:
        state['metadata']['session_count'] = state['metadata'].get('session_count', 0) + 1
        state['metadata']['last_account_switch'] = datetime.now().isoformat(timespec='seconds')

    return save_session(state)


def get_default_state() -> Dict[str, Any]:
    """Get a default session state structure.

    Returns:
        Dictionary with default session state structure

    Example:
        >>> state = get_default_state()
        >>> state['context']['current_task'] = "My task"
        >>> save_session(state)
    """
    now = datetime.now().isoformat(timespec='seconds')

    return {
        "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "last_updated": now,
        "account": "unknown",
        "token_limit_approaching": False,
        "status": "active",
        "context": {
            "current_task": "Not set",
            "phase": "initialization",
            "last_commit": "Unknown",
            "branch": "main",
            "working_directory": str(Path.cwd())
        },
        "todos": {
            "completed": [],
            "in_progress": [],
            "pending": []
        },
        "decisions": [],
        "next_actions": [],
        "files_modified": [],
        "important_context": {},
        "metadata": {
            "schema_version": "1.0",
            "created": now,
            "last_account_switch": None,
            "session_count": 1
        }
    }


def demo():
    """Demonstrate session manager functionality."""
    print("=== Session Manager Demo ===\n")

    # Check for existing session
    if has_recent_session():
        print(get_session_summary())
    else:
        print("No recent session found. Creating new session...\n")
        state = get_default_state()
        state['context']['current_task'] = "Demo task"
        save_session(state)
        print("Created new session.")

    print("\n=== Adding updates ===")
    update_session_context(current_task="Testing session manager", phase="demo")
    add_completed_todo("Create session manager")
    add_decision("Use JSON for session state")
    add_next_action("Test in production")

    print("\n=== Updated session ===")
    print(get_session_summary())


if __name__ == "__main__":
    demo()
