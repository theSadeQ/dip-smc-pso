#!/usr/bin/env python3
"""Analyze Lighthouse audit results"""
import json
import sys

audit_file = '.codex/phase3/validation/lighthouse/wave2_exit/final_audit_mathjax_override.json'

with open(audit_file) as f:
    data = json.load(f)

audits = data['audits']

# Performance Metrics
print("=== PERFORMANCE METRICS ===")
print(f"Performance Score: {data['categories']['performance']['score'] * 100:.0f}/100")
print(f"LCP: {audits['largest-contentful-paint']['displayValue']}")
print(f"FCP: {audits['first-contentful-paint']['displayValue']}")
print(f"Speed Index: {audits['speed-index']['displayValue']}")
print(f"TTI: {audits['interactive']['displayValue']}")
print(f"TBT: {audits['total-blocking-time']['displayValue']}")
print()

# Render-Blocking Resources
print("=== RENDER-BLOCKING RESOURCES ===")
render_blocking = audits.get('render-blocking-resources', {})
if 'details' in render_blocking and 'items' in render_blocking['details']:
    items = render_blocking['details']['items']
    print(f"Total: {len(items)} resources")
    for item in items[:10]:
        url = item.get('url', 'N/A')
        # Extract just filename
        filename = url.split('/')[-1] if '/' in url else url
        size_kb = item.get('totalBytes', 0) / 1024
        print(f"  - {filename}: {size_kb:.1f} KB")
else:
    print("No render-blocking resources data")
print()

# Opportunities
print("=== OPTIMIZATION OPPORTUNITIES ===")
opportunities = [
    ('unused-css-rules', 'Unused CSS'),
    ('unused-javascript', 'Unused JavaScript'),
    ('unminified-css', 'Unminified CSS'),
    ('unminified-javascript', 'Unminified JavaScript'),
    ('offscreen-images', 'Offscreen Images'),
]

for audit_key, label in opportunities:
    if audit_key in audits:
        audit = audits[audit_key]
        if 'details' in audit and 'overallSavingsMs' in audit['details']:
            savings_ms = audit['details']['overallSavingsMs']
            savings_kb = audit['details'].get('overallSavingsBytes', 0) / 1024
            if savings_ms > 100 or savings_kb > 10:
                print(f"{label}: {savings_ms:.0f} ms, {savings_kb:.0f} KB savings")
