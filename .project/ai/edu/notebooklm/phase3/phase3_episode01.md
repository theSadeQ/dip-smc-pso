# Episode 1: Environment Setup and Your First Command

**Duration**: 18-20 minutes | **Learning Time**: 2.5 hours | **Difficulty**: Beginner

**Part of**: Phase 3.1 - Running Your First Simulation (Part 1 of 8)

---

## Opening Hook

You've spent weeks learning theory - control systems, PID, sliding mode control, PSO optimization, the double-inverted pendulum structure. Now it's time to TOUCH the code. To run a simulation. To see those pendulums balance on your screen. But before we can make magic happen, we need to set the stage: activate your virtual environment, navigate to the project directory, and understand the command-line interface. Think of this episode as checking your gear before climbing a mountain. Let's make sure everything is ready!

---

## Why Environment Setup Matters

**The Problem Without Virtual Environments**:

Imagine your computer is a shared workshop. Python projects are like workbenches, each needing different tools. Project A needs NumPy version one-point-twenty-one. Project B needs NumPy version one-point-eighteen (older version for compatibility). If you install both globally, they CONFLICT - only one version can be active at a time.

**The Solution: Virtual Environments**:

A virtual environment is like a portable toolbox. Each project gets its own isolated copy of Python and its dependencies. You can have NumPy one-point-twenty-one in Project A's toolbox, and NumPy one-point-eighteen in Project B's toolbox. No conflicts!

**For This Project**:

We created a virtual environment in Phase 1 (remember Phase 1.3?). Now we need to ACTIVATE it before running simulations. Activation tells your terminal: "Hey, use THIS project's toolbox, not the global one."

---

## Step 1: Navigate to the Project Directory

**Where Is Your Project?**

You installed the DIP-SMC-PSO project somewhere on your computer. Common locations:

**Windows**:
- `C:\Users\YourName\Documents\Projects\dip-smc-pso`
- `D:\Projects\dip-smc-pso`

**Mac/Linux**:
- `/Users/YourName/projects/dip-smc-pso`
- `~/projects/dip-smc-pso` (tilde is shorthand for your home directory)

**How to Get There**:

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and use the `cd` command:

**Windows Example**:
```
cd D:\Projects\dip-smc-pso
```

Let me spell that out:
- `c-d` (change directory command)
- `D colon backslash Projects backslash dip hyphen s-m-c hyphen p-s-o`

**Mac/Linux Example**:
```
cd ~/projects/dip-smc-pso
```

That's:
- `c-d`
- `tilde slash projects slash dip hyphen s-m-c hyphen p-s-o`

**Verify You're There**:

Run the `ls` command (macOS/Linux) or `dir` command (Windows):

```
ls
```

