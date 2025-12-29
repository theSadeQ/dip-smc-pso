# Windows Batch Files Guide - Checkpoint Task Launcher

**No command line knowledge needed!** Just double-click and follow prompts.

---

## Quick Overview

Three batch files to choose from:

| File | Use Case | How It Works |
|------|----------|------------|
| **launch-checkpoint-task.bat** | General launcher | Double-click → interactive prompts OR command-line args |
| **LAUNCH_TEMPLATE.bat** | Custom tasks | Edit file, fill in details, save, double-click |
| **EXAMPLES-launch-checkpoint.bat** | Quick examples | Double-click → pick example from menu |

---

## Method 1: Interactive Launcher (Easiest)

**File:** `.ai_workspace/dev_tools/launch-checkpoint-task.bat`

### Step 1: Open File Explorer
Navigate to: `D:\Projects\main\.project\dev_tools\`

### Step 2: Double-Click
Double-click `launch-checkpoint-task.bat`

### Step 3: Answer Prompts
```
Enter Task ID (e.g., LT-4, MT-6): LT-4
Enter Agent ID (e.g., agent1_theory): agent1_theory
Enter Agent Role (e.g., Theory Specialist): Theory Specialist
Enter Task Description: Derive Lyapunov proofs
Enter your full prompt (type DONE when finished):
>> Given the 5 SMC controllers...
>> [type your prompt]
>> DONE
```

### Step 4: Done!
Task launches automatically with checkpoint protection.

---

## Method 2: Edit Template (Custom Tasks)

**File:** `.ai_workspace/dev_tools/LAUNCH_TEMPLATE.bat`

### Step 1: Right-Click and Edit

Right-click `LAUNCH_TEMPLATE.bat` → "Edit with Notepad"

### Step 2: Fill In Your Details

```batch
REM EDIT THESE VALUES
set TASK_ID=LT-4
set AGENT_ID=agent1_theory
set ROLE=Theory Specialist
set DESCRIPTION=Derive Lyapunov proofs
set PROMPT_TEXT=Given the 5 SMC controllers, derive complete Lyapunov stability proofs...
```

### Step 3: Save
Press Ctrl+S to save

### Step 4: Save As
File → Save As → `my-custom-task.bat`

### Step 5: Double-Click
Double-click your new `my-custom-task.bat` file to launch!

---

## Method 3: Pre-Made Examples

**File:** `.ai_workspace/dev_tools/EXAMPLES-launch-checkpoint.bat`

### Step 1: Double-Click

Double-click `EXAMPLES-launch-checkpoint.bat`

### Step 2: Pick Example

```
Choose an example to launch:

[1] Lyapunov Proof Theory Work (LT-4)
[2] PSO Optimization (MT-6)
[3] Research Paper Writing (LT-7)
[4] Data Analysis (MT-7)
[5] Custom Task (Interactive)

Enter your choice (1-5):
```

### Step 3: Done!
Task launches with full checkpoint protection

---

## Real Examples You Can Use Now

### Example 1: Copy-Paste Ready

Create a new file: `my-pso-task.bat`

```batch
@echo off
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task MT-6 ^
    --agent agent1_pso ^
    --role "PSO Optimization Engineer" ^
    --description "Optimize PSO parameters" ^
    --prompt "Run PSO optimization for Classical SMC with objectives: minimize chattering, fast response, bounded gains"

pause
```

Then just double-click `my-pso-task.bat`!

### Example 2: Theory Work

Create: `my-theory-task.bat`

```batch
@echo off
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task LT-4 ^
    --agent agent1_theory ^
    --role "Lyapunov Proof Specialist" ^
    --description "Complete Lyapunov stability proofs" ^
    --prompt "Derive complete Lyapunov stability proofs for 5 SMC controllers with peer-review ready mathematical rigor"

pause
```

Double-click and done!

---

## What Happens When You Launch

### Automatic Checkpointing

```
[INFO] Launching checkpoint task...
[INFO] Task: LT-4
[INFO] Agent: agent1_theory
[INFO] Role: Lyapunov Proof Specialist
[INFO] Type: general-purpose

[CHECKPOINT] Agent launched: LT-4/agent1_theory
[CHECKPOINT] Agent completed: LT-4/agent1_theory
[INFO] Hours spent: X.XX

======================================================================
RESULTS
======================================================================
Hours spent: X.XX
Checkpoint file: .artifacts\lt4_agent1_theory_complete.json
Output artifact: .artifacts\lt4_agent1_theory_output.json
Success: True

Recovery command (if needed):
  /resume LT-4 agent1_theory
