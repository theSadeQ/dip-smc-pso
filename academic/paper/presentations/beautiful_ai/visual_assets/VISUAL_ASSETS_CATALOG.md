# Visual Assets Catalog for Beautiful.ai Phase 1 Presentations
**Purpose:** Reference guide for all visual elements needed in Phase 1 slide decks (E001-E005)

**Source:** Extracted from podcast cheatsheet PDFs and episode markdown descriptions

---

## Asset Organization

```
visual_assets/
├── VISUAL_ASSETS_CATALOG.md (this file)
├── descriptions/            (text descriptions for Beautiful.ai prompts)
│   ├── E001_diagrams.md
│   ├── E002_diagrams.md
│   ├── E003_diagrams.md
│   ├── E004_diagrams.md
│   └── E005_diagrams.md
└── source_references/       (references to LaTeX PDF sources)
    ├── phase1_foundational_pdfs.md
    └── extraction_notes.md
```

---

## E001: Project Overview - Visual Assets

### ASSET 1.1: Double Inverted Pendulum System Diagram
**Slide:** E001 Slide 2
**Type:** Technical schematic
**Description:**
- Cart on horizontal track (blue rectangle)
- Pendulum 1 (bottom link, green line from cart to joint)
- Pendulum 2 (top link, orange line from joint to tip)
- Angle labels: θ₁ (pendulum 1 from vertical), θ₂ (pendulum 2 from vertical)
- Force arrow F (horizontal, on cart, orange)
- Coordinate system (x-axis horizontal, vertical reference line)
**Beautiful.ai Prompt:** "System diagram with cart, two connected pendulums, angle labels, force arrow"
**Source:** E001 PDF page 1, Figure: DIP System Schematic

### ASSET 1.2: SpaceX Rocket Landing Comparison
**Slide:** E001 Slide 2, E002 Slide 1
**Type:** Real-world photo/icon
**Description:** SpaceX Falcon 9 booster in vertical landing phase (stock photo or simplified icon)
**Beautiful.ai Prompt:** "Rocket in vertical position with engines firing downward, stability control"
**Source:** Public domain rocket landing image or simplified vector icon

### ASSET 1.3: Controller Hierarchy Pyramid
**Slide:** E001 Slide 4
**Type:** Organizational diagram
**Description:**
- 4-tier pyramid showing sophistication levels
- Tier 1 (bottom, largest): Classical SMC (blue box)
- Tier 2: Super-Twisting (green box, medium)
- Tier 3: Adaptive + Hybrid + Conditional (3 orange boxes)
- Tier 4 (top): Swing-Up + MPC (2 purple boxes)
- Arrows labeled "increasing sophistication"
- Performance metric callouts (e.g., "+21.4%" for Hybrid)
**Beautiful.ai Prompt:** "Pyramid diagram with 4 tiers, color-coded boxes, performance labels"
**Source:** E001 PDF page 2, derived from text descriptions

### ASSET 1.4: Model Quality Settings Comparison
**Slide:** E001 Slide 5
**Type:** Comparison table/icons
**Description:**
- 3 columns: Simplified, Full, Low-Rank
- Icons: Speedometer (fast), Trophy (accurate), Lightning (balanced)
- Star ratings: Accuracy (★★☆, ★★★★★, ★★★☆)
- Speed ratings: ⚡⚡⚡⚡⚡, ⚡, ⚡⚡⚡⚡
**Beautiful.ai Prompt:** "Three-column comparison with icons and star ratings"
**Source:** E001 PDF page 2, model comparison section

### ASSET 1.5: PSO Swarm Visualization
**Slide:** E001 Slide 6
**Type:** Animated diagram
**Description:**
- 30-50 blue dots (particles) in 3D search space
- Contour map background showing "cost function landscape" (hills/valleys)
- Arrows from each particle showing movement direction
- Golden dot showing "global best" location
- Convergence arrows showing particles clustering
**Beautiful.ai Prompt:** "Particle swarm in 3D cost landscape with convergence arrows"
**Source:** E001 PDF page 3, PSO visualization concept

