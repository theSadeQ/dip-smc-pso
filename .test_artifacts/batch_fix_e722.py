"""Batch fix E722 bare-except errors"""
import json
import re
from pathlib import Path

# Load error data
with open('.test_artifacts/ruff_initial_scan.json') as f:
    errors = json.load(f)

# Filter E722 errors
e722_errors = [e for e in errors if e['code'] == 'E722']

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for err in e722_errors:
    by_file[err['filename']].append(err)

fixed_count = 0
failed_files = []

for filepath, file_errors in sorted(by_file.items()):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Get line numbers (1-indexed)
        error_lines = {err['location']['row'] for err in file_errors}

        # Replace except: with except Exception:
        modified = False
        for line_num in error_lines:
            idx = line_num - 1  # Convert to 0-indexed
            if idx < len(lines):
                original = lines[idx]
                # Replace 'except:' with 'except Exception:'
                new_line = re.sub(r'(\s+)except:', r'\1except Exception:', original)
                if new_line != original:
                    lines[idx] = new_line
                    modified = True
                    fixed_count += 1

        # Write back if modified
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Fixed {len(error_lines)} errors in {Path(filepath).relative_to(Path.cwd())}")

    except Exception as e:
        failed_files.append((filepath, str(e)))
        print(f"ERROR fixing {Path(filepath).relative_to(Path.cwd())}: {e}")

print(f"\n✓ Fixed {fixed_count} bare-except errors across {len(by_file)} files")
if failed_files:
    print(f"\n✗ Failed to fix {len(failed_files)} files")