```

---

## If Token Limit Hits

**No complicated recovery!**

Just use:
```bash
/recover
```

Then:
```bash
/resume LT-4 agent1_theory
```

Done! Your agent picks up where it left off.

---

## Creating Your Own Batch Files

### Template (Copy This)

```batch
@echo off
REM My Custom Checkpoint Task

python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task YOUR_TASK_ID ^
    --agent YOUR_AGENT_ID ^
    --role "YOUR_ROLE_HERE" ^
    --description "YOUR_DESCRIPTION" ^
    --prompt "YOUR_FULL_PROMPT_HERE"

pause
```

### Steps to Create

1. Open Notepad
2. Copy template above
3. Fill in YOUR_* placeholders
4. Save as `my-task-name.bat` in `.ai_workspace/dev_tools/`
5. Double-click to launch!

---

## Batch File Parameters Explained

```batch
--task LT-4                              # Task ID from roadmap
--agent agent1_theory                    # Unique agent identifier
--role "Lyapunov Proof Specialist"       # What the agent does
--description "Derive proofs"            # Brief task description
--prompt "Your full prompt here..."      # Complete instructions for agent
--type general-purpose                   # Subagent type (general-purpose, Explore, Plan)
--poll-interval 300                      # Check progress every N seconds
--auto-progress                          # Enable auto-polling (default)
--no-auto-progress                       # Disable auto-polling
```

---

## File Organization

```
.ai_workspace/dev_tools/
├── launch-checkpoint-task.bat           # Interactive launcher
├── LAUNCH_TEMPLATE.bat                  # Edit and customize
├── EXAMPLES-launch-checkpoint.bat       # Pre-made examples
├── my-custom-task.bat                   # Your custom task (create this)
├── launch_checkpoint_task.py            # Python backend (don't edit)
├── task_wrapper.py                      # Core system (don't edit)
└── ...
```

---

## Step-by-Step: Create Your First Task

### 1. Open Notepad
Press Windows key, type "Notepad", hit Enter

### 2. Copy This Template
```batch
@echo off
REM My First Checkpoint Task

python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task TEST1 ^
    --agent agent1 ^
    --role "Test Agent" ^
    --description "Test task" ^
    --prompt "Hello world test"

pause
```

### 3. Save File
File → Save As → Navigate to: `D:\Projects\main\.project\dev_tools\`
Filename: `test-my-first-task.bat`

### 4. Double-Click File
Open File Explorer → Navigate to `.project\dev_tools\`
Double-click `test-my-first-task.bat`

### 5. Check Results
Command window shows:
```
[OK] Task completed successfully!
Checkpoint file: .artifacts\test1_agent1_complete.json
Recovery command: /resume TEST1 agent1
```

**Done!** Your first checkpoint task is complete!

---

## Troubleshooting

### Error: "python is not recognized"

**Solution:** Make sure you're running from project root:
```
cd D:\Projects\main
```

Or edit batch file and use full python path:
```batch
python ".project\dev_tools\launch_checkpoint_task.py" ^
```

### Error: "launch_checkpoint_task.py not found"

**Solution:** Make sure you're in the right directory:
```
D:\Projects\main\.project\dev_tools\launch-checkpoint-task.bat
```

### Command window closes too fast

**Solution:** Keep `pause` at the end of your batch file:
```batch
pause
```

This waits for you to press a key before closing.

---

## Advanced: Command-Line Usage

If you prefer command line, you can also run:

```bash
cd D:\Projects\main

REM Simple format
.\project\dev_tools\launch-checkpoint-task.bat LT-4 agent1_theory "Theory Specialist" "Your prompt"

REM Or Python directly
python .project\dev_tools\launch_checkpoint_task.py --task LT-4 --agent agent1 --role "Role" --prompt "Prompt"
```

---

## Summary

**Pick Your Method:**

1. **Super Easy:** Double-click → Answer prompts → Done
   - Use: `launch-checkpoint-task.bat`

2. **Customizable:** Edit file → Save → Double-click → Done
   - Use: `LAUNCH_TEMPLATE.bat`

3. **Quick Examples:** Double-click → Pick example → Done
   - Use: `EXAMPLES-launch-checkpoint.bat`

**All three methods:**
- ✅ Automatically create checkpoints
- ✅ Save output to `academic/`
- ✅ Enable `/recover` and `/resume` commands
- ✅ Show recovery instructions

**No Python knowledge needed. Just double-click!**

---

**Questions?** See `.ai_workspace/dev_tools/QUICK_START_CHECKPOINT.md` for more details.
