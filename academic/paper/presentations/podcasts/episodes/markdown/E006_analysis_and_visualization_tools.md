# E006: Analysis and Visualization Tools

**Part:** Part 2 Infrastructure & Tooling
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Visualization System

---

## Opening Hook

**Sarah:** A picture is worth a thousand words. But which picture? And what does it actually tell you?

**Alex:** Visualization is not about making pretty graphs. It is about extracting meaning from data. You can plot the same simulation result ten different ways and learn ten different things. Today we talk about the analysis and visualization toolkit -- performance metrics, statistical validation, real-time animation, and the 14 figures that made it into the research paper.

**Sarah:** Fourteen figures out of how many generated?

**Alex:** Hundreds. Most were exploratory -- trying to understand what was happening. A few became publication-ready after refinement. The art is knowing which visualizations reveal truth and which ones mislead.

---

## The Visualization Problem

**Sarah:** What makes visualization hard? You have data, you plot it, you look at it. Done.

**Alex:** Three challenges. First: choosing the right representation. Time series, phase portraits, frequency domain, statistical distributions -- each reveals different aspects. Second: avoiding misleading scales. Start your y-axis at zero or not? Log scale or linear? These choices change interpretation. Third: managing complexity. You have six state variables, one control signal, performance metrics, disturbances, model uncertainty -- how do you show all that without overwhelming the viewer?

**Sarah:** So visualization is editorial. You make choices about what to show and what to hide.

**Alex:** Exactly. And those choices have consequences.

---

## Four Primary Performance Metrics

**Sarah:** You mentioned performance metrics. What do you measure?

**Alex:** Four metrics that characterize controller behavior. First: settling time. How long until the pendulum reaches equilibrium and stays there? Mathematically: t_settle equals the minimum time where both angles remain below epsilon for all future time. Second: overshoot. How far does the pendulum swing past equilibrium before settling? Third: energy consumption. Integral of control effort squared over the simulation. Fourth: chattering frequency. High-frequency oscillation measured via FFT -- the bane of sliding mode control.

**Sarah:** Why those four?

**Alex:** They capture the tradeoffs. Fast settling time is good, but if you use massive control effort, you burn energy and wear out actuators. Low chattering is good, but if you smooth the control too much with a boundary layer, you lose tracking accuracy. A good controller balances all four metrics.

**Sarah:** How do you visualize these metrics?

**Alex:** Bar charts for single-number comparisons across controllers. Time series to see how metrics evolve during the simulation. Pareto frontiers for multi-objective optimization -- settling time vs energy consumption, chattering vs tracking accuracy. Heatmaps for parameter sensitivity analysis.

---

## Statistical Analysis: Monte Carlo and Bootstrap

**Sarah:** You do not just run one simulation and call it done. Explain the statistical validation.

**Alex:** Monte Carlo validation. Run 100 trials with randomized initial conditions, sensor noise, parameter uncertainty. Compute metrics for each trial. Now you have distributions, not single numbers. Classical SMC settling time: mean 2.47 seconds, standard deviation 0.08 seconds, 95% confidence interval [2.45, 2.55] via bootstrap.

**Sarah:** What is bootstrap?

**Alex:** Resampling method for computing confidence intervals. You have 100 settling time measurements. Bootstrap resamples those 100 values with replacement 10,000 times, computes the mean each time, builds a distribution of means. The 2.5th and 97.5th percentiles give you the 95% confidence interval. No parametric assumptions required.

**Sarah:** Why not just use the standard error formula?

**Alex:** Because performance metrics are not normally distributed. Settling time can be skewed -- most trials settle quickly, a few outliers take much longer. Bootstrap handles non-normal distributions correctly.

---

## Comparing Controllers: Welch's t-test and ANOVA

**Sarah:** How do you determine if one controller is actually better than another?

**Alex:** Statistical hypothesis testing. Compare Classical SMC to STA-SMC: Classical mean 2.5 seconds, STA mean 2.1 seconds. Is that difference real or random noise? Welch's t-test: p-value less than 0.001, meaning less than 0.1% chance the difference is due to randomness. We conclude STA is significantly faster.

**Sarah:** What about comparing all seven controllers simultaneously?

