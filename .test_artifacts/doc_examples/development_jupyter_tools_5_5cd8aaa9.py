# Example from: docs\reference\utils\development_jupyter_tools.md
# Index: 5
# Runnable: True
# Hash: 5cd8aaa9

# Error handling
try:
    result = component.process(data)
except ComponentError as e:
    print(f"Error: {e}")