# Episode 7: Troubleshooting Guide - Fixing Common Errors

**Duration**: 14-16 minutes | **Learning Time**: 2 hours | **Difficulty**: Beginner

**Part of**: Phase 3.5 - Troubleshooting Common Issues (Part 7 of 8)

---

## Opening Hook

You've run simulations, compared controllers, tweaked configs, optimized with PSO. But what happens when something goes WRONG? ModuleNotFoundError. YAML syntax error. Simulation diverges. Plots don't show. Welcome to the real world of software! Errors are inevitable, but they're also FIXABLE - if you know where to look. In this episode, I'll walk you through the five most common errors, explain what they mean, and show you step-by-step fixes. By the end, you'll be a confident troubleshooter!

---

## Error 1: ModuleNotFoundError - The Missing Package Problem

**What You See**:

```
Traceback (most recent call last):
  File "simulate.py", line 5, in <module>
    import numpy as np
ModuleNotFoundError: No module named 'numpy'
```

**What It Means**:

Python can't find the NumPy package. This means:
1. You're NOT in the virtual environment, OR
2. Packages aren't installed in the virtual environment

**How to Fix**:

**Step 1: Check if Virtual Environment is Active**

Look at your terminal prompt. Do you see `(venv)` at the beginning?

**YES** - Virtual environment is active. Go to Step 2.

**NO** - Activate it first:

Windows (Command Prompt):
```
venv\Scripts\activate.bat
```

Windows (PowerShell):
```
venv\Scripts\Activate.ps1
```

Mac/Linux:
```
source venv/bin/activate
```

**Step 2: Install Packages**

```
pip install -r requirements.txt
```

This installs all dependencies listed in `requirements.txt`. Takes one to two minutes.

**Step 3: Verify Installation**

```
python -c "import numpy, scipy, matplotlib; print('OK')"
```

If you see `OK`, packages are installed correctly!

**Why This Happens**:

You forgot to activate the virtual environment, or you're in a new terminal session that doesn't have it activated.

**Prevention**:

ALWAYS activate the virtual environment before running simulations. Make it muscle memory!

---

## Error 2: YAML Syntax Error - The Indentation Nightmare

**What You See**:

```
yaml.scanner.ScannerError: mapping values are not allowed here
  in "config.yaml", line 15, column 20
```

Or:

```
yaml.parser.ParserError: while parsing a block mapping
  expected <block end>, but found '<block mapping start>'
  in "config.yaml", line 22, column 3
```

**What It Means**:

Your `config.yaml` file has a syntax error. YAML is whitespace-sensitive - incorrect indentation breaks parsing.

**Common Mistakes**:

**Mistake 1: Using Tabs Instead of Spaces**

```yaml
plant:
→   cart_mass: 1.0  # ← This is a TAB (BAD!)
```

Should be:

```yaml
plant:
  cart_mass: 1.0  # ← Two SPACES (GOOD!)
```

**Mistake 2: Inconsistent Indentation**

```yaml
plant:
  cart_mass: 1.0
   pendulum1_mass: 0.1  # ← Three spaces (BAD! Should be two)
```

**Mistake 3: Missing Space After Colon**

```yaml
plant:
  cart_mass:1.0  # ← No space after colon (BAD!)
```

Should be:

```yaml
plant:
  cart_mass: 1.0  # ← Space after colon (GOOD!)
```

**How to Fix**:

**Step 1: Open config.yaml in a Text Editor**

Use an editor that shows whitespace characters (VS Code, Sublime Text, Notepad++).

**Step 2: Find the Offending Line**

The error message tells you the line number: `"in config.yaml, line 15"`.

Go to line 15.

**Step 3: Check Indentation**

- Are you using spaces (not tabs)?
- Is indentation consistent (all two-space increments)?
- Is there a space after every colon?

**Step 4: Validate YAML Online**

Copy-paste your `config.yaml` into https://www.yamllint.com/

It'll highlight syntax errors with helpful messages.

**Step 5: Restore from Backup**

If you're stuck, restore the default config:

```
git checkout config.yaml
```

Or copy from backup:

```
cp config_backup.yaml config.yaml
```

**Prevention**:

- Use an editor with YAML syntax highlighting
- Enable "show whitespace" in your editor
- Use spaces, NEVER tabs
- Validate after major changes

---

## Error 3: Simulation Diverges (NaN Values)

**What You See**:

```
RuntimeWarning: invalid value encountered in multiply
  state = state + derivative * dt
RuntimeError: Simulation diverged (NaN values detected at t=2.3s)
```

And plots show:

```
theta1: [0.1, 0.15, 0.25, 0.45, 1.2, inf, nan, nan...]
```

**What It Means**:

The simulation became unstable. The pendulums fell faster than the controller could catch them, angles grew without bound, and numerical integration failed (division by zero, NaN = "Not a Number").

**Common Causes**:

1. **Controller gains too low**: Insufficient control authority
2. **Plant parameters extreme**: Too heavy, too long, too much friction
3. **Initial disturbance too large**: System started outside basin of attraction
4. **Time step too large**: Numerical integration inaccurate

**How to Fix**:

**Step 1: Check config.yaml**

Did you modify it recently? Restore defaults:

```
git checkout config.yaml
```

Run simulation again. If it works, your modifications were the problem.

**Step 2: Reduce Initial Disturbance**

```yaml
simulation:
  initial_disturbance:
    theta1: 0.05  # Smaller disturbance (was 0.1 or larger)
    theta2: 0.05
```

**Step 3: Increase Controller Gains**

```yaml
controllers:
  classical_smc:
    gains: [15.0, 7.5, 12.0, 4.5, 22.5, 3.0]  # 50% higher
```

**Step 4: Check Plant Parameters**

Are masses or lengths unreasonably large?

