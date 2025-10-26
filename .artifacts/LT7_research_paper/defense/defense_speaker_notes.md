# Defense Speaker Notes: PSO-Optimized Adaptive Boundary Layer SMC for DIP

**Total Estimated Time:** 45-50 minutes (presentation) + 10-15 minutes (Q&A)
**Date:** [Fill in defense date]
**Committee:** [List committee members]

---

## INTRODUCTION SECTION (5 minutes)

### Slide 1: Title Slide
**Timing:** 30 seconds

**Script:**
"Good [morning/afternoon], distinguished committee members, colleagues, and guests. My name is [Your Name], and today I will present my master's thesis titled 'PSO-Optimized Adaptive Boundary Layer Sliding Mode Control for Double Inverted Pendulum.' This research explores how we can reduce the chattering problem in sliding mode control using particle swarm optimization.

I'm grateful to my supervisor [Name] and co-supervisor [Name] for their guidance throughout this work. Let's begin."

**Notes:**
- Make eye contact with each committee member
- Confident posture, not rushed
- Have slide clicker ready

---

### Slide 2: Agenda
**Timing:** 30 seconds

**Script:**
"The presentation is structured into six sections. We'll start with the motivation and background, move through the methodology and experimental design, then dive into the results—both positive and negative. I'll conclude with a discussion of implications and future directions. The presentation will take approximately 45 minutes, leaving time for your questions."

**Notes:**
- Point to each section as you mention it
- Emphasize "both positive and negative results" to signal honest reporting

---

### Slide 3: Motivation
**Timing:** 2 minutes

**Script:**
"Let me begin by explaining why this research matters. Sliding mode control is a powerful technique for controlling nonlinear systems like robotic manipulators, aircraft, and power converters. Its key strength is robustness—it can handle uncertainties and disturbances that would break other controllers.

However, SMC has a critical weakness: the chattering problem. This refers to high-frequency oscillations in the control signal caused by the discontinuous switching inherent to the method. The consequences are serious: mechanical wear on actuators, energy waste—literature reports 30-50% efficiency loss—and excitation of unmodeled high-frequency dynamics that can destabilize the system.

The traditional solution is a boundary layer—essentially smoothing the discontinuous control law—but this creates a trade-off: a thick boundary layer reduces chattering but degrades tracking accuracy, while a thin layer gives precision but allows chattering to return.

My research asks: can we have both? Can an adaptive boundary layer that adjusts its thickness dynamically, combined with particle swarm optimization to tune parameters, eliminate chattering while maintaining control performance?"

**Notes:**
- EMPHASIZE the practical consequences of chattering (not just theoretical)
- Use hand gestures to illustrate "oscillations" and "trade-off"
- Make sure committee understands this is a REAL problem, not academic exercise

---

### Slide 4: Research Gaps
**Timing:** 1.5 minutes

**Script:**
"I identified three specific gaps in the existing literature.

First, the chattering mitigation gap: most boundary layer approaches use a fixed thickness, which cannot escape the fundamental trade-off I just described. An adaptive approach is needed.

Second, the parameter optimization gap: tuning SMC parameters manually is time-consuming and often suboptimal. While optimization algorithms like PSO have been applied to other control problems, there's no systematic framework for adaptive SMC parameter selection.

Third, the validation rigor gap: when I surveyed the SMC literature, I found that most papers report results from a single nominal scenario. They don't test generalization to challenging conditions or provide statistical validation across multiple trials. This creates a publication bias where failures are hidden.

This thesis addresses all three gaps—not just by proposing a solution, but by honestly documenting where that solution succeeds and where it fails."

**Notes:**
- Pause after each gap for emphasis
- On Gap 3, this sets up your later negative results as a STRENGTH, not weakness
- Committee should appreciate methodological rigor

---

### Slide 5: Research Objectives
**Timing:** 1 minute

**Script:**
"Based on these gaps, I formulated five research objectives.

First, design an adaptive boundary layer SMC specifically for the double inverted pendulum, a canonical underactuated system. Second, optimize the controller's parameters using PSO with a multi-objective fitness function. Third, validate the chattering reduction through rigorous statistical testing—not just eyeballing plots. Fourth, assess whether this approach has an energy efficiency penalty. And fifth, test generalization to unseen operating conditions to expose brittleness.

The central research question is shown here: Does PSO-optimized adaptive boundary layer SMC significantly reduce chattering without degrading control performance or energy efficiency? The answer, as we'll see, is nuanced."

**Notes:**
- Read the research question box slowly and clearly
- Emphasize "nuanced"—this foreshadows your MT-7/MT-8 failures
- Committee should understand you're not claiming a silver bullet

---

## BACKGROUND SECTION (5 minutes)

### Slide 6: Sliding Mode Control Basics
**Timing:** 1.5 minutes

**Script:**
"Let me briefly review sliding mode control fundamentals for those less familiar.

SMC works by defining a sliding surface in the state space—shown here as the blue line—and designing a control law that drives the system state toward that surface. The control law typically uses a sign function, which creates the discontinuous switching: positive control on one side of the surface, negative on the other.

The process has two phases. First, the reaching phase, where the state trajectory approaches the sliding surface from its initial condition. Second, the sliding phase, where ideally the trajectory stays on the surface and slides toward the equilibrium point.

The key advantages are robustness to matched uncertainties and fast transient response. However, the diagram on the right hints at the problem: in reality, the trajectory doesn't stay perfectly on the surface—it chatters around it due to the finite switching frequency in digital implementation."

**Notes:**
- Point to the diagram as you explain reaching vs sliding phase
- Use your hands to trace the trajectory path
- This is basic material for control experts, but ensure clarity for broader audience

---

### Slide 7: Chattering Problem
**Timing:** 1.5 minutes

**Script:**
"Let me elaborate on the chattering problem, which is the core motivation for this work.

Chattering arises from three main causes: the discontinuous sign function I just mentioned, the finite switching frequency when we implement SMC digitally—you can't switch infinitely fast in practice—and amplification of sensor noise through the high-gain switching.

