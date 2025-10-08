# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 11
# Runnable: True
# Hash: 94fe7b16

# Validates paths resolve correctly
if not source_file.exists():
    invalid_paths.append((doc_file, directive, source_file))