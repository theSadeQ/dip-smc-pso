# E010: Documentation System and Navigation

**Part:** Part 2 Infrastructure & Tooling
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Documentation System

---

## Opening Hook

**Sarah:** How do you document 105,000 lines of code? Where do you even start?

**Alex:** You start by assuming that future you will forget everything current you knows. Documentation is not for users. It is for the person reading your code six months from now who has no memory of why you made these decisions.

**Sarah:** And if that person is you?

**Alex:** Then you are grateful that past you was thorough. Today we talk about the documentation system -- how we organized 706 documentation files, built automated API reference, and created navigation that works for five different audience types.

---

## The Documentation Problem

**Sarah:** 105,000 lines of production code across 358 files. How many documentation files does that require?

**Alex:** 706 files in the Sphinx documentation system alone. That does not count README files, docstrings, code comments, or the AI workspace guides. Just the structured documentation.

**Sarah:** How do you prevent that from becoming a mess?

**Alex:** Three principles. First: colocate documentation with code. Every controller in `src/controllers/` has a corresponding page in `sphinx_docs/controllers/`. Second: automate what you can. API reference is generated from docstrings -- we never write it manually. Third: multiple navigation strategies for different mental models.

---

## Sphinx Documentation System

**Sarah:** Walk me through the Sphinx setup. What is Sphinx and why use it?

**Alex:** Sphinx is a documentation generator. You write pages in markdown or reStructuredText, and Sphinx builds them into searchable HTML with cross-references, automatic indexing, and API reference generation. It is the standard in the Python ecosystem -- NumPy, SciPy, Django, Flask all use it.

**Sarah:** Where does it live in the project?

**Alex:** `academic/paper/sphinx_docs/` directory. The configuration is in `conf.py` -- 19 kilobytes of settings for themes, extensions, autodoc behavior, and build options. The source files are organized into subdirectories: `api/`, `controllers/`, `benchmarks/`, `architecture/`, `development/`, `deployment/`, `examples/`.

**Sarah:** How does the build process work?

**Alex:** You run `sphinx-build -M html sphinx_docs sphinx_docs/_build`. Sphinx reads `conf.py` for configuration, parses all markdown and reStructuredText files, generates API reference from Python docstrings using autodoc, builds cross-reference links, and outputs HTML to `sphinx_docs/_build/html/`.

**Sarah:** What if the build fails?

**Alex:** You use the `-W` flag: `sphinx-build -M html sphinx_docs sphinx_docs/_build -W --keep-going`. This treats warnings as errors and continues building to show all problems at once. Common failures: broken cross-references, missing docstrings for public functions, invalid reStructuredText syntax.

---

## Directory Structure: Organizing 706 Files

**Sarah:** How are those 706 files organized?

**Alex:** Eight main categories. `api/` has auto-generated API reference -- every public class, function, and module documented from docstrings. `controllers/` has theory and implementation details for each of the seven controllers. `benchmarks/` has performance results and analysis. `architecture/` explains design decisions and patterns. `development/` has contributor guides and coding standards. `deployment/` covers installation and production setup. `examples/` has runnable tutorials. `for_reviewers/` has materials for academic paper reviewers.

**Sarah:** Give me the file count breakdown.

**Alex:** I do not have exact per-category counts, but the largest sections are `api/` with auto-generated reference for 358 source files, and `benchmarks/` with results from 11 research tasks. The `controllers/` section has at least 7 subdirectories -- one per controller type.

---

## API Reference: Automated Documentation

**Sarah:** Explain how API reference generation works.

**Alex:** Sphinx autodoc extension. You write docstrings in your Python code following a standard format -- usually NumPy style or Google style. In the Sphinx source, you use the `automodule`, `autoclass`, or `autofunction` directive. Sphinx imports the module, extracts the docstring, parses the parameter descriptions and return types, and generates formatted HTML.

**Sarah:** Show me an example.

**Alex:** In Python code:

```python
def compute_control(state, last_control, history):
    """Compute control signal from current state.

    Parameters
    ----------
    state : ndarray, shape (6,)
        System state [x, x_dot, theta1, theta1_dot, theta2, theta2_dot]
    last_control : float
        Previous control signal in Newtons
    history : SimulationHistory
        Complete simulation history for adaptive controllers

    Returns
    -------
    float
        Control force in Newtons, bounded by max_force

    Notes
    -----
    This method is called at every simulation timestep (100 Hz).
    Subclasses must implement their specific control laws here.
    """
```

In Sphinx markdown:

```markdown
## compute_control

.. automethod:: BaseController.compute_control
```

Sphinx generates a formatted reference page with parameter table, return value description, and notes section.

**Sarah:** What happens if you forget to document a public function?

