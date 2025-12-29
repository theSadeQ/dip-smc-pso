# .ai_workspace/state - Project State Files

**Purpose**: Canonical location for all project state tracking files.

## Contents

### Core State Files

- **project_state.json**: Master project state tracking
  - Current phase, completed phases, task progress
  - Last updated timestamps, commit references
  - Primary source of truth for project status

- **session_state.json**: Current session state
  - Active tasks, agent state, execution context
  - Updated during multi-agent workflows

- **agents.json**: Agent configuration and status
  - Agent definitions, capabilities, checkpoints
  - Multi-agent orchestration state

### Backup Files

- **session_state_backup.json**: Session state backup from previous phase
- **session_state_backup_phase3.json**: Phase 3 session state archive

## Integration

These state files are consumed by:

- `.ai_workspace/tools/recovery/recover_project.sh` - 30-second recovery workflow
- `.ai_workspace/tools/recovery/project_state_manager.py` - State management CLI
- `.ai_workspace/tools/recovery/roadmap_tracker.py` - Roadmap progress tracking
- `.ai_workspace/tools/checkpoints/agent_checkpoint.py` - Agent checkpoint system

## Usage

```bash
# View current project state
cat .ai_workspace/state/project_state.json | jq '.current_phase'

# Update project state (via state manager)
python .ai_workspace/tools/recovery/project_state_manager.py update --phase "Research"

# Check session state
cat .ai_workspace/state/session_state.json | jq '.active_tasks'
```

## Maintenance

- State files are automatically updated by git pre-commit hooks
- Manual updates should use project_state_manager.py for consistency
- Backups are created before major phase transitions

## Migration History

- **2025-12-18**: Consolidated from `.ai_workspace/config/` and `recovery/state/` to canonical location
- **Phase 3 Migration**: Dual-path support for backward compatibility (completed)
- **Current**: Single canonical location at `.ai_workspace/state/`
