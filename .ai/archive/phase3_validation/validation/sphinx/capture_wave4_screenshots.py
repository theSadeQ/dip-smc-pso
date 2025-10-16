"""Capture Phase 3 Wave 4 Sphinx documentation screenshots."""
from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[4]
BUILD_ROOT = PROJECT_ROOT / "docs_build" / "html"
OUTPUT_DIR = Path(__file__).resolve().parent / "before_after" / "after"

PAGES = [
    ("index", "index.html"),
    ("getting-started", "guides/getting-started.html"),
    ("controller-reference", "reference/controllers/index.html"),
    ("benchmarks", "benchmarks/index.html"),
]

VIEWPORT = {"width": 1920, "height": 1080}
TIMEOUT_MS = 45_000


async def capture() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport=VIEWPORT)
        for slug, relative_path in PAGES:
            target = (BUILD_ROOT / relative_path).resolve()
            if not target.exists():
                print(f"SKIP {slug}: missing {target}")
                continue
            uri = target.as_uri()
            try:
                await page.goto(uri, wait_until="load", timeout=TIMEOUT_MS)
                await page.wait_for_timeout(1000)  # allow fonts/styles to settle
                await page.screenshot(
                    path=OUTPUT_DIR / f"{slug}_desktop_1920.png",
                    full_page=True,
                )
                print(f"CAPTURED {slug}")
            except Exception as exc:  # noqa: BLE001 - log and continue
                print(f"FAILED {slug}: {exc}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture())
