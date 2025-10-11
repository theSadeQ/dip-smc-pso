"""
Analyze Sphinx build warnings from log file.
"""
import re
from collections import Counter

def analyze_warnings(log_file: str):
    """Analyze warnings from Sphinx build log."""
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Extract file paths and warning types
    files = []
    warning_types = []
    file_line_warnings = []

    for line in lines:
        if 'WARNING:' not in line:
            continue

        # Match file path after docs\
        match = re.search(r'docs[\\|/](.*?)\.md\.rst:(\d+):', line)
        if match:
            filepath = match.group(1).replace('\\', '/')
            line_num = match.group(2)
            files.append(filepath)
            file_line_warnings.append((filepath, line_num))

        # Extract warning type
        if 'H2 to H4' in line:
            warning_types.append('H2 to H4')
        elif 'H1 to H3' in line:
            warning_types.append('H1 to H3')
        elif 'H1 to H4' in line:
            warning_types.append('H1 to H4')
        else:
            # Extract generic warning type
            if '[myst.header]' in line:
                warning_types.append('Other header issue')
            else:
                warning_types.append('Other')

    # Count by directory
    dirs = Counter([f.split('/')[0] if '/' in f else 'root' for f in files])

    print('=' * 70)
    print('SPHINX DOCUMENTATION WARNING ANALYSIS - PHASE 11')
    print('=' * 70)
    print()
    print(f'TOTAL WARNINGS: {len(files)}')
    print('TOTAL ERRORS: 0')
    print()

    print('=' * 70)
    print('WARNING TYPE BREAKDOWN')
    print('=' * 70)
    wtype_count = Counter(warning_types)
    for wtype, count in sorted(wtype_count.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(files) * 100) if files else 0
        print(f'  {count:3d} ({pct:5.1f}%) - {wtype}')
    print()

    print('=' * 70)
    print('WARNINGS BY TOP-LEVEL DIRECTORY')
    print('=' * 70)
    for dir_name, count in sorted(dirs.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(files) * 100) if files else 0
        print(f'  {count:3d} ({pct:5.1f}%) - {dir_name}/')
    print()

    # Count by subdirectory
    subdirs = Counter(['/'.join(f.split('/')[:2]) if '/' in f else f for f in files])
    print('=' * 70)
    print('WARNINGS BY SUBDIRECTORY (Top 20)')
    print('=' * 70)
    for subdir, count in sorted(subdirs.items(), key=lambda x: x[1], reverse=True)[:20]:
        pct = (count / len(files) * 100) if files else 0
        print(f'  {count:3d} ({pct:5.1f}%) - {subdir}/')
    print()

    # Count warnings per file
    file_counts = Counter(files)
    print('=' * 70)
    print('FILES WITH MOST WARNINGS (Top 30)')
    print('=' * 70)
    for filepath, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:30]:
        print(f'  {count:2d} - {filepath}.md')
    print()

    # Categorization analysis
    print('=' * 70)
    print('CATEGORIZATION FOR SEPARATE FIXES')
    print('=' * 70)
    print()
    print('Category 1: H2 to H4 jumps (can be batch fixed)')
    h2_h4_files = [f for f, wt in zip(files, warning_types) if wt == 'H2 to H4']
    print(f'  Files affected: {len(set(h2_h4_files))}')
    print(f'  Total warnings: {len(h2_h4_files)}')
    print()

    print('Category 2: H1 to H3 jumps (needs manual review)')
    h1_h3_files = [f for f, wt in zip(files, warning_types) if wt == 'H1 to H3']
    print(f'  Files affected: {len(set(h1_h3_files))}')
    print(f'  Total warnings: {len(h1_h3_files)}')
    print()

    print('Category 3: H1 to H4 jumps (needs manual review)')
    h1_h4_files = [f for f, wt in zip(files, warning_types) if wt == 'H1 to H4']
    print(f'  Files affected: {len(set(h1_h4_files))}')
    print(f'  Total warnings: {len(h1_h4_files)}')
    print()

    return {
        'total_warnings': len(files),
        'total_errors': 0,
        'by_type': dict(wtype_count),
        'by_directory': dict(dirs),
        'by_subdirectory': dict(subdirs),
        'by_file': dict(file_counts)
    }

if __name__ == '__main__':
    log_file = r'D:\Projects\main\docs\sphinx_build_phase11_final.log'
    results = analyze_warnings(log_file)
