"""Retry homepage baseline screenshot with increased timeout."""
from __future__ import annotations

import asyncio
import hashlib
from pathlib import Path

from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots" / "mobile_320"
BASE_URL = "http://localhost:9000"
VIEWPORT = {"width": 320, "height": 720}
TIMEOUT_MS = 60_000  # Increased from 30s to 60s


async def capture_homepage() -> None:
    """Capture homepage screenshot with extended timeout."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    screenshot_path = OUTPUT_DIR / "home.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport=VIEWPORT)

        try:
            print(f"Navigating to {BASE_URL} (timeout: {TIMEOUT_MS}ms)...")
            await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)

            print("Capturing full-page screenshot...")
            await page.screenshot(path=screenshot_path, full_page=True)

            # Compute SHA256 hash
            sha256 = hashlib.sha256(screenshot_path.read_bytes()).hexdigest()

            print(f"SUCCESS: Screenshot saved to {screenshot_path}")
            print(f"SHA256: {sha256}")

        except Exception as exc:
            print(f"FAILED: {exc}")
            raise
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(capture_homepage())
