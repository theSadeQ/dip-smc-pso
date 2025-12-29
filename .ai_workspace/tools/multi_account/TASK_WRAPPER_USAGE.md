# Task Wrapper Usage Guide

## Overview

The Task Wrapper system automatically checkpoints Claude Code Task tool invocations, enabling recovery from token limits, crashes, and session interruptions.

**Key Promise:** Work is never wasted - even if a token limit hits mid-task, recovery is transparent and automatic.

---

## Quick Start (1 minute)

### Basic Pattern

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Launch agent with automatic checkpointing
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Derive Lyapunov proofs",
        "prompt": "Your detailed prompt here..."
    },
    role="Theory Specialist - Derive Lyapunov proofs"
)

# That's it! Automatic checkpointing happens internally
print(f"Hours spent: {result['hours_spent']}")
print(f"Checkpoint saved: {result['checkpoint_file']}")
print(f"Output artifact: {result['output_artifact']}")
```

### After Token Limit

```bash
/recover                          # Shows incomplete agents
/resume LT-4 agent1_theory       # Auto-relaunches from where it left off
```

Done! No manual work needed.

---

## Installation

The task wrapper is automatically available:

```python
# Import directly
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Or use full path
import sys
sys.path.insert(0, '.ai_workspace/dev_tools')
from task_wrapper import checkpoint_task_launch
```

---

## API Reference

### `checkpoint_task_launch()`

**Signature:**
```python
def checkpoint_task_launch(
    task_id: str,
    agent_id: str,
    task_config: Dict[str, Any],
    role: str,
    dependencies: Optional[List[str]] = None,
    auto_progress: bool = True,
    poll_interval_seconds: int = 300
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `task_id` | str | YES | Task identifier | "LT-4", "MT-6" |
| `agent_id` | str | YES | Agent identifier | "agent1_theory" |
| `task_config` | dict | YES | Task configuration | See below |
| `role` | str | YES | Agent role description | "Theory Specialist - Derive Lyapunov proofs" |
| `dependencies` | list | NO | Dependency files | ["docs/theory/base.md"] |
| `auto_progress` | bool | NO | Enable auto-polling (default: True) | True |
| `poll_interval_seconds` | int | NO | Polling interval (default: 300s = 5min) | 300 |

**task_config structure:**

```python
task_config = {
    "subagent_type": "general-purpose",        # REQUIRED: agent type
    "description": "Brief task description",   # REQUIRED: what the task does
    "prompt": "Your detailed prompt here...",  # REQUIRED: full prompt for agent
    # Optional fields:
    "model": "opus",                           # Optional: override model
    "timeout": 600000                          # Optional: timeout in ms
}
```

**Valid subagent_type values:**
- `"general-purpose"` - General-purpose agent for complex tasks
- `"Explore"` - Fast codebase explorer
- `"Plan"` - Planning and strategy agent

**Returns:**

```python
{
    "task_result": {},              # Agent output/results
    "checkpoint_file": "path/...",  # Location of complete checkpoint
    "hours_spent": 2.5,             # Hours spent on task
    "deliverables": [],             # Files created
    "output_artifact": "path/...",  # Location of output JSON
    "success": True                 # Task success flag
}
```

---

### `checkpoint_agent_progress()`

**Update progress during execution (optional - automatic if auto_progress=True):**

```python
from .project.dev_tools.task_wrapper import checkpoint_agent_progress

checkpoint_agent_progress(
    task_id="LT-4",
    agent_id="agent1_theory",
    hours_completed=2.5,
    deliverables_created=["docs/theory/classical_smc_proof.md"],
    current_phase="Proving STA SMC (Classical done, STA 50%)",
    notes="On track, no blockers"
)
```

---

### `checkpoint_agent_failed()`

**Mark agent as failed (if manually handling interruptions):**

```python
from .project.dev_tools.task_wrapper import checkpoint_agent_failed

checkpoint_agent_failed(
    task_id="LT-4",
    agent_id="agent1_theory",
    hours_spent=2.5,
    failure_reason="Session timeout (token limit)",
    partial_deliverables=["docs/theory/classical_smc_proof.md"],
    recovery_recommendation="Re-launch from Hour 0"
)
```

---

## Usage Patterns

### Pattern 1: Single Agent Task

**Scenario:** One agent handles the entire task

```python
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Derive Lyapunov stability proofs for 5 controllers",
        "prompt": """
        Analyze the 5 SMC controllers and derive complete Lyapunov stability proofs.

        Controllers: Classical SMC, STA SMC, Adaptive SMC, Hybrid Adaptive STA-SMC, Swing-Up SMC

        Deliverables:
        1. docs/theory/lyapunov_stability_proofs.md - Complete proofs for all 5
        2. scripts/validate_stability.py - Validation script

        Requirements:
        - Rigorous mathematical proofs
        - All assumptions clearly stated
        - Peer-review ready
        """
    },
    role="Theory Specialist - Derive Lyapunov proofs"
)

print(f"Work complete in {result['hours_spent']:.1f} hours")
print(f"Output saved to: {result['output_artifact']}")
```

**Recovery (if token limit hits):**
```bash
/recover
# Output shows:
# Agent: agent1_theory
# Last progress: Proving Classical SMC (Hour 2-3.5)
# RECOMMENDATION: /resume LT-4 agent1_theory

/resume LT-4 agent1_theory
# Agent relaunches automatically
```

---

### Pattern 2: Parallel Agents (Independent Work)

**Scenario:** Two agents work independently on different parts

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Agent 1: Simulations
result1 = checkpoint_task_launch(
    task_id="MT-6",
    agent_id="agent1_sim",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Run comprehensive simulation benchmarks",
        "prompt": "Run simulations for all 5 controllers..."
    },
    role="Simulation Engineer"
)

