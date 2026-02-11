# 14-Day Full Immersion Daily Checklist

Print this document and check off items as you complete them. Each day is designed for 8-10 hours of focused learning.

---

## WEEK 1: THEORY + ARCHITECTURE

### Day 1: Project Foundations [___ / 8 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E001 podcast (18 min)
- [ ] Hour 1-2: Read E001 cheatsheet PDF
- [ ] Hour 3-4: Listen to E002 podcast (18 min)
- [ ] Hour 3-4: Read E002 cheatsheet PDF

**Afternoon Block (4 hours)**
- [ ] Hour 5-6: Read `.ai_workspace/guides/session_continuity.md`
- [ ] Hour 5-6: Read `CLAUDE.md` (project conventions)
- [ ] Hour 7: Setup environment: Clone repo if needed
- [ ] Hour 7: Install dependencies: `pip install -r requirements.txt`
- [ ] Hour 8: Run first simulation: `python simulate.py --ctrl classical_smc --plot`
- [ ] Hour 8: Verify Streamlit works: `streamlit run streamlit_app.py`

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 2 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 2: Plant Dynamics [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E003 podcast
- [ ] Hour 1-2: Read E003 cheatsheet PDF
- [ ] Hour 3-4: Code walkthrough: `src/plant/models/simplified_dynamics.py`
- [ ] Hour 3-4: Code walkthrough: `src/plant/models/full_nonlinear_dynamics.py`

**Afternoon Block (4 hours)**
- [ ] Hour 5: Study low-rank dynamics variant
- [ ] Hour 6-7: Read `docs/theory/plant-dynamics.md`
- [ ] Hour 8: Visualize pendulum physics (double pendulum animations)

**Evening Block (2 hours)**
- [ ] Hour 9: Open `config.yaml`, find plant parameters section
- [ ] Hour 9: Modify mass values (m1, m2), observe simulation behavior
- [ ] Hour 10: Modify length values (l1, l2), observe stability changes

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 3 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 3: Optimization Fundamentals [___ / 9 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E004 podcast (26 min)
- [ ] Hour 1-2: Read E004 cheatsheet PDF
- [ ] Hour 3-5: Code walkthrough: `src/optimizer/pso_optimizer.py` (413 lines)
- [ ] Hour 3-5: Understand PSO parameters: swarm size, iterations, bounds

**Afternoon Block (3 hours)**
- [ ] Hour 6-7: Read research paper excerpts on PSO theory
- [ ] Hour 6-7: Study `academic/paper/experiments/` structure

**Evening Block (2 hours)**
- [ ] Hour 8: Run PSO optimization: `python simulate.py --ctrl classical_smc --run-pso --save day3_gains.json`
- [ ] Hour 9: Analyze results: Compare tuned vs. default gains
- [ ] Hour 9: Visualize convergence plots

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 4 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 4: Simulation Engine [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E005 podcast (26 min)
- [ ] Hour 1-2: Read E005 cheatsheet PDF
- [ ] Hour 3-5: Code walkthrough: `src/core/simulation_runner.py`
- [ ] Hour 3-5: Code walkthrough: `src/core/simulation_context.py`

**Afternoon Block (4 hours)**
- [ ] Hour 6: Study integrators: RK45, Euler, custom methods
- [ ] Hour 7: Understand vectorized simulation in `src/core/vector_sim.py`
- [ ] Hour 8: Study Numba optimizations and performance

**Evening Block (2 hours)**
- [ ] Hour 9: Run batch simulations with different integrators
- [ ] Hour 10: Compare accuracy and speed tradeoffs
- [ ] Hour 10: Document findings in personal notes

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 5 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 5: Controllers Part 1 [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Read E030 cheatsheet PDF (Controller Base & Factory)
- [ ] Hour 3-5: Code deep-dive: `src/controllers/base/base_controller.py`
- [ ] Hour 3-5: Code deep-dive: `src/controllers/factory/controller_factory.py`

**Afternoon Block (4 hours)**
- [ ] Hour 6-8: Classical SMC implementation study
- [ ] Hour 6-8: File: `src/controllers/smc/algorithms/classical_smc.py` (538 lines)
- [ ] Hour 6-8: Understand sliding surface, reaching law, control law

**Evening Block (2 hours)**
- [ ] Hour 9-10: Hands-on: Implement sliding surface equation from scratch
- [ ] Hour 9-10: Verify your implementation against production code
- [ ] Hour 9-10: Test with simple pendulum case

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 6 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 6: Controllers Part 2 [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-3: Super-Twisting SMC deep-dive
- [ ] Hour 1-3: File: `src/controllers/smc/algorithms/super_twisting_smc.py` (592 lines)
- [ ] Hour 1-3: Understand chattering reduction mechanism

**Afternoon Block (4 hours)**
- [ ] Hour 4-6: Adaptive SMC study
- [ ] Hour 4-6: File: `src/controllers/smc/algorithms/adaptive_smc.py` (473 lines)
- [ ] Hour 4-6: Understand gain adaptation rules

**Evening Block (2 hours)**
- [ ] Hour 7-9: Hybrid Adaptive STA-SMC
- [ ] Hour 7-9: File: `src/controllers/smc/algorithms/hybrid_adaptive_sta_smc.py` (277 lines)
- [ ] Hour 10: Compare chattering behavior across all 4 controllers
- [ ] Hour 10: Run simulations with each controller, measure chattering index

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 7 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 7: Analysis & Visualization [___ / 9 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E006 podcast (28 min - LONGEST)
- [ ] Hour 1-2: Read E006 cheatsheet PDF
- [ ] Hour 3-5: Code walkthrough: `src/analysis/` directory
- [ ] Hour 3-5: Code walkthrough: `src/utils/visualization/` directory

**Afternoon Block (3 hours)**
- [ ] Hour 6-7: Study benchmark framework: `src/benchmarks/`
- [ ] Hour 6-7: Review `benchmarks/figures/` - publication-quality examples

**Evening Block (2 hours)**
- [ ] Hour 8: Generate plots: State trajectories, control effort, chattering
- [ ] Hour 9: Calculate chattering metrics for all controllers
- [ ] Hour 9: Create comparison table

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn this week?
- [ ] Review Week 1 progress: What % do I understand? ___
- [ ] Preview Day 8 materials
- [ ] Rate overall Week 1: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

## WEEK 2: PRACTICE + INTEGRATION

### Day 8: Testing & Quality [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E007 podcast
- [ ] Hour 1-2: Read E007 cheatsheet PDF
- [ ] Hour 3-5: Explore `tests/test_controllers/` directory
- [ ] Hour 3-5: Study test patterns for all 6 controllers

**Afternoon Block (4 hours)**
- [ ] Hour 6-7: Read `.ai_workspace/config/testing_standards.md`
- [ ] Hour 6-7: Understand coverage requirements (85%/95%/100%)

**Evening Block (2 hours)**
- [ ] Hour 8: Run pytest suite: `python -m pytest tests/test_controllers/ -v`
- [ ] Hour 9: Write test for custom controller variant
- [ ] Hour 10: Generate coverage report: `python -m pytest --cov=src --cov-report=html`
- [ ] Hour 10: Review coverage in `htmlcov/index.html`

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 9 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 9: Research Outputs [___ / 9 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E008 podcast (27 min)
- [ ] Hour 1-2: Read E008 cheatsheet PDF
- [ ] Hour 3-5: Read LT-7 research paper (submission-ready version)
- [ ] Hour 3-5: Location: `academic/paper/publications/`

**Afternoon Block (3 hours)**
- [ ] Hour 6-7: Study experiment structure: `academic/paper/experiments/comparative/`
- [ ] Hour 6-7: Review MT-5 comprehensive benchmark results

**Evening Block (2 hours)**
- [ ] Hour 8: Analyze MT-7 robust PSO results
- [ ] Hour 9: Review MT-8 disturbance rejection benchmarks
- [ ] Hour 9: Compare your Day 3 PSO results with published benchmarks

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 10 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 10: Systems Integration [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E012 podcast (HIL system)
- [ ] Hour 1-2: Listen to E013 podcast (Monitoring infrastructure)
- [ ] Hour 3-5: Code walkthrough: `src/hil/plant_server.py`
- [ ] Hour 3-5: Code walkthrough: `src/hil/controller_client.py`

**Afternoon Block (4 hours)**
- [ ] Hour 6-8: Study monitoring infrastructure: `src/utils/monitoring/`
- [ ] Hour 6-8: Understand latency tracking, deadline monitoring, weakly-hard constraints

**Evening Block (2 hours)**
- [ ] Hour 9: Run HIL simulation: `python simulate.py --run-hil --plot`
- [ ] Hour 10: Visualize real-time monitoring data
- [ ] Hour 10: Analyze control loop timing statistics

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 11 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 11: Professional Standards [___ / 8 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-3: Read E015-E019 cheatsheets (batch reading session)
  - [ ] E015: Architectural Standards
  - [ ] E016: Documentation Quality
  - [ ] E017: Multi-agent Orchestration
  - [ ] E018: Testing Philosophy
  - [ ] E019: Production Safety

**Afternoon Block (3 hours)**
- [ ] Hour 4-5: Study `.ai_workspace/guides/architectural_standards.md`
- [ ] Hour 4-5: Understand critical invariants (NEVER VIOLATE section)
- [ ] Hour 6-7: Review `.ai_workspace/guides/controller_memory.md`
- [ ] Hour 6-7: Understand weakref patterns, cleanup methods

**Evening Block (1 hour)**
- [ ] Hour 8: Read E020 cheatsheet (Git workflow)
- [ ] Hour 8: Practice git operations: branch, commit, merge
- [ ] Hour 8: Review `.ai_workspace/config/repository_management.md`

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 12 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 12: Configuration & Deployment [___ / 10 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E011 podcast
- [ ] Hour 1-2: Read E011 cheatsheet PDF
- [ ] Hour 3-5: Deep-dive into `config.yaml` - ALL sections
  - [ ] Physics parameters
  - [ ] Controller gains (all 6 controllers)
  - [ ] PSO parameters
  - [ ] Simulation settings
  - [ ] HIL configuration
  - [ ] Fault detection thresholds

**Afternoon Block (4 hours)**
- [ ] Hour 6-8: Study Pydantic validation: `src/config/` directory
- [ ] Hour 6-8: Understand config loading, validation, error handling

**Evening Block (2 hours)**
- [ ] Hour 9: Create custom config for swing-up controller
- [ ] Hour 9: Test config validation with intentional errors
- [ ] Hour 10: Run simulation with custom config
- [ ] Hour 10: Document config best practices

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 13 materials
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 13: Documentation & MCP [___ / 9 hours]

**Morning Block (4 hours)**
- [ ] Hour 1-2: Listen to E009 podcast (Educational Materials)
- [ ] Hour 1-2: Listen to E010 podcast (Documentation System)
- [ ] Hour 3-4: Navigate complete docs using `docs/NAVIGATION.md`
- [ ] Hour 3-4: Explore all 11 navigation systems

**Afternoon Block (3 hours)**
- [ ] Hour 5-6: Study `.ai_workspace/guides/mcp_usage_guide.md`
- [ ] Hour 5-6: Understand 12 available MCP servers

**Evening Block (2 hours)**
- [ ] Hour 7: Build Sphinx documentation: `sphinx-build -M html docs docs/_build`
- [ ] Hour 8: Explore MCP servers: sequential-thinking, pytest-mcp
- [ ] Hour 9: Practice using filesystem and sqlite-mcp servers

**Evening Reflection**
- [ ] Write 3-5 sentences: What did I learn today?
- [ ] Preview Day 14 materials (CAPSTONE!)
- [ ] Rate understanding: 1-10 ___

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

### Day 14: Capstone Project [___ / 10 hours]

**Morning Block (2 hours)**
- [ ] Hour 1-2: Listen to E021 podcast (Future Work & Roadmap)
- [ ] Hour 1-2: Read E024 cheatsheet (Lessons Learned)

**CAPSTONE EXERCISE (8 hours)**

**Phase 1: Design (1 hour)**
- [ ] Hour 3: Define research question
  - Example: "Which controller minimizes chattering under 10% measurement noise?"
- [ ] Hour 3: Plan experiment methodology
- [ ] Hour 3: Document expected outcomes

**Phase 2: Configuration (1 hour)**
- [ ] Hour 4: Create custom `capstone_config.yaml`
- [ ] Hour 4: Select 2 controllers to compare
- [ ] Hour 4: Configure noise levels, simulation duration

**Phase 3: Optimization (2 hours)**
- [ ] Hour 5-6: Run PSO optimization for Controller 1
- [ ] Hour 5-6: Run PSO optimization for Controller 2
- [ ] Hour 5-6: Save gains: `capstone_controller1_gains.json`, `capstone_controller2_gains.json`

**Phase 4: Benchmark (2 hours)**
- [ ] Hour 7: Execute comparative benchmark
- [ ] Hour 7: Run 20 Monte Carlo trials per controller
- [ ] Hour 8: Calculate statistics: mean, std, confidence intervals
- [ ] Hour 8: Measure chattering index, settling time, tracking error

**Phase 5: Analysis (1 hour)**
- [ ] Hour 9: Generate plots: state trajectories, control effort, chattering
- [ ] Hour 9: Create comparison table
- [ ] Hour 9: Statistical significance testing (t-test)

**Phase 6: Documentation (1 hour)**
- [ ] Hour 10: Write markdown report (`capstone_report.md`)
- [ ] Hour 10: Include: research question, methodology, results, conclusions
- [ ] Hour 10: Commit work using proper git workflow
- [ ] Hour 10: Push to repository (if applicable)

**Evening Reflection - FINAL**
- [ ] Write 1 page: What did I accomplish in 14 days?
- [ ] List 5 most important things learned
- [ ] Self-assess: Understanding ___ / 100, Skills ___ / 100
- [ ] Plan next steps: Tutorial 01, research tasks, or custom projects

**Notes:**
_________________________________________________________________________________________________
_________________________________________________________________________________________________
_________________________________________________________________________________________________

---

## COMPLETION CERTIFICATE

I, _________________________, completed the 14-Day Full Immersion DIP-SMC-PSO Learning Program.

**Start Date:** _______________
**End Date:** _______________
**Total Hours:** _____

**Achievements:**
- [ ] Understand all 6 controller algorithms
- [ ] Can run and modify simulations independently
- [ ] Completed PSO optimization successfully
- [ ] Generated publication-quality plots
- [ ] Completed capstone project
- [ ] Ready to contribute code to the project

**Signature:** _________________________ **Date:** _______________

---

## Next Steps After Completion

1. [ ] Begin Tutorial 01: `docs/guides/getting-started.md`
2. [ ] Continue 1-2 hours/day for 2-3 months (reach mastery)
3. [ ] Use podcasts during commute for reinforcement
4. [ ] Join research tasks: `.ai_workspace/planning/research/`
5. [ ] Contribute to open issues or propose new features
6. [ ] Consider publishing your capstone findings

**Target Mastery Date:** _______________