**Alex:** ANOVA -- analysis of variance. Tests whether any controller is different from the others. If ANOVA is significant, you do pairwise comparisons with Bonferroni correction to control for multiple testing. Result: Hybrid Adaptive STA ranks first, STA second, Adaptive third, Classical fourth.

**Sarah:** What is effect size?

**Alex:** Cohen's d -- how many standard deviations apart are the means? Cohen's d of 0.2 is a small effect, 0.5 is medium, 0.8 is large. Classical vs Hybrid Adaptive STA: Cohen's d equals 2.5 -- a huge effect. Not just statistically significant, but practically important.

---

## Real-Time Animation with DIPAnimator

**Sarah:** You have a real-time animation system. How does that work?

**Alex:** DIPAnimator class. You create an animator with a timestep -- `DIPAnimator(dt=0.01, show_traces=True)`. During the simulation loop, call `animator.update(state)` every timestep. The animator draws the cart, the two pendulum links, and optionally traces showing the trajectory of the second pendulum tip.

**Sarah:** What framerate?

**Alex:** 30 frames per second. With a 10-second simulation at 0.01-second timestep, you have 1,000 simulation steps. Rendering at 30 FPS means you show every 33rd timestep. Still looks smooth.

**Sarah:** Can you save the animation?

**Alex:** Yes. `animator.save('simulation.mp4', fps=30)` exports to video. Takes 10 to 30 seconds per second of simulated time -- slower than real-time because rendering to video is expensive. But useful for presentations and debugging.

**Sarah:** What does trace visualization show?

**Alex:** Path of the second pendulum tip. If the controller stabilizes quickly, you see a tight spiral converging to the origin. If the controller oscillates, you see loops. If it fails, the trace explodes off screen. Visual debugging -- you spot problems immediately.

---

## Chattering Analysis: Frequency Domain

**Sarah:** Chattering is high-frequency oscillation. How do you quantify it?

**Alex:** FFT -- Fast Fourier Transform. Convert the time-domain control signal to frequency domain. Compute power spectral density. Define a cutoff frequency -- say 10 Hz. Sum all energy above the cutoff. That is your high-frequency energy metric.

**Sarah:** Why 10 Hz cutoff?

**Alex:** Physical intuition. The pendulum natural frequencies are around 5 Hz. Control needed to stabilize the pendulum should be below 10 Hz. Anything above 10 Hz is chattering -- the controller switching faster than the dynamics can respond. Pure waste of actuator effort.

**Sarah:** Results for different controllers?

**Alex:** Classical SMC with zero boundary layer: 45% of energy above 10 Hz. Severe chattering. Classical SMC with 0.05 rad boundary layer: 8% of energy above 10 Hz. Much better. STA-SMC: 3% of energy above 10 Hz. Excellent chattering suppression. This is why super-twisting exists -- chattering mitigation is built into the algorithm.

---

## Boundary Layer Optimization: MT-6 Task

**Sarah:** You mentioned boundary layer optimization. Explain that research task.

**Alex:** Task MT-6 from the 72-hour research roadmap. Problem: Classical SMC chattering is too high. Solution: optimize the boundary layer thickness delta to minimize chattering while maintaining tracking accuracy. Method: grid search over delta in [0.01, 0.5] radians, run 100 Monte Carlo trials per delta, plot chattering vs tracking error.

**Sarah:** What did you find?

**Alex:** Optimal delta equals 0.05 radians. Chattering reduction: 60 to 80% compared to delta equals 0.01. Tracking accuracy: within 0.02 radians. Larger boundary layers reduce chattering further but degrade tracking -- not worth the tradeoff. Smaller boundary layers improve tracking slightly but chattering explodes.

**Sarah:** How do you visualize this tradeoff?

**Alex:** Two-axis plot. X-axis: boundary layer thickness. Y-axis left: chattering metric (lower is better). Y-axis right: tracking error (lower is better). Two curves on the same plot. The optimal point is where both curves are acceptably low. That is delta equals 0.05.

---

## Publication-Ready Figures: 14 for LT-7 Paper

**Sarah:** You generated 14 figures for the research paper. Walk me through them.

