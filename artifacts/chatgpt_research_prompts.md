# ChatGPT Research Prompts for Citation Finding

**Purpose:** Copy-paste ready prompts for efficient batch research using ChatGPT/Claude
**Strategy:** Group similar claims, research together, reuse citations

---

## How to Use These Prompts

### Step 1: Choose Your Batch
Look at `research_batch_plan.json` or filter CSV by topic

### Step 2: Copy Batch-Specific Prompt
Copy the entire prompt template below for your topic

### Step 3: Add Claims to Prompt
Insert 5-10 claims from your batch into the prompt

### Step 4: Get Results from ChatGPT
Paste prompt → Get citations → Fill CSV

### Step 5: Reuse Citations
Same citations often work for multiple claims in same batch!

---

## Prompt Template: CRITICAL Priority - Theorems/Lemmas

```
I need academic citations for mathematical theorems and control theory claims in a research project. Please provide:

1. **Most authoritative citation** (prefer IEEE TAC, Automatica, or seminal textbooks)
2. **BibTeX key** (format: firstauthor_year_keyword)
3. **DOI or URL**
4. **Reference type** (journal/conference/book)
5. **Brief note** (1 sentence why this is the right citation)

Please research these CRITICAL theoretical claims:

---

CLAIM 1:
- **ID:** FORMAL-THEOREM-001
- **Statement:** "Hysteresis with deadband δ prevents oscillation for residuals with bounded derivative."
- **Context:** Fault detection and isolation (FDI) threshold calibration
- **Topic:** Control systems, hysteresis, oscillation prevention

---

CLAIM 2:
- **ID:** FORMAL-THEOREM-004
- **Statement:** "The PSO-optimized gains ensure global asymptotic stability of the DIP system."
- **Context:** Particle Swarm Optimization for double inverted pendulum control
- **Topic:** PSO optimization, global stability, inverted pendulum

---

[Add 3-8 more claims here...]

---

For each claim, provide citation in this format:

**CLAIM 1 (FORMAL-THEOREM-001):**
- Citation: Hespanha et al. (2003)
- BibTeX Key: hespanha2003hysteresis
- DOI: 10.1109/TAC.2003.812777
- Type: journal
- Note: Proves hysteresis with deadband prevents oscillation in switching systems (IEEE TAC)

**CLAIM 2 (FORMAL-THEOREM-004):**
- Citation: ...
```

---

## Prompt Template: HIGH Priority - Sliding Mode Control (Classical)

```
I'm documenting implementation claims for classical sliding mode control in a research codebase. Please find citations for these algorithm implementations:

**Focus Area:** Classical SMC, boundary layer, chattering reduction, sliding surfaces

For each claim, provide:
1. Primary citation (prefer: Slotine & Li, Utkin, Edwards & Spurgeon)
2. BibTeX key
3. DOI/URL
4. Why this citation fits the claim

---

CLAIM 1:
- **ID:** CODE-IMPL-042
- **Description:** "Classical SMC with boundary layer for chattering reduction"
- **File:** src/controllers/smc/classic_smc.py
- **Context:** Implements tanh boundary layer to smooth control signal
- **Keywords:** boundary layer, chattering, smooth switching

---

CLAIM 2:
- **ID:** CODE-IMPL-055
- **Description:** "Sliding surface design with eigenvalue placement"
- **File:** src/controllers/smc/classic_smc.py
- **Context:** Surface coefficients chosen for desired closed-loop poles
- **Keywords:** sliding surface, eigenvalue placement, reaching law

---

[Add more claims...]

---

**Suggested Common Citations (verify applicability):**
- Slotine & Li (1991) "Applied Nonlinear Control" - THE classical SMC textbook
- Utkin (1992) "Sliding Modes in Control and Optimization" - Foundational work
- Edwards & Spurgeon (1998) "Sliding Mode Control" - Comprehensive reference

Please provide specific citations matching each claim's focus.
```

---

## Prompt Template: HIGH Priority - Super-Twisting Algorithm

