# .ai_workspace/tools/recovery - 30-Second Recovery System

**Purpose**: Comprehensive recovery workflows for token limits, crashes, and multi-month gaps.

## Core Tools

### recover_project.sh
**Main entry point for 30-second recovery**

**What it does**:
1. Shows project state (current phase, completed tasks, roadmap progress)
2. Displays recent Git commits (last 5)
3. Shows current Git status (branch, uncommitted changes)
4. Lists recent checkpoint files (if any)

**Usage**:
```bash
bash .ai_workspace/tools/recovery/recover_project.sh

# Or via alias (if installed)
/recover
```

**Output Sections**:
- [1] PROJECT STATE: Phase, tasks, completion status
- [2] RECENT WORK: Last 5 commits with hashes
- [3] CURRENT GIT STATUS: Branch, remote, uncommitted files
- [4] RECENT CHECKPOINT FILES: Agent checkpoints from last 7 days

**Reliability**: 10/10 Git commits, 9/10 project state, 9/10 checkpoints

### project_state_manager.py
**CLI for project state management**

**Commands**:
```bash
# View current state
python project_state_manager.py show

# Initialize new project state
python project_state_manager.py init

# Update current phase
python project_state_manager.py update --phase "Research"

# Add completed task
python project_state_manager.py add-task --id LT-7 --title "Research Paper"
```

**State File**: `.ai_workspace/state/project_state.json`

**Automated Updates**: Git pre-commit hooks auto-detect task IDs and update state

### roadmap_tracker.py
**Parse and track roadmap progress**

**Usage**:
```bash
# Show roadmap status
python roadmap_tracker.py

# Parse specific roadmap
python roadmap_tracker.py --roadmap .ai_workspace/planning/research/ROADMAP_EXISTING_PROJECT.md
```

**Output**:
- Total tasks, completed tasks, percentage
- Quick wins, medium-term, long-term breakdown
- Task details with estimates and deliverables

**Roadmap Format**: Parses markdown with `- [ ]` checkboxes and task metadata

### quick_recovery.bat
**Windows one-click recovery launcher**

**Usage**: Double-click or run from command line
```batch
quick_recovery.bat
```

**Executes**:
1. `bash recover_project.sh`
2. `python roadmap_tracker.py`
3. `python .ai_workspace/tools/checkpoints/analyze_checkpoints.py`

**Platform**: Windows (Git Bash required)

## Recovery Scenarios

### Scenario 1: Token Limit Hit
**Problem**: Claude Code conversation hits token limit, loses context

**Solution**:
```bash
bash recover_project.sh
# Review output, continue work from current state
```

**What Survives**: Git commits (10/10), project state (9/10), checkpoints (9/10)

### Scenario 2: Multi-Month Gap
**Problem**: Returning to project after weeks/months, no memory of progress

**Solution**:
```bash
bash recover_project.sh
python roadmap_tracker.py
cat .ai_workspace/planning/CURRENT_STATUS.md
```

**Output**: Phase status, completed tasks, roadmap progress, recent work

### Scenario 3: Multi-Account Switch
**Problem**: Switching between Claude accounts, need context transfer

**Solution**:
```bash
# On Account A (before switch)
git add . && git commit -m "checkpoint: work in progress"
git push

# On Account B (after switch)
git pull
bash recover_project.sh
python .ai_workspace/tools/checkpoints/analyze_checkpoints.py
```

**See**: `.ai_workspace/tools/multi_account/MULTI_ACCOUNT_RECOVERY_GUIDE.md`

### Scenario 4: Agent Crash
**Problem**: Multi-agent workflow interrupted, partial work lost

**Solution**:
```bash
# Analyze checkpoints
python .ai_workspace/tools/checkpoints/analyze_checkpoints.py

# Resume from checkpoint
python .ai_workspace/tools/checkpoints/launch_checkpoint_task.py --resume LT-4
```

**Checkpoint System**: Auto-saves every 5-10 minutes during agent execution

## Integration

### Git Pre-Commit Hook
Automatically updates project_state.json when commit message contains task ID

**Example**:
```bash
git commit -m "feat(MT-6): Complete boundary layer optimization"
# Hook auto-detects MT-6, updates project_state.json
```

**Hook Location**: `.git/hooks/pre-commit` (via `.ai_workspace/tools/automation/git-hooks/`)

### Recovery Script Dependencies
```
recover_project.sh
├─ .ai_workspace/state/project_state.json (via project_state_manager.py)
├─ git log (recent commits)
├─ git status (current branch, changes)
└─ .ai_workspace/checkpoints/*.json (agent checkpoints)
```

## Testing

**Test Coverage**: 11/11 tests passing (100%)
- State manager: 5 tests
- Roadmap tracker: 3 tests
- Recovery workflow: 3 integration tests

**Test Location**: `tests/test_integration/test_recovery_system/`

**Run Tests**:
```bash
python -m pytest tests/test_integration/test_recovery_system/ -v
```

## Migration History

**2025-12-18**: Consolidated from `.ai_workspace/dev_tools/` to `.ai_workspace/tools/recovery/`
- `recover_project.sh` moved from dev_tools/ root
- `project_state_manager.py` moved from dev_tools/ root
- `roadmap_tracker.py` moved from dev_tools/ root
- `quick_recovery.bat` moved from dev_tools/ root

**State File Migration**: `.ai_workspace/config/project_state.json` -> `.ai_workspace/state/project_state.json`
