"""Detailed inspection of benchmarks page ARIA violation."""
from __future__ import annotations

import asyncio

from playwright.async_api import async_playwright

URL = "http://localhost:9000/benchmarks/index.html"
AXE_CORE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.8.2/axe.min.js"


async def inspect_aria_violation() -> None:
    """Get detailed node information for ARIA violation."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print(f"Navigating to {URL}...")
        await page.goto(URL, wait_until="networkidle", timeout=60_000)

        print("Injecting axe-core...")
        await page.add_script_tag(url=AXE_CORE_URL)
        await page.wait_for_function("typeof axe !== 'undefined'", timeout=5000)

        print("Running detailed axe scan...")
        results = await page.evaluate("""
            async () => {
                const results = await axe.run({
                    rules: {
                        'aria-required-attr': { enabled: true }
                    }
                });
                return results.violations;
            }
        """)

        print("\n" + "="*60)
        print("ARIA-REQUIRED-ATTR VIOLATION DETAILS")
        print("="*60 + "\n")

        for violation in results:
            if violation["id"] == "aria-required-attr":
                print(f"Rule: {violation['id']}")
                print(f"Impact: {violation['impact']}")
                print(f"Description: {violation['description']}")
                print(f"Help: {violation['help']}\n")

                for i, node in enumerate(violation.get("nodes", []), 1):
                    print(f"Node {i}:")
                    print(f"  HTML: {node['html'][:200]}...")
                    print(f"  Failure summary: {node['failureSummary']}")
                    print(f"  Target: {node['target']}")
                    print("  Any messages:")
                    for msg in node.get("any", []):
                        print(f"    - {msg['message']}")
                    print()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect_aria_violation())
