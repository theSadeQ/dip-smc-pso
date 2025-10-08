"""Error distribution analysis for RUFF results"""
import json
from collections import Counter
from pathlib import Path

# Load error data
with open('.test_artifacts/ruff_initial_scan.json') as f:
    errors = json.load(f)

# Analyze distribution
error_codes = Counter([e['code'] for e in errors])
files = Counter([Path(e['filename']).name for e in errors])

# Identify auto-fixable errors
auto_fixable = [e for e in errors if e.get('fix') is not None]

print('Error Distribution Analysis')
print('=' * 50)
print(f'Total errors: {len(errors)}')
print(f'Auto-fixable: {len(auto_fixable)} ({len(auto_fixable)/len(errors)*100:.1f}%)')
print(f'Manual fixes needed: {len(errors) - len(auto_fixable)}')
print()
print('By error code:')
for code, count in error_codes.most_common():
    print(f'  {code}: {count}')
print()
print('Top 10 files with errors:')
for file, count in files.most_common(10):
    print(f'  {file}: {count}')