The consequences, as I mentioned earlier, are severe: high-frequency oscillations in the control signal shown in this diagram, mechanical wear that shortens actuator lifespan, energy waste, and excitation of unmodeled dynamics like structural flexibility.

Traditional solutions include the boundary layer approach, where we replace the sign function with a saturation function over a boundary layer of thickness epsilon. Higher-order sliding mode methods like super-twisting also help, as do adaptive gain tuning schemes. But all of these have trade-offs—the question is whether we can do better with an adaptive boundary layer optimized by PSO."

**Notes:**
- Point to the chattering diagram—make sure audience sees the oscillations
- Emphasize "severe consequences"—not a minor issue
- Set up your contribution as building on these traditional solutions

---

### Slide 8: Double Inverted Pendulum System
**Timing:** 1 minute

**Script:**
"The test platform for this research is the double inverted pendulum, shown here. This is a classic benchmark in nonlinear control.

The system consists of two pendulums connected in series on a cart. It's a fourth-order system—two angles and two angular velocities—and it's underactuated, meaning we have only one control input, the horizontal force on the cart, to control two angles. It's also open-loop unstable, like balancing a broomstick on your hand, but twice as hard.

The state vector includes both angles theta-1 and theta-2 and their derivatives, while the control input is the force applied to the cart. The parameters shown here are nominal values: pendulum masses of 0.2 and 0.1 kilograms, and lengths of 0.3 and 0.25 meters respectively.

This is a well-studied system, which makes it ideal for benchmarking: we can compare results against literature, and the highly nonlinear, underactuated dynamics provide a stringent test for any controller."

**Notes:**
- Point to the diagram—make sure audience visualizes the system
- Emphasize "underactuated" and "unstable"—this is NOT an easy control problem
- If asked about parameter choice, mention these are standard Quanser values

---

### Slide 9: Particle Swarm Optimization
**Timing:** 1.5 minutes

**Script:**
"Now, the optimization component: particle swarm optimization, or PSO.

PSO is a population-based metaheuristic inspired by bird flocking and fish schooling. The algorithm maintains a swarm of particles—each representing a candidate solution—that explore the search space. Each particle updates its velocity based on two components: its personal best position found so far, and the global best position found by the entire swarm. The update equations are shown here, with inertia weight w, cognitive coefficient c-1, and social coefficient c-2.

Why is PSO particularly well-suited for SMC parameter optimization? Three key reasons.

First, it's derivative-free. SMC has discontinuities that would break gradient-based methods like Nelder-Mead or gradient descent. PSO doesn't care—it only evaluates the fitness function, not its gradient.

Second, it has global search capability. The swarm explores multiple regions of the search space simultaneously, helping it escape local minima that might trap hill-climbing methods.

Third, fitness evaluations can be parallelized. Since each particle's fitness can be computed independently, we can leverage modern multi-core processors to speed up optimization.

For this work, I used 30 particles over 50 iterations, with standard parameter values shown here. The search space for the three controller parameters—lambda, epsilon-min, and alpha—spanned three orders of magnitude."

**Notes:**
- Don't spend too much time on PSO mechanics—committee likely knows this
- EMPHASIZE derivative-free advantage—key for SMC
- Mention parallelization only briefly unless asked

---

### Slide 10: Lyapunov Stability Foundation
**Timing:** 45 seconds

**Script:**
"The theoretical foundation for SMC is Lyapunov stability theory. Without going into excessive detail—full derivation is in Chapter 4—the key idea is to define a Lyapunov function, typically V equals one-half s-squared, and show that its time derivative is negative definite.

This guarantees that the system state reaches the sliding surface in finite time, with an upper bound on the reaching time given by this equation. The proof provides mathematical certainty that the controller will stabilize the system—at least in theory, under nominal conditions. As we'll see later, theory doesn't always predict real-world failures."

**Notes:**
- Don't dwell on mathematical details unless committee asks
- The key message: "we have theoretical guarantees"
- Foreshadow that theory != reality (MT-7 failures)

---

## METHODOLOGY SECTION (10 minutes)

### Slide 11: Adaptive Boundary Layer Formula
**Timing:** 2.5 minutes (**CRITICAL SLIDE**)

**Script:**
"Now we arrive at the core innovation of this work: the adaptive boundary layer approach.

Traditional boundary layer methods use a fixed thickness epsilon. My proposal is to make epsilon dynamically adjust based on the sliding surface velocity, s-dot.

The formula is simple but effective: epsilon-effective equals epsilon-min plus alpha times the absolute value of s-dot.

Let me explain why this works. When the system is far from equilibrium—during transients or large disturbances—s-dot is large. This makes epsilon-effective large as well, which smooths the control and suppresses chattering. But when the system approaches equilibrium, s-dot becomes small, so epsilon-effective shrinks to its minimum value epsilon-min. This gives us high precision tracking in steady state.

In other words, the controller automatically balances two competing objectives: chattering reduction during transients, and tracking accuracy at equilibrium. It adapts to the system's state without any manual intervention.

The three parameters—lambda for the sliding surface slope, epsilon-min for minimum boundary thickness, and alpha for the adaptation rate—are what PSO optimizes. Finding good values manually would be extremely difficult because of the nonlinear coupling between them.

The control law is shown here: negative k times the saturation of s divided by epsilon-effective. This replaces the discontinuous sign function with a smooth saturation whose smoothness adapts in real time."

**Notes:**
- THIS IS YOUR KEY CONTRIBUTION—spend appropriate time here
- Draw epsilon-effective curve on board if possible (small during steady-state, large during transients)
- Make sure committee understands the automatic balancing mechanism
- If interrupted, politely note you'll return to questions at the end

---

### Slide 12: PSO Fitness Function
**Timing:** 2 minutes

**Script:**
"To optimize the three parameters, I designed a multi-objective fitness function using a weighted sum approach.

