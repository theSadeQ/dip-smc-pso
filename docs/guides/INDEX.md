# Documentation Navigation Hub **Welcome to the DIP SMC PSO Framework Documentation** This is your central navigation hub for all project documentation. Whether you're a beginner taking your first steps or an experienced researcher implementing novel controllers, you'll find the right resources here. --- ## Table of Contents - [Documentation Map](#documentation-map)
- [Getting Started](#getting-started)
- [Learning Paths](#learning-paths)
- [Documentation by Category](#documentation-by-category)
- [Most Popular Pages](#most-popular-pages)
- [Recently Updated](#recently-updated)
- [Quick Search](#quick-search) --- ## Documentation Map ```mermaid
flowchart TD ROOT["📚 Documentation Hub<br/>(You are here)"] ROOT --> QUICK["🚀 Getting Started"] ROOT --> TUTORIALS["📚 Tutorials"] ROOT --> HOWTO["📖 How-To Guides"] ROOT --> API["🔧 API Reference"] ROOT --> THEORY["📐 Theory & Explanation"] QUICK --> Q1["Getting Started<br/>(15 min)"] QUICK --> Q2["User Guide<br/>(30 min)"] QUICK --> Q3["Quick Reference<br/>(5 min)"] TUTORIALS --> T1["Tutorial 01: First Simulation<br/>(45 min)"] TUTORIALS --> T2["Tutorial 02: Controller Comparison<br/>(60 min)"] TUTORIALS --> T3["Tutorial 03: PSO Optimization<br/>(90 min)"] TUTORIALS --> T4["Tutorial 04: Custom Controller<br/>(120 min)"] TUTORIALS --> T5["Tutorial 05: Research Workflow<br/>(120 min)"] HOWTO --> H1["Running Simulations<br/>(20 min)"] HOWTO --> H2["Result Analysis<br/>(20 min)"] HOWTO --> H3["Optimization Workflows<br/>(25 min)"] HOWTO --> H4["Testing & Validation<br/>(20 min)"] API --> A1["Controllers API<br/>(30 min)"] API --> A2["Simulation API<br/>(25 min)"] API --> A3["Optimization API<br/>(25 min)"] API --> A4["Configuration API<br/>(20 min)"] API --> A5["Plant Models API<br/>(20 min)"] API --> A6["Utilities API<br/>(20 min)"] THEORY --> TH1["SMC Theory<br/>(30 min)"] THEORY --> TH2["PSO Theory<br/>(25 min)"] THEORY --> TH3["DIP Dynamics<br/>(25 min)"] style ROOT fill:#ccccff style QUICK fill:#ccffcc style TUTORIALS fill:#ffffcc style HOWTO fill:#ffcccc style API fill:#ccccff style THEORY fill:#ccffcc
``` **Total Documentation**: 12,525 lines across 28 documents --- ## Getting Started ### New to the Framework? Start here for installation, configuration, and your first simulation: 1. **[Getting Started Guide](getting-started.md)** ⭐ *Most popular* - Installation and setup (Python, dependencies) - Configuration overview - First simulation walkthrough - Web UI introduction - **Duration**: 15 minutes - **Level**: Beginner 2. **[User Guide](user-guide.md)** 📖 *Comprehensive* - Complete reference for daily usage - All CLI commands explained - Configuration deep dive - Batch processing and analysis - **Duration**: 30 minutes - **Level**: Beginner to Intermediate 3. **[Quick Reference](QUICK_REFERENCE.md)** ⚡ *Cheat sheet* - Command syntax at a glance - Common workflows - Troubleshooting tips - **Duration**: 5 minutes - **Level**: All levels **Recommended Start**: Getting Started Guide → Tutorial 01 → User Guide --- ## Learning Paths ### Choose Your Journey ```mermaid
flowchart LR GOAL{What's your goal?} GOAL -->|Quick prototype| PATH1["Path 1: Quick Start<br/>⏱️ 1-2 hours<br/>🟢 Beginner"] GOAL -->|Compare controllers| PATH2["Path 2: Controller Expert<br/>⏱️ 4-6 hours<br/>🟡 Intermediate"] GOAL -->|Build custom SMC| PATH3["Path 3: Custom Development<br/>⏱️ 8-12 hours<br/>🔴 Advanced"] GOAL -->|Research publication| PATH4["Path 4: Research Workflow<br/>⏱️ 12+ hours<br/>🔴 Advanced"] style PATH1 fill:#ccffcc style PATH2 fill:#ffffcc style PATH3 fill:#ffcccc style PATH4 fill:#ccccff
``` ### Path 1: Quick Start (1-2 hours) 🟢 **Perfect for**: First-time users, rapid prototyping, initial exploration **Journey:**
1. [Getting Started](getting-started.md) → Installation & setup
2. [Tutorial 01](tutorials/tutorial-01-first-simulation.md) → Understand DIP & Classical SMC
3. [How-To: Running Simulations](how-to/running-simulations.md) → Explore CLI and Streamlit **Outcome**: ✅ Run simulations, modify parameters, interpret basic results --- ### Path 2: Controller Expert (4-6 hours) 🟡 **Perfect for**: Control systems researchers, comparative studies, selecting optimal controller **Journey:**
1. [Getting Started](getting-started.md) → Setup
2. [Tutorial 01](tutorials/tutorial-01-first-simulation.md) → Basics
3. [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) → Compare 4 SMC types
4. [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) → Automatic gain tuning
5. [SMC Theory](theory/smc-theory.md) → Understand mathematical foundations
6. [How-To: Optimization Workflows](how-to/optimization-workflows.md) → Advanced PSO tuning **Outcome**: ✅ Select best controller for your application, optimize gains, understand tradeoffs --- ### Path 3: Custom Development (8-12 hours) 🔴 **Perfect for**: Implementing novel SMC algorithms, extending the framework **Journey:**
1. [Getting Started](getting-started.md) → Setup
2. [Tutorials 01-02](tutorials/) → Learn framework basics
3. [Controllers API](api/controllers.md) → Understand factory and base classes
4. [Tutorial 04](tutorials/tutorial-04-custom-controller.md) → Implement custom controller
5. [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) → Optimize custom controller
6. [How-To: Testing & Validation](how-to/testing-validation.md) → testing
7. [SMC Theory](theory/smc-theory.md) → Lyapunov stability proofs **Outcome**: ✅ Custom SMC ready for research, fully tested, integrated with PSO --- ### Path 4: Research Publication (12+ hours) 🔴 **Perfect for**: Graduate students, academic researchers, industrial R&D **Journey:**
1. Complete Paths 1-2 (understand framework & controllers)
2. [Tutorial 05](tutorials/tutorial-05-research-workflow.md) → End-to-end research project
3. [How-To: Result Analysis](how-to/result-analysis.md) → Statistical validation and visualization
4. [PSO Theory](theory/pso-theory.md) → Optimization foundations
5. [DIP Dynamics](theory/dip-dynamics.md) → System modeling
6. [User Guide - Batch Processing](user-guide.md#batch-processing) → Monte Carlo studies
7. All API Reference guides → Technical depth **Outcome**: ✅ Publication-ready research with statistical validation, reproducible results --- ## Documentation by Category ### 📚 Tutorials (Step-by-Step Learning) | Tutorial | Level | Duration | Topics |
|----------|-------|----------|--------|
| **[Tutorial 01: First Simulation](tutorials/tutorial-01-first-simulation.md)** | 🟢 Beginner | 45 min | DIP system, Classical SMC, result interpretation |
| **[Tutorial 02: Controller Comparison](tutorials/tutorial-02-controller-comparison.md)** | 🟡 Intermediate | 60 min | 4 SMC types, performance tradeoffs, selection criteria |
| **[Tutorial 03: PSO Optimization](tutorials/tutorial-03-pso-optimization.md)** | 🟡 Intermediate | 90 min | Automated gain tuning, convergence analysis, custom cost functions |
| **[Tutorial 04: Custom Controller](tutorials/tutorial-04-custom-controller.md)** | 🔴 Advanced | 120 min | Terminal SMC from scratch, factory integration, testing |
| **[Tutorial 05: Research Workflow](tutorials/tutorial-05-research-workflow.md)** | 🔴 Advanced | 120 min | End-to-end research project, statistical analysis, publication workflow | **Total**: 5 tutorials, 635 minutes (10.5 hours) of guided learning --- ### 📖 How-To Guides (Task-Oriented Recipes) | Guide | Topics | Duration |
|-------|--------|----------|
| **[Running Simulations](how-to/running-simulations.md)** | CLI usage, Streamlit dashboard, programmatic API, batch processing | 20 min |
| **[Result Analysis](how-to/result-analysis.md)** | Metrics interpretation, statistical analysis, visualization, data export | 20 min |
| **[Optimization Workflows](how-to/optimization-workflows.md)** | PSO tuning, custom cost functions, convergence diagnostics, parallel execution | 25 min |
| **[Testing & Validation](how-to/testing-validation.md)** | Test suite overview, unit testing, performance benchmarking, coverage analysis | 20 min | **Total**: 4 guides, practical approaches for common tasks --- ### 🔧 API Reference (Technical Documentation) | API Guide | Modules Covered | Lines | Duration |
|-----------|-----------------|-------|----------|
| **[API Index](api/README.md)** | Overview and navigation | 203 | 10 min |
| **[Controllers API](api/controllers.md)** | Factory system, SMC types, gain bounds, custom controllers | 726 | 30 min |
| **[Simulation API](api/simulation.md)** | SimulationRunner, dynamics models, batch processing, performance | 517 | 25 min |
| **[Optimization API](api/optimization.md)** | PSOTuner, cost functions, gain bounds, convergence monitoring | 543 | 25 min |
| **[Configuration API](api/configuration.md)** | YAML loading, validation, programmatic configuration | 438 | 20 min |
| **[Plant Models API](api/plant-models.md)** | Physics models, parameter configuration, custom dynamics | 424 | 20 min |
| **[Utilities API](api/utilities.md)** | Validation, control primitives, monitoring, analysis tools | 434 | 20 min | **Total**: 7 API guides, 3,285 lines of technical documentation **Usage Pattern**: Reference while coding, copy-paste examples, understand internals --- ### 📐 Theory & Explanation (Mathematical Foundations) | Theory Guide | Topics | Lines | Duration |
|--------------|--------|-------|----------|
| **[Theory Index](theory/README.md)** | Overview and navigation | 104 | 5 min |
| **[SMC Theory](theory/smc-theory.md)** | Lyapunov stability, chattering analysis, super-twisting mathematics, practical design | 619 | 30 min |
| **[PSO Theory](theory/pso-theory.md)** | Swarm intelligence principles, convergence theory, parameter selection, benchmarks | 438 | 25 min |
| **[DIP Dynamics](theory/dip-dynamics.md)** | Lagrangian derivation, equations of motion, linearization, controllability analysis | 501 | 25 min | **Total**: 4 theory guides, 1,662 lines explaining the "why" behind the code **Usage Pattern**: Understand fundamentals, verify implementations, design new controllers --- ## Most Popular Pages Based on user engagement and typical workflows: 1. **[Getting Started Guide](getting-started.md)** ⭐⭐⭐⭐⭐ - Entry point for 95% of users - Installation and first simulation - 523 lines, 15 minutes 2. **[Tutorial 01: First Simulation](tutorials/tutorial-01-first-simulation.md)** ⭐⭐⭐⭐⭐ - Hands-on introduction to DIP and Classical SMC - Expected results and troubleshooting - 600 lines, 45 minutes 3. **[Tutorial 03: PSO Optimization](tutorials/tutorial-03-pso-optimization.md)** ⭐⭐⭐⭐ - Automated gain tuning is highly requested - Practical convergence analysis - 865 lines, 90 minutes 4. **[Controllers API](api/controllers.md)** ⭐⭐⭐⭐ - Essential for programmatic usage - Factory patterns and gain bounds - 726 lines, 30 minutes 5. **[User Guide](user-guide.md)** ⭐⭐⭐⭐ - reference - Daily usage workflows - 826 lines, 30 minutes --- ## Recently Updated **October 2025** - Week 16 updates: - **NEW**: [Documentation Navigation Hub](INDEX.md) - This page
- **ENHANCED**: [README.md](../../README.md) - Added Documentation & Learning section, architecture diagrams
- **ENHANCED**: [Tutorial 01](tutorials/tutorial-01-first-simulation.md) - Added expected results sections
- **ENHANCED**: [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) - Added comparison visuals
- **ENHANCED**: [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) - Added PSO workflow diagrams **Previous Major Updates**:
- **Week 15**: Added Theory Guides (SMC, PSO, DIP Dynamics)
- **Week 14**: Expanded API Reference guides
- **Week 13**: Created How-To guides
- **Week 12**: Completed Tutorial series --- ## Quick Search ### By Task | I want to... | Go to |
|--------------|-------|
| **Install the framework** | [Getting Started](getting-started.md) |
| **Run my first simulation** | [Tutorial 01](tutorials/tutorial-01-first-simulation.md) |
| **Compare different controllers** | [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) |
| **Optimize controller gains** | [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) |
| **Create a custom controller** | [Tutorial 04](tutorials/tutorial-04-custom-controller.md) |
| **Understand SMC mathematics** | [SMC Theory](theory/smc-theory.md) |
| **Use the factory system** | [Controllers API](api/controllers.md) |
| **Configure PSO parameters** | [Optimization API](api/optimization.md) |
| **Interpret performance metrics** | [How-To: Result Analysis](how-to/result-analysis.md) |
| **Run batch simulations** | [User Guide - Batch Processing](user-guide.md#batch-processing) | ### By Component | Component | Documentation |
|-----------|---------------|
| **Controllers** | [Controllers API](api/controllers.md), [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) |
| **Plant Models** | [Plant Models API](api/plant-models.md), [DIP Dynamics Theory](theory/dip-dynamics.md) |
| **PSO Optimization** | [Optimization API](api/optimization.md), [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) |
| **Simulation Engine** | [Simulation API](api/simulation.md), [How-To: Running Simulations](how-to/running-simulations.md) |
| **Configuration** | [Configuration API](api/configuration.md), [User Guide](user-guide.md) | ### By Skill Level | Level | Start Here |
|-------|------------|
| **🟢 Beginner** | [Getting Started](getting-started.md) → [Tutorial 01](tutorials/tutorial-01-first-simulation.md) |
| **🟡 Intermediate** | [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) → [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) |
| **🔴 Advanced** | [Tutorial 04](tutorials/tutorial-04-custom-controller.md) → [Theory Guides](theory/README.md) | --- ## Organization Principles This documentation follows the **Diátaxis framework** for technical documentation: 1. **Tutorials** (Learning-oriented): Step-by-step lessons for beginners
2. **How-To Guides** (Task-oriented): Recipes for accomplishing specific goals
3. **API Reference** (Information-oriented): Technical specifications and details
4. **Theory & Explanation** (Understanding-oriented): Conceptual and mathematical foundations **Benefits of this structure:**
- Clear separation of concerns
- Easy to find what you need
- Supports different learning styles
- Scales with project complexity --- ## Navigation Tips ### Finding Documentation Fast 1. **Start with your goal**: Use the [Learning Paths](#learning-paths) decision tree
2. **Search by task**: Use the [Quick Search](#quick-search) tables
3. **Browse by category**: Explore [Documentation by Category](#documentation-by-category)
4. **Follow the flow**: Each document links to related content ### Reading Order **For newcomers:**
```
Getting Started → Tutorial 01 → Tutorial 02 → Tutorial 03
``` **For researchers:**
```
Tutorials 01-03 → Theory Guides → Tutorial 05 → API Reference
``` **For developers:**
```
Tutorials 01-02 → API Reference → Tutorial 04 → How-To: Testing
``` ### Best Practices - ✅ **Start with tutorials** for hands-on learning
- ✅ **Use How-To guides** for specific tasks
- ✅ **Reference API docs** while coding
- ✅ **Read theory guides** for deep understanding
- ✅ **Keep Quick Reference** open during work --- ## Contributing to Documentation Found an issue or want to improve the docs? 1. **Open an issue**: [GitHub Issues](https://github.com/theSadeQ/dip-smc-pso/issues)
2. **Suggest improvements**: Tag issues with `documentation`
3. **Follow the style guide**: Consistent formatting, clear examples, Mermaid diagrams **Documentation Quality Standards:**
- All code examples must be tested and working
- Mermaid diagrams for visual explanations
- Cross-references between related documents
- Estimated reading times for planning
- Clear learning objectives --- ## External Resources **Control Theory Background:**
- [Khalil - Nonlinear Systems](http://www.springer.com/gp/book/9780130673893)
- [Utkin - Sliding Mode Control](https://link.springer.com/book/10.1007/978-3-642-84379-2)
- [Slotine & Li - Applied Nonlinear Control](http://www.pearson.com/us/higher-education/program/Slotine-Applied-Nonlinear-Control/PGM200693.html) **PSO & Optimization:**
- [PySwarms Documentation](https://pyswarms.readthedocs.io/)
- [Kennedy & Eberhart - Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) **Python & Scientific Computing:**
- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/) --- **Last Updated**: October 2025 (Week 16) **Total Documentation Size**: 12,525 lines across 28 documents **Questions?** See [User Guide - Troubleshooting](user-guide.md#troubleshooting) or open an issue. --- **Happy Learning!** 🚀 Return to [Project README](../../README.md) | Browse [Theory Guides](theory/README.md) | Start [Tutorial 01](tutorials/tutorial-01-first-simulation.md)
