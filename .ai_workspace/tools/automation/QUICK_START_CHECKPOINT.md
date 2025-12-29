# Quick Start: Checkpoint Task Launcher

**No complicated Python imports needed!** Use simple commands to launch checkpoint-protected tasks.

---

## Method 1: Simplest Way (Python Command)

```bash
cd D:\Projects\main

python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task LT-4 \
    --agent agent1_theory \
    --role "Theory Specialist" \
    --description "Derive Lyapunov proofs" \
    --prompt "Given the 5 SMC controllers, derive complete Lyapunov stability proofs..."
```

**That's it!** No Python imports, no complicated code. Just a command.

---

## Method 2: Super Simple (Bash Wrapper)

```bash
cd D:\Projects\main

./checkpoint-task LT-4 agent1_theory "Theory Specialist" "Derive Lyapunov proofs..."
```

Even simpler! Just 4 arguments: TASK_ID, AGENT_ID, ROLE, PROMPT

---

## Method 3: In Your Python Code (If You Prefer)

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Derive Lyapunov proofs",
        "prompt": "Your full prompt..."
    },
    role="Theory Specialist"
)
```

---

## Real Examples

### Example 1: PSO Optimization

```bash
python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task MT-6 \
    --agent agent1_pso \
    --role "PSO Optimization Engineer" \
    --description "Optimize PSO parameters" \
    --prompt "Run PSO optimization for Classical SMC controller with objectives: 1. Minimize chattering 2. Fast response 3. Bounded gains"
```

### Example 2: Theory Work

```bash
python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task LT-4 \
    --agent agent1_theory \
    --role "Lyapunov Proof Specialist" \
    --description "Complete Lyapunov stability proofs" \
    --prompt "Analyze the 5 SMC controllers and derive complete, peer-review-ready Lyapunov stability proofs for each controller"
```

### Example 3: Research Paper

```bash
python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task LT-7 \
    --agent agent1_paper \
    --role "Research Paper Specialist" \
    --description "Write research paper" \
    --prompt "Based on the benchmarks and theoretical analysis, write a comprehensive research paper on SMC controller optimization with 14 figures, complete bibliography, and publication-ready formatting"
```

---

## What Happens Automatically

When you run the command:

1. **Checkpoint created** → Task starts
   ```
   academic/
   └── mt6_agent1_pso_launched.json
   ```

2. **Progress tracked** → Every 5 minutes
   ```
   academic/
   ├── mt6_agent1_pso_launched.json
   └── mt6_agent1_pso_progress.json  (updated every 5 min)
   ```

3. **Output saved** → At completion
   ```
   academic/
   ├── mt6_agent1_pso_launched.json
   ├── mt6_agent1_pso_progress.json
   ├── mt6_agent1_pso_complete.json
   └── mt6_agent1_pso_output.json
   ```

---

## If Token Limit Hits

You don't lose any work! Just do:

```bash
# See what was interrupted
/recover

# Auto-resume the agent
/resume MT-6 agent1_pso
```

Done! Agent picks up where it left off.

---

## All Command-Line Options

```bash
python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task LT-4                           # Task ID (required)
    --agent agent1_theory                 # Agent ID (required)
    --role "Theory Specialist"            # Agent role (required)
    --description "Task description"      # Brief description (required)
    --prompt "Full prompt..."             # Full prompt (required)
    --type general-purpose                # Subagent type: general-purpose, Explore, Plan
    --poll-interval 300                   # Progress check interval (seconds)
    --auto-progress                       # Enable auto-polling (default: ON)
    --no-auto-progress                    # Disable auto-polling
```

---

## Copy-Paste Template

Just fill in the blanks:

```bash
python .ai_workspace/dev_tools/launch_checkpoint_task.py \
    --task [YOUR_TASK_ID] \
    --agent [YOUR_AGENT_ID] \
    --role "[YOUR_AGENT_ROLE]" \
    --description "[BRIEF_DESCRIPTION]" \
    --prompt "[YOUR_FULL_PROMPT_HERE]"
```

---

## Recovery Commands

After your task completes (or if interrupted):

```bash
# Check status of all incomplete agents
/recover

# Resume a specific agent
/resume [TASK_ID] [AGENT_ID]

# Example:
/resume LT-4 agent1_theory
```

---

## Why This Is Better

| Old Way | New Way |
|---------|---------|
| Complicated Python imports | Simple bash command |
| Token limit = lost work | Token limit = safe checkpoint |
| Manual recovery setup | One-command: `/resume` |
| No progress tracking | Auto-tracked every 5 min |

---

## Next Steps

1. Try a simple command:
   ```bash
   python .ai_workspace/dev_tools/launch_checkpoint_task.py \
       --task TEST \
       --agent test_agent \
       --role "Test Agent" \
       --description "Test" \
       --prompt "Hello world"
   ```

2. Check the output:
   ```bash
   ls -la academic/test_*.json
   ```

3. Use `/recover` to see checkpoint files

That's it! No complicated Python knowledge needed.
