"""Analyze render-blocking resources from Lighthouse report."""
import json
from pathlib import Path

report_path = Path(__file__).parent / "wave2_exit" / "phase2-production-homepage.json"
data = json.load(open(report_path))

# Render-blocking resources audit
audit = data['audits'].get('render-blocking-resources', {})
print('='*80)
print('Render-Blocking Resources Analysis')
print('='*80)
print(f"Impact: {audit.get('displayValue', 'N/A')}")
print(f"Score: {audit.get('score', 'N/A')}")

items = audit.get('details', {}).get('items', [])
print(f"Count: {len(items)} resources")

total_bytes = sum(item.get('totalBytes', 0) for item in items)
print(f"Total Size: {total_bytes/1024:.1f} KB")

print('\nTop 10 Blocking Resources:')
print('-'*80)
for i, item in enumerate(items[:10], 1):
    url = item.get('url', 'N/A')
    filename = url.split('/')[-1][:60]
    size_kb = item.get('totalBytes', 0) / 1024
    wastedMs = item.get('wastedMs', 0)
    print(f"{i:2d}. {filename:<60} {size_kb:>6.1f} KB  {wastedMs:>5.0f}ms")

# LCP element
lcp_audit = data['audits']['largest-contentful-paint']
lcp_element = data['audits'].get('largest-contentful-paint-element', {})
print('\n' + '='*80)
print('LCP Element Details')
print('='*80)
print(f"LCP Time: {lcp_audit['displayValue']}")
print(f"LCP Element: {lcp_element.get('displayValue', 'N/A')}")

# Total blocking time
tbt_audit = data['audits'].get('total-blocking-time', {})
print('\n' + '='*80)
print('Total Blocking Time')
print('='*80)
print(f"TBT: {tbt_audit.get('displayValue', 'N/A')}")
print(f"Score: {tbt_audit.get('score', 'N/A')}")

# First Contentful Paint
fcp_audit = data['audits'].get('first-contentful-paint', {})
print('\n' + '='*80)
print('First Contentful Paint')
print('='*80)
print(f"FCP: {fcp_audit.get('displayValue', 'N/A')}")
print(f"Score: {fcp_audit.get('score', 'N/A')}")