**Alex:** Build warning if you enable strict checking: "WARNING: no docstring found for BaseController.cleanup". We have a validation script that checks for missing docstrings in critical modules before every commit.

---

## Learning Paths: Five Audience Types

**Sarah:** You mentioned five learning paths. Who are they for?

**Alex:** Path 0: Complete beginners with zero programming or control theory background. 125 to 150 hours of prerequisite material on Python, physics, calculus, linear algebra, and control fundamentals. This lives in `.ai_workspace/education/beginner-roadmap.md`.

**Sarah:** That is a long path.

**Alex:** It is. But if you are a mechanical engineering student who has never coded, you need that foundation before you can understand sliding mode control. Path 0 gets you to the starting line.

**Sarah:** What about Path 1?

**Alex:** Path 1 is quick start for users with prerequisites. Get a simulation running in 1 to 2 hours. `docs/guides/getting-started.md` -- install Python, clone the repo, create virtual environment, run `python simulate.py`, see the pendulum stabilize. Then Tutorial 01 walks through configuration and visualization.

**Sarah:** And Paths 2 through 4?

**Alex:** Path 2 is advanced usage -- custom controllers, PSO tuning, batch simulations. Path 3 is research workflows -- running benchmarks, analyzing results, writing papers. Path 4 is production deployment -- thread safety, memory management, HIL integration. Each path builds on the previous.

**Sarah:** How do users know which path to follow?

**Alex:** README.md has a decision tree. "Have you programmed in Python before? No -> Path 0. Yes -> Do you know control theory? No -> Path 0 theory section. Yes -> Do you want to run a quick demo? Yes -> Path 1. Do you want to write custom controllers? Yes -> Path 2." And so on.

---

## Cross-References and Linkage

**Sarah:** With 706 files, how do you prevent broken links?

**Alex:** Sphinx cross-reference syntax. You write `:ref:\`section-label\`` to link to a section, `:doc:\`path/to/file\`` to link to a document, `:class:\`ClassName\`` to link to API reference. Sphinx validates all references during build and emits warnings for broken links.

**Sarah:** What if you reorganize the docs?

**Alex:** Update the references. Sphinx catches broken links, you fix them, rebuild passes. This is why automated validation is critical -- you cannot manually verify 706 files for link integrity.

**Sarah:** Do you have a policy for internal vs external links?

**Alex:** Internal links use Sphinx references. External links use plain markdown: `[NumPy Documentation](https://numpy.org/doc/)`. We have a separate link checker script that validates external URLs once per week to catch dead links.

---

## Docstring Standards: NumPy Style

**Sarah:** You mentioned NumPy style docstrings. What does that mean?

**Alex:** A format specification for documenting Python functions. NumPy style uses underlined section headers: Parameters, Returns, Raises, Notes, Examples. Each parameter gets a name, type, and description. Return values get type and description. Examples show runnable code.

**Sarah:** Show me a complete example.

**Alex:** Sure:

```python
def run_simulation(controller, dynamics, initial_state, dt=0.01, duration=10.0):
    """Run closed-loop simulation of DIP system.

    Parameters
    ----------
    controller : BaseController
        Controller instance implementing compute_control method
    dynamics : DynamicsInterface
        Dynamics model implementing compute_derivatives method
    initial_state : ndarray, shape (6,)
        Initial state [x=0, x_dot=0, theta1, theta1_dot, theta2, theta2_dot]
    dt : float, optional
        Simulation timestep in seconds (default: 0.01 for 100 Hz)
    duration : float, optional
        Total simulation time in seconds (default: 10.0)

    Returns
    -------
    SimulationResult
        Object containing time arrays, state trajectories, control history,
        and performance metrics

    Raises
    ------
    ValueError
        If dt <= 0 or duration <= 0
    PhysicsViolationError
        If initial_state contains NaN or Inf values

    Notes
    -----
    The simulation uses RK4 integration by default. Termination occurs
    if the pendulum falls (abs(theta1) > pi/4 or abs(theta2) > pi/4).

    Examples
    --------
    >>> controller = create_controller('classical_smc', config)
    >>> dynamics = SimplifiedDIPDynamics(config.physics_params)
    >>> initial = np.array([0, 0, 0.1, 0, 0.05, 0])
    >>> result = run_simulation(controller, dynamics, initial)
    >>> print(f"Settled in {result.settling_time:.2f} seconds")
    Settled in 2.34 seconds
    """
```

**Sarah:** That is thorough.

**Alex:** That is the standard. Every public function in `src/` has this level of documentation. Private functions -- those with names starting with underscore -- can have shorter docstrings, but still must document parameters and return values.

---

## Documentation Build Workflow

**Sarah:** When do you rebuild the documentation?

