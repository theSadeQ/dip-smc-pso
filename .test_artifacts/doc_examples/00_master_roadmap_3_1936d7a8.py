# Example from: docs\plans\citation_system\00_master_roadmap.md
# Index: 3
# Runnable: True
# Hash: 1936d7a8

# Mitigation: Session state auto-save (already in CLAUDE.md)
from .dev_tools.session_manager import update_session_context, finalize_session

# Every major milestone
update_session_context(
    current_task="Phase 2: Researching claims 250-300",
    phase="ai_research",
    last_checkpoint="research_checkpoint_250.json"
)

# When approaching limit
finalize_session("Phase 2: 300/500 claims researched")
# Next session: Auto-resume from checkpoint