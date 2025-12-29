# .ai_workspace/tools/checkpoints - Agent Checkpoint System

**Purpose**: Automatic checkpoint system for multi-agent workflows to prevent loss of work on token limits, crashes, or interruptions.

## Core Tools

### agent_checkpoint.py
**Main checkpoint API for agent orchestration**

**Functions**:
```python
# Plan approved checkpoint
checkpoint_plan_approved(task_id, plan_summary, hours, agents, deliverables)

# Agent launched checkpoint
checkpoint_agent_launched(task_id, agent_id, role, hours)

# Progress checkpoint (every 5-10 minutes)
checkpoint_agent_progress(task_id, agent_id, hours_completed, deliverables, current_phase)

# Agent completion checkpoint
checkpoint_agent_complete(task_id, agent_id, hours, deliverables, summary)

# Agent failure checkpoint
checkpoint_agent_failed(task_id, agent_id, hours, reason, recovery_recommendation)
```

**Output Location**: `.ai_workspace/checkpoints/{task_id}_{agent_id}_{timestamp}.json`

**See**: `.ai_workspace/orchestration/agent_checkpoint_system.md` for complete API

### analyze_checkpoints.py
**Checkpoint status analyzer and recovery helper**

**Usage**:
```bash
# Analyze all checkpoints
python analyze_checkpoints.py

# Analyze specific task
python analyze_checkpoints.py --task LT-4

# Last 24 hours only
python analyze_checkpoints.py --since 24h
```

**Output**:
- Total checkpoints, task count, incomplete tasks
- Per-task summary: agents, hours, deliverables, status
- Recovery recommendations for incomplete work

**Example Output**:
```
[CHECKPOINT ANALYSIS]
Total Checkpoints: 15
Tasks Found: 3
Incomplete Tasks: 1

Task: LT-4
  Agents: agent1, agent2, agent3
  Hours: 12.5 / 15.0 (83%)
  Deliverables: 8 / 12 (67%)
  Status: IN_PROGRESS
  Recovery: Resume from agent3 checkpoint at hour 12.5
```

### launch_checkpoint_task.py
**Task launcher with automatic checkpointing**

**Usage**:
```bash
# Launch new task
python launch_checkpoint_task.py --task LT-4 --agent agent1

# Resume from checkpoint
python launch_checkpoint_task.py --resume LT-4 --agent agent3

# With config override
python launch_checkpoint_task.py --task MT-6 --config custom.yaml
```

**Features**:
- Auto-checkpoint every 5 minutes
- Crash recovery (restart from last checkpoint)
- Output preservation (saves to `academic/`)
- Progress tracking (hours completed, deliverables)

### cleanup_test_checkpoints.py
**Test checkpoint cleanup utility**

**Usage**:
```bash
# Cleanup test checkpoints (older than 7 days)
python cleanup_test_checkpoints.py

# Dry run (preview what would be deleted)
python cleanup_test_checkpoints.py --dry-run

# Cleanup all checkpoints (including production)
python cleanup_test_checkpoints.py --all
```

**Safety**: Only removes checkpoints with "test_" prefix by default

## Checkpoint File Format

### Example Checkpoint
```json
{
  "task_id": "LT-4",
  "agent_id": "agent1",
  "role": "Control Systems Specialist",
  "timestamp": "2025-11-07T10:30:00",
  "checkpoint_type": "progress",
  "hours_completed": 3.5,
  "hours_estimated": 8.0,
  "deliverables_completed": [
    "Lyapunov function derivation",
    "Stability proof outline"
  ],
  "deliverables_pending": [
    "Numerical validation",
    "Documentation"
  ],
  "current_phase": "Proof validation",
  "recovery_point": "Continue with numerical validation section"
}
```

### Checkpoint Types
- `plan_approved`: Task planning phase complete
- `agent_launched`: Agent started work
- `progress`: Incremental progress update (every 5-10 min)
- `agent_complete`: Agent finished successfully
- `agent_failed`: Agent encountered error/blocker

## Recovery Workflows

### Workflow 1: Token Limit During Multi-Agent Task
**Scenario**: 6-agent orchestration, token limit at agent 3

**Recovery Steps**:
```bash
# 1. Analyze checkpoints
python analyze_checkpoints.py --task LT-4

# 2. Resume from agent 3 checkpoint
python launch_checkpoint_task.py --resume LT-4 --agent agent3

# 3. Verify output preserved
ls academic/LT4_research_paper/
```

**Result**: Agents 1-2 work preserved, agent 3 continues from last checkpoint

### Workflow 2: Crash Recovery
**Scenario**: System crash during agent execution

**Recovery Steps**:
```bash
# 1. Check Git status (may have uncommitted work)
git status

# 2. Analyze checkpoints
python analyze_checkpoints.py

# 3. Review deliverables in academic/
ls academic/

# 4. Resume from last checkpoint
python launch_checkpoint_task.py --resume <task_id> --agent <agent_id>
```

**Result**: Work preserved up to last checkpoint (5-10 min loss max)

### Workflow 3: Multi-Account Context Transfer
**Scenario**: Switch Claude accounts mid-task

**Recovery Steps**:
```bash
# On Account A (before switch)
git add .ai_workspace/checkpoints/ && git commit -m "checkpoint: agent progress"
git push

# On Account B (after switch)
git pull
python analyze_checkpoints.py
python launch_checkpoint_task.py --resume <task_id>
```

**Result**: Seamless continuation across accounts

## Integration

### Task Wrapper Integration
Checkpoints are automatically created when using task_wrapper.py:

```python
from .project.tools.multi_account.task_wrapper import checkpoint_task_launch
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1",
    task_config={...}
)
```

**See**: `.ai_workspace/tools/multi_account/TASK_WRAPPER_USAGE.md`

### Multi-Agent Orchestration
Ultimate Orchestrator pattern uses checkpoints for:
- Plan approval tracking
- Agent progress monitoring
- Crash recovery
- Cross-account coordination

**See**: `.ai_workspace/orchestration/agent_orchestration.md`

## Testing

**Test Coverage**: 9/9 tests passing (100%)
- Checkpoint creation: 3 tests
- Checkpoint analysis: 2 tests
- Recovery workflows: 4 tests

**Test Location**: `tests/test_integration/test_checkpoint_system/`

**Run Tests**:
```bash
python -m pytest tests/test_integration/test_checkpoint_system/ -v
```

## Migration History

**2025-12-18**: Consolidated from multiple locations:
- `agent_checkpoint.py` from `.ai_workspace/dev_tools/`
- `analyze_checkpoints.py` from `.ai_workspace/dev_tools/`
- `launch_checkpoint_task.py` from `.ai_workspace/dev_tools/`
- `checkpoint_manager.py` from `.ai_workspace/dev_tools/research/`

**Checkpoint Location**: `.ai_workspace/checkpoints/` (unchanged)