**Alex:** Three scenarios. First: during development when you add new features. You write the code, write the docstring, run `sphinx-build`, verify the API reference looks correct. Second: before committing. Pre-commit hook runs `sphinx-build -W` and fails the commit if there are documentation errors. Third: in CI/CD. GitHub Actions builds the docs and deploys them to GitHub Pages on every merge to main.

**Sarah:** What if the build is slow?

**Alex:** Incremental builds. Sphinx caches parsed content and only rebuilds changed files. First build might take 30 seconds for 706 files. Subsequent builds with one file changed take 2 to 3 seconds.

**Sarah:** Does the documentation get deployed automatically?

**Alex:** Yes. CI workflow builds HTML, creates a tarball, and pushes to the `gh-pages` branch. GitHub Pages serves it at `https://thesadeq.github.io/dip-smc-pso/`. Users always see the latest docs matching the main branch.

---

## Code Examples and Runnable Tutorials

**Sarah:** You mentioned examples. How are those organized?

**Alex:** `examples/` subdirectory with numbered tutorials. `tutorial_01_quick_start.py` -- run a simulation with default settings. `tutorial_02_custom_gains.py` -- modify controller gains and compare. `tutorial_03_pso_tuning.py` -- optimize gains with PSO. `tutorial_04_batch_simulation.py` -- run Monte Carlo validation. `tutorial_05_hil_setup.py` -- configure hardware-in-the-loop.

**Sarah:** Are these runnable scripts or markdown?

**Alex:** Runnable Python scripts with extensive comments. You can copy-paste the code and run it. Each tutorial also has a corresponding markdown file in `sphinx_docs/examples/` that explains the concepts, shows the code, and displays expected output.

**Sarah:** How do you ensure the examples stay up to date?

**Alex:** CI runs all tutorial scripts as integration tests. If a tutorial fails, the build fails. This prevents broken examples from being merged. We also have a validation script that checks if code blocks in markdown match the actual tutorial script files.

---

## Search and Indexing

**Sarah:** With 706 files, how do users find what they need?

**Alex:** Sphinx search. The built HTML includes a JavaScript search index with every heading, function name, class name, and significant term. You type "sliding surface" in the search box, you get links to theory pages, API reference for the sliding surface module, and tutorial examples.

**Sarah:** How granular is the indexing?

**Alex:** Section-level. Every heading is indexed. So if you search for "boundary layer chattering", you get direct links to the section in the Classical SMC theory page where boundary layers are explained, the API reference for the boundary layer parameter, and the benchmark results showing chattering reduction.

**Sarah:** Does it index code snippets?

**Alex:** No. Only headings, API signatures, and manually marked index entries. If you want a code example to appear in search, you add an explicit index entry: `.. index:: PSO; cost function`.

---

## Maintenance and Freshness

**Sarah:** How do you keep 706 files from going stale?

**Alex:** Three mechanisms. First: automated API reference never goes stale because it is generated from code. Change a function signature, the docs update automatically. Second: link validation. Weekly cron job checks all internal and external links, files an issue if any are broken. Third: deprecation warnings. If we mark a function as deprecated, the docstring says so, and Sphinx generates a warning box in the rendered page.

**Sarah:** What about conceptual docs that explain design decisions?

**Alex:** Those require manual review. We have a policy: any pull request that changes architecture must update the corresponding `architecture/` documentation page. The PR template has a checklist: "Updated architecture docs? Yes/No". Reviewer verifies before approving.

**Sarah:** How do you handle documentation debt?

**Alex:** Quarterly audits. We use a script that lists files in `src/` without corresponding documentation in `sphinx_docs/`. That list goes on a backlog. If a module is undocumented but is not used by anyone, we either document it or mark it as deprecated. Undocumented and used modules get priority.

---

## Beginner Roadmap: Path 0

**Sarah:** Tell me more about Path 0. You said 125 to 150 hours of material.

**Alex:** Five phases. Phase 1: Computing basics -- command line, text editors, Git, Python fundamentals. 20 to 30 hours. Phase 2: Math foundations -- calculus, linear algebra, differential equations. 30 to 40 hours. Phase 3: Physics -- Newtonian mechanics, Lagrangian dynamics, pendulum systems. 20 to 25 hours. Phase 4: Control theory -- feedback, PID control, state-space methods. 30 to 35 hours. Phase 5: Sliding mode control -- fundamentals, Lyapunov stability, chattering mitigation. 25 to 30 hours.

**Sarah:** That is a full semester course.

**Alex:** It is. And that is deliberate. We do not want someone to reach Tutorial 01, hit a line of code that says `np.linalg.eig(A)`, and have no idea what eigenvalues are. Path 0 ensures you have the prerequisites.

**Sarah:** Where does Path 0 live?

**Alex:** `.ai_workspace/education/beginner-roadmap.md`. It is separate from the Sphinx docs because it is not project-specific -- it is general education. We link to external resources: Python courses on Codecademy, linear algebra on Khan Academy, control theory on MIT OpenCourseWare.

