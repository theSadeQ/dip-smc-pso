#!/usr/bin/env python3
"""Quick script to extract audit statistics."""

import json
from pathlib import Path

audit_file = Path('.artifacts/docs_audit/ai_pattern_detection_report.json')
data = json.load(open(audit_file, 'r', encoding='utf-8'))

print('Total issues:', data.get('total_issues', 0))
print('Files with issues:', data.get('files_with_issues', 0))
print('Total files scanned:', data.get('total_files_scanned', 0))
print('Severity breakdown:', data.get('severity_breakdown', {}))
print('Pattern frequency (top 10):')
for pattern, count in list(data.get('pattern_frequency', {}).items())[:10]:
    print(f'  {pattern}: {count}')

# Create file lists by severity from 'files' key (which is a list)
files_data = data.get('files', [])
critical_files = []
high_files = []
medium_files = []
low_files = []

for file_info in files_data:
    severity = file_info.get('severity', 'UNKNOWN')
    file_path = file_info.get('file', '')
    if severity == 'CRITICAL':
        critical_files.append(file_path)
    elif severity == 'HIGH':
        high_files.append(file_path)
    elif severity == 'MEDIUM':
        medium_files.append(file_path)
    elif severity == 'LOW':
        low_files.append(file_path)

print(f'\nCRITICAL files: {len(critical_files)}')
print(f'HIGH files: {len(high_files)}')
print(f'MEDIUM files: {len(medium_files)}')
print(f'LOW files: {len(low_files)}')

# Save file lists for batch processing
output_dir = Path('.test_artifacts')
output_dir.mkdir(parents=True, exist_ok=True)

json.dump(critical_files, open(output_dir / 'critical_files.json', 'w'), indent=2)
json.dump(high_files, open(output_dir / 'high_files.json', 'w'), indent=2)
json.dump(medium_files, open(output_dir / 'medium_files.json', 'w'), indent=2)
json.dump(low_files, open(output_dir / 'low_files.json', 'w'), indent=2)

print(f'\nFile lists saved to {output_dir}/')
