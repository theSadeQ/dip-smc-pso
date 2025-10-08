# Contributing to DIP-SMC-PSO

Thank you for your interest in contributing to the Double Inverted Pendulum Sliding Mode Control with PSO Optimization project! This document provides guidelines and best practices for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Quality Standards](#quality-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Documentation](#documentation)
- [Testing](#testing)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup

1. **Fork and clone the repository:**
   ```bash
   git fork https://github.com/theSadeQ/dip-smc-pso.git
   cd dip-smc-pso
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up git hooks:**
   ```bash
   git config commit.template .gitmessage
   chmod +x .git/hooks/pre-commit  # On Unix-like systems
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest tests/ -v
   ```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feat/your-feature-name
```

**Branch naming conventions:**
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `test/` - Test additions or fixes

### 2. Make Your Changes

- Follow the [coding standards](#coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Keep commits atomic and focused

### 3. Run Quality Checks

Before committing, run local validation:

```bash
# Auto-fix common issues
python scripts/validation/fix_common_issues.py

# Run comprehensive quality checks
python scripts/validation/run_quality_checks.py
```

### 4. Commit Your Changes

Follow [commit guidelines](#commit-guidelines):

```bash
git add <files>
git commit
# Follow the commit template (.gitmessage)
```

### 5. Push and Create Pull Request

```bash
git push origin feat/your-feature-name
```

Then create a pull request on GitHub.

---

## Quality Standards

### Coding Standards

- **Style:** PEP 8 compliant (enforced by ruff)
- **Type Hints:** ≥95% coverage required (blocking gate)
- **Docstrings:** ≥95% coverage required (blocking gate)
- **Line Length:** 100 characters maximum
- **Imports:** Organized with isort (standard → third-party → local)

### Documentation Requirements

- All public functions/classes must have docstrings
- Docstrings must follow NumPy/Google style
- Include:
  - Brief description
  - Parameters (with types)
  - Returns (with type)
  - Raises (if applicable)
  - Examples (recommended)

**Example:**
```python
def compute_control(self, state: np.ndarray, gains: List[float]) -> float:
    """
    Compute control force for current system state.

    Parameters
    ----------
    state : np.ndarray
        System state vector [x, dx, θ1, dθ1, θ2, dθ2]
    gains : List[float]
        Controller gain parameters

    Returns
    -------
    float
        Control force in Newtons, clipped to [-max_force, max_force]

    Raises
    ------
    ValueError
        If state dimension is invalid or gains are out of bounds

    Examples
    --------
    >>> controller = ClassicalSMC(gains=[10, 5, 8, 3, 15, 2])
    >>> force = controller.compute_control(state, gains)
    >>> assert -150 <= force <= 150
    """
    ...
```

### Testing Requirements

- Unit tests for all new functions/classes
- Integration tests for feature additions
- Maintain ≥85% overall test coverage
- Property-based tests for critical algorithms (Hypothesis)
- Benchmark tests for performance-critical code

---

## Commit Guidelines

### Conventional Commits Format

We use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

**Format:**
```
type(scope): subject

body (optional)

footer (optional)
```

**Valid Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, no functional change)
- `refactor` - Code refactoring
- `perf` - Performance improvement
- `test` - Adding or updating tests
- `chore` - Maintenance (dependencies, config)
- `ci` - CI/CD changes
- `build` - Build system changes
- `revert` - Revert previous commit

**Common Scopes:**
- `controllers` - SMC controllers
- `pso` - PSO optimization
- `simulation` - Simulation engine
- `plant` - Plant dynamics
- `docs` - Documentation
- `tests` - Test files
- `ci` - CI/CD workflows

**Examples:**
```
feat(controllers): add terminal sliding mode controller

Implements Terminal SMC with finite-time convergence guarantees.
Includes PSO optimization integration and comprehensive tests.

Closes #42
```

```
fix(pso): resolve convergence issue in high-dimensional spaces

PSO was failing to converge for 8+ dimensional parameter spaces.
Adjusted inertia weight decay schedule to improve exploration.

Related to #78
```

```
docs(api): update optimization module API reference

Added missing docstrings for PSOTuner methods.
Updated parameter descriptions with units and ranges.
```

### Breaking Changes

For breaking changes, add `BREAKING CHANGE:` in the footer:

```
feat(controllers): redesign controller factory API

BREAKING CHANGE: create_controller() now requires explicit
controller_type parameter. Previous positional argument syntax
is no longer supported.

Migration guide: docs/migration/v2.0.0.md
```

### AI-Assisted Commits

For AI-assisted or collaborative commits, add attribution:

```
feat(visualization): add interactive performance dashboard

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Pull Request Process

### Before Creating PR

1. **Ensure quality gates pass:**
   ```bash
   python scripts/validation/run_quality_checks.py
   ```

2. **Update documentation:**
   - Add docstrings to new code
   - Update relevant markdown files
   - Add examples if applicable

3. **Write tests:**
   - Unit tests for new functions
   - Integration tests for features
   - Verify coverage: `pytest --cov=src --cov-report=term-missing`

4. **Run full test suite:**
   ```bash
   pytest tests/ -v
   ```

### PR Template

When creating a pull request, include:

**Title:** Use conventional commit format
```
feat(controllers): add terminal sliding mode controller
```

**Description:**
```markdown
## Summary
Brief description of changes

## Motivation
Why are these changes needed?

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How were these changes tested?

## Screenshots (if applicable)
Include relevant visualizations

## Checklist
- [ ] Tests pass locally
- [ ] Quality checks pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)

Closes #issue_number
```

### Review Process

1. **Automated checks:**
   - CI must pass (docs-quality.yml, commit-lint.yml)
   - All blocking quality gates must pass

2. **Code review:**
   - At least one approval required
   - Address all review comments

3. **Merge:**
   - Squash and merge (maintainers only)
   - Delete branch after merge

---

## Release Process

### Version Bumping

Use the automated version bumping script:

```bash
# Bump patch version (1.2.3 -> 1.2.4)
python scripts/release/bump_version.py --bump patch

# Bump minor version (1.2.3 -> 1.3.0)
python scripts/release/bump_version.py --bump minor

# Bump major version (1.2.3 -> 2.0.0)
python scripts/release/bump_version.py --bump major

# Dry run (preview changes)
python scripts/release/bump_version.py --bump minor --dry-run
```

### Release Workflow

1. **Prepare release:**
   ```bash
   # Bump version
   python scripts/release/bump_version.py --bump minor

   # Review changes
   git diff

   # Commit version bump
   git add .
   git commit -m "chore: bump version to v1.3.0"
   ```

2. **Create and push tag:**
   ```bash
   git push origin main
   git push origin v1.3.0
   ```

3. **Automated steps (via GitHub Actions):**
   - Version validation
   - Changelog generation (git-cliff)
   - GitHub Release creation
   - Documentation version update
   - ReadTheDocs build trigger

4. **Post-release:**
   - Verify GitHub Release
   - Check ReadTheDocs build
   - Announce on relevant channels

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

---

## Documentation

### Types of Documentation

1. **API Reference:**
   - Auto-generated from docstrings
   - Location: `docs/api/`

2. **User Guides:**
   - Step-by-step tutorials
   - Location: `docs/guides/`

3. **Theory:**
   - Mathematical foundations
   - Location: `docs/theory/`

4. **Development:**
   - Quality gates, workflows
   - Location: `docs/development/`

### Building Documentation Locally

```bash
cd docs
make html
# Open _build/html/index.html in browser
```

### Documentation Quality Gates

- **Link Validation:** 0 broken links (blocking)
- **Markdown Linting:** Style consistency (advisory)
- **Spell Checking:** Typos (advisory)

---

## Testing

### Test Structure

```
tests/
├── test_controllers/       # Controller unit tests
├── test_integration/       # Integration tests
├── test_benchmarks/        # Performance benchmarks
└── test_documentation/     # Doc tests, link validation
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_controllers/test_classical_smc.py -v

# With coverage
pytest --cov=src --cov-report=html

# Benchmarks only
pytest tests/test_benchmarks/ --benchmark-only

# Fast tests (skip slow)
pytest -m "not slow"
```

### Writing Tests

**Example:**
```python
import pytest
import numpy as np
from src.controllers.smc import ClassicalSMC

def test_classical_smc_initialization():
    """Test ClassicalSMC initializes with valid parameters."""
    gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
    controller = ClassicalSMC(gains=gains, max_force=150.0, boundary_layer=0.3)

    assert controller.max_force == 150.0
    assert controller.boundary_layer == 0.3
    np.testing.assert_array_equal(controller.gains, gains)

def test_classical_smc_control_force_bounds():
    """Test control force is clipped to max_force."""
    controller = ClassicalSMC(
        gains=[100, 100, 100, 100, 100, 100],  # Very high gains
        max_force=150.0,
        boundary_layer=0.3
    )

    state = np.array([1.0, 0.0, 0.5, 0.0, 0.3, 0.0])  # Large error
    force = controller.compute_control(state)

    assert -150.0 <= force <= 150.0, "Force exceeds bounds"
```

---

## Questions?

- **Issues:** https://github.com/theSadeQ/dip-smc-pso/issues
- **Discussions:** https://github.com/theSadeQ/dip-smc-pso/discussions
- **Documentation:** https://dip-smc-pso.readthedocs.io/

---

**Thank you for contributing!** 🚀

---

**Last Updated:** Phase 6.6 (2025-10-08)