**Sarah:** How do you test if someone has completed Path 0?

**Alex:** We do not. It is self-paced. But Tutorial 01 assumes you know Python syntax, can read NumPy array operations, and understand what a differential equation is. If you do not, you go back to Path 0.

---

## Version-Specific Documentation

**Sarah:** Do you maintain docs for multiple versions?

**Alex:** Not yet. We are at version 0.x -- pre-1.0 release. Documentation tracks the main branch only. Once we hit 1.0, we will use Sphinx versioning extension to maintain docs for major releases. Users could switch between "latest", "stable", "v1.0", "v2.0" in the web UI.

**Sarah:** What about deprecated features?

**Alex:** Docstring includes a deprecation notice:

```python
def old_function(x):
    """Legacy function for backward compatibility.

    .. deprecated:: 0.8.0
       Use :func:`new_function` instead. This function will be
       removed in version 1.0.
    """
```

Sphinx renders this with a prominent warning box in the HTML.

---

## User-Contributed Documentation

**Sarah:** Can external contributors add documentation?

**Alex:** Yes. Pull requests welcome for typos, clarifications, new examples. The contribution guide is in `sphinx_docs/development/contributing.md`. Guidelines: follow NumPy docstring style, run `sphinx-build -W` locally to verify no errors, add yourself to the contributors list.

**Sarah:** How do you review documentation PRs?

**Alex:** Same process as code PRs. Check for technical accuracy, verify examples run correctly, ensure links work, confirm the new content fits the existing structure. If the PR adds a new concept, we check that it links to related pages and is reachable from the main navigation.

---

## Key Takeaways

**Sarah:** Let us recap the documentation system.

**Alex:** 706 files in Sphinx documentation system. Organized into eight main categories: API reference, controllers, benchmarks, architecture, development, deployment, examples, reviewer materials.

**Sarah:** API reference is auto-generated from NumPy-style docstrings using Sphinx autodoc. Change the code, the docs update automatically.

**Alex:** Five learning paths for different audiences: Path 0 for complete beginners (125-150 hours), Path 1 for quick start (1-2 hours), Paths 2-4 for advanced usage, research, and production.

**Sarah:** Sphinx validates cross-references during build. Broken links cause build warnings. CI runs docs build on every commit to prevent merging broken documentation.

**Alex:** Runnable tutorials in `examples/` directory. CI executes them as integration tests to ensure examples stay up to date with code changes.

**Sarah:** Three freshness mechanisms: automated API generation, weekly link validation, PR checklist requiring architecture docs updates.

**Alex:** Path 0 beginner roadmap lives in `.ai_workspace/education/` with 125-150 hours of prerequisite material on Python, math, physics, and control theory.

**Sarah:** Quarterly audits identify undocumented modules. Prioritize based on usage. Document or deprecate.

---

## Pronunciation Guide

For listeners unfamiliar with technical terms used in this episode:

- **Sphinx**: A documentation generator. Pronounced "SFINKS" (like the mythical creature).
- **reStructuredText**: A markup language. Often abbreviated as "reST." Pronounced "rest" or "R-S-T."
- **autodoc**: Sphinx extension for automatic API documentation. Pronounced "auto-dock."
- **NumPy**: Numerical Python library. Pronounced "NUM-pie."
- **Docstring**: Documentation string inside Python code. Pronounced "dock-string."
- **Markdown**: A lightweight markup language. Pronounced "MARK-down."
- **YAML**: A configuration file format. Pronounced "YAM-ul" (rhymes with "camel").

---

## What's Next

**Sarah:** Next episode, Episode 11, we cover configuration and deployment. How `config.yaml` validates parameters, how Pydantic ensures type safety, and what it takes to deploy this system in different environments.

**Alex:** Configuration as code. Validation as a design principle.

**Sarah:** Episode 11. Coming soon.

---

## Pause and Reflect

Documentation is not a chore. It is a design tool. When you write a docstring explaining what a function does, you often realize the function is too complex. When you write a tutorial showing how to use your system, you discover that your API is confusing. Good documentation makes you write better code. If you cannot explain it clearly, you probably should not build it. The 706 files in this project are not just for users. They are a mirror showing us where the design is clean and where it is still messy. And that mirror is invaluable.

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Sphinx Documentation:** `academic/paper/sphinx_docs/`
- **Documentation Build System:** `.ai_workspace/guides/documentation_build_system.md`
- **Beginner Roadmap (Path 0):** `.ai_workspace/education/beginner-roadmap.md`
- **Getting Started (Path 1):** `sphinx_docs/guides/getting-started.md`

---

*Educational podcast episode -- documenting 105,000 lines of research software*
