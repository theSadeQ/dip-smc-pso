# Example from: docs\reports\docs_visual_audit_report.md
# Index: 2
# Runnable: True
# Hash: c2bc8312

# Change from "networkidle" to "domcontentloaded"
await page.goto(file_url, wait_until="domcontentloaded", timeout=30000)

# Then wait for specific elements
await page.wait_for_selector("body", timeout=10000)