**Alex:** Figure 1: Control architecture overview. Block diagram showing plant, controller, observer, disturbance inputs. Establishes notation. Figure 2: Classical SMC boundary layer illustration. Plots the saturation function transitioning smoothly near the sliding surface. Figure 3: STA phase portrait. Shows the twisting motion in the sliding surface phase plane -- this is why it is called "twisting."

**Sarah:** Figures 4 through 8?

**Alex:** Figure 4: PSO convergence curves for all seven controllers. Shows how cost function decreases over 100 iterations. Figure 5: Settling time comparison. Bar chart with error bars from Monte Carlo. Figure 6: Overshoot comparison. Same format. Figure 7: Energy consumption comparison. Figure 8: Chattering frequency comparison. These four figures together show the performance tradeoffs.

**Sarah:** Figures 9 through 11?

**Alex:** Figure 9: Disturbance rejection time series from task MT-8. Shows how each controller responds to a 10-Newton step disturbance at t equals 2 seconds. Hybrid Adaptive STA recovers fastest. Figure 10: Model uncertainty robustness from task LT-6. Shows settling time vs parameter perturbation magnitude. Adaptive controllers degrade gracefully, classical SMC fails above 20% uncertainty. Figure 11: Lyapunov stability regions. Theoretical analysis showing guaranteed convergence zones.

**Sarah:** The final three?

**Alex:** Figure 12: Monte Carlo statistical validation. Histograms of settling time for 100 trials per controller, overlaid to show distributions. Figure 13: Controller ranking matrix. Heatmap where rows are controllers, columns are metrics, color shows rank (1 equals best, 7 equals worst). Figure 14: Pareto frontier for multi-objective PSO. Plots controllers in settling-time vs energy space. Shows Hybrid Adaptive STA dominates the frontier.

---

## Figure Quality Standards: IEEE Publication Requirements

**Sarah:** What are the technical requirements for publication-ready figures?

**Alex:** Vector format preferred: PDF or EPS. These scale infinitely without pixelation. Raster fallback: 300 DPI PNG. Anything less looks blurry in print. Font size: 10 to 12 points in a two-column IEEE format. Smaller fonts are unreadable. File size: under 500 KB per figure. Journals have upload limits.

**Sarah:** How do you ensure consistency?

**Alex:** Matplotlib style sheets. Define font family, font sizes, line widths, colors, legend placement once in a style file. Apply the style to all figures. Now they all look consistent. We use the `seaborn-paper` style with custom tweaks for IEEE compliance.

**Sarah:** What about color blindness?

**Alex:** Use colorblind-safe palettes. The default Matplotlib colors are terrible for red-green colorblind viewers. We use the "colorblind" palette from seaborn -- blue, orange, green, red, purple, brown. Each pair is distinguishable even in grayscale.

---

## Automated Figure Generation: Scripts

**Sarah:** Do you generate figures manually or via scripts?

**Alex:** Fully automated. `python scripts/research/lt7_generate_figures.py --task LT-7 --output academic/paper/experiments/figures/`. This script loads simulation results, computes metrics, generates all 14 figures, saves them with standardized naming. Takes 60 seconds to regenerate everything.

**Sarah:** Why automate?

**Alex:** Reproducibility and iteration. If you find a bug in the simulation or change a parameter, you regenerate all figures with one command. If you made figures manually in a GUI, you would have to redo every figure by hand. That takes hours and introduces inconsistencies. Automation ensures figures always match the latest data.

**Sarah:** What about figure captions?

**Alex:** Stored in a JSON file with the same basename as the figure. `figure_05_settling_time.pdf` has a caption in `figure_05_settling_time.json`. LaTeX document reads the JSON and inserts captions automatically. Change the caption in the JSON, recompile LaTeX, done. No manual editing.

---

## Parameter Sensitivity Analysis: Grid Search and Heatmaps

**Sarah:** How do you visualize how controller performance changes with parameters?

**Alex:** Parameter sensitivity analysis. Take a controller parameter -- say boundary layer thickness for Classical SMC. Create a grid: delta in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5] radians. For each delta value, run 100 Monte Carlo trials, compute mean settling time and standard deviation. Plot settling time vs delta with error bars. This shows how sensitive performance is to parameter choice.

**Sarah:** What about two parameters simultaneously?