### ASSET 1.6: Workflow Timeline
**Slide:** E001 Slide 7
**Type:** Process timeline
**Description:**
- 5 connected boxes (left to right)
- Phase 1 (blue): "Getting Lab Ready, 15 min"
- Phase 2 (green): "First Experiments, 30 min"
- Phase 3 (orange): "Intelligent Tuning, 2-4 hrs"
- Phase 4 (purple): "Serious Benchmarking, 1-2 days"
- Phase 5 (red): "Research & Publication, weeks-months"
- Arrows connecting phases
- Cumulative timeline at bottom: 15m → 4h → 2d → weeks → publication
**Beautiful.ai Prompt:** "5-phase timeline with duration estimates and cumulative progress bar"
**Source:** E001 PDF page 4, workflow section

---

## E002: Control Theory Fundamentals - Visual Assets

### ASSET 2.1: State Vector Dashboard
**Slide:** E002 Slide 2
**Type:** Infographic
**Description:**
- 6 dashboard gauges/indicators arranged in grid
- Cart position (meter, horizontal position)
- Cart velocity (speedometer, m/s)
- θ₁ angle (protractor, radians)
- θ₁' angular velocity (tachometer, rad/s)
- θ₂ angle (protractor)
- θ₂' angular velocity (tachometer)
- Each with current value display and units
**Beautiful.ai Prompt:** "Dashboard with 6 gauges showing state variables"
**Source:** E002 PDF page 1, state-space section

### ASSET 2.2: Lyapunov Marble-in-Bowl 3D Plot
**Slide:** E002 Slide 3
**Type:** 3D visualization
**Description:**
- Bowl-shaped surface (blue gradient, darker at bottom)
- Marble (orange sphere) at various positions
- Trajectory spiral showing marble rolling inward
- Gravity vector (downward arrow)
- Energy contour lines on bowl surface
- Labels: "Equilibrium (V=0)" at bottom, "Higher energy" at rim
**Beautiful.ai Prompt:** "3D bowl surface with marble trajectory spiraling to bottom center"
**Source:** E002 PDF page 2, Lyapunov stability visualization

### ASSET 2.3: Sliding Surface Guard Rail Mountain
**Slide:** E002 Slide 4
**Type:** Conceptual diagram
**Description:**
- Mountain slope (gray) in profile view
- Guardrail path (golden line) from top to cabin at bottom
- Hiker icon at 3 positions:
  1. Off-path (red marker, "Reaching phase")
  2. Approaching path (yellow marker, arrow toward path)
  3. On path sliding down (green marker, "Sliding phase")
- Wind gust icons (disturbances)
- Cabin at bottom (equilibrium/target)
**Beautiful.ai Prompt:** "Mountain profile with guardrail path, hiker positions, wind icons"
**Source:** E002 PDF page 3, SMC analogy illustration

### ASSET 2.4: Chattering Waveform Comparison
**Slide:** E002 Slide 6
**Type:** Side-by-side waveforms
**Description:**
- Left: Classical SMC control signal (jagged, rapid oscillations)
  - High-frequency switching visible
  - Red color indicating problem
  - Label: "Harsh buzzing sound"
- Right: Continuous approximation (smooth curve)
  - Green color indicating solution
  - Label: "Smooth, continuous"
- Time axis (0-5 seconds)
- Amplitude axis (-50 to +50 N)
**Beautiful.ai Prompt:** "Two waveform plots side-by-side, left jagged, right smooth"
**Source:** E002 PDF page 4, chattering section

### ASSET 2.5: Super-Twisting Phase Plane
**Slide:** E002 Slide 7
**Type:** Phase plane trajectory plot
**Description:**
- 2D plot: sliding surface s (horizontal) vs. ṡ (vertical)
- Classical SMC trajectory (red, oscillating approach to origin)
- Super-Twisting trajectory (green, smooth spiral to origin)
- Origin (0,0) marked with star (equilibrium)
- Grid background
- Legend distinguishing Classical vs. STA
**Beautiful.ai Prompt:** "Phase plane with two trajectories converging to origin, one jagged, one smooth"
**Source:** E002 PDF page 4, STA visualization