You should see files like:
- `simulate.py` (the main script we'll run!)
- `config.yaml` (configuration file)
- `requirements.txt` (list of dependencies)
- `src/` (source code directory)
- `venv/` (virtual environment directory)

If you DON'T see these, you're in the wrong directory. Navigate up or down using:
- `cd ..` (go up one directory)
- `cd folder_name` (go into a subdirectory)

**Tip**: Use tab-completion! Type `cd dip` then press TAB - the terminal will auto-complete to `cd dip-smc-pso/`.

---

## Step 2: Activate the Virtual Environment

**The Activation Command**:

**Windows (Command Prompt)**:
```
venv\Scripts\activate.bat
```

That's:
- `venv backslash Scripts backslash activate dot b-a-t`

**Windows (PowerShell)**:
```
venv\Scripts\Activate.ps1
```

That's:
- `venv backslash Scripts backslash Activate dot p-s-one`

**Mac/Linux**:
```
source venv/bin/activate
```

That's:
- `source venv slash bin slash activate`

**What Happens**:

After running the activation command, your terminal prompt changes! You'll see `(venv)` at the beginning:

**Before activation**:
```
C:\Projects\dip-smc-pso>
```

**After activation**:
```
(venv) C:\Projects\dip-smc-pso>
```

That `(venv)` prefix is your confirmation - the virtual environment is ACTIVE!

**Troubleshooting**:

**Error: "activate.bat is not recognized"**
- You're not in the project directory. Run `cd` to your project folder first.

**Error: "Execution of scripts is disabled on this system" (PowerShell)**
- PowerShell's security policy blocks scripts by default. Solution:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  Then try activating again.

**Error: "Permission denied" (Mac/Linux)**
- The activate script isn't executable. Fix with:
  ```
  chmod +x venv/bin/activate
  source venv/bin/activate
  ```

---

## Step 3: Verify Package Installation

**Check Python Version**:

Run:
```
python --version
```

**Windows users**: Use `python` NOT `python3` (python3 doesn't exist on Windows).

**Mac/Linux users**: Use `python3` if you have multiple Python versions installed.

You should see:
```
Python 3.9.7
```

Or any version three-point-nine or higher. If you see Python two-point-seven, you're using the wrong Python!

**Check Installed Packages**:

Run:
```
python -c "import numpy, scipy, matplotlib; print('OK - All packages installed')"
```

Let me explain this command:
- `python` - Run Python interpreter
- `dash c` - Execute the following code
- `"import numpy, scipy, matplotlib; print('OK - All packages installed')"` - Import key packages and print success message

If you see `OK - All packages installed`, you're good!

**If You Get ImportError**:

```
ImportError: No module named 'numpy'
```

Your packages aren't installed. Fix with:
```
pip install -r requirements.txt
```

This reads `requirements dot txt` (a list of all dependencies) and installs them. It'll take one to two minutes.

---

## Step 4: Understanding the Project Structure

Before running simulations, let's tour the project layout. Run:

```
ls -l
```

(On Windows with Command Prompt, use `dir` instead)

**What You See**:

```
dip-smc-pso/
├── simulate.py           # ← YOU WILL RUN THIS
├── streamlit_app.py      # Web interface (Phase 4)
├── config.yaml           # Configuration file
├── requirements.txt      # Dependencies list
├── README.md             # Project documentation
├── src/                  # Source code (controllers, plant, optimizer)
│   ├── controllers/      # SMC implementations
│   ├── plant/            # DIP dynamics
│   ├── optimizer/        # PSO tuner
│   └── utils/            # Helper functions
├── tests/                # Test suite
├── docs/                 # Documentation
└── venv/                 # Virtual environment (active!)
```

**Key Files**:

- **simulate.py**: The main entry point. This is the script you'll run to start simulations.
- **config.yaml**: Stores all configuration (controller gains, plant parameters, simulation settings). You'll edit this in Episode 5.
- **src/controllers/**: Python files implementing Classical SMC, Super-Twisting, Adaptive, Hybrid controllers.
- **src/plant/**: DIP dynamics equations (the physics).
- **src/optimizer/**: PSO optimization for automatic gain tuning.

**You Don't Need to Understand the Code Yet**:

In Phase 3, you're a USER of the system. You run simulations and interpret results. In Phase 4, you'll dive into the code itself. For now, just know WHERE things are.

---

## Step 5: The Help Command - Your First Interaction

**Run This**:

```
python simulate.py --help
```

Let me spell that:
- `python simulate dot p-y space dash dash help`

**What You See** (abbreviated):

```
usage: simulate.py [options]

Double-Inverted Pendulum Simulation with Sliding Mode Control

Options:
  --ctrl CONTROLLER     Controller type: classical_smc, sta_smc, adaptive_smc, hybrid_adaptive_sta_smc
  --plot                Show plots after simulation
  --save FILE           Save results to JSON file
  --run-pso             Run PSO optimization to find optimal gains
  --config FILE         Use custom configuration file (default: config.yaml)
  --print-config        Print current configuration and exit
  -h, --help            Show this help message and exit

Examples:
  python simulate.py --ctrl classical_smc --plot
  python simulate.py --ctrl sta_smc --save results.json
  python simulate.py --ctrl adaptive_smc --run-pso
```

**Let's Decode This**:

**`--ctrl CONTROLLER`**:
- Selects which controller to use
- Options: `classical_smc`, `sta_smc`, `adaptive_smc`, `hybrid_adaptive_sta_smc`
- Example: `--ctrl classical_smc`

**`--plot`**:
- Shows plots after simulation (opens a new window with six subplots)
- Use this to SEE the results visually

**`--save FILE`**:
- Saves simulation results to a JSON file
- Example: `--save my_results.json`
- Useful for comparing multiple runs

**`--run-pso`**:
- Runs Particle Swarm Optimization to automatically find optimal controller gains
- Takes ten to twenty minutes
- We'll use this in Episode 6

**`--config FILE`**:
- Uses a custom configuration file instead of the default `config.yaml`
- Example: `--config my_custom_config.yaml`

**`--print-config`**:
- Prints the current configuration to the terminal
- Doesn't run a simulation, just shows parameters
- Useful for checking what gains are active

---

## Step 6: Print Current Configuration

Before running a simulation, let's see what the default configuration looks like:

```
python simulate.py --print-config
```

**Output** (shortened):

```
=== DIP System Configuration ===

Plant Parameters:
  Cart mass: 1.0 kg
  Pendulum 1 mass: 0.1 kg
  Pendulum 1 length: 0.5 m
  Pendulum 2 mass: 0.1 kg
  Pendulum 2 length: 0.5 m
  Gravity: 9.81 m/s²
  Friction coefficient: 0.01

Classical SMC Gains:
  k1: 10.0
  k2: 5.0
  k3: 8.0
  k4: 3.0
  k5: 15.0
  eta: 2.0
  Boundary layer: 0.1

Simulation Settings:
  Duration: 10.0 seconds
  Timestep: 0.01 seconds (100 Hz control loop)
  Initial disturbance: theta1=0.1 rad, theta2=0.1 rad
```

**What This Means**:

- **Plant Parameters**: Physical properties of the DIP system (masses, lengths, gravity)
- **Controller Gains**: Six numbers (k1 through k5, eta) that determine controller behavior
- **Boundary Layer**: Parameter to reduce chattering (smooth the control signal)
- **Simulation Settings**: How long to simulate (ten seconds), time step (zero-point-zero-one seconds = ten millisecond updates = one hundred Hertz control frequency)
- **Initial Disturbance**: Starting condition (both pendulums tilted zero-point-one radians = five-point-seven degrees)

**Don't Worry About the Numbers Yet**:

In Episode 5, you'll learn what each parameter does and how to change them. For now, just know this is the configuration the simulator will use.

---

## Step 7: The Simplest Simulation Command

**You're Ready!** Let's run your first simulation:

```
python simulate.py --ctrl classical_smc --plot
```

Let me break this down phonetically:
- `python` - The Python interpreter
- `simulate dot p-y` - The main script
- `dash dash ctrl` - Controller option
- `classical underscore s-m-c` - Controller name (classical sliding mode control)
- `dash dash plot` - Show plots

**What Happens**:

1. Script loads `config.yaml`
2. Creates Classical SMC controller with default gains
3. Creates DIP plant (cart plus two pendulums)
4. Sets initial state (small disturbance)
5. Runs simulation loop (one thousand time steps, ten seconds total)
6. Generates six plots
7. Opens plot window

**Console Output**:

```
[INFO] Starting simulation...
[INFO] Controller: Classical SMC
[INFO] Initial state: [0.0, 0.0, 0.1, 0.0, 0.1, 0.0]
[INFO] Simulation time: 10.0 seconds
[INFO] Timestep: 0.01 seconds (1000 steps)

Simulating: [====================] 100% (1000/1000) ETA: 0s

[INFO] Simulation complete in 2.3 seconds
[INFO] Performance Metrics:
  - Settling time: 4.2 seconds
  - Max overshoot: 0.03 rad (1.7 degrees)
  - Control effort: 125.4 J
  - Chattering index: 0.42

[INFO] Generating plots...
[OK] Plots displayed. Close plot window to exit.
```

**A new window appears** with six subplots showing:
1. Cart position vs time
2. Pendulum 1 angle vs time
3. Pendulum 2 angle vs time
4. Cart velocity vs time
5. Pendulum angular velocities vs time
6. Control force vs time

**Close the plot window** to return to the terminal.

**Congratulations!** You just ran your first simulation! 🎉

---

## Common Mistakes and How to Avoid Them

**Mistake 1: Running Without Activating Virtual Environment**

**What happens**: `ModuleNotFoundError: No module named 'numpy'`

**Why**: You're using the global Python, which doesn't have the packages installed.

**Fix**: Activate the virtual environment first (see Step 2).

---

**Mistake 2: Typing Controller Name Wrong**

**What happens**: `ValueError: Unknown controller type 'classical'`

**Why**: Controller names are case-sensitive and use underscores.

**Correct names**:
- `classical_smc` (NOT `classical` or `ClassicalSMC`)
- `sta_smc` (NOT `sta` or `STA_SMC`)
- `adaptive_smc`
- `hybrid_adaptive_sta_smc`

**Fix**: Use exact names from `--help` output.

---

**Mistake 3: Forgetting the `--plot` Flag**

**What happens**: Simulation runs, but no plots appear. You just see metrics in the terminal.

**Why**: The `--plot` flag is required to display plots.

**Fix**: Add `--plot` to your command:
```
python simulate.py --ctrl classical_smc --plot
```

---

**Mistake 4: Running From Wrong Directory**

**What happens**: `FileNotFoundError: [Errno 2] No such file or directory: 'config.yaml'`

**Why**: The script looks for `config.yaml` in the current directory. You're not in the project folder.

**Fix**: Navigate to the project directory first (`cd /path/to/dip-smc-pso`), THEN run the script.

---

## Deactivating the Virtual Environment (Optional)

**When you're done**:

If you want to exit the virtual environment (to work on a different project or close the terminal), run:

```
deactivate
```

The `(venv)` prefix disappears, and you're back to the global Python environment.

**Next time you work on this project**:
1. Navigate to the project directory
2. Activate the virtual environment again
3. Run simulations

---

## Key Takeaways

**1. Virtual Environments Isolate Dependencies**: Each project gets its own toolbox, no conflicts.

**2. Activation is Mandatory**: Always activate before running simulations. Look for the `(venv)` prefix.

**3. The Project Structure**: `simulate.py` is the entry point, `config.yaml` stores settings, `src/` contains the code.

**4. The Help Command is Your Friend**: `python simulate.py --help` shows all options.

**5. The Simplest Command**: `python simulate.py --ctrl classical_smc --plot` runs a simulation and shows plots.

**6. Common Mistakes Are Fixable**: Wrong directory, wrong controller name, forgot `--plot`, forgot to activate venv.

---

## Pronunciation Guide

- **Virtual environment**: VER-choo-ul en-VY-run-ment
- **YAML**: YAM-ul (file format for configuration)
- **Activate**: AK-tih-vate
- **Deactivate**: dee-AK-tih-vate
- **Underscore**: UN-der-score (the `_` character)

---

## Pause and Reflect: You're Ready!

You've now:
✅ Navigated to the project directory
✅ Activated the virtual environment
✅ Verified package installation
✅ Understood the project structure
✅ Learned the command-line interface
✅ Ran your first simulation

**What's next?**

In **Episode 2**, we'll dissect those six plots. You'll learn to read each curve like a story - where the pendulums started, how the controller responded, when they settled, and what "good" performance looks like. We'll spend twenty-five minutes doing a DEEP dive into plot interpretation. Get ready to become a simulation plot expert!

---

## What's Next

In **Episode 2**, we'll take the six plots from your first simulation and analyze them in DETAIL:
- Verbal descriptions of each plot's shape
- What each line means physically
- How to spot good vs poor performance
- The four performance metrics decoded
- Building visual intuition for control system behavior

You'll learn to read plots like a pro!

---

**Episode 1 of 8** | Phase 3: Hands-On Learning

**Previous**: [Phase 2 Complete!](../../phase2/README.md) | **Next**: [Episode 2 - Understanding Simulation Results](phase3_episode02.md)

---

**Usage**: Upload to NotebookLM for podcast discussion of environment setup and CLI basics.

---

## For NotebookLM: Audio Rendering Notes

**Pacing**: Slow down when spelling out commands (listeners need time to type along)

**Repetition**: Repeat activation commands twice (muscle memory reinforcement)

**Platform Clarity**: Clearly distinguish Windows vs Mac/Linux instructions with audio cues ("Windows users...", "Mac and Linux users...")

**Command Spelling**: Spell out special characters:
- Underscore as "underscore"
- Dash/hyphen as "dash" or "hyphen"
- Backslash as "backslash"
- Forward slash as "slash"

**Error Prevention**: Emphasize common mistakes with warning tone ("Be careful not to...")

**Encouragement**: End with motivational tone - listeners should feel confident and ready
