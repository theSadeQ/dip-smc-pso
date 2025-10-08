# Example from: docs\test_infrastructure_documentation.md
# Index: 14
# Runnable: True
# Hash: 7a17c223

# Automatic configuration in tests/conftest.py
os.environ.setdefault("MPLBACKEND", "Agg")
matplotlib.use("Agg", force=True)

# Runtime ban on plt.show()
def _no_show(*args, **kwargs):
    raise AssertionError("plt.show() is banned in tests. Use savefig() or return Figure.")
plt.show = _no_show