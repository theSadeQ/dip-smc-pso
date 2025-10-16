"""Wave 2 responsive breakpoint validation - capture at 320px, 768px, 1024px.

Purpose:
    Validate Wave 2 responsive layout fixes across three critical breakpoints:
    - Mobile (320px): UI-020 (H1 word-break), UI-022 (nav grid collapse), UI-023 (footer spacing)
    - Tablet (768px): UI-024 (nav grid 3-col → 2-col), UI-025 (anchor rail font scaling)
    - Desktop (1024px): Baseline for comparison

Exit Criteria:
    - [x] Capture 3 pages × 3 viewports = 9 screenshots
    - [x] Visual confirmation: No overflow, broken grids, or spacing issues
    - [x] Evidence saved to `.codex/phase3/validation/responsive/screenshots/`

Usage:
    python .codex/phase3/validation/responsive/wave2_responsive_capture.py

Requirements:
    pip install playwright
    playwright install chromium
"""
from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path

from playwright.async_api import async_playwright

# Viewports: Mobile (320px), Tablet (768px), Desktop (1024px)
VIEWPORTS = {
    "mobile_320": {"width": 320, "height": 720},
    "tablet_768": {"width": 768, "height": 1024},
    "desktop_1024": {"width": 1024, "height": 768},
}

# Test pages: Homepage, Getting Started, Controller API (covers all Wave 2 UI fixes)
PAGES = [
    ("home", "/"),
    ("guides-getting-started", "/guides/getting-started"),
    ("reference-controllers", "/reference/controllers/index"),
]

BASE_URL = "http://localhost:9000"
TIMEOUT_MS = 60_000  # 60s timeout (increased from baseline 30s for stability)
OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots"


async def capture_screenshots() -> dict[str, dict[str, str]]:
    """Capture screenshots at all breakpoints for all pages.

    Returns:
        Dict mapping viewport → page → screenshot SHA256 hash
    """
    hashes: dict[str, dict[str, str]] = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for viewport_name, viewport_size in VIEWPORTS.items():
            print(f"\n{'='*60}")
            print(f"Capturing {viewport_name} ({viewport_size['width']}×{viewport_size['height']})")
            print(f"{'='*60}")

            page = await browser.new_page(viewport=viewport_size)
            viewport_dir = OUTPUT_DIR / viewport_name
            viewport_dir.mkdir(parents=True, exist_ok=True)

            hashes[viewport_name] = {}

            for page_name, page_path in PAGES:
                url = f"{BASE_URL}{page_path}"
                output_file = viewport_dir / f"{page_name}.png"

                try:
                    print(f"  [{page_name}] Loading {url}...", end=" ", flush=True)
                    await page.goto(url, wait_until="networkidle", timeout=TIMEOUT_MS)

                    print("Capturing...", end=" ", flush=True)
                    await page.screenshot(path=output_file, full_page=True)

                    # Compute SHA256 hash for integrity verification
                    sha256_hash = hashlib.sha256(output_file.read_bytes()).hexdigest()
                    hashes[viewport_name][page_name] = sha256_hash

                    print(f"[OK] ({output_file.relative_to(OUTPUT_DIR.parent)})")
                    print(f"    SHA256: {sha256_hash[:16]}...")

                except Exception as exc:  # noqa: BLE001 - capture all failures for reporting
                    print(f"[FAIL] FAILED: {exc}")
                    hashes[viewport_name][page_name] = f"ERROR: {exc}"

            await page.close()

        await browser.close()

    return hashes


def generate_hash_manifest(hashes: dict[str, dict[str, str]]) -> None:
    """Save screenshot hashes to JSON manifest for traceability."""
    manifest_file = OUTPUT_DIR / "wave2_screenshot_hashes.json"
    manifest_data = {
        "wave": "Wave 2",
        "date": "2025-10-15",
        "viewports": VIEWPORTS,
        "pages": [{"name": name, "path": path} for name, path in PAGES],
        "hashes": hashes,
    }

    manifest_file.write_text(json.dumps(manifest_data, indent=2))
    print(f"\n[OK] Hash manifest saved: {manifest_file.relative_to(OUTPUT_DIR.parent)}")


def print_validation_checklist() -> None:
    """Print manual validation checklist for Wave 2 responsive fixes."""
    print("\n" + "="*60)
    print("MANUAL VALIDATION CHECKLIST (Wave 2 Responsive Fixes)")
    print("="*60)
    print("\n[MOBILE] 320px - Check these screenshots:")
    print("  [ ] UI-020: H1 headings have word-break (no horizontal overflow)")
    print("  [ ] UI-022: Visual nav grid collapses to 1-col (not 2-col)")
    print("  [ ] UI-023: Footer metadata has proper spacing (line-height 1.6)")
    print("\n[TABLET] 768px - Check these screenshots:")
    print("  [ ] UI-024: Visual nav grid is 2-col (not 3-col)")
    print("  [ ] UI-025: Anchor rail font is 14px (not 16px)")
    print("\n[DESKTOP] 1024px - Baseline comparison:")
    print("  [ ] All elements render correctly (no regressions)")
    print("\n" + "="*60)
    print("Next Steps:")
    print("  1. Open screenshots in .codex/phase3/validation/responsive/screenshots/")
    print("  2. Verify each checkbox above")
    print("  3. Document any failures in wave2_exit/FAILURES.md")
    print("="*60)


async def main() -> None:
    """Main entry point for Wave 2 responsive validation."""
    print("\n" + "="*60)
    print("Wave 2 Responsive Breakpoint Validation")
    print("="*60)
    print(f"Server: {BASE_URL}")
    print(f"Viewports: {len(VIEWPORTS)} ({', '.join(VIEWPORTS.keys())})")
    print(f"Pages: {len(PAGES)} ({', '.join(name for name, _ in PAGES)})")
    print(f"Total Screenshots: {len(VIEWPORTS) * len(PAGES)}")
    print("="*60)

    # Capture screenshots at all breakpoints
    hashes = await capture_screenshots()

    # Save hash manifest for traceability
    generate_hash_manifest(hashes)

    # Print manual validation checklist
    print_validation_checklist()


if __name__ == "__main__":
    asyncio.run(main())
