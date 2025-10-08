# Example from: docs\CLAUDE.md
# Index: 1
# Runnable: True
# Hash: c9e1fcc9

from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / ".dev_tools"))

from session_manager import has_recent_session, get_session_summary, load_session

if has_recent_session():
    print(get_session_summary())
    state = load_session()
    # Resume work based on state['context'] and state['next_actions']