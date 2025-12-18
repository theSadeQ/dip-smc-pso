# .project/tools - Development Tools

**Purpose**: Function-organized development and automation tools for project workflows.

## Directory Structure

```
tools/
├─ recovery/          # Recovery and state management tools
├─ checkpoints/       # Agent checkpoint and task tracking
├─ multi_account/     # Multi-account recovery workflows
├─ automation/        # Documentation, citation, and build automation
├─ analysis/          # Performance and code quality analysis
├─ migration/         # Migration scripts and utilities
└─ misc/              # Miscellaneous utilities
```

## Subdirectories

### recovery/
**Purpose**: 30-second recovery system and project state management

**Key Tools**:
- `recover_project.sh` - Main recovery entry point (30-second promise)
- `project_state_manager.py` - CLI for project state updates
- `roadmap_tracker.py` - Parse and track roadmap progress
- `quick_recovery.bat` - Windows one-click recovery

**See**: `recovery/README.md` for complete documentation

### checkpoints/
**Purpose**: Multi-agent checkpoint system for crash recovery

**Key Tools**:
- `agent_checkpoint.py` - Core checkpoint API
- `analyze_checkpoints.py` - Checkpoint status analyzer
- `launch_checkpoint_task.py` - Task launcher with checkpointing
- `cleanup_test_checkpoints.py` - Test checkpoint cleanup

**See**: `.project/ai/orchestration/agent_checkpoint_system.md` for design

### multi_account/
**Purpose**: Multi-account token management and recovery workflows

**Key Tools**:
- `MULTI_ACCOUNT_RECOVERY_GUIDE.md` - Primary workflow guide
- `task_wrapper.py` - Automatic checkpoint wrapper for Task tool
- `TASK_WRAPPER_USAGE.md` - Usage examples and patterns
- `test_task_wrapper.py` - Test suite for task wrapper

**See**: `multi_account/MULTI_ACCOUNT_RECOVERY_GUIDE.md` for complete guide

### automation/
**Purpose**: Documentation generation, citation management, build automation

**Key Tools**:
- Documentation automation (navigation footers, link validation)
- Citation discovery and enrichment (web search, bibtex generation)
- Quality audits (coverage, code quality, system health)
- Git hooks and pre-commit checks

**Contents**: 200+ automation scripts from legacy `.project/dev_tools/`

**See**: `automation/AUTOMATION_GUIDE.md` for script index

### analysis/
**Purpose**: Performance analysis and benchmarking tools

**Key Tools**:
- `issue_2_surface_design_analysis.py` - Response surface analysis
- `sta_smc_overshoot_analysis.py` - Controller overshoot analysis
- `results/` - Analysis output artifacts

**See**: `.artifacts/research/` for full analysis reports

### migration/
**Purpose**: Migration scripts and path update utilities

**Key Tools**:
- `update_paths.py` - Automated path reference updates (planned)

### misc/
**Purpose**: Miscellaneous utilities and demonstrations

**Contents**: Code beautification, documentation generators, demos

## Common Workflows

### Recovery Workflow
```bash
# Full 30-second recovery
bash .project/tools/recovery/recover_project.sh

# Windows one-click
.project\tools\recovery\quick_recovery.bat

# View project state
python .project/tools/recovery/project_state_manager.py show
```

### Checkpoint Workflow
```bash
# Launch task with checkpointing
python .project/tools/checkpoints/launch_checkpoint_task.py --task LT-4

# Analyze checkpoint status
python .project/tools/checkpoints/analyze_checkpoints.py

# Cleanup test checkpoints
python .project/tools/checkpoints/cleanup_test_checkpoints.py
```

### Multi-Account Recovery
```bash
# See comprehensive guide
cat .project/tools/multi_account/MULTI_ACCOUNT_RECOVERY_GUIDE.md

# Task wrapper usage
python .project/tools/multi_account/task_wrapper.py --help
```

## Migration Notes

**2025-12-18**: Reorganized from 3 legacy locations:
- `.project/dev_tools/` -> `tools/automation/` (200+ files)
- `.project/recovery/` -> `tools/recovery/` and `tools/checkpoints/`
- `.project/ai/config/tools/` -> `tools/misc/`

**Goal**: Function-based organization for easier discovery and maintenance