### ASSET 2.6: Adaptive Gain Evolution
**Slide:** E002 Slide 8
**Type:** Time-series plot
**Description:**
- Plot showing gain value over time (0-10 seconds)
- Gain starts low, increases when error is large, decreases when error is small
- Dead zone regions shaded (gray)
- Annotations: "Large error → increase", "Small error → decrease"
**Beautiful.ai Prompt:** "Line plot showing adaptive gain changing over time with annotations"
**Source:** E002 PDF page 5, adaptive SMC section

---

## E003: Plant Models and Dynamics - Visual Assets

### ASSET 3.1: Lagrangian Energy Surfaces
**Slide:** E003 Slide 2
**Type:** 3D energy plot
**Description:**
- Kinetic energy surface T (blue, increasing with velocity)
- Potential energy surface V (red, increasing with height)
- Lagrangian L = T - V (purple, combined surface)
- Axes: generalized coordinates q, velocities q̇, energy
**Beautiful.ai Prompt:** "3D surface plots showing kinetic, potential, and Lagrangian energy"
**Source:** E003 PDF page 1, Lagrangian mechanics

### ASSET 3.2: Small Angle Approximation Graph
**Slide:** E003 Slide 3
**Type:** Function comparison plot
**Description:**
- X-axis: angle θ (degrees, -10° to +10°)
- Y-axis: function value
- Two curves:
  - sin(θ) actual (blue curve)
  - θ linear approximation (red straight line)
- Shaded region showing valid approximation range (±5°)
- Divergence beyond ±10° visible
**Beautiful.ai Prompt:** "Graph comparing sin(θ) curve to linear θ approximation, highlighting valid range"
**Source:** E003 PDF page 2, simplified model section

### ASSET 3.3: Complete Force Diagram (Full Nonlinear)
**Slide:** E003 Slide 4
**Type:** Free-body diagram
**Description:**
- Cart with mass M, force F (horizontal)
- Pendulum 1 with mass m₁, length L₁, angle θ₁
  - Gravity m₁g (down)
  - Joint reaction forces Fx₁, Fy₁
  - Coriolis force (curved arrow)
  - Centrifugal force (outward arrow)
- Pendulum 2 similar forces labeled
- Coupling arrows showing interaction between pendulums
- Color-coded: Gravity (green), reactions (blue), inertial (red)
**Beautiful.ai Prompt:** "Detailed force diagram with all forces labeled and color-coded"
**Source:** E003 PDF page 3, full dynamics section

### ASSET 3.4: Mass Matrix Structure
**Slide:** E003 Slide 6
**Type:** Matrix visualization
**Description:**
- 3×3 matrix M(θ) with elements labeled
- Diagonal elements highlighted (inertia terms)
- Off-diagonal elements (coupling terms)
- Angle-dependence indicated (θ₁, θ₂ in elements)
- Color gradient showing magnitude (darker = larger influence)
**Beautiful.ai Prompt:** "3x3 matrix with labeled elements and color gradient"
**Source:** E003 PDF page 3, mass matrix section

### ASSET 3.5: Model Speed Comparison Bar Chart
**Slide:** E003 Slide 7
**Type:** Horizontal bar chart
**Description:**
- 3 bars showing relative speed:
  - Simplified: 100x (green, longest bar)
  - Low-Rank: 10x (orange, medium bar)
  - Full Nonlinear: 1x (blue, baseline bar)
- Annotations with actual times (e.g., "1 second", "10 seconds", "100 seconds")
**Beautiful.ai Prompt:** "Horizontal bar chart comparing model computation speeds"
**Source:** E003 PDF page 4, performance comparison

---

## E004: PSO Optimization - Visual Assets

### ASSET 4.1: Bird Flock Seeking Food
**Slide:** E004 Slide 2
**Type:** Nature illustration
**Description:**
- Flock of birds (10-15 silhouettes) moving together
- Food source (target) at one location
- Motion arrows showing birds converging
- Individual birds exploring different areas
- Annotations: "Personal best", "Global best"
**Beautiful.ai Prompt:** "Bird flock illustration with movement arrows converging to target"
**Source:** E004 PDF page 1, PSO metaphor

