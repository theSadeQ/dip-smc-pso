"""Generate checksums and extract critical design token values for Phase 3."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
TOKENS_V2 = PROJECT_ROOT / ".codex" / "phase2_audit" / "design_tokens_v2.json"
OUTPUT_DIR = Path(__file__).resolve().parent

CRITICAL_TOKENS = [
    "--color-text-muted",
    "--color-code-notice-bg",
    "--color-code-notice-text",
    "--spacing-stack-sm",
    "--spacing-stack-md",
    "--spacing-inline-sm",
    "--font-size-h1-mobile",
    "--font-weight-link",
]


def md5(content: bytes) -> str:
    return hashlib.md5(content).hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def main() -> None:
    if not TOKENS_V2.exists():
        raise SystemExit(f"design_tokens_v2.json not found at {TOKENS_V2}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = TOKENS_V2.read_bytes()
    tokens = load_json(TOKENS_V2)

    checksum_payload = {
        "file": str(TOKENS_V2),
        "bytes": len(raw),
        "md5": md5(raw),
    }
    write_json(OUTPUT_DIR / "checksums.json", checksum_payload)

    critical = {
        token: tokens.get(token)
        for token in CRITICAL_TOKENS
        if token in tokens
    }
    write_json(OUTPUT_DIR / "token_values_critical.json", critical)

    print("[OK] design_tokens_v2.json integrity recorded")
    print(f"     md5: {checksum_payload['md5']}")
    print(f"     critical tokens exported: {len(critical)}")


if __name__ == "__main__":
    main()