# Agent 2: Data Analysis
result2 = checkpoint_task_launch(
    task_id="MT-6",
    agent_id="agent2_analysis",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Analyze benchmark results",
        "prompt": "Analyze simulation results and create statistics..."
    },
    role="Data Scientist"
)

print(f"Agent 1: {result1['hours_spent']:.1f}h")
print(f"Agent 2: {result2['hours_spent']:.1f}h")
```

**Recovery (if token limit hits partway):**
```bash
/recover
# Shows BOTH agents' status:
# Agent 1: agent1_sim - COMPLETE (3.5 hours)
# Agent 2: agent2_analysis - IN_PROGRESS (Last at Hour 2.2)

/resume MT-6 agent2_analysis  # Only relaunch the incomplete one
```

---

### Pattern 3: Sequential Agents (Handoff)

**Scenario:** Agent 2 depends on Agent 1's output

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Step 1: Agent 1 completes research
result1 = checkpoint_task_launch(
    task_id="LT-7",
    agent_id="agent1_research",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Research phase - gather theory",
        "prompt": "Research the following topics..."
    },
    role="Research Specialist"
)

# Step 2: Check handoff file exists
output_artifact = result1["output_artifact"]
print(f"Agent 1 output: {output_artifact}")

# Step 3: Agent 2 uses it as input
result2 = checkpoint_task_launch(
    task_id="LT-7",
    agent_id="agent2_paper",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Write research paper using research output",
        "prompt": f"""
        Using the research compiled in {output_artifact},
        write the final research paper...
        """
    },
    role="Technical Writer",
    dependencies=[output_artifact]  # Agent 2 depends on Agent 1's output
)
```

**Recovery (if token limit hits during Agent 2):**
```bash
/recover
# Shows:
# Agent 1: agent1_research - COMPLETE
# Agent 2: agent2_paper - IN_PROGRESS (Hour 2.1)
# Dependency: {output_artifact} exists

/resume LT-7 agent2_paper  # Relaunches Agent 2 with dependency preserved
```

