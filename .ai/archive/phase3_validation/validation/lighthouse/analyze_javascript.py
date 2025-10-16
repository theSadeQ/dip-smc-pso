"""Analyze JavaScript bottlenecks causing 18.4s bootup time."""
import json
from pathlib import Path

report_path = Path(__file__).parent / "wave2_exit" / "phase2-production-homepage.json"
data = json.load(open(report_path))

print('='*80)
print('JavaScript Performance Analysis')
print('='*80)

# Bootup time breakdown
bootup = data['audits'].get('bootup-time', {})
items = bootup.get('details', {}).get('items', [])
print(f'\nBootup Time Breakdown ({bootup.get("displayValue", "N/A")}):')
print('-'*80)
total_bootup = sum(item.get('scripting', 0) for item in items)
print(f"Total Bootup: {total_bootup:.0f}ms")
print('\nTop 10 scripts by execution time:')
for i, item in enumerate(items[:10], 1):
    url = item.get('url', '').split('/')[-1][:50]
    scripting = item.get('scripting', 0)
    script_parse_compile = item.get('scriptParseCompile', 0)
    total = item.get('total', 0)
    print(f"{i:2d}. {url:<50} {scripting:>7.0f}ms exec, {script_parse_compile:>7.0f}ms parse, {total:>7.0f}ms total")

# Network requests - JS files only
network_requests = data['audits'].get('network-requests', {})
items = network_requests.get('details', {}).get('items', [])
js_files = [item for item in items if item.get('resourceType') == 'Script']
print(f'\n\nJavaScript Network Requests ({len(js_files)} files):')
print('-'*80)
total_js_size = sum(item.get('transferSize', 0) for item in js_files)
print(f"Total JS Transfer Size: {total_js_size/1024:.1f} KB")
print('\nAll JavaScript files:')
for i, item in enumerate(js_files, 1):
    url = item.get('url', '').split('/')[-1][:50]
    transfer_size = item.get('transferSize', 0) / 1024
    resource_size = item.get('resourceSize', 0) / 1024
    finish_time = (item.get('endTime', 0) - item.get('startTime', 0)) * 1000
    print(f"{i:2d}. {url:<50} {transfer_size:>7.1f}KB xfer, {resource_size:>7.1f}KB orig, {finish_time:>7.0f}ms")

# Legacy JavaScript
legacy_js = data['audits'].get('legacy-javascript', {})
print(f'\n\nLegacy JavaScript Issues:')
print(f"Potential Savings: {legacy_js.get('displayValue', 'N/A')}")
print(f"Score: {legacy_js.get('score', 'N/A')}")

# Third-party code
third_party = data['audits'].get('third-party-summary', {})
items = third_party.get('details', {}).get('items', [])
print(f'\n\nThird-Party Code ({len(items)} entities):')
print('-'*80)
for i, item in enumerate(items[:10], 1):
    entity = item.get('entity', {}).get('text', 'Unknown')
    transfer_size = item.get('transferSize', 0) / 1024
    blocking_time = item.get('blockingTime', 0)
    print(f"{i:2d}. {entity:<50} {transfer_size:>7.1f}KB, {blocking_time:>7.0f}ms blocking")

# Mainthread work breakdown
mainthread = data['audits'].get('mainthread-work-breakdown', {})
items = mainthread.get('details', {}).get('items', [])
print(f'\n\nMain Thread Work Breakdown ({mainthread.get("displayValue", "N/A")}):')
print('-'*80)
for item in items[:10]:
    group = item.get('group', 'Unknown')
    duration = item.get('duration', 0)
    print(f"{group:<50} {duration:>7.0f}ms")

print('\n' + '='*80)
print('DIAGNOSIS')
print('='*80)
print('The 18.4s JS bootup time is blocking FCP/LCP at 7.6s.')
print('Root cause: Heavy JavaScript execution on page load.')
print('Recommendation: Defer non-critical JS, code-split, lazy-load.')
