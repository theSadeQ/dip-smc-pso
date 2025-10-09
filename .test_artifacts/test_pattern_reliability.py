#!/usr/bin/env python3
"""Test the reliability of AI pattern detection."""

import re

# These are the actual patterns from the script
AI_PATTERNS = {
    "greeting": [
        r"\bLet's\b",
        r"\bWelcome\b",
    ],
    "enthusiasm": [
        r"\bpowerful\b",
        r"\bcomprehensive\b",
        r"\bseamless\b",
        r"\bcutting-edge\b",
    ],
    "hedge_words": [
        r"\bleverage\b",
        r"\butilize\b",
        r"\benable\b(?! flag| option| the| this)",  # Context-aware
        r"\bexploit\b(?! vulnerability)",  # Context-aware
    ],
}

def test_patterns():
    """Test cases for reliability."""
    test_cases = [
        # (text, should_detect, reason)
        ("This comprehensive framework is powerful", True, "AI marketing language"),
        ("The controller uses H-infinity robust control", False, "Technical term 'robust'"),
        ("Let's explore this exciting feature!", True, "Conversational greeting"),
        ("Use --enable flag to enable logging", False, "Technical 'enable' with flag"),
        ("We leverage cutting-edge algorithms", True, "AI buzzwords"),
        ("This exploits vulnerability CVE-2024-1234", False, "Security context 'exploit'"),
        ("The PSO optimizer minimizes cost", False, "Direct technical description"),
        ("Seamless integration with powerful capabilities", True, "Marketing fluff"),
        ("Enable the debug mode using config", False, "'Enable' in technical context"),
        ("Utilize the comprehensive toolset", True, "Hedge word + marketing"),
    ]

    print("PATTERN DETECTION RELIABILITY TEST")
    print("=" * 80)

    correct = 0
    total = len(test_cases)

    for text, should_detect, reason in test_cases:
        detected = False
        matches = []

        for category, patterns in AI_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected = True
                    matches.append(f"{category}:{pattern}")

        is_correct = (detected == should_detect)
        correct += is_correct

        status = "[OK] CORRECT" if is_correct else "[FAIL] WRONG"
        print(f"\n{status}")
        print(f"  Text: {text}")
        print(f"  Expected: {'DETECT' if should_detect else 'PASS'}")
        print(f"  Actual: {'DETECTED' if detected else 'PASSED'}")
        print(f"  Reason: {reason}")
        if matches:
            print(f"  Matches: {', '.join(matches)}")

    print("\n" + "=" * 80)
    print(f"ACCURACY: {correct}/{total} ({100*correct/total:.1f}%)")
    return correct, total

if __name__ == "__main__":
    correct, total = test_patterns()