```
I need citations for Super-Twisting Algorithm (STA) implementations in a sliding mode control project.

**Focus:** Second-order sliding modes, finite-time convergence, chattering-free control

For each claim, cite the most relevant work from: Levant (2003, 2005, 2007), Moreno & Osorio (2012), Shtessel et al. (2014)

---

CLAIM 1:
- **ID:** CODE-IMPL-078
- **Description:** "Super-twisting algorithm with continuous control"
- **Context:** Implements Levant's twisting algorithm for chattering-free finite-time convergence
- **Keywords:** super-twisting, second-order sliding, continuous control

---

CLAIM 2:
- **ID:** CODE-IMPL-082
- **Description:** "Finite-time convergence proof for super-twisting"
- **Context:** Lyapunov analysis showing finite-time reaching
- **Keywords:** finite-time, Lyapunov, convergence proof

---

[Add more claims...]

---

**Common STA Citations (verify applicability):**
- Levant (2003) "Higher-order sliding modes, differentiation and output-feedback control" - Original STA paper
- Moreno & Osorio (2012) "Strict Lyapunov Functions for the Super-Twisting Algorithm" - Stability proof
- Shtessel et al. (2014) "Sliding Mode Control and Observation" - Modern reference

Match each claim to specific aspects covered in these papers.
```

---

## Prompt Template: HIGH Priority - PSO Optimization

```
I need citations for Particle Swarm Optimization (PSO) implementation and theory in a control systems tuning project.

**Focus:** PSO algorithm, gain tuning, parameter optimization, swarm intelligence

For each claim, provide citation (prefer: Kennedy & Eberhart, Shi & Eberhart, Clerc & Kennedy)

---

CLAIM 1:
- **ID:** CODE-IMPL-125
- **Description:** "PSO-based controller gain tuning"
- **Context:** Uses PSO to optimize SMC gains for minimal tracking error
- **Keywords:** PSO, gain tuning, parameter optimization

---

CLAIM 2:
- **ID:** CODE-IMPL-130
- **Description:** "Inertia weight scheduling in PSO"
- **Context:** Implements linearly decreasing inertia weight for convergence
- **Keywords:** inertia weight, convergence, Shi & Eberhart

---

[Add more claims...]

---

**Common PSO Citations:**
- Kennedy & Eberhart (1995) "Particle swarm optimization" - THE original PSO paper
- Shi & Eberhart (1998) "A modified particle swarm optimizer" - Inertia weight innovation
- Clerc & Kennedy (2002) "The particle swarm - explosion, stability, and convergence" - Theoretical analysis

Please match each claim to specific PSO aspects.
```

---

## Prompt Template: HIGH Priority - Adaptive Control

```
I need citations for adaptive sliding mode control implementations.

**Focus:** Adaptation laws, online gain adjustment, uncertainty estimation

For each claim, cite from: Slotine & Li (1987, 1991), Plestan et al. (2010), Utkin et al. (1999)

---

CLAIM 1:
- **ID:** CODE-IMPL-156
- **Description:** "Adaptive law for uncertainty estimation"
- **Context:** Online adaptation of SMC gains based on tracking error
- **Keywords:** adaptive law, uncertainty, online estimation

---

CLAIM 2:
- **ID:** CODE-IMPL-160
- **Description:** "Gradient-based parameter adaptation"
- **Context:** Uses Lyapunov design for stable parameter updates
- **Keywords:** gradient adaptation, Lyapunov design, parameter update

---

[Add more claims...]

---

**Common Adaptive SMC Citations:**
- Slotine & Li (1987) "On the Adaptive Control of Robot Manipulators" - Classic adaptive SMC
- Plestan et al. (2010) "New methodologies for adaptive sliding mode control" - Modern techniques
- Utkin et al. (1999) "Sliding Mode Control in Electromechanical Systems" - Applied adaptive SMC

Match claims to specific adaptation techniques.
```

---

## Prompt Template: HIGH Priority - Numerical Methods