**Alex:** Heatmaps. For PSO tuning, you might vary swarm size (10, 20, 30, 40, 50) and inertia weight (0.4, 0.5, 0.6, 0.7, 0.8). That is a 5x5 grid -- 25 combinations. Run PSO with each combination, record final cost. Plot a 2D heatmap where x-axis is swarm size, y-axis is inertia, color shows cost. Optimal region appears as a dark blue area if lower cost is better.

**Sarah:** How long does that take?

**Alex:** Depends on evaluation cost. If one PSO run takes 5 minutes and you have a 5x5 grid, that is 125 minutes -- about 2 hours. Parallelizable across 8 cores: 15 minutes wall time. For larger grids like 10x10, you might run overnight.

---

## Error Handling: Visualization Pipeline Robustness

**Sarah:** What goes wrong when generating figures?

**Alex:** Four categories of failures. First: data loading errors. JSON file is corrupted, CSV has mismatched columns, expected keys are missing. Second: computational errors. Division by zero when normalizing, NaN propagation from invalid operations, out-of-memory when plotting 10 million points. Third: rendering errors. Font not found, figure size too large, unsupported format. Fourth: file system errors. Permission denied, disk full, path too long on Windows.

**Sarah:** How do you handle these gracefully?

**Alex:** Try-catch with specific exceptions. For data loading, catch FileNotFoundError and JSONDecodeError, log which file failed, skip that figure and continue. For computational errors, validate data before plotting -- check for NaN with `np.isfinite()`, clip extreme outliers. For rendering errors, fall back to default fonts and raster format if vector fails. For file system errors, provide clear error messages with path and required permissions.

**Sarah:** Example from real debugging?

**Alex:** MT-5 comprehensive benchmark generated 42 figures. During the first run, figure 23 failed: "ValueError: x and y must have same first dimension." Root cause: one controller trial crashed and wrote an incomplete JSON file with 999 timesteps instead of 1000. Fix: add validation after loading -- verify all arrays have expected length, fill missing data with NaN, plot with NaN-aware functions that skip gaps.

---

## Integration with Research Tasks: From Data to Publication

**Sarah:** Walk me through a concrete example -- how does visualization integrate with a research task?

**Alex:** Task MT-8: disturbance rejection analysis. Goal: compare how fast each controller recovers from a 10-Newton step disturbance at t equals 2 seconds. Step 1: run 7 controllers, 100 trials each, with disturbance. Save 700 JSON files. Step 2: load all files, extract cart position, compute recovery time (when position returns to within 0.01 meters of setpoint). Step 3: statistical analysis -- mean and 95% CI for each controller. Step 4: generate Figure 9 -- time series showing cart position from t=1.5 to t=4 seconds for one representative trial per controller. Step 5: generate Figure S3 (supplementary) -- bar chart of recovery times with error bars.

**Sarah:** How long from raw data to final figures?

**Alex:** With automated scripts: 2 minutes. Load 700 files (30 seconds), compute metrics (10 seconds), generate 2 figures (20 seconds), save PDFs (5 seconds). Manually in a GUI: 2 hours. You would load files one by one, copy data to Excel, make plots, export images, adjust formatting. Automation is 60x faster and eliminates human error.

---

## Validation Workflows: Catching Visualization Bugs

**Sarah:** How do you validate that a figure shows what you think it shows?

**Alex:** Four-stage validation. Stage 1: Data sanity checks. Does the plotted data match raw data? Spot-check 10 random points -- read values from JSON, verify they appear correctly in the plot. Stage 2: Unit consistency. Are axes labeled with correct units? Is settling time in seconds, not milliseconds? Are angles in radians, not degrees? Stage 3: Visual inspection. Does the plot pass the "eyeball test"? If Classical SMC should oscillate more than STA, does the figure show that? Stage 4: Independent reproduction. Can someone else load the same data and generate the same figure?

**Sarah:** Give me an example where validation caught a bug.

**Alex:** Figure 5 in the LT-7 paper: settling time comparison. First version showed Classical SMC as best -- 1.2 seconds, STA as worst -- 4.8 seconds. This contradicted expectations and simulation logs. Validation stage 2: checked units. The code computed settling time in timesteps, not seconds. With dt=0.01 seconds, Classical SMC was actually 0.012 seconds (impossibly fast), STA was 0.048 seconds (also impossibly fast). Root cause: forgot to multiply by dt. Fix: `settling_time_seconds = settling_time_steps * dt`. Regenerated figure: Classical 2.5 seconds, STA 2.1 seconds. Now consistent with expectations.

