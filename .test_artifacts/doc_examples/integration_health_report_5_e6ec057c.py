# Example from: docs\reports\integration_health_report.md
# Index: 5
# Runnable: False
# Hash: e6ec057c

# example-metadata:
# runnable: false

# Required Fix: ModularHybridSMC control computation
# Location: src/controllers/smc/algorithms/hybrid/controller.py

# Issue: Accessing .get() method on numpy array instead of dict
# Fix: Ensure state parameter is properly handled as dict/object