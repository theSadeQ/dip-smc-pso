# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 10
# Runnable: True
# Hash: 68a44b7c

# Validates source files exist
if not source_file.exists():
    continue

# Validates relative paths
try:
    relative = os.path.relpath(source_file, doc_file.parent)
except ValueError:
    return str(source_file)