---

## Common Visualization Pitfalls

**Sarah:** What mistakes do people make with visualization?

**Alex:** Seven common pitfalls. First: insufficient Monte Carlo trials. Running 10 trials and computing statistics is meaningless. You need at least 100 for adequate power, 1000 for publication-quality confidence intervals. Second: ignoring autocorrelation. If your trials are not independent -- say you use sequential random seeds -- confidence intervals are too narrow. Use block bootstrap or subsample every 10th trial. Third: p-hacking with multiple comparisons. If you compare 21 pairs of controllers and do not correct for multiple testing, you will find spurious significance. Apply Bonferroni correction: divide alpha by number of comparisons.

**Sarah:** Fourth through seventh?

**Alex:** Fourth: poor figure resolution. Using 72 DPI images from a screen capture -- they look terrible in print. Always export at 300 DPI or use vector formats. Fifth: misleading y-axis scales. Starting a bar chart at 2.0 instead of zero makes a 10% difference look like a 300% difference. Either start at zero or clearly mark the discontinuity with a break symbol. Sixth: overplotting. If you plot 10,000 scatter points, they obscure each other. Use transparency (alpha=0.1), hexbin plots, or density contours. Seventh: inconsistent styling. Mixing fonts, line widths, and color schemes across figures makes your paper look unprofessional. Use a style sheet.

**Sarah:** How do you prevent these systematically?

**Alex:** Checklists and code review. Before submitting any figure, run through a 15-item checklist: resolution adequate? Units labeled? Axes start at zero or marked? Colorblind-safe? Font size 10-12pt? Error bars present? Legend readable? Consistent with other figures? Second pair of eyes reviews every figure before inclusion in paper.

---

## Data Processing Pipeline: Raw Data to Figures

**Sarah:** Describe the data pipeline from simulation to publication-ready figure.

**Alex:** Seven stages. Stage 1: Simulation execution. Controller runs for 10 seconds with 0.01-second timestep, generating 1000 state samples plus control signals. Stage 2: Data serialization. Save to JSON with metadata (controller name, gains, timestamp, git commit hash). File size: 150 KB per trial. Stage 3: Batch aggregation. For 100 Monte Carlo trials, combine into a single HDF5 file -- 15 MB compressed. Stage 4: Metric computation. Load HDF5, compute settling time, overshoot, energy, chattering for each trial -- 500 milliseconds total. Stage 5: Statistical analysis. Bootstrap 95% confidence intervals -- 2 seconds per metric. Stage 6: Figure generation. Matplotlib renders plots with error bars, legends, labels -- 5 seconds per figure. Stage 7: Format conversion. Save to PDF (vector) and PNG (300 DPI raster) -- 2 seconds.

**Sarah:** What is the bottleneck?

**Alex:** Data loading. Reading 700 JSON files sequentially takes 45 seconds due to disk I/O. Solution: use HDF5 for batch storage -- load all trials in one read (3 seconds). This is a 15x speedup.

---

## Phase Portraits: Visualizing Nonlinear Dynamics

**Sarah:** You mentioned phase portraits. What do they show?

**Alex:** State space trajectories. For a double inverted pendulum, you have six state variables. A phase portrait plots two of them -- typically angle theta_1 on x-axis, angular velocity theta_1_dot on y-axis. Each point is a state at a moment in time. A trajectory is a path through this space as time evolves.

**Sarah:** What do you learn from a phase portrait?

**Alex:** Stability structure. A stable equilibrium appears as a spiral converging to the origin. An unstable equilibrium appears as trajectories diverging away. Limit cycles appear as closed loops. For Classical SMC, the trajectory spirals toward the origin but with oscillations due to chattering. For STA-SMC, the trajectory spirals smoothly -- the twisting motion that gives super-twisting its name.

**Sarah:** How many phase portraits did you generate?