```
I need citations for numerical stability techniques in control system simulations.

**Focus:** Matrix regularization, condition number analysis, numerical integration, ill-conditioned systems

---

CLAIM 1:
- **ID:** CODE-IMPL-200
- **Description:** "Matrix regularization for ill-conditioned systems"
- **Context:** Adds small regularization term to prevent singular matrix errors
- **Keywords:** regularization, ill-conditioned, matrix inversion

---

CLAIM 2:
- **ID:** CODE-IMPL-205
- **Description:** "Runge-Kutta 4th order integration"
- **Context:** RK4 method for pendulum dynamics simulation
- **Keywords:** RK4, numerical integration, ODE solver

---

[Add more claims...]

---

**Common Numerical Methods Citations:**
- Golub & Van Loan (2013) "Matrix Computations" - Matrix algorithms bible
- Press et al. (2007) "Numerical Recipes" - Practical numerical methods
- Hairer et al. (1993) "Solving Ordinary Differential Equations" - ODE integration theory

Provide citations matching specific numerical techniques used.
```

---

## Prompt Template: HIGH Priority - Benchmarking & Performance Metrics

```
I need citations for performance metrics used in control system evaluation.

**Focus:** ISE, ITAE, RMS error, statistical analysis, Monte Carlo validation

---

CLAIM 1:
- **ID:** CODE-IMPL-250
- **Description:** "Integral of Squared Error (ISE) performance metric"
- **Context:** Uses ISE to quantify tracking performance
- **Keywords:** ISE, performance metric, tracking error

---

CLAIM 2:
- **ID:** CODE-IMPL-255
- **Description:** "Monte Carlo statistical validation"
- **Context:** Runs 1000 trials with random initial conditions for robustness testing
- **Keywords:** Monte Carlo, statistical validation, robustness

---

[Add more claims...]

---

**Common Performance Metrics Citations:**
- Franklin et al. (2014) "Feedback Control of Dynamic Systems" - Standard control metrics
- Åström & Murray (2008) "Feedback Systems" - Performance analysis
- Ogata (2010) "Modern Control Engineering" - Classical metrics reference

Match each metric to textbook/paper where it's formally defined.
```

---

## Prompt Template: MEDIUM Priority - Citation Validation

```
I need to VALIDATE existing citations in a control systems project. Please verify these are correct and suggest improvements if needed.

For each claim:
1. Confirm citation is appropriate
2. Provide DOI if missing
3. Suggest better citation if current one is weak

---

CLAIM 1:
- **ID:** CODE-IMPL-300
- **Current Citation:** Levant (2003)
- **Citation Format:** {cite}`levant2003higher`
- **Claim:** "Super-twisting algorithm for second-order sliding modes"
- **Question:** Is this the right Levant paper? Should we cite a more specific one?

---

CLAIM 2:
- **ID:** CODE-IMPL-305
- **Current Citation:** Slotine & Li (1991)
- **Citation Format:** Author (Year) in text
- **Claim:** "Sliding surface design with eigenvalue placement"
- **Question:** Is chapter/page reference needed? Any DOI for this book?

---

[Add more validation requests...]

---

Please verify each citation and suggest improvements.
```

---

## General Tips for ChatGPT Research

### Getting Better Results

**1. Be Specific About Context**
```
❌ "Find citation for sliding mode control"
✅ "Find citation for classical SMC with boundary layer chattering reduction,
   preferably from Slotine & Li or Utkin"
```

**2. Request Specific Output Format**
```
Always ask for:
- Author (Year) format
- BibTeX key suggestion
- DOI
- Brief justification
```

**3. Batch Similar Claims**
```
Research 5-10 related claims together
→ ChatGPT can identify shared citations
→ You fill CSV faster with copy-paste
```

**4. Verify Important Claims**
```
For CRITICAL theorems:
"Please double-check this is the seminal paper for this theorem.
If there's a more authoritative source, suggest it."
```

### Handling ChatGPT Responses