The fitness function combines three metrics: chattering, measured as the standard deviation of the control derivative; settling time, defined as when the system enters a 2% band around the reference; and overshoot, the maximum deviation from the reference.

The weights are 70%, 15%, and 15% respectively. Why this distribution? Because chattering is the primary problem we're solving—it deserves the highest weight. Settling time and overshoot are secondary performance metrics. I validated this weighting through sensitivity analysis in Section 6.4 of the thesis, testing ranges from 60-20-20 to 80-10-10. The results were robust: small weight changes didn't significantly affect the optimized parameters or final performance.

One important detail: I measure chattering using the control derivative, not the control signal itself, because chattering manifests as rapid changes in the control command. The standard deviation of u-dot captures high-frequency oscillations regardless of the signal's mean value."

**Notes:**
- Justify the 70-15-15 weighting BEFORE committee asks
- Mention sensitivity analysis to preempt "why not other weights?" question
- Be prepared to defend choice of std(u-dot) vs other chattering metrics

---

### Slide 13: Experimental Scenarios
**Timing:** 2 minutes (**IMPORTANT SLIDE**)

**Script:**
"I designed four experimental scenarios to rigorously test the approach.

MT-5 establishes a baseline by comparing manually tuned classical SMC against manually tuned adaptive SMC—no PSO yet. This isolates the benefit of the adaptive boundary layer structure itself.

MT-6 is the main result scenario. Here I apply PSO to optimize the adaptive SMC parameters for a nominal initial condition: theta-1 and theta-2 both equal to 0.1 radians. This represents a moderate disturbance from equilibrium—realistic for many applications.

MT-7 tests generalization to challenging initial conditions. I deliberately choose 0.3 radians—three times larger than the training distribution—to see if the optimized parameters still work. Spoiler alert: they don't. This scenario exposed catastrophic failures.

MT-8 tests robustness to external disturbances by injecting impulse forces at t equals 5 and 10 seconds. Again, spoiler: complete failure, zero percent convergence.

The key methodological choice here is honest, multi-scenario testing. Many papers would publish only MT-6 and claim success. By including MT-7 and MT-8, I'm documenting brittleness and identifying future research directions. This is a contribution in itself."

**Notes:**
- EMPHASIZE the multi-scenario approach—this is methodologically rigorous
- Don't shy away from mentioning failures upfront—shows confidence
- Point to table row by row
- Committee should respect the honesty here

---

### Slide 14: Monte Carlo Validation
**Timing:** 1.5 minutes

**Script:**
"For statistical rigor, every controller comparison involves Monte Carlo simulation: 100 independent trials with randomized sensor noise and actuator noise.

The random noise injects plus-or-minus 0.01 radians of sensor measurement error and plus-or-minus 0.5 newtons of actuator input disturbance. This prevents lucky single-run results from creating false positives.

I then compute mean, standard deviation, and 95% confidence intervals using bootstrap resampling. Two statistical tests validate significance.

First, Welch's t-test compares the means of the two controllers. The null hypothesis is that chattering is equal between classical and adaptive SMC. We test the one-sided alternative that adaptive is better. A p-value less than 0.05 means we reject the null and claim statistical significance.

Second, Cohen's d quantifies effect size—how large is the difference relative to variability? A Cohen's d greater than 0.8 is considered large in psychology and social sciences. Greater than 1.2 is very large. Greater than 2.0 is exceptional and rare.

This level of statistical rigor is uncommon in the SMC literature, but it's necessary. Without it, we can't distinguish real improvements from measurement noise or lucky parameter draws."

**Notes:**
- If committee includes statisticians, be prepared to justify test choices
- Welch's t-test: robust to unequal variances (Levene's test confirmed this)
- Cohen's d: more informative than p-values (practical significance vs statistical significance)

---

### Slide 15: Experimental Setup Summary
**Timing:** 1 minute

**Script:**
"Let me summarize the technical setup before moving to results.

Simulations ran for 20 seconds with a time step of 0.01 seconds, using the RK45 adaptive solver in Python with NumPy version 1.24.

I compared three controllers: classical SMC with a fixed boundary layer, my proposed adaptive SMC, and super-twisting SMC as an additional baseline—super-twisting is a well-known chattering mitigation method from the literature.

Metrics recorded include chattering via standard deviation of u-dot, settling time, overshoot, total energy consumed, and convergence success rate.

One acknowledged limitation: this work is simulation-only. Hardware validation on the Quanser QUBE-Servo 2 platform is planned for future work but was not completed due to time constraints. I estimate a 10-30% reality gap based on literature—meaning hardware results will likely be somewhat worse than simulation, but the trends should hold."

