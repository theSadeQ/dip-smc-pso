# Recovery System

Unified recovery and checkpoint system for the DIP-SMC-PSO project.

## Directory Structure

- `core/` - Core recovery scripts (recover_project.sh, project_state_manager.py, recovery_validator.py, recovery_analyzer.py)
- `checkpoints/` - Checkpoint system (agent_checkpoint.py, task_wrapper.py, checkpoint_analyzer.py)
- `state/` - State files (project_state.json, session_state.json, agents.json)
- `multi_account/` - Multi-account tools (account switchers, token tracker)
- `docs/` - Recovery documentation (checkpoint system, session continuity, multi-account guide, recovery dashboard)

## Purpose

This directory consolidates all recovery-related components that were previously scattered across `.project/dev_tools/`, `.project/ai/config/`, and `.project/claude/commands/`. The unified structure improves discoverability and makes the recovery system easier to maintain.

## Key Features

- 30-second recovery from token limits
- Multi-agent checkpoint system
- Cross-account recovery support
- Git-based persistence (10/10 reliability)
- Sequential-thinking MCP integration for intelligent recovery decisions

## Quick Start

```bash
# Test recovery system
bash .project/recovery/core/recover_project.sh

# Check recovery health
python .project/recovery/core/recovery_validator.py

# Analyze recovery context (uses sequential-thinking MCP)
python .project/recovery/core/recovery_analyzer.py

# Scan checkpoints
python .project/recovery/checkpoints/checkpoint_analyzer.py
```

## Documentation

See `docs/` subdirectory for complete recovery system documentation.
