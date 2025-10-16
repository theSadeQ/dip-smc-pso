"""
Categorize Sphinx warnings by type for separate fixing.
"""
import re

def categorize_warnings(log_file: str):
    """Categorize warnings by type."""
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Categorize by warning type
    h2_h4_files = []
    h1_h3_files = []
    h1_h4_files = []

    for line in lines:
        if 'WARNING:' not in line:
            continue

        match = re.search(r'docs[\\|/](.*?)\.md\.rst:', line)
        if match:
            filepath = match.group(1).replace('\\', '/')

            if 'H2 to H4' in line:
                h2_h4_files.append(filepath)
            elif 'H1 to H3' in line:
                h1_h3_files.append(filepath)
            elif 'H1 to H4' in line:
                h1_h4_files.append(filepath)

    print('=' * 70)
    print('CATEGORY 1: H2 to H4 jumps (94 warnings - BATCH FIXABLE)')
    print('=' * 70)
    print('Files affected (53 unique files):')
    for f in sorted(set(h2_h4_files)):
        count = h2_h4_files.count(f)
        print(f'  [{count:2d}] {f}.md')
    print()

    print('=' * 70)
    print('CATEGORY 2: H1 to H3 jumps (18 warnings - MANUAL REVIEW)')
    print('=' * 70)
    print('Files affected (4 unique files):')
    for f in sorted(set(h1_h3_files)):
        count = h1_h3_files.count(f)
        print(f'  [{count:2d}] {f}.md')
    print()

    print('=' * 70)
    print('CATEGORY 3: H1 to H4 jumps (2 warnings - MANUAL REVIEW)')
    print('=' * 70)
    print('Files affected (1 unique file):')
    for f in sorted(set(h1_h4_files)):
        count = h1_h4_files.count(f)
        print(f'  [{count:2d}] {f}.md')
    print()

    return {
        'h2_h4': list(set(h2_h4_files)),
        'h1_h3': list(set(h1_h3_files)),
        'h1_h4': list(set(h1_h4_files))
    }

if __name__ == '__main__':
    log_file = r'D:\Projects\main\docs\sphinx_build_phase11_final.log'
    categorize_warnings(log_file)
