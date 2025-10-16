# Baseline Evidence Staging

Store Wave 0 screenshot captures, checksums, and future baseline refresh assets here.

Current structure:
- `playwright_capture.py` - Automation harness used for mobile_320 runs.
- `INDEX.md` - Page-by-page status with hash cross-reference.
- `mobile_320_hashes.json` - SHA256 digests for captured PNGs.
- `screenshots/mobile_320/` - Location for raw PNG captures (see `README.txt`).
- `tokens/` - Checksums, critical token values, and v1->v2 comparison report.

Add new viewports or reruns under subdirectories using the same naming convention.