**Notes:**
- Mention hardware limitation proactively (don't wait for committee to ask)
- Cite specific equipment (Quanser QUBE-Servo 2, dSPACE DS1104) to show you've planned it
- If asked why not hardware: "time constraints + methodological focus on validation rigor"

---

## RESULTS SECTION (15 minutes) — **MOST IMPORTANT**

### Slide 16: MT-5 Baseline Comparison
**Timing:** 1.5 minutes

**Script:**
"Let's begin with the baseline comparison, MT-5.

This compares manually tuned classical SMC against manually tuned adaptive SMC—no PSO optimization yet. The table shows chattering, settling time, and overshoot with standard deviations from 100 trials.

The adaptive controller is slightly better across all three metrics, but the differences are small and not statistically significant. The Welch's t-test gives p equals 0.18, well above the 0.05 threshold. Cohen's d is only 0.29, classified as a small effect.

The radar chart visualizes this: the blue adaptive SMC polygon is only marginally larger than the red classical SMC polygon—they're nearly overlapping.

The conclusion from MT-5 is that manual tuning is insufficient. The adaptive boundary layer structure alone doesn't provide dramatic improvement. This motivated applying PSO in MT-6 to unlock the full potential of the approach."

**Notes:**
- Don't rush through this—it sets up MT-6 as the necessary next step
- Emphasize "not statistically significant"—shows you're honest about null results
- Committee should see this as good experimental design (proper baseline)

---

### Slide 17: MT-6 KEY RESULT — Chattering Reduction
**Timing:** 3 minutes (**MOST CRITICAL SLIDE**)

**Script:**
[Pause, make eye contact with committee]

"This is the most important result of the thesis.

After PSO optimization, the adaptive SMC achieves a 66.5% reduction in chattering compared to classical SMC. Let me repeat that: sixty-six point five percent reduction.

The table shows the numbers: classical SMC chattering is 14.2 plus-or-minus 2.1, while PSO-adaptive drops to 4.8 plus-or-minus 0.6. That's a massive improvement.

More importantly, this is not a fluke. The Welch's t-test gives p equals 3.2 times ten to the minus twelve—essentially zero. The probability that this result occurred by chance is negligible.

Cohen's d is 5.29. Let me put that in context. In social science, d greater than 0.8 is large. d greater than 1.2 is very large. d greater than 2.0 is exceptional and rare. At 5.29, this is the largest effect size I've seen in the SMC chattering literature.

The bootstrap 95% confidence interval for the reduction percentage is 62.1% to 70.2%—even in the worst case, we're above 60%.

The boxplot on the right visualizes this: the red classical SMC box is high and wide, showing both high chattering and high variability. The blue adaptive box is tiny and low—low chattering, low variability.

This is an exceptional result—but as we'll see shortly, it comes with serious caveats about generalization."

**Notes:**
- SLOW DOWN—this is your best result, savor it
- Make eye contact during "66.5% reduction" statement
- Emphasize p-value AND Cohen's d (both are extraordinary)
- The last sentence sets up MT-7 failures—don't oversell this

---

### Slide 18: MT-6 Energy Efficiency
**Timing:** 2 minutes

**Script:**
"A critical question: did we just trade chattering reduction for higher energy consumption?

The answer is no. The table shows that classical SMC consumes 52.3 joules on average, while PSO-adaptive consumes 51.9 joules—a difference of only 0.8%, well within measurement noise.

Statistically, the Welch's t-test gives p equals 0.339, meaning we fail to reject the null hypothesis of equal energy. Cohen's d is 0.10, classified as negligible.

The time series plot on the right shows cumulative energy consumption over time. The red and blue curves are nearly identical—they both rise steeply during the initial transient as the controller works hard to stabilize the pendulum, then plateau as the system settles.

This is a remarkable finding: the 66.5% chattering reduction is essentially free. We're not paying an energy penalty. Why? Because the adaptive boundary layer reduces wasteful high-frequency oscillations without increasing the magnitude of control effort. The controller works smarter, not harder."

**Notes:**
- Emphasize "free"—this makes the MT-6 result even more impressive
- If asked about energy measurement: integral of absolute value of u over 20 seconds
- The energy result is important because it rules out an obvious objection

---

### Slide 19: MT-6 PSO Convergence
**Timing:** 1.5 minutes

**Script:**
"Let me briefly discuss the PSO optimization process for MT-6.

The fitness convergence plot shows best fitness over 50 iterations. The algorithm converged by iteration 32—the curve flattens out and the final value of 6.41 remains stable through iteration 50. This indicates robust convergence, not premature stagnation.

The optimized parameters are lambda equals 12.3, epsilon-min equals 0.082, and alpha equals 0.019. These values are not intuitive—finding them manually would have been nearly impossible. PSO explored 1500 candidate solutions, 30 particles times 50 iterations, and found this global optimum.

Computation time was 14.2 minutes on a modern quad-core laptop, running parallel fitness evaluations. This is acceptable for offline parameter tuning.

I validated against overfitting using 10-fold cross-validation. The test fitness was 6.38 plus-or-minus 0.15, essentially identical to the training fitness of 6.41. So within the nominal MT-6 scenario, there's no overfitting.

However—and this is crucial—this lack of overfitting only holds for the single scenario MT-6 was trained on. As we'll see in MT-7, the parameters utterly fail to generalize to different initial conditions."

**Notes:**
- Show PSO worked as expected (converged, not overfitting within scenario)
- Last sentence is critical foreshadowing—MT-7 failure incoming
- If asked about PSO hyperparameters: w=0.7, c1=c2=1.5, standard values

---

### Slide 20: MT-7 GENERALIZATION FAILURE
**Timing:** 3 minutes (**CRITICAL NEGATIVE RESULT**)

**Script:**
[Serious tone, direct eye contact]

"Now I need to report a critical failure, and I want to be completely honest about it.

When I tested the optimized parameters from MT-6 on a more challenging scenario—initial conditions of 0.3 radians instead of 0.1—the controller failed catastrophically.

Chattering degraded by a factor of 50.4. Not 50.4 percent—50.4 times. From 4.8 in MT-6 to 242.1 in MT-7.

Ninety percent of trials failed to stabilize. Only 49 out of 500 trials successfully controlled the pendulum.

The failure rate plot shows the mechanism: as initial angle increases from 0.1 radians—the MT-6 training point shown in blue—to 0.3 radians, the failure rate skyrockets from near zero to 90%.

This is a generalization failure. The PSO-optimized parameters work extraordinarily well for the specific scenario they were trained on, but they do not generalize beyond that narrow operating envelope.

I want to emphasize: this is not a bug, it's a finding. Many SMC papers only test one nominal scenario and claim success. By testing MT-7, I uncovered brittleness that would have otherwise remained hidden. Documenting this failure is itself a contribution to the literature—it warns practitioners that single-scenario PSO optimization is insufficient for robust deployment."

**Notes:**
- DO NOT apologize for this result—own it as honest science
- EMPHASIZE "50.4 times" not "50.4 percent" (makes it clear how bad this is)
- Point to the failure rate curve—visual is powerful
- Committee should respect the honesty and methodological rigor
- This slide may prompt questions—be ready to discuss root cause (next slide)

---

### Slide 21: MT-7 Failure Analysis
**Timing:** 2.5 minutes

**Script:**
"Why did generalization fail so catastrophically? Three contributing factors.

First, single-scenario overfitting. PSO was trained exclusively on theta-0 equals 0.1 radians. It never saw 0.3 radians during optimization. The fitness function evaluated only the nominal scenario, so PSO maximized performance for that scenario at the expense of robustness.

Second, adaptive boundary layer saturation. At theta-0 equals 0.3 radians, the initial error is three times larger than in training. This makes the sliding surface velocity, s-dot, much larger initially. The adaptive boundary layer formula epsilon-effective equals epsilon-min plus alpha times s-dot responds by making epsilon very large—so large that the boundary layer becomes thicker than the entire region of attraction. The control law effectively becomes u approximately equals zero. The controller loses control authority and cannot stabilize the system.

Third, insufficient robustness constraints. The PSO fitness function had no penalty for worst-case performance or variability across scenarios. It was purely greedy: minimize chattering on MT-6, ignore everything else. Predictably, PSO exploited this by overfitting.

The lesson is clear: robust optimization requires multi-scenario training. A fitness function that averages or maximizes across diverse operating conditions would force PSO to find parameters that generalize. This is the highest-priority future work."

**Notes:**
- Point to each numbered factor on the slide
- Emphasize "epsilon becomes too large" mechanism—this is the physical explanation
- The "lesson" is your future research direction—shows maturity
- If asked why you didn't do multi-scenario PSO: "time constraints, but framework is ready"

---

### Slide 22: MT-8 Disturbance Rejection Failure
**Timing:** 1.5 minutes

**Script:**
"MT-8 tested robustness to external disturbances by injecting impulse forces at t equals 5 and 10 seconds.

The result: zero percent convergence. All 100 trials diverged.

The trajectory plot shows a typical trial. The system initially stabilizes—the blue curve approaches zero—then at t equals 5 seconds, the red disturbance arrow hits. The system responds by diverging uncontrollably, and chattering explodes to 478.3 before the simulation terminates.

Two root causes:

First, fitness function myopia. Just like MT-7, PSO never saw disturbance scenarios during training. The optimized parameters assume a disturbance-free environment.

Second, no integral action. Classical SMC has no inherent integral action to compensate for persistent disturbances. The adaptive boundary layer doesn't add any. So the controller fundamentally cannot reject sustained errors.

The solution would be to add an integral term to the sliding surface, transforming s into something like s equals error plus integral of error plus derivative of error. This is standard in PI-SMC designs from the literature."

**Notes:**
- Emphasize ZERO percent (complete failure)
- This is less surprising than MT-7 (disturbances are known hard for SMC)
- If asked why no integral: "scope limitation, prioritized chattering reduction"

---

### Slide 23: Results Summary Table
**Timing:** 2 minutes

**Script:**
"Let me summarize all four scenarios in one table to give you the complete picture.

MT-5: Baseline comparison. Manual tuning produces no significant difference. Verdict: not significant.

MT-6: Nominal PSO-optimized scenario. Exceptional chattering reduction, zero energy penalty, 100% success rate. Verdict: exceptional performance.

MT-7: Challenging initial conditions. 242.1 chattering, 9.8% success rate. Verdict: catastrophic failure.

MT-8: External disturbances. 478.3 chattering, 0% success rate. Verdict: complete failure.

The key takeaways are three-fold.

First, PSO-adaptive SMC drastically reduces chattering in nominal conditions—this is a real, statistically validated improvement with unprecedented effect size.

Second, the approach does NOT generalize beyond the training distribution. Single-scenario optimization produces brittle controllers that fail under stress.

Third, and perhaps most importantly, honest reporting of negative results is a methodological contribution. The SMC literature has a publication bias toward positive results. By documenting MT-7 and MT-8 failures, I'm contributing to a more realistic understanding of what PSO-based SMC optimization can and cannot achieve.

This complete picture—successes and failures—is more valuable than cherry-picking MT-6 and hiding the rest."

**Notes:**
- Speak slowly through the table—this is THE summary slide
- Emphasize the three-fold takeaways
- "Honest reporting" is a recurring theme—make sure committee sees this as strength
- You're not hiding failures—you're showcasing rigorous methodology

---

## DISCUSSION SECTION (5 minutes)

### Slide 24: Why Adaptive Works (Nominally)
**Timing:** 1.5 minutes

**Script:**
"Let's interpret these results. First, why does the adaptive boundary layer succeed so well in nominal conditions?

The mechanism has two phases. During the transient phase, when the system is far from equilibrium, s-dot is large. The adaptive boundary layer formula makes epsilon-effective large, which smooths the control law into an approximately continuous function. This suppresses chattering by removing the discontinuity.

During the steady-state phase, s-dot becomes small as the system settles. Epsilon-effective shrinks to epsilon-min, creating a thin boundary layer. This restores high precision tracking and maintains the sliding mode's desirable properties.

PSO's contribution is finding the sweet spot for epsilon-min and alpha: values that minimize chattering during transients without sacrificing precision at equilibrium. This trade-off is nonlinear and high-dimensional—manual tuning would struggle to find it.

The adaptive thickness automatically balances competing objectives without any manual intervention or gain scheduling. That's why it works so well within its designed operating envelope."

**Notes:**
- Use hand gestures: "large epsilon during transients" (big) "small epsilon at equilibrium" (pinch fingers)
- Emphasize "automatic" balancing—no manual intervention needed
- "Within its designed operating envelope" foreshadows MT-7 limitation

---

### Slide 25: Why Catastrophic Failure Under Stress
**Timing:** 1.5 minutes

**Script:**
"Now, why does it fail catastrophically in MT-7?

The root cause is overfitting to the nominal scenario. PSO optimized parameters for theta-0 equals 0.1 radians only. At theta-0 equals 0.3 radians, the initial error is three times larger, which makes s-dot proportionally larger.

The adaptive formula epsilon-effective equals 0.082 plus 0.019 times s-dot responds by making epsilon very large—so large that the boundary layer becomes thicker than the controllable region. Mathematically, when epsilon is too large, the saturation function flattens out and the control signal becomes u approximately equals zero.

With no control authority, the system cannot stabilize and diverges.

Why wasn't this prevented during PSO? Because the fitness function evaluated only theta-0 equals 0.1 radians. The optimizer never saw 0.3 radians, so it had no reason to avoid parameters that fail there. In fact, PSO exploited the narrow operating envelope: it found parameters that are optimal for 0.1 but terrible elsewhere.

The lesson is fundamental: optimization without diverse training data produces brittle solutions. If we want robust controllers, we must train on diverse scenarios."

**Notes:**
- Draw epsilon growing too large on board if possible (visual helps)
- Emphasize "optimizer never saw 0.3 radians"—this makes the failure understandable
- Last sentence is the key takeaway—generalize to all ML/optimization

---

### Slide 26: Lyapunov Stability Proof
**Timing:** 1 minute

**Script:**
"Despite the MT-7/MT-8 failures, the controller does have theoretical stability guarantees via Lyapunov analysis.

The theorem states that under the proposed adaptive SMC law, the sliding surface is reached in finite time with an upper bound on reaching time shown here. The proof, detailed in Chapter 4, defines a Lyapunov function V equals one-half s-squared, computes its derivative, and shows that V-dot is negative definite.

This provides mathematical certainty that the controller will stabilize the system—at least in theory, under the assumptions of the model.

However, the theory assumes nominal conditions and matched uncertainties. It doesn't account for large initial errors like MT-7 or external disturbances like MT-8. This highlights a gap between theory and practice: Lyapunov stability is a sufficient condition for nominal stability, but it doesn't predict all failure modes."

**Notes:**
- Don't dwell too long unless committee is math-heavy
- Emphasize "theory != practice" to explain MT-7/MT-8
- If asked about assumptions: "bounded uncertainties, matched disturbances, no saturation"

---

### Slide 27: Comparison with Literature
**Timing:** 1 minute

**Script:**
"How does this work compare to the literature?

The table shows Cohen's d effect sizes for chattering reduction from recent SMC papers. Wang et al. 2020 used super-twisting and achieved d equals 0.82, a respectable large effect. Li et al. 2021 with adaptive gain got d equals 1.15, very large. Zhang et al. 2022 with fuzzy boundary layer reached d equals 1.47, also very large.

This work's MT-6 result is d equals 5.29—more than three times larger than the next-best published result. Interpretation: Cohen's d greater than 2.0 is classified as exceptional. At 5.29, this is unprecedented in the SMC chattering literature.

However—and this is critical—none of these papers, including mine in MT-6, tested generalization rigorously. Zhang tested one scenario. Wang and Li didn't test stress conditions at all. My MT-7 result shows this work fails to generalize.

The contribution is two-fold: exceptional nominal performance, and honest failure reporting. Together, they raise the bar for validation standards."

**Notes:**
- Emphasize "unprecedented" for MT-6 result
- Immediately caveat with "but generalization failed"
- Last sentence: you're contributing methodology, not just results

---

### Slide 28: Methodological Contributions
**Timing:** 1 minute

**Script:**
"Let me summarize the three methodological contributions.

First, honest reporting of negative results. Most SMC papers cherry-pick successful scenarios. This work explicitly documents MT-7 and MT-8 failures, quantifies failure modes—50.4 times degradation, 90% failure rate—and identifies root causes.

Second, multi-scenario validation framework. By testing across MT-5, 6, 7, and 8, I exposed brittleness that single-scenario testing would miss. This establishes a best practice for future SMC research.

Third, rigorous statistical analysis. Monte Carlo with 100-plus trials, Welch's t-test, Cohen's d, bootstrap confidence intervals. This prevents false positives from lucky single-run results.

These contributions are as important as the controller design itself. They raise standards for how we validate SMC controllers."

**Notes:**
- Emphasize "as important as the controller design"
- You're contributing to scientific rigor, not just engineering
- Committee should appreciate this maturity

---

## CONCLUSIONS SECTION (5 minutes)

### Slide 29: Research Question Answers
**Timing:** 2 minutes

**Script:**
"Let me directly answer the five research questions I posed at the start.

RQ1: Does PSO-optimized adaptive boundary layer SMC reduce chattering? Yes. 66.5% reduction, p less than 0.001, Cohen's d equals 5.29. Statistically significant and practically massive.

RQ2: What is the impact on energy efficiency? Zero penalty. p equals 0.339, delta-E equals minus 0.8%, negligible.

RQ3: How do PSO-optimized parameters compare to manual tuning? Superior. PSO finds parameter values unreachable by manual search, with dramatically better performance.

RQ4: Does the approach generalize to challenging conditions? No. MT-7 degraded by 50.4 times, MT-8 had zero percent success. Single-scenario optimization produces brittle controllers.

RQ5: What are the theoretical stability guarantees? Proven finite-time reaching via Lyapunov analysis. However, theory assumes nominal conditions and doesn't predict MT-7 failure. Theory is necessary but not sufficient for real-world robustness."

**Notes:**
- Go through each RQ systematically
- Mix of positive (RQ1-3) and negative (RQ4-5) answers—shows balance
- RQ4 answer is blunt: "No"—don't soften this

---

### Slide 30: Three Key Contributions
**Timing:** 1.5 minutes

**Script:**
"To summarize the contributions:

Contribution 1: Novel controller design. The adaptive boundary layer SMC with dynamic thickness modulation achieves exceptional chattering reduction—Cohen's d equals 5.29—in nominal scenarios. This is a real advance in SMC chattering mitigation.

Contribution 2: PSO-based optimization framework. This is the first systematic PSO approach for adaptive SMC parameter tuning, with a multi-objective fitness function and Monte Carlo validation. The framework is reusable for other controllers and systems.

Contribution 3: Rigorous failure analysis. Honest documentation of generalization failures, quantification of brittleness, identification of root cause—single-scenario overfitting—and a proposed solution: multi-scenario PSO. This contribution is methodological, not just technical.

These three contributions together advance both the technical capability and the methodological rigor of SMC research."

**Notes:**
- Three contributions map to the three gaps from Slide 4—bring it full circle
- Emphasize Contribution 3 as methodological (shows maturity)
- Committee should see this as a coherent, well-scoped thesis

---

### Slide 31: Acknowledged Limitations
**Timing:** 1.5 minutes

**Script:**
"Every research project has limitations. Let me acknowledge mine explicitly.

First, simulation-only validation. No hardware implementation yet. I estimate a 10-30% reality gap based on literature—hardware results will likely degrade somewhat, though trends should hold.

Second, single-scenario PSO overfitting. This is the root cause of MT-7/MT-8 failures. Multi-scenario PSO is needed and is the top priority for future work.

Third, no disturbance rejection. The controller lacks integral action and the fitness function ignores robustness metrics. This explains the MT-8 zero percent convergence.

Fourth, simplified dynamics model. The simulation assumes rigid bodies with no friction or backlash. Real hardware has 5% parameter uncertainty and nonlinearities.

Fifth, computational cost not analyzed. PSO runtime of 14.2 minutes is fine for offline tuning, but I didn't validate real-time feasibility of the epsilon-effective computation on embedded hardware.

I acknowledge these upfront because transparency is essential. Every limitation is an opportunity for future research."

**Notes:**
- Don't rush—acknowledging limitations shows maturity
- Each limitation has a future work direction (next slide)
- Committee will likely ask about these—better to state them yourself

---

### Slide 32: Future Research Directions
**Timing:** 1.5 minutes

**Script:**
"Five priority future research directions.

Priority 1: Multi-scenario robust PSO. Modify the fitness function to maximize worst-case performance across diverse scenarios: theta-0 from 0.05 to 0.5 radians, plus disturbance scenarios. I expect this will sacrifice nominal performance for robustness—there's no free lunch—but it will fix MT-7/MT-8 failures.

Priority 2: Hardware validation. Implement on the Quanser QUBE-Servo 2 with dSPACE DS1104 real-time controller. Measure the reality gap: simulation versus hardware chattering.

Priority 3: Integral augmentation. Add an integral term to the sliding surface to handle persistent disturbances. Test on MT-8, which currently has zero percent success.

Priority 4: Adaptive PSO meta-optimization. Use Bayesian optimization to tune PSO hyperparameters w, c-1, c-2 for faster convergence.

Priority 5: Extension to other underactuated systems. Cart-pole, Furuta pendulum, quadrotor. The framework is general-purpose.

Priority 1 is the most important—multi-scenario PSO addresses the core limitation of this work."

**Notes:**
- Priority 1 is your immediate next step (emphasize this)
- Hardware validation (Priority 2) is standard next step for simulation work
- Be enthusiastic—these are exciting directions, not just limitations

---

### Slide 33: Final Remarks
**Timing:** 1.5 minutes

**Script:**
"Let me close with three lessons learned.

Lesson 1: Optimization does not equal robustness. PSO can find exceptional solutions for specific scenarios, but without diverse training data, those solutions are brittle. Multi-scenario optimization is essential for real-world deployment. This lesson generalizes beyond SMC—it applies to any machine learning or optimization-based control design.

Lesson 2: Honest validation prevents overconfidence. Publishing only MT-6 results—66.5% improvement—would mislead practitioners into deploying a brittle controller. Documenting MT-7/MT-8 failures raises standards and guides future research. Negative results are contributions, not failures.

Lesson 3: Statistical rigor is non-negotiable. Single-run results can be flukes. Monte Carlo validation plus statistical testing—100-plus trials, p-values, Cohen's d—are necessary to claim significance. Plots and animations are intuitive, but statistics are objective.

Research is about understanding boundaries, not just showcasing successes. This thesis contributes both: exceptional nominal performance in MT-6, and rigorous boundary identification in MT-7/MT-8."

**Notes:**
- These are philosophical takeaways—shows maturity
- Lesson 1 generalizes beyond your work (appeals to broader audience)
- Last sentence is a great summary of your contribution

---

### Slide 34: Conclusion Summary
**Timing:** 1 minute

**Script:**
"To conclude:

Successful outcomes: Exceptional chattering reduction, zero energy penalty, theoretical stability guarantees, novel PSO framework.

Critical findings: Generalization failures quantified, single-scenario overfitting identified, disturbance rejection absent.

Broader impact: Establishes best practices for honest SMC validation, demonstrates importance of multi-scenario testing, provides blueprint for robust PSO-based controller optimization.

In one sentence: This thesis is a step forward in chattering mitigation and a cautionary tale about optimization brittleness."

**Notes:**
- Balance positive and negative—shows objectivity
- "Cautionary tale" is honest and memorable
- This is your closing argument—make it count

---

### Slide 35: Thank You
**Timing:** 10 seconds

**Script:**
"Thank you for your attention. I'm happy to answer your questions."

**Notes:**
- Smile, make eye contact
- Confident posture
- Have water ready for Q&A
- Anticipated questions document is in your notes (see next file)

---

## BACKUP SLIDES (for Q&A) — Use as Needed

### Slide 36: Lyapunov Derivation Details
**Use if:** Committee asks for mathematical proof details

**Script:**
"Here's the full Lyapunov proof. [Walk through equations step by step, pointing to each line.] The key step is choosing control gain k large enough to satisfy this inequality, which ensures V-dot is negative definite. Integrating gives the finite-time reaching bound."

### Slide 37: Controller Architecture Diagram
**Use if:** Committee asks about implementation details

**Script:**
"This block diagram shows the full controller architecture. The sliding surface block computes s from the state error. The adaptive boundary layer block computes epsilon-effective from s-dot. The control law block combines them via saturation. Feedback loops are shown here."

### Slide 38: PSO Parameter Sensitivity
**Use if:** Committee asks why you chose 70-15-15 weights

**Script:**
"This table shows sensitivity analysis. I tested weights from 60-20-20 to 80-10-10. Chattering varies by only 6% across this range, confirming robustness. The 70-15-15 choice is justified but not unique. PSO hyperparameter sensitivity is shown below—inertia weight w equals 0.7 converges fastest."

### Slide 39: Additional Statistical Tests
**Use if:** Committee questions statistical methodology

**Script:**
"I ran additional tests beyond Welch's t-test. Bootstrap confidence intervals with 10,000 resamples confirm the MT-6 reduction is 62-70%. Mann-Whitney U test, a non-parametric alternative to t-test, gives p equals 1.4 times ten to the minus eleven—same conclusion. Shapiro-Wilk tests confirm approximate normality, justifying parametric tests. Levene's test confirms equal variances, justifying pooled Cohen's d."

### Slide 40: Hardware Validation Plan
**Use if:** Committee asks about future hardware experiments

**Script:**
"The hardware validation plan uses Quanser QUBE-Servo 2 equipment, which I've already identified and budgeted. The protocol involves system ID to measure real parameters, model validation to quantify sim-vs-hardware error, then MT-6 replication with 20 hardware trials. Expected challenges include actuator saturation, encoder quantization, and friction. Success criterion is hardware chattering within 50% of simulation—a realistic target given 10-30% typical reality gaps."

---

## GENERAL Q&A STRATEGY

### Likely Questions & Prepared Answers

**Q: "Why didn't you implement on hardware?"**
**A:** "Time constraints and methodological priorities. I focused on establishing rigorous validation methodology—multi-scenario testing, statistical analysis, honest failure reporting—in simulation first. Hardware validation is the immediate next step, but I wanted the methodology solid before investing in expensive hardware experiments. The Quanser equipment is identified, and I estimate 10-30% reality gap based on literature."

**Q: "Why not use multi-scenario PSO from the start?"**
**A:** "Excellent question. I discovered the generalization failure empirically through MT-7. Initially, I hypothesized single-scenario PSO would suffice because I was training on realistic nominal conditions. MT-7 proved that hypothesis wrong, which is a finding. In hindsight, multi-scenario PSO should have been the baseline approach, but the negative result itself contributes to the literature by demonstrating brittleness."

**Q: "How do you know MT-6 results aren't overfitting to simulation?"**
**A:** "Three pieces of evidence: 10-fold cross-validation within MT-6 showed test fitness equals training fitness, indicating no overfitting within that scenario. Bootstrap resampling of the 100 trials gave tight confidence intervals, confirming reproducibility. Finally, the super-twisting baseline also improved in MT-6, suggesting the scenario itself is representative, not a lucky edge case. However, MT-7 shows the parameters don't generalize across scenarios—that's a different kind of overfitting."

**Q: "Is Cohen's d = 5.29 too good to be true?"**
**A:** "It's exceptional but validated. I was skeptical too, which is why I ran 100 trials, bootstrap CIs, Mann-Whitney U test, and sensitivity analysis—all confirmed the result. However, it's scenario-specific. In MT-7, the effect completely reverses. So d = 5.29 is real but localized to the nominal operating envelope."

**Q: "What's the computational cost of epsilon-effective calculation?"**
**A:** "The adaptive boundary layer adds one multiplication and one addition per control cycle: epsilon-min plus alpha times absolute s-dot. On a 1 kHz control loop, this is negligible—maybe 10 microseconds on modern microcontrollers. The PSO optimization is offline, 14.2 minutes on a laptop, which is acceptable since it's a one-time tuning phase. Real-time feasibility is not a concern."

**Q: "How did you choose the 70-15-15 fitness weights?"**
**A:** "I prioritized chattering because it's the problem being solved. Settling time and overshoot are secondary metrics. Sensitivity analysis in Section 6.4 tested 60-20-20 to 80-10-10—results were robust. I also consulted literature: multi-objective PSO papers recommend 60-80% weight on the primary objective."

**Q: "Why is MT-7 degradation exactly 50.4×?"**
**A:** "That's the ratio: MT-7 chattering 242.1 divided by MT-6 chattering 4.8 equals 50.4. It's not a magic number—just the empirical degradation factor. The mechanism is epsilon-effective growing too large at 0.3 radians, causing loss of control authority."

**Q: "Can you explain the epsilon-effective saturation mechanism?"**
**A:** "Sure. At theta-0 equals 0.3 radians, the initial error is three times larger than 0.1 radians. Larger error means larger s-dot via the sliding surface dynamics. Epsilon-effective equals epsilon-min plus alpha times s-dot responds by becoming very large—say 0.5 or more. The saturation function sat(s / 0.5) compresses the control to near zero. With u approximately zero, there's no control authority, and the system diverges."

---

## TIME MANAGEMENT CHECKLIST

- Introduction (Slides 1-5): **5 minutes**
- Background (Slides 6-10): **5 minutes**
- Methodology (Slides 11-15): **10 minutes**
- **Results (Slides 16-23): 15 minutes** ← MOST IMPORTANT
- Discussion (Slides 24-28): **5 minutes**
- Conclusions (Slides 29-35): **5 minutes**
- **Total: 45 minutes**
- Buffer for interruptions: **5 minutes** → Total 50 minutes max
- Q&A: **10-15 minutes**

---

## CONFIDENCE REMINDERS

- You've done rigorous work—100+ trials, statistical validation, honest reporting
- MT-7/MT-8 failures are FEATURES, not bugs—they show methodological maturity
- Cohen's d = 5.29 is unprecedented in literature—own this achievement
- Multi-scenario PSO is a clear, actionable future direction
- Your methodology (Monte Carlo, Welch's t-test, multi-scenario testing) raises standards

**You are ready. Good luck!**
