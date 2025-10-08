# Example from: docs\reference\simulation\safety_guards.md
# Index: 3
# Runnable: True
# Hash: c42c2702

try:
    result = instance.process(data)
except Exception as e:
    print(f"Error: {e}")