**Alex:** 28 total. Seven controllers, four state variable pairs each: (theta_1, theta_1_dot), (theta_2, theta_2_dot), (x, x_dot), (sliding_surface, sliding_surface_dot). Only three made it into the main paper -- the others are supplementary material.

---

## Frequency Analysis: Beyond FFT

**Sarah:** You use FFT for chattering analysis. What else do you analyze in frequency domain?

**Alex:** Three additional analyses. First: power spectral density for state variables. Shows the dominant frequencies of oscillation. For the pendulum, you should see peaks at natural frequencies -- around 4.8 Hz for the first mode, 12.3 Hz for the second mode. If you see a peak at 150 Hz, something is wrong. Second: cross-spectral density between control and state. Shows how control frequency content correlates with state response. Ideally, control energy should be concentrated below 10 Hz where the pendulum can respond. Third: spectrogram for time-varying analysis. Shows how frequency content changes during the simulation -- high chattering initially during transients, low chattering after convergence.

**Sarah:** How do you generate a spectrogram?

**Alex:** Short-time Fourier transform. Divide the 10-second control signal into 1-second windows with 50% overlap. Compute FFT for each window. Stack the FFTs vertically with time on y-axis, frequency on x-axis, power as color. Result: a heatmap showing frequency evolution over time.

**Sarah:** What did spectrograms reveal?

**Alex:** Classical SMC chattering is worst during initial transient (0-2 seconds), then decreases as the state approaches the sliding surface. Adaptive SMC chattering stays low throughout -- the boundary layer adapts to reduce chattering as state converges. This confirmed the adaptive mechanism works as designed.

---

## Integration with Research Workflow

**Sarah:** How does visualization fit into the overall research workflow?

**Alex:** Seven-step process. Step 1: Task definition. Define research task (MT-8: disturbance rejection) with clear objectives and metrics. Step 2: Data collection. Run experiments -- 7 controllers, 100 trials each, save 700 JSON files (total 105 MB). Step 3: Statistical validation. Load data, compute metrics with 95% confidence intervals using bootstrap (2,000 resamples per controller). Step 4: Figure generation. Execute automated script -- 60 seconds generates all plots. Step 5: Quality review. Check figures against 15-item checklist, verify units, validate data consistency. Step 6: LaTeX integration. Include figures with `\includegraphics`, write captions, add cross-references. Step 7: Reproducibility documentation. Write README with exact commands, document software versions (Python 3.11, Matplotlib 3.8.2), commit data and scripts to repository.

**Sarah:** Why is reproducibility so important?

**Alex:** Academic integrity and peer review. Reviewers must be able to reproduce your figures from the data. If they cannot, your results are suspect. We include a `REPRODUCTION.md` file in `academic/paper/experiments/figures/` with exact commands: `python scripts/research/lt7_generate_figures.py --task LT-7 --data academic/paper/experiments/data/lt7_results.h5 --output academic/paper/experiments/figures/`. Run that command, get identical figures. Anyone with the repository can verify our claims.

**Sarah:** Has anyone actually reproduced your figures?

**Alex:** Yes. During Phase 5 research completion, we tested reproducibility by deleting all figures and regenerating from data. 14 out of 14 figures reproduced exactly -- bit-for-bit identical PDFs. This confirmed the pipeline works.

---

## Performance Benchmarks: Figure Generation Speed

**Sarah:** How long does it take to generate figures?

**Alex:** Single simple figure: 2 to 5 seconds. Scatter plot with 1,000 points, axis labels, legend, save to PDF. All 14 paper figures: 45 to 60 seconds. This includes loading data, computing statistics, generating plots, saving to files. Animation: 10 to 30 seconds per second of simulated video at 30 FPS. Rendering 10 seconds of simulation takes 100 to 300 seconds of wall time.

**Sarah:** What limits the speed?

**Alex:** Matplotlib rendering. Each plot requires drawing thousands of objects -- points, lines, text. That is CPU-intensive. Saving to vector format is slower than raster because every object must be encoded. Animations are slowest because you are rendering 30 frames per second and encoding to video.

**Sarah:** Could you parallelize?

**Alex:** Yes. Generate each of the 14 figures in a separate process. With 8 cores, total time drops from 60 seconds to 10 seconds. But we do not bother -- 60 seconds is fast enough.

---

## Memory Usage: Managing Large Datasets