**After Getting Results:**
1. **Copy citations to notepad** (don't lose them!)
2. **Verify DOI links** (click to confirm they work)
3. **Fill CSV immediately** (don't procrastinate!)
4. **Mark Research_Status** "completed"
5. **Reuse for similar claims** in same batch

**If Citation Seems Wrong:**
- Ask ChatGPT for alternatives
- Google Scholar the claim keywords
- Check if citation matches claim specifics

---

## Reusable Citation Database (Build as You Go)

### Core SMC Citations (use 50+ times)

```
Slotine & Li (1991) - Applied Nonlinear Control
  BibTeX: slotine1991applied
  Use for: Classical SMC, sliding surfaces, reaching laws, chattering

Utkin (1992) - Sliding Modes in Control and Optimization
  BibTeX: utkin1992sliding
  Use for: SMC theory, variable structure, switching functions

Levant (2003) - Higher-order sliding modes
  BibTeX: levant2003higher
  DOI: 10.1080/0020717031000099029
  Use for: Super-twisting, 2nd order sliding, finite-time convergence

Moreno & Osorio (2012) - Strict Lyapunov Functions for STA
  BibTeX: moreno2012strict
  DOI: 10.1109/TAC.2012.2186179
  Use for: STA stability proofs, Lyapunov analysis

Kennedy & Eberhart (1995) - Particle swarm optimization
  BibTeX: kennedy1995pso
  Use for: PSO algorithm, swarm intelligence, optimization
```

### Build Your Database
After each batch, note "super-citations" used 5+ times
→ These become your go-to references
→ Speeds up future batches dramatically

---

## Example Research Session (Real Workflow)

**Batch:** HIGH Priority - Sliding Mode Classical (18 claims)

**Step 1:** Filter CSV
```
Priority = HIGH
Research_Description contains "sliding mode" or "classical smc"
→ Got 18 claims
```

**Step 2:** Group claims by sub-topic
```
- Boundary layer (5 claims)
- Sliding surface design (4 claims)
- Reaching law (3 claims)
- Chattering reduction (6 claims)
```

**Step 3:** Research first sub-group (Boundary layer)
```
Copied 5 boundary layer claims into ChatGPT prompt
→ Got results:
  All 5 → Slotine & Li (1991), Chapter 7
  3 of them also → Slotine (1984) original paper
```

**Step 4:** Fill CSV (5 claims in 2 minutes!)
```
All 5 claims:
  Suggested_Citation: Slotine & Li (1991)
  BibTeX_Key: slotine1991applied
  Reference_Type: book
  Research_Status: completed
  Research_Notes: Chapter 7 on SMC (3 also cite Slotine 1984)
```

**Step 5:** Repeat for other sub-groups
```
Total time: 18 claims in ~30 minutes
  (vs 3+ hours researching individually!)
```

---

## Tracking Progress

As you complete batches, track which topics are done:

### CRITICAL Batches (Priority 1)
- [ ] sliding_mode_classical (4 claims)
- [ ] pso_optimization (3 claims)
- [ ] control_theory_general (3 claims)
- [ ] lyapunov_stability (2 claims)
- [ ] inverted_pendulum (2 claims)
- [ ] sliding_mode_super_twisting (2 claims)
- [ ] fault_detection (1 claim)

### HIGH Batches (Priority 2) - Top 10 by Count
- [ ] implementation_general (314 claims) ← Biggest batch!
- [ ] fault_detection (27 claims)
- [ ] numerical_methods (20 claims)
- [ ] sliding_mode_classical (18 claims)
- [ ] benchmarking_performance (17 claims)
- [ ] pso_optimization (16 claims)
- [ ] sliding_mode_super_twisting (13 claims)
- [ ] inverted_pendulum (11 claims)
- [ ] sliding_mode_adaptive (11 claims)
- [ ] control_theory_general (7 claims)

**Strategy:** Tackle HIGH batches by topic, not sequentially
→ Research all SMC together, all PSO together, etc.
→ Massive time savings from citation reuse!

---

**Total Prompts Provided:** 8 topic-specific templates
**Estimated Time Savings:** 60-70% vs individual research
**Ready to use:** Copy, paste, customize with your claims!

🚀 **Start with CRITICAL batches → Build citation database → Reuse for HIGH batches!**
