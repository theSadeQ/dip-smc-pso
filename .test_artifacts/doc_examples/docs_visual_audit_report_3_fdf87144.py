# Example from: docs\reports\docs_visual_audit_report.md
# Index: 3
# Runnable: True
# Hash: fdf87144

# Add special handling for known slow pages
if "genindex" in str(html_file) or "coverage_analysis" in str(html_file):
    await page.goto(file_url, wait_until="load", timeout=60000)
else:
    await page.goto(file_url, wait_until="networkidle", timeout=30000)