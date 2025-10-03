# utils.reproducibility.__init__

**Source:** `src\utils\reproducibility\__init__.py`

## Module Overview

Reproducibility utilities for control engineering experiments.

This package provides tools for managing random seeds and ensuring
reproducible results across experiments and simulations.

## Complete Source Code

```{literalinclude} ../../../src/utils/reproducibility/__init__.py
:language: python
:linenos:
```

---

## Functions

### `with_seed(seed)`

Dummy function for backward compatibility.

#### Source Code

```{literalinclude} ../../../src/utils/reproducibility/__init__.py
:language: python
:pyobject: with_seed
:linenos:
```

---

### `random_seed_context(seed)`

Dummy context manager for backward compatibility.

#### Source Code

```{literalinclude} ../../../src/utils/reproducibility/__init__.py
:language: python
:pyobject: random_seed_context
:linenos:
```

---

## Dependencies

This module imports:

- `from .seed import set_global_seed, SeedManager, create_rng`