```yaml
plant:
  pendulum1_mass: 0.1  # Should be reasonable (not 10.0!)
  pendulum1_length: 0.5  # Should be reasonable (not 5.0!)
```

**Step 5: Reduce Time Step (Last Resort)**

```yaml
simulation:
  timestep: 0.005  # Half the default (was 0.01)
```

Smaller time step = more accurate integration, but slower simulation.

**Prevention**:

- Don't make extreme parameter changes
- Test with small disturbances first
- Use PSO to find stable gains

---

## Error 4: Plots Don't Show - The Matplotlib Backend Problem

**What You See**:

Simulation runs successfully, metrics print to console, but NO plot window appears.

**What It Means**:

Matplotlib's backend can't display plots (headless environment, or backend misconfigured).

**How to Fix**:

**Step 1: Use --save Instead**

Save plots to a file instead of displaying:

```
python simulate.py --ctrl classical_smc --save results.json
```

Then open `results.json` in a plotting tool or Python script.

**Step 2: Change Matplotlib Backend**

Windows (Command Prompt):
```
set MPLBACKEND=TkAgg
python simulate.py --ctrl classical_smc --plot
```

Mac/Linux:
```
export MPLBACKEND=TkAgg
python simulate.py --ctrl classical_smc --plot
```

**Step 3: Check if Running Remotely**

If you're SSH'd into a remote server (no graphical interface), plots CAN'T display. Use `--save` or forward X11 (advanced).

**Prevention**:

- Test plotting early (run a simple simulation first)
- If remote, always use `--save`

---

## Error 5: Controller Not Found - The Typo Problem

**What You See**:

```
ValueError: Unknown controller type: 'classical'
```

Or:

```
KeyError: 'ClassicalSMC' not found in controller factory
```

**What It Means**:

You typed the controller name wrong. Controller names are case-sensitive and use underscores.

**Correct Names**:

- `classical_smc` (NOT `classical`, `ClassicalSMC`, or `classical-smc`)
- `sta_smc` (NOT `sta`, `STA`, or `STA-SMC`)
- `adaptive_smc`
- `hybrid_adaptive_sta_smc` (long name!)

**How to Fix**:

**Step 1: Check Spelling**

Look at your command:

```
python simulate.py --ctrl classical_smc --plot
```

Is `classical_smc` spelled exactly right? Underscores, not hyphens?

**Step 2: List Available Controllers**

```
python simulate.py --help
```

Under `--ctrl CONTROLLER`, you'll see the list of valid names.

**Prevention**:

- Copy-paste controller names from help output
- Use tab-completion if your shell supports it

---

## General Debugging Strategy

**When You Encounter ANY Error**:

**Step 1: Read the Error Message Carefully**

Error messages are your FRIEND! They tell you:
- What went wrong (ModuleNotFoundError, ValueError, RuntimeError)
- Where it happened (file name, line number)
- Sometimes, HOW to fix it

**Step 2: Check the Obvious**:

- Is virtual environment activated? (`(venv)` in prompt?)
- Are you in the project directory? (`ls` shows `simulate.py`?)
- Did you recently edit `config.yaml`? (Restore it!)

**Step 3: Search Online**:

Copy-paste the error message into Google or Stack Overflow. Add context:
```
"ModuleNotFoundError: No module named 'numpy'" python virtual environment
```

Someone has likely encountered the same error!

**Step 4: Check Documentation**:

- `docs/guides/getting-started.md`
- `README.md`
- Phase 3 roadmap (this episode!)

**Step 5: Ask for Help**:

- GitHub Discussions
- Stack Overflow (tag: `[python] [control-systems]`)
- Course forums (if this is coursework)

**What to Include When Asking**:
- Full error message (copy-paste from terminal)
- What you were trying to do
- What you tried already
- Your setup (OS, Python version)

---

## Key Takeaways

**1. Errors Are Normal**: Every developer encounters them daily. It's part of the process!

**2. Error Messages Are Helpful**: Read them carefully - they tell you what's wrong.

**3. Five Common Errors**: ModuleNotFoundError, YAML syntax, simulation divergence, plots don't show, controller not found.

**4. Systematic Debugging**: Check obvious things first, then investigate deeper.

**5. Prevention**: Activate venv, validate YAML, test with defaults before extreme modifications.

---

## Pronunciation Guide

- **ModuleNotFoundError**: MOD-yool-not-found-error
- **YAML**: YAM-ul
- **NaN**: Not a Number (N-A-N)
- **Traceback**: TRACE-back (error message stack)

---

## What's Next

In **Episode 8** (finale!), we'll wrap up Phase 3:
- Celebrate what you've accomplished
- Review the five sub-phases
- Self-assessment checklist
- Preview Phase 4 (advancing skills, reading code, understanding math)
- Final tips for continued learning

You're almost done with hands-on learning!

---

**Episode 7 of 8** | Phase 3: Hands-On Learning

**Previous**: [Episode 6 - PSO Optimization](phase3_episode06.md) | **Next**: [Episode 8 - Phase 3 Wrap-Up](phase3_episode08.md)

---

**Usage**: Upload to NotebookLM for podcast discussion of troubleshooting common simulation errors.

---

## For NotebookLM: Audio Rendering Notes

**Error Messages**: Use robotic/monotone voice for error text to distinguish from narration

**Debugging Steps**: Use clear, step-by-step tone - "Step one: PAUSE. Step two: PAUSE."

**Emphasis**: Highlight fixes - "THIS is how you solve it!"

**Encouragement**: Use reassuring tone - "Don't panic! This is fixable."

**Prevention Tips**: Use advisory tone - "Here's how to avoid this in the future..."

**Real-World Analogies**: Errors are like car warning lights - they tell you what's wrong!
