# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 3
# Runnable: True
# Hash: 172bb85d

# Use safe ASCII preview to avoid UnicodeEncodeError on Windows
preview = content[:500].encode('ascii', errors='replace').decode('ascii')
print(preview)