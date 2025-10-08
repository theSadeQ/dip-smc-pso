# Example from: docs\test_infrastructure_validation_report.md
# Index: 1
# Runnable: True
# Hash: eb078001

# Automatic headless enforcement via tests/conftest.py
os.environ.setdefault("MPLBACKEND", "Agg")
matplotlib.use("Agg", force=True)

# Runtime ban on plt.show() for CI safety
def _no_show(*args, **kwargs):
    raise AssertionError("plt.show() is banned in tests. Use savefig() or return Figure.")
plt.show = _no_show