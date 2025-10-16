"""Deep dive into Lighthouse diagnostics to find root cause of 7.6s FCP/LCP."""
import json
from pathlib import Path

report_path = Path(__file__).parent / "wave2_exit" / "phase2-production-homepage.json"
data = json.load(open(report_path))

print('='*80)
print('Deep Diagnostic Analysis - Root Cause Investigation')
print('='*80)

# Server response time
server_response = data['audits'].get('server-response-time', {})
print('\n1. Server Response Time:')
print(f"   Time: {server_response.get('displayValue', 'N/A')}")
print(f"   Score: {server_response.get('score', 'N/A')}")

# Bootup time (JavaScript execution)
bootup = data['audits'].get('bootup-time', {})
print('\n2. JavaScript Bootup Time:')
print(f"   Time: {bootup.get('displayValue', 'N/A')}")
print(f"   Score: {bootup.get('score', 'N/A')}")

# Mainthread work breakdown
mainthread = data['audits'].get('mainthread-work-breakdown', {})
print('\n3. Main Thread Work:')
print(f"   Time: {mainthread.get('displayValue', 'N/A')}")
print(f"   Score: {mainthread.get('score', 'N/A')}")

# Network requests
network_requests = data['audits'].get('network-requests', {})
items = network_requests.get('details', {}).get('items', [])
print(f'\n4. Network Requests: {len(items)} total')
print('   First 10 requests:')
for i, item in enumerate(items[:10], 1):
    url = item.get('url', '').split('/')[-1][:50]
    status = item.get('statusCode', 'N/A')
    transfer_size = item.get('transferSize', 0) / 1024
    resource_type = item.get('resourceType', 'N/A')
    finish_time = item.get('endTime', 0) - item.get('startTime', 0)
    print(f"   {i:2d}. {url:<50} {status:>3} {transfer_size:>6.1f}KB {finish_time:>7.0f}ms {resource_type}")

# Diagnostics audit
diagnostics = data['audits'].get('diagnostics', {})
diag_details = diagnostics.get('details', {}).get('items', [{}])[0]
print('\n5. Key Diagnostics:')
print(f"   Max Rasterize: {diag_details.get('maxRasterDuration', 0):.0f}ms")
print(f"   Max Server Latency: {diag_details.get('maxServerLatency', 0):.0f}ms")
print(f"   Total Byte Weight: {diag_details.get('totalByteWeight', 0)/1024:.0f}KB")
print(f"   Main Document Transfer Size: {diag_details.get('mainDocumentTransferSize', 0)/1024:.1f}KB")

# Speed Index
speed_index = data['audits'].get('speed-index', {})
print('\n6. Speed Index:')
print(f"   Time: {speed_index.get('displayValue', 'N/A')}")
print(f"   Score: {speed_index.get('score', 'N/A')}")

# Time to Interactive
tti = data['audits'].get('interactive', {})
print('\n7. Time to Interactive:')
print(f"   Time: {tti.get('displayValue', 'N/A')}")
print(f"   Score: {tti.get('score', 'N/A')}")

# Unused CSS
unused_css = data['audits'].get('unused-css-rules', {})
print('\n8. Unused CSS:')
print(f"   Potential Savings: {unused_css.get('displayValue', 'N/A')}")
print(f"   Score: {unused_css.get('score', 'N/A')}")
items = unused_css.get('details', {}).get('items', [])
if items:
    print('   Top 5 stylesheets with unused CSS:')
    for i, item in enumerate(items[:5], 1):
        url = item.get('url', '').split('/')[-1][:50]
        total_bytes = item.get('totalBytes', 0) / 1024
        wasted_bytes = item.get('wastedBytes', 0) / 1024
        wasted_percent = item.get('wastedPercent', 0)
        print(f"   {i}. {url:<50} {total_bytes:>6.1f}KB total, {wasted_bytes:>6.1f}KB unused ({wasted_percent:.0f}%)")

print('\n' + '='*80)
print('SUMMARY')
print('='*80)
print(f"FCP: {data['audits']['first-contentful-paint']['displayValue']}")
print(f"LCP: {data['audits']['largest-contentful-paint']['displayValue']}")
print(f"TBT: {data['audits']['total-blocking-time']['displayValue']}")
print(f"Performance Score: {data['categories']['performance']['score']*100:.0f}/100")