### ASSET 4.2: Particle Velocity/Position Update Diagram
**Slide:** E004 Slide 3
**Type:** Vector diagram
**Description:**
- Current particle position (blue dot)
- Current velocity vector (black arrow)
- Personal best direction (green arrow)
- Global best direction (gold arrow)
- New velocity (purple arrow, weighted combination)
- New position (blue dot moved)
- Equations overlaid: v_{new} = w·v + c₁·(p_best-x) + c₂·(g_best-x)
**Beautiful.ai Prompt:** "Vector diagram showing particle movement with velocity components"
**Source:** E004 PDF page 2, PSO mechanics

### ASSET 4.3: Multi-Objective Trade-Off Triangle
**Slide:** E004 Slide 4
**Type:** Trade-off diagram
**Description:**
- Triangle with 3 vertices:
  - Top: "Fast convergence" (minimize state error)
  - Bottom-left: "Low energy" (minimize control effort)
  - Bottom-right: "Smooth control" (minimize chattering)
- Center point: "Optimal balance" (PSO solution)
- Arrows showing cannot maximize all three simultaneously
**Beautiful.ai Prompt:** "Triangle diagram with three competing objectives and optimal balance point"
**Source:** E004 PDF page 2, multi-objective section

### ASSET 4.4: PSO Convergence Curve
**Slide:** E004 Slide 6
**Type:** Line plot
**Description:**
- X-axis: Iteration number (0-50)
- Y-axis: Best cost (log scale, 1-1000)
- Cost curve showing typical convergence:
  - Iteration 0: Cost ~500 (random initialization)
  - Iterations 1-20: Rapid drop to ~20 (exploration)
  - Iterations 20-40: Gradual decrease to ~5 (exploitation)
  - Iterations 40-50: Plateau at ~2 (convergence)
- Phases labeled: Exploration, Exploitation, Convergence
**Beautiful.ai Prompt:** "Line plot showing cost decreasing over iterations with phases labeled"
**Source:** E004 PDF page 3, convergence behavior

### ASSET 4.5: Before/After Performance Table
**Slide:** E004 Slide 7
**Type:** Comparison table
**Description:**
- Rows: 7 controllers (Classical, STA, Adaptive, Hybrid, Conditional, Swing-Up, MPC)
- Columns: Manual Gains (cost), PSO Gains (cost), Improvement (%)
- Color-coded: Green for improvements >20%, Yellow for 5-20%, White for <5%
- Hybrid row highlighted (21.4% improvement)
**Beautiful.ai Prompt:** "Performance comparison table with color-coded improvement percentages"
**Source:** E004 PDF page 4, results section

---

## E005: Simulation Engine - Visual Assets

### ASSET 5.1: Three-Tier Engine Diagram
**Slide:** E005 Slide 1
**Type:** Architecture diagram
**Description:**
- 3 connected tiers with gear icons:
  - Tier 1 (bottom): "Simulation Runner" (blue, single-threaded icon)
  - Tier 2 (middle): "Vectorized Simulator" (green, parallel arrows icon)
  - Tier 3 (top): "Simulation Context" (purple, config file icon)
- Data flow arrows between tiers
- Speed callout: "1500 sims in 2-4 hours"
**Beautiful.ai Prompt:** "Three-tier architecture with gears and data flow arrows"
**Source:** E005 PDF page 1, architecture overview

### ASSET 5.2: Integration Method Comparison
**Slide:** E005 Slide 3
**Type:** Accuracy vs. speed scatter plot
**Description:**
- X-axis: Speed (fast → slow)
- Y-axis: Accuracy (low → high)
- 3 points:
  - Euler (top-left: fast, low accuracy)
  - RK4 (center: moderate speed, high accuracy)
  - RK45 (top-right: adaptive, high accuracy)
- Point sizes indicating computational cost
**Beautiful.ai Prompt:** "Scatter plot comparing integration methods on speed vs. accuracy axes"
**Source:** E005 PDF page 2, integration section

### ASSET 5.3: Sequential vs. Vectorized Timeline
**Slide:** E005 Slide 4
**Type:** Timeline comparison
**Description:**
- Top: Sequential execution (100 sims, one after another)
  - 100 small boxes in a long line
  - Duration: 1000 seconds
- Bottom: Vectorized execution (100 sims simultaneously)
  - 100 small boxes stacked vertically
  - Duration: 30 seconds