**Sarah:** What about memory usage for visualization?

**Alex:** Single figure: 100 to 200 MB. Matplotlib loads the data, creates the figure object, renders to bitmap for preview. All 14 figures in sequence: peaks at 500 MB. Animation: 200 to 500 MB depending on trace length. If you animate a 100-second simulation, you store 10,000 state vectors -- that is 480 KB of state data, but Matplotlib internal structures take much more.

**Sarah:** How do you prevent memory exhaustion?

**Alex:** Generate figures one at a time and close them. `plt.figure()`, `plt.plot()`, `plt.savefig()`, `plt.close()`. This releases memory before the next figure. If you generate all 14 figures without closing, you accumulate 2 GB of memory and might OOM on machines with 4 GB RAM.

---

## Key Takeaways

**Sarah:** Let us recap the analysis and visualization toolkit.

**Alex:** Four primary performance metrics: settling time, overshoot, energy consumption, chattering frequency. These capture controller tradeoffs.

**Sarah:** Statistical validation via Monte Carlo with 100+ trials, bootstrap confidence intervals, Welch's t-test for pairwise comparison, ANOVA for multiple controllers.

**Alex:** Real-time animation at 30 FPS with DIPAnimator. Shows cart, pendulum links, trajectory traces. Saves to video for presentations.

**Sarah:** Chattering analysis via FFT. High-frequency energy above 10 Hz cutoff. Boundary layer optimization (MT-6) found delta equals 0.05 rad optimal.

**Alex:** Fourteen publication-ready figures for LT-7 paper. Automated generation in 60 seconds. Vector format (PDF/EPS), 300 DPI raster fallback, IEEE compliance.

**Sarah:** Figure quality standards: 10-12 pt fonts, colorblind-safe palettes, consistent styling via Matplotlib style sheets.

**Alex:** Common pitfalls: insufficient trials, ignoring autocorrelation, p-hacking, poor resolution, misleading scales.

**Sarah:** Five-step research workflow: data collection, statistical validation, automated figure generation, LaTeX integration, reproducibility documentation.

---

## Pronunciation Guide

For listeners unfamiliar with technical terms used in this episode:

- **Monte Carlo**: A simulation method. Pronounced "MON-tee CAR-low."
- **Bootstrap**: A resampling technique. Pronounced "BOOT-strap."
- **ANOVA**: Analysis of variance. Pronounced as letters "A-N-O-V-A."
- **Cohen's d**: Effect size measure. Cohen is pronounced "CO-en" (like "Owen").
- **FFT**: Fast Fourier Transform. Say each letter: "F-F-T."
- **Matplotlib**: Python plotting library. Pronounced "MAT-plot-lib."
- **Seaborn**: Matplotlib extension. Pronounced "SEE-born."
- **Pareto**: Named after economist Vilfredo Pareto. Pronounced "puh-RAY-toe."

---

## What's Next

**Sarah:** Next episode, Episode 7, we cover testing and quality assurance. The 4,563 tests that validate 105,000 lines of code, coverage standards, property-based testing, and the quality gates that separate research-ready from production-ready.

**Alex:** Testing is not about proving correctness. It is about documenting how things fail.

**Sarah:** Episode 7. Coming soon.

---

## Pause and Reflect

Visualization is translation. You translate numerical data into visual patterns that human perception can process. A good visualization reveals structure that is invisible in raw numbers. A bad visualization obscures truth or misleads. The responsibility is heavy -- your visualization choices influence how others interpret the work. A misleading y-axis can make a 5% improvement look like a 50% breakthrough. A cherry-picked example can make a flawed controller appear robust. Good visualization requires honesty, not just technical skill. Show the failures alongside the successes. Plot the error bars, not just the means. Make figures that survive scrutiny, not just figures that impress.

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Visualization Toolkit:** `src/utils/visualization/` (animation, plotting, figure generation)
- **Analysis Toolkit:** `src/utils/analysis/` (statistics, metrics, Monte Carlo)
- **Figure Generation Scripts:** `scripts/research/lt7_generate_figures.py`
- **Research Paper Figures:** `academic/paper/experiments/figures/` (14 figures)

---

*Educational podcast episode -- visualizing control systems research data*
