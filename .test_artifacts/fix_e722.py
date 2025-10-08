"""Fix E722 bare-except errors by replacing except: with except Exception:"""
import json
from pathlib import Path

# Load error data
with open('.test_artifacts/ruff_initial_scan.json') as f:
    errors = json.load(f)

# Filter E722 errors
e722_errors = [e for e in errors if e['code'] == 'E722']

print(f"Found {len(e722_errors)} E722 (bare-except) errors")
print()

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for err in e722_errors:
    by_file[err['filename']].append(err)

# Display grouped errors
for filepath, file_errors in sorted(by_file.items()):
    print(f"\n{Path(filepath).relative_to('D:\\\\Projects\\\\main')}:")
    for err in sorted(file_errors, key=lambda x: x['location']['row']):
        print(f"  Line {err['location']['row']}: {err['message']}")
