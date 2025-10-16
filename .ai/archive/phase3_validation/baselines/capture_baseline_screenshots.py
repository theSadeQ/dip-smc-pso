"""Playwright baseline screenshot capture for Phase 3 Wave 0."""
from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

PAGES = [
    ("home", "/"),
    ("guides-getting-started", "/guides/getting-started"),
    ("guides-theory-smc", "/guides/theory/smc-theory"),
    ("reference-controllers", "/reference/controllers/index"),
    ("reference-optimization", "/reference/optimization/index"),
    ("analysis-controller-comparison", "/analysis/controller_comparison"),
    ("benchmarks-overview", "/benchmarks/index"),
    ("production-readiness", "/production/index"),
]

OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots" / "mobile_320"
BASE_URL = "http://localhost:9000"
VIEWPORT = {"width": 320, "height": 720}
TIMEOUT_MS = 30_000


async def capture() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport_size=VIEWPORT)
        for name, path in PAGES:
            url = f"{BASE_URL}{path}"
            try:
                await page.goto(url, wait_until="networkidle", timeout=TIMEOUT_MS)
                await page.screenshot(path=OUTPUT_DIR / f"{name}.png", full_page=True)
            except Exception as exc:  # noqa: BLE001 - log and continue
                print(f"FAILED {name}: {exc}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture())
