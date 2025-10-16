"""
Streamlit Dashboard Screenshot Capture for Wave 3 Theme Validation.

Captures screenshots of Streamlit dashboard in different states for visual regression testing.
Can be used for both baseline (theme disabled) and themed (theme enabled) captures.

Usage:
    python wave3_screenshot_capture.py baseline  # Capture without theme
    python wave3_screenshot_capture.py themed    # Capture with theme
"""
from __future__ import annotations

import asyncio
import sys
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page


BASE_URL = "http://localhost:8501"
TIMEOUT_MS = 30_000


async def wait_for_streamlit_ready(page: Page) -> None:
    """Wait for Streamlit to finish loading."""
    try:
        # Wait for Streamlit's internal ready state
        await page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=TIMEOUT_MS)
        # Additional wait for dynamic content
        await asyncio.sleep(2)
    except Exception as e:
        print(f"[WARN] Streamlit ready check failed: {e}")


async def capture_homepage(page: Page, output_dir: Path) -> None:
    """Capture homepage with controller selection."""
    print("\n[1/7] Capturing homepage...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    screenshot_path = output_dir / "01_homepage.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"  [OK] Saved: {screenshot_path.name}")


async def capture_sidebar(page: Page, output_dir: Path) -> None:
    """Capture sidebar navigation."""
    print("\n[2/7] Capturing sidebar...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    # Ensure sidebar is visible
    try:
        sidebar = await page.query_selector('section[data-testid="stSidebar"]')
        if sidebar:
            screenshot_path = output_dir / "02_sidebar.png"
            await sidebar.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")
        else:
            print(f"  [WARN] Sidebar not found")
    except Exception as e:
        print(f"  [FAIL] {e}")


async def capture_buttons(page: Page, output_dir: Path) -> None:
    """Capture primary button states."""
    print("\n[3/7] Capturing button states...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    try:
        # Find first button
        button = await page.query_selector('.stButton button')
        if button:
            # Normal state
            screenshot_path = output_dir / "03_button_normal.png"
            await button.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")

            # Hover state
            await button.hover()
            await asyncio.sleep(0.5)  # Wait for hover animation
            screenshot_path = output_dir / "04_button_hover.png"
            await button.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")

            # Focus state
            await button.focus()
            await asyncio.sleep(0.5)  # Wait for focus ring
            screenshot_path = output_dir / "05_button_focus.png"
            await button.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")
        else:
            print(f"  [WARN] Button not found")
    except Exception as e:
        print(f"  [FAIL] {e}")


async def capture_metrics(page: Page, output_dir: Path) -> None:
    """Capture metrics cards if present."""
    print("\n[4/7] Capturing metrics cards...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    try:
        # Look for metrics
        metrics = await page.query_selector_all('div[data-testid="stMetric"]')
        if metrics:
            # Capture first metric card
            screenshot_path = output_dir / "06_metric_card.png"
            await metrics[0].screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name} ({len(metrics)} metrics found)")
        else:
            print(f"  [WARN] No metrics found (might need simulation run)")
    except Exception as e:
        print(f"  [FAIL] {e}")


async def capture_tabs(page: Page, output_dir: Path) -> None:
    """Capture tabs if present."""
    print("\n[5/7] Capturing tabs...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    try:
        tabs = await page.query_selector('div[data-testid="stTabs"]')
        if tabs:
            screenshot_path = output_dir / "07_tabs.png"
            await tabs.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")
        else:
            print(f"  [INFO] No tabs found (may not be present on homepage)")
    except Exception as e:
        print(f"  [FAIL] {e}")


async def capture_full_viewport(page: Page, output_dir: Path) -> None:
    """Capture full viewport for overall theme parity check."""
    print("\n[6/7] Capturing full viewport...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    screenshot_path = output_dir / "08_full_viewport.png"
    await page.screenshot(path=screenshot_path)
    print(f"  [OK] Saved: {screenshot_path.name}")


async def capture_code_block(page: Page, output_dir: Path) -> None:
    """Capture code block if present."""
    print("\n[7/7] Capturing code block...")
    await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)
    await wait_for_streamlit_ready(page)

    try:
        code_block = await page.query_selector('div[data-testid="stCodeBlock"]')
        if code_block:
            screenshot_path = output_dir / "09_code_block.png"
            await code_block.screenshot(path=screenshot_path)
            print(f"  [OK] Saved: {screenshot_path.name}")
        else:
            print(f"  [INFO] No code block found (may not be present on homepage)")
    except Exception as e:
        print(f"  [FAIL] {e}")


async def run_capture_session(mode: str) -> dict:
    """Run complete screenshot capture session."""
    output_dir = Path(__file__).parent / "wave3" / mode
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "output_dir": str(output_dir),
        "screenshots_captured": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        try:
            # Run all capture tasks
            await capture_homepage(page, output_dir)
            results["screenshots_captured"].append("01_homepage.png")

            await capture_sidebar(page, output_dir)
            results["screenshots_captured"].append("02_sidebar.png")

            await capture_buttons(page, output_dir)
            results["screenshots_captured"].extend([
                "03_button_normal.png",
                "04_button_hover.png",
                "05_button_focus.png"
            ])

            await capture_metrics(page, output_dir)
            results["screenshots_captured"].append("06_metric_card.png")

            await capture_tabs(page, output_dir)
            results["screenshots_captured"].append("07_tabs.png")

            await capture_full_viewport(page, output_dir)
            results["screenshots_captured"].append("08_full_viewport.png")

            await capture_code_block(page, output_dir)
            results["screenshots_captured"].append("09_code_block.png")

        except Exception as e:
            print(f"\n[ERROR] Capture session failed: {e}")
            results["error"] = str(e)
        finally:
            await browser.close()

    return results


def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python wave3_screenshot_capture.py [baseline|themed]")
        print("\nExamples:")
        print("  python wave3_screenshot_capture.py baseline  # Capture without theme")
        print("  python wave3_screenshot_capture.py themed    # Capture with theme")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in ["baseline", "themed"]:
        print(f"[ERROR] Invalid mode: {mode}")
        print("Must be 'baseline' or 'themed'")
        sys.exit(1)

    print(f"{'='*60}")
    print(f"Wave 3 Screenshot Capture - {mode.upper()} Mode")
    print(f"{'='*60}")
    print(f"Base URL: {BASE_URL}")
    print(f"Output: wave3/{mode}/")
    print(f"{'='*60}\n")

    print("[INFO] Make sure Streamlit is running on http://localhost:8501")
    if mode == "baseline":
        print("[INFO] Ensure config.yaml has: streamlit.enable_dip_theme: false")
    else:
        print("[INFO] Ensure config.yaml has: streamlit.enable_dip_theme: true")
    print()

    results = asyncio.run(run_capture_session(mode))

    print(f"\n{'='*60}")
    print(f"CAPTURE COMPLETE - {mode.upper()}")
    print(f"{'='*60}")
    print(f"Screenshots captured: {len(results['screenshots_captured'])}")
    print(f"Output directory: {results['output_dir']}")

    if "error" in results:
        print(f"\n[ERROR] Session encountered errors: {results['error']}")
        sys.exit(1)
    else:
        print(f"\n[SUCCESS] All screenshots captured successfully")


if __name__ == "__main__":
    main()
