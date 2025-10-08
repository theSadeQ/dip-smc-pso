# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 9
# Runnable: True
# Hash: 8a6f9633

# tests/conftest.py (top of file, before any imports)
"""
Matplotlib enforcement: headless tests with Agg backend and show-ban.
This file MUST be imported before any test that imports matplotlib.pyplot.
"""
import os
import warnings

# 1) Enforce Agg backend as early as possible
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib
matplotlib.use("Agg", force=True)

# 2) Treat Matplotlib warnings as errors
warnings.filterwarnings("error", message=r".*Matplotlib.*", category=UserWarning)

def pytest_sessionstart(session):
    """Verify Agg backend at session start."""
    backend = matplotlib.get_backend().lower()
    assert backend == "agg", (
        f"Matplotlib backend is {backend!r}, expected 'agg'. "
        "Ensure MPLBACKEND=Agg is set before matplotlib import."
    )

# 3) Runtime ban on plt.show()
import matplotlib.pyplot as plt

def _no_show(*args, **kwargs):
    raise AssertionError(
        "plt.show() is banned in tests. Use savefig(), return the Figure, "
        "or use image comparisons."
    )

plt.show = _no_show  # type: ignore[assignment]