- Arrow showing "33x faster"
**Beautiful.ai Prompt:** "Two timelines comparing sequential vs. parallel execution with speedup arrow"
**Source:** E005 PDF page 3, vectorization section

### ASSET 5.4: NumPy Broadcasting Visualization
**Slide:** E005 Slide 5
**Type:** Array dimension diagram
**Description:**
- Single state array: [6] (1D, blue)
- Batch state array: [100, 6] (2D grid, green)
- Operation applied element-wise shown with arrows
- Annotations: "Same operation to all 100 rows simultaneously"
**Beautiful.ai Prompt:** "Array dimension visualization showing 1D to 2D broadcasting"
**Source:** E005 PDF page 3, NumPy section

### ASSET 5.5: Performance Benchmark Bar Chart
**Slide:** E005 Slide 7
**Type:** Horizontal bar chart
**Description:**
- 4 bars showing execution times:
  - Single sim: 10 seconds
  - Vectorized 100 sims: 30 seconds
  - Vectorized 1000 sims: 300 seconds (5 min)
  - PSO 1500 sims: 7200 seconds (2 hours)
- Color gradient: Green (fast) to red (slow)
- Speedup annotations
**Beautiful.ai Prompt:** "Bar chart comparing execution times for different simulation scales"
**Source:** E005 PDF page 4, performance section

### ASSET 5.6: Phase 1 Journey Timeline
**Slide:** E005 Slide 10
**Type:** Episode progression visual
**Description:**
- 5 connected circles (E001 → E002 → E003 → E004 → E005)
- Icons for each episode:
  - E001: Project overview (building blocks)
  - E002: Control theory (equations)
  - E003: Physics (pendulum)
  - E004: Optimization (swarm)
  - E005: Computation (gears)
- Arc labeled "From overview to mastery"
- Color gradient: Blue → purple progression
**Beautiful.ai Prompt:** "Timeline with 5 episode icons connected by arc showing progression"
**Source:** E005 PDF page 5, summary section

---

## Asset Usage Guidelines

### For Beautiful.ai Users:
1. Use text descriptions as prompts for Beautiful.ai's smart template system
2. Adapt colors to match Beautiful.ai's color palette
3. Add animations where suggested (particle movement, convergence, etc.)
4. Use Beautiful.ai's icon library for symbols (speedometer, trophy, etc.)

### For Manual Creation:
1. Descriptions provide enough detail to recreate in tools like:
   - PowerPoint/Keynote (manual diagramming)
   - Draw.io/Lucidchart (technical diagrams)
   - matplotlib/seaborn (data visualizations)
   - TikZ (LaTeX users)

### Color Palette Consistency:
- **Classical SMC / Foundation:** Blue (#2196F3)
- **Super-Twisting / Smooth:** Green (#4CAF50)
- **Adaptive / Intelligent:** Orange (#FF9800)
- **Advanced / Experimental:** Purple (#9C27B0)
- **Problems / Warnings:** Red (#F44336)
- **Solutions / Success:** Green (#4CAF50)

### Icon Recommendations:
- **Speed:** Speedometer, lightning bolt, rocket
- **Accuracy:** Target, trophy, checkmark
- **Balance:** Scales, triangle, slider
- **Optimization:** Swarm, flock, particles
- **Computation:** Gears, CPU, assembly line
- **Control:** Steering wheel, joystick, dial

---

## Source References

**LaTeX PDF Cheatsheets (Phase 1 Foundational):**
- E001_project_overview_and_introduction.pdf (5 pages, 400 KB)
- E002_control_theory_fundamentals.pdf (6 pages, 420 KB)
- E003_plant_models_and_dynamics.pdf (5 pages, 390 KB)
- E004_pso_optimization_fundamentals.pdf (7 pages, 480 KB)
- E005_simulation_engine_architecture.pdf (6 pages, 450 KB)

**Location:** `D:/Projects/main/academic/paper/presentations/podcasts/cheatsheets/phase1_foundational/`

**Extraction Method:** Text descriptions derived from PDF visual elements and markdown source episodes

---

**Total Visual Assets Cataloged:** 25 assets across 5 episodes
**Estimated Creation Time:** 6-8 hours for all assets (manual creation) | 2-3 hours (Beautiful.ai prompts)
