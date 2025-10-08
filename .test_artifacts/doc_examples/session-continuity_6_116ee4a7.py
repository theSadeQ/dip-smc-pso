# Example from: docs\session-continuity.md
# Index: 6
# Runnable: True
# Hash: 116ee4a7

from session_manager import has_recent_session, get_session_summary

# Check if there's a recent session to continue
if has_recent_session(threshold_hours=24):
    print(get_session_summary())