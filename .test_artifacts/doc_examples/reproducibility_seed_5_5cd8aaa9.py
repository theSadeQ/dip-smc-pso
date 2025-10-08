# Example from: docs\reference\utils\reproducibility_seed.md
# Index: 5
# Runnable: True
# Hash: 5cd8aaa9

# Error handling
try:
    result = component.process(data)
except ComponentError as e:
    print(f"Error: {e}")