---

### Pattern 4: With Manual Progress Tracking

**Scenario:** You want to manually update progress (optional enhancement)

```python
from .project.dev_tools.task_wrapper import (
    checkpoint_task_launch,
    checkpoint_agent_progress
)

result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={...},
    role="Theory Specialist"
    # auto_progress=True (default) - also works with manual updates
)

# During execution, you can manually enhance progress
# (or let auto-polling do it automatically)
checkpoint_agent_progress(
    task_id="LT-4",
    agent_id="agent1_theory",
    hours_completed=2.5,
    deliverables_created=["docs/theory/classical_proof.md"],
    current_phase="Classical SMC Lyapunov proof (H3/5)",
    notes="Mathematical proofs verified by peer review"
)
```

---

## Recovery Workflow

### Step 1: Detect Incomplete Work

```bash
/recover
```

Output shows all incomplete agents with context:

```
[5] INCOMPLETE AGENT WORK
------------------------------------------------------------------------------
WARNING: Incomplete agent work detected!

Task: LT-4
  Agent: agent1_theory
    Role: Theory Specialist - Derive Lyapunov proofs
    Launched: 2025-11-11T10:30:00
    Last progress: Proving Classical SMC (Hour 2-3.5)

RECOMMENDATION: /resume LT-4 agent1_theory
```

### Step 2: Auto-Resume

```bash
/resume LT-4 agent1_theory
```

The agent automatically relaunches. The recovery system:
- Preserves all partial work from `academic/`
- Shows where the agent left off in context
- Relaunches from Hour 0 with full history available
- Continues seamlessly

### Step 3: Verify Completion

```bash
/recover
# Now shows:
# Agent: agent1_theory - COMPLETE (11.5 hours)

# Checkpoint file location
ls -la academic/lt4_agent1_theory_complete.json
# Shows completed checkpoint with deliverables
```

---

## Checkpoint Files & Location

All checkpoints are stored in `academic/`:

### File Structure

```
academic/
├── lt4_plan_approved.json              # Task approval metadata
├── lt4_agent1_theory_launched.json     # Agent start (created at launch)
├── lt4_agent1_theory_progress.json     # Updated every 5 min (hybrid polling)
├── lt4_agent1_theory_complete.json     # Created at completion
├── lt4_agent1_theory_output.json       # Agent output (auto-captured)
├── lt4_agent2_validation_launched.json
├── lt4_agent2_validation_progress.json
└── lt4_agent2_validation_complete.json
```

### Reading Checkpoint Files

```bash
# View agent progress
cat academic/lt4_agent1_theory_progress.json

# View output
cat academic/lt4_agent1_theory_output.json

# Check task status
python -c "
from .project.dev_tools.agent_checkpoint import get_task_status
status = get_task_status('LT-4')
print(f\"Agents: {status['total_agents']} | Complete: {status['completed_agents']}\")
"
```

---

## Cleanup After Completion

Once a task is committed to git, cleanup checkpoints:

```python
from .project.dev_tools.agent_checkpoint import cleanup_task_checkpoints

cleanup_task_checkpoints("LT-4")
# Removes all academic/lt4_*.json files
```

Or via bash:

```bash
rm -f academic/lt4_*.json
```

---

## Configuration

### Custom Polling Interval

```python
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={...},
    role="Theory Specialist",
    poll_interval_seconds=600  # Check every 10 minutes instead of 5
)
```

### Disable Auto-Progress

```python
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={...},
    role="Theory Specialist",
    auto_progress=False  # Disable hybrid polling (manual updates only)
)
```

---

## Troubleshooting

### Checkpoint Files Not Created

**Check:** Are you calling `checkpoint_task_launch()`?

```python
# Wrong:
result = Task(subagent_type="general-purpose", ...)

# Right:
result = checkpoint_task_launch(
    task_id="YOUR_TASK",
    agent_id="agent1",
    task_config={...},
    role="..."
)
```

### Recovery Doesn't Show Agent

**Check:** Did the agent actually launch?

```bash
# Look for launched checkpoint
ls -la academic/*_launched.json

# If nothing, agent was never launched with checkpoint_task_launch()
```

### Output Artifact Missing

**Check:** Is checkpoint system working?

```bash
# Verify task_wrapper.py exists
python -c "from .project.dev_tools.task_wrapper import checkpoint_task_launch; print('[OK] Module loaded')"

# Check academic/ permissions
ls -ld academic/
```

---

## Best Practices

### 1. Always Use Task Wrapper for Multi-Agent Tasks

**Good:**
```python
result = checkpoint_task_launch(task_id="LT-4", agent_id="agent1", ...)
```

**Bad:**
```python
result = Task(subagent_type="general-purpose", ...)  # No checkpointing!
```

### 2. Use Consistent Task/Agent IDs

```python
# Good: Clear naming
task_id="LT-4"
agent_id="agent1_theory"

# Avoid: Unclear naming
task_id="foo"
agent_id="a1"
```

### 3. Include Descriptive Roles

```python
# Good: Clear what agent does
role="Theory Specialist - Derive Lyapunov proofs for 5 controllers"

# Okay:
role="Theory Specialist"
```

### 4. Handle Dependencies

```python
# If Agent 2 depends on Agent 1's output
result1 = checkpoint_task_launch(task_id="LT-7", agent_id="agent1_research", ...)
result2 = checkpoint_task_launch(
    task_id="LT-7",
    agent_id="agent2_paper",
    dependencies=[result1["output_artifact"]]
)
```

### 5. Cleanup After Commit

```bash
# After committing to git
python -c "from .project.dev_tools.agent_checkpoint import cleanup_task_checkpoints; cleanup_task_checkpoints('LT-4')"

# Or manually
rm -f academic/lt4_*.json
```

---

## Examples from Your Project

### Example 1: Phase 5 Research Tasks

```python
# Orchestrate research paper generation (LT-7)
result = checkpoint_task_launch(
    task_id="LT-7",
    agent_id="research_agent",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Generate research paper on SMC optimization",
        "prompt": """
        Based on the controller benchmarks in benchmarks/results/,
        write a comprehensive research paper including:
        - Title, abstract, introduction
        - Methodology and controller descriptions
        - Benchmark results and analysis
        - 14 figures with captions
        - Conclusion and future work
        - Complete bibliography

        Output: academic/LT-7_research_paper.pdf
        """
    },
    role="Research Paper Specialist"
)
```

### Example 2: Parallel PSO Optimization (MT-6)

```python
# Parallel optimization agents
agents = [
    ("agent1_classical", "Classical SMC Optimizer"),
    ("agent2_adaptive", "Adaptive SMC Optimizer"),
    ("agent3_sta", "STA SMC Optimizer")
]

results = []
for agent_id, role in agents:
    result = checkpoint_task_launch(
        task_id="MT-6",
        agent_id=agent_id,
        task_config={
            "subagent_type": "general-purpose",
            "description": f"Optimize {role}",
            "prompt": f"Run PSO optimization for {role}..."
        },
        role=role
    )
    results.append(result)
```

---

## Summary

The task wrapper provides:

✅ **Automatic Checkpointing** - No manual calls needed
✅ **Token Limit Protection** - Work survives interruptions
✅ **Progress Tracking** - Know exactly where agents left off
✅ **Output Preservation** - Agent work saved to academic/
✅ **Auto-Resume** - `/resume` command relaunches interrupted agents
✅ **Seamless Recovery** - Recovery is transparent and automatic

**Remember:** One-line integration, automatic everything else!

```python
result = checkpoint_task_launch(task_id="YOUR_TASK", agent_id="agent1", ...)
```

That's all you need. The rest is automatic.
