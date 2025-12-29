# SUPER EASY START - Checkpoint Task Launcher

**No command line. No Python. No complicated setup.**

Just **double-click** and you're protected from token limits!

---

## The Simplest Way (3 Steps)

### Step 1: Open File Explorer

Windows Key → Type "file" → Click "File Explorer"

### Step 2: Navigate to Batch Files

```
D:\Projects\main\.project\dev_tools\
```

### Step 3: Double-Click a Batch File

Pick ONE:

| File | What It Does |
|------|-------------|
| **launch-checkpoint-task.bat** | Interactive - Answer questions |
| **EXAMPLES-launch-checkpoint.bat** | Pick from menu of examples |
| **LAUNCH_TEMPLATE.bat** | Edit and customize |

---

## Option A: Interactive (Easiest)

**File:** `launch-checkpoint-task.bat`

```
Double-click → Answer questions → Task launches with checkpoint protection
```

**Questions it asks:**
```
Enter Task ID: LT-4
Enter Agent ID: agent1_theory
Enter Agent Role: Theory Specialist
Enter Task Description: Derive Lyapunov proofs
Enter your full prompt: [type your prompt, then type DONE]
```

**Done!** Checkpoints created automatically every 5 minutes.

---

## Option B: Pre-Made Examples

**File:** `EXAMPLES-launch-checkpoint.bat`

```
Double-click → Pick example from menu → Task launches
```

**Examples included:**
1. Lyapunov Proof Theory Work
2. PSO Optimization
3. Research Paper Writing
4. Data Analysis

Just pick one and it launches!

---

## Option C: Custom Template

**File:** `LAUNCH_TEMPLATE.bat`

**Steps:**

1. Right-click `LAUNCH_TEMPLATE.bat`
2. Select "Edit with Notepad"
3. Change these lines:
   ```batch
   set TASK_ID=YOUR_TASK_ID          → set TASK_ID=LT-4
   set AGENT_ID=YOUR_AGENT_ID        → set AGENT_ID=agent1_theory
   set ROLE=YOUR_ROLE                → set ROLE=Theory Specialist
   set DESCRIPTION=YOUR_DESCRIPTION  → set DESCRIPTION=Derive proofs
   set PROMPT_TEXT=YOUR_PROMPT       → set PROMPT_TEXT=Your full prompt...
   ```
4. Press Ctrl+S to save
5. File → Save As → Name: `my-custom-task.bat`
6. Double-click `my-custom-task.bat` to launch!

---

## What Happens When You Launch

```
===============================================
  Launching Checkpoint Task
===============================================

Task ID:     LT-4
Agent ID:    agent1_theory
Role:        Theory Specialist
Description: Derive Lyapunov proofs

Launching in 2 seconds...

[CHECKPOINT] Agent launched: LT-4/agent1_theory
[CHECKPOINT] Agent completed: LT-4/agent1_theory

===============================================
  Task Launch Complete
===============================================

Hours spent: 2.5
Checkpoint file: .artifacts\lt4_agent1_theory_complete.json
Output artifact: .artifacts\lt4_agent1_theory_output.json
Success: True

Recovery command (if needed):
  /recover
  /resume LT-4 agent1_theory
```

---

## If Token Limit Hits (Recovery)

**Don't panic! Your work is safe!**

Just do:

```bash
/recover
```

Shows:
```
[5] INCOMPLETE AGENT WORK
Task: LT-4
  Agent: agent1_theory
  Last progress: Proving Classical SMC (Hour 2-3.5)

RECOMMENDATION: /resume LT-4 agent1_theory
```

Then:

```bash
/resume LT-4 agent1_theory
```

**Done!** Agent automatically relaunches from where it left off.

---

## Example Tasks You Can Launch Right Now

### Example 1: PSO Optimization

Edit `LAUNCH_TEMPLATE.bat` with:
```batch
set TASK_ID=MT-6
set AGENT_ID=agent1_pso
set ROLE=PSO Optimization Engineer
set DESCRIPTION=Optimize PSO parameters
set PROMPT_TEXT=Run PSO optimization for Classical SMC controller. Minimize chattering, maintain fast response, keep gains bounded. Generate detailed benchmark results.
```

Save as `launch-pso-task.bat` → Double-click!

### Example 2: Theory Work

Edit `LAUNCH_TEMPLATE.bat` with:
```batch
set TASK_ID=LT-4
set AGENT_ID=agent1_theory
set ROLE=Lyapunov Proof Specialist
set DESCRIPTION=Derive Lyapunov stability proofs
set PROMPT_TEXT=Analyze 5 SMC controllers. Derive complete Lyapunov stability proofs with mathematical rigor suitable for peer review.
```

Save as `launch-theory-task.bat` → Double-click!

### Example 3: Research Paper

Edit `LAUNCH_TEMPLATE.bat` with:
```batch
set TASK_ID=LT-7
set AGENT_ID=agent1_paper
set ROLE=Research Paper Specialist
set DESCRIPTION=Write research paper
set PROMPT_TEXT=Based on benchmarks and analysis, write publication-ready research paper with 14+ figures, comprehensive bibliography, IEEE format.
```

Save as `launch-paper-task.bat` → Double-click!

---

## Features (Automatic!)

When you double-click a batch file:

✅ **Checkpoint created** at start
✅ **Progress tracked** every 5 minutes automatically
✅ **Output saved** to `academic/`
✅ **Recovery command** shown in output
✅ **Zero setup** needed

---

## Multi-Agent Tasks (Parallel)

If you need multiple agents working at the same time:

**Task 1:** Double-click `launch-checkpoint-task.bat`
```
Task ID: MT-7
Agent ID: agent1_sim
Role: Simulation Engineer
```

**Task 2:** Double-click `launch-checkpoint-task.bat` again
```
Task ID: MT-7
Agent ID: agent2_analysis
Role: Data Scientist
```

Both run in parallel. If one hits token limit:

```bash
/recover
# Shows which agent is incomplete

/resume MT-7 agent2_analysis
# Only resumes the incomplete one
```

---

## File Locations

All batch files are here:
```
D:\Projects\main\.project\dev_tools\
```

Your checkpoints and output saved here:
```
D:\Projects\main\.artifacts\
```

---

## Troubleshooting

### Problem: Command window closes too fast

**Solution:** Batch file should have `pause` at end. It does by default. Just click in window and press any key.

### Problem: "python is not recognized"

**Solution:** Make sure `python` is installed:
```bash
python --version
```

Should show Python 3.x version.

### Problem: File not found error

**Solution:** Make sure you're in the right directory:
```
D:\Projects\main\.project\dev_tools\
```

All batch files must be in this directory.

---

## That's It!

**You now have checkpoint protection for multi-agent tasks!**

### Just:
1. Double-click a batch file
2. Answer questions (or pick example)
3. Task launches with automatic checkpointing
4. Work survives token limits
5. Recovery is one command: `/resume`

**No command line. No Python knowledge. No complicated setup.**

---

## For More Details

See these files in `.ai_workspace/dev_tools/`:

- **BATCH_FILES_GUIDE.md** - Complete batch file documentation
- **QUICK_START_CHECKPOINT.md** - Python/command-line reference
- **TASK_WRAPPER_USAGE.md** - Full technical documentation

---

## Questions?

All batch files include comments explaining each step. Just right-click and "Edit with Notepad" to see the details!

**Enjoy automatic checkpoint protection! No more wasted work from token limits!**

🎉
