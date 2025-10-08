# Example from: docs\reports\test_infrastructure_analysis_report.md
# Index: 7
# Runnable: False
# Hash: 6618b0cd

# Force Agg backend before any figures created
os.environ.setdefault("MPLBACKEND", "Agg")
matplotlib.use("Agg", force=True)

# Runtime ban on plt.show()
def _no_show(*args, **kwargs):
    raise AssertionError("plt.show() is banned in tests...")
plt.show = _no_show