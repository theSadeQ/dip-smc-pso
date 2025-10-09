#!/bin/bash
echo "=== Baseline Claim Pattern Scan ===" > artifacts/baseline_scan_results.txt
echo "Generated: $(date)" >> artifacts/baseline_scan_results.txt
echo "" >> artifacts/baseline_scan_results.txt

echo "## Formal Claims (Markdown Documentation)" >> artifacts/baseline_scan_results.txt
echo "Searching for **Theorem|Lemma|Proposition|Corollary|Definition patterns..." >> artifacts/baseline_scan_results.txt
grep -r --include="*.md" -E '\*\*(Theorem|Lemma|Proposition|Corollary|Definition)' docs 2>/dev/null | wc -l >> artifacts/baseline_scan_results.txt
echo "" >> artifacts/baseline_scan_results.txt

echo "## Implementation Claims (Python Code)" >> artifacts/baseline_scan_results.txt
echo "Searching for Implements|Implementation of|Based on patterns..." >> artifacts/baseline_scan_results.txt
grep -r --include="*.py" -E 'Implements?|Implementation of|Based on' src 2>/dev/null | wc -l >> artifacts/baseline_scan_results.txt
echo "" >> artifacts/baseline_scan_results.txt

echo "## Existing Citations" >> artifacts/baseline_scan_results.txt
echo "Searching for {cite} syntax..." >> artifacts/baseline_scan_results.txt
grep -r --include="*.md" '{cite}' docs 2>/dev/null | wc -l >> artifacts/baseline_scan_results.txt
echo "" >> artifacts/baseline_scan_results.txt

echo "## File Counts" >> artifacts/baseline_scan_results.txt
echo -n "Total markdown files: " >> artifacts/baseline_scan_results.txt
find docs -name "*.md" -type f 2>/dev/null | wc -l >> artifacts/baseline_scan_results.txt
echo -n "Total Python files: " >> artifacts/baseline_scan_results.txt
find src -name "*.py" -type f 2>/dev/null | wc -l >> artifacts/baseline_scan_results.txt

cat artifacts/baseline_scan_results.txt
