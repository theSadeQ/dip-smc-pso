"""Quick analysis of broken links for Phase 6 cleanup."""
import json
from pathlib import Path
from collections import Counter

# Load broken links
broken_links_file = Path('.test_artifacts/cross_references/broken_links.json')
with open(broken_links_file, 'r', encoding='utf-8') as f:
    links = json.load(f)

print(f"Total broken links: {len(links)}")
print("=" * 60)

# Analyze by source file
source_counts = Counter()
for link in links:
    source = link.get('source', 'unknown')
    # Get just the filename
    source_file = source.split('\\')[-1] if '\\' in source else source.split('/')[-1]
    source_counts[source_file] += 1

print("\nTop 15 files with most broken links:")
for i, (file, count) in enumerate(source_counts.most_common(15), 1):
    print(f"{i:2}. {file:50} {count:3} broken links")

# Analyze by type
print("\n" + "=" * 60)
print("Broken link categories:")
print("=" * 60)

missing_docs = []
incorrect_paths = []
placeholder_links = []
external_refs = []

for link in links:
    target = link.get('target', '')

    if target.startswith('..') and ('.py' in target or '/src/' in target):
        external_refs.append(link)
    elif any(placeholder in target.lower() for placeholder in ['config', 'value', 'key', 'type', 'other-page']):
        placeholder_links.append(link)
    elif '/' in target or '\\' in target:
        incorrect_paths.append(link)
    else:
        missing_docs.append(link)

print(f"\n1. External directory references: {len(external_refs)}")
print(f"2. Placeholder/example links: {len(placeholder_links)}")
print(f"3. Incorrect relative paths: {len(incorrect_paths)}")
print(f"4. Missing documentation files: {len(missing_docs)}")

# Show top missing docs
print("\n" + "=" * 60)
print("Top missing documentation files:")
print("=" * 60)
missing_targets = Counter()
for link in missing_docs[:50]:  # Analyze first 50
    missing_targets[link.get('target', '')] += 1

for i, (target, count) in enumerate(missing_targets.most_common(10), 1):
    print(f"{i:2}. {target:40} ({count} references)")
