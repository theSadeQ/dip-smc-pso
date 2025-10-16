#!/usr/bin/env python3
"""Parse pytest results and generate CI summary JSON."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from typing import Dict, List, Any


def parse_junit_xml(xml_path: str) -> Dict[str, Any]:
    """Parse JUnit XML file and extract test results."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find the testsuite element
    testsuite = root.find('.//testsuite')
    if testsuite is None:
        raise ValueError("No testsuite found in JUnit XML")

    # Extract stats
    stats = {
        "tests": int(testsuite.get("tests", 0)),
        "passed": 0,
        "failed": int(testsuite.get("failures", 0)),
        "errors": int(testsuite.get("errors", 0)),
        "skipped": int(testsuite.get("skipped", 0)),
        "xfail": 0,  # Not directly available in this XML format
        "xpass": 0,  # Not directly available in this XML format
        "duration_seconds": float(testsuite.get("time", 0.0))
    }

    # Calculate passed tests
    stats["passed"] = stats["tests"] - stats["failed"] - stats["errors"] - stats["skipped"]

    # Extract failures
    failures = []
    slow_tests = []

    for testcase in testsuite.findall('.//testcase'):
        classname = testcase.get("classname", "")
        name = testcase.get("name", "")
        time = float(testcase.get("time", 0.0))

        # Build nodeid
        nodeid = f"{classname}::{name}" if classname else name

        # Collect slow tests (>0.05s for this analysis)
        if time > 0.05:
            slow_tests.append({
                "nodeid": nodeid,
                "duration_seconds": time
            })

        # Check for failures
        failure = testcase.find('failure')
        if failure is not None:
            message = failure.get("message", "")
            text = failure.text or ""

            # Extract file and line from traceback
            file_line_match = re.search(r'([^\\]+\.py):(\d+):', text)
            file_path = file_line_match.group(1) if file_line_match else "unknown"
            line_num = int(file_line_match.group(2)) if file_line_match else 0

            # Categorize failure
            category = categorize_failure(message, text)

            # Extract first user frame (simplified)
            first_user_frame = extract_user_frame(text)

            # Generate hint
            hint_md = generate_hint(nodeid, message, category)

            failures.append({
                "nodeid": nodeid,
                "file": file_path,
                "line": line_num,
                "short_message": message[:100] + "..." if len(message) > 100 else message,
                "category": category,
                "first_user_frame": first_user_frame,
                "hint_md": hint_md
            })

    # Sort slow tests by duration
    slow_tests.sort(key=lambda x: x["duration_seconds"], reverse=True)

    return stats, failures, slow_tests[:5]  # Top 5 slowest


def categorize_failure(message: str, text: str) -> str:
    """Categorize failure based on error message and traceback."""
    if "AssertionError" in message:
        if "'FAULT' == 'OK'" in message:
            return "logic regression"
        return "logic regression"
    elif "ImportError" in text or "ModuleNotFoundError" in text:
        return "import/pathing"
    elif "AttributeError" in message:
        return "API mismatch"
    elif "TimeoutError" in message or "timeout" in message.lower():
        return "timing/flaky"
    elif "ConnectionError" in message or "OSError" in message:
        return "env/deps"
    else:
        return "logic regression"


def extract_user_frame(text: str) -> str:
    """Extract first user code frame from traceback."""
    lines = text.split('\n')
    for line in lines:
        if '.py:' in line and 'site-packages' not in line:
            # Extract file:line pattern
            match = re.search(r'([^\\\/]+\.py):(\d+)', line)
            if match:
                return f"{match.group(1)}:{match.group(2)}"
    return "unknown"


def generate_hint(nodeid: str, message: str, category: str) -> str:
    """Generate helpful hint for failure."""
    if "test_fixed_threshold_operation" in nodeid and "'FAULT' == 'OK'" in message:
        return "- Check FDI threshold configuration in fault detection system\n- Verify test random seed for reproducible noise generation"
    elif category == "import/pathing":
        return "- Check PYTHONPATH includes src/ directory\n- Verify all required dependencies are installed"
    elif category == "logic regression":
        return "- Review recent changes to core logic\n- Check boundary conditions and edge cases"
    elif category == "timing/flaky":
        return "- Add sleep/retry logic for timing-sensitive operations\n- Consider using mocks for time-dependent tests"
    else:
        return f"- Re-run locally: pytest -k '{nodeid.split('::')[-1]}' -vv\n- Check logs for additional context"


def main():
    """Main function to generate CI summary."""
    base_dir = Path(__file__).parent

    # Parse results
    try:
        stats, failures, slow_tests = parse_junit_xml(base_dir / "junit.xml")

        # Determine status
        if stats["failed"] > 0 or stats["errors"] > 0:
            status = "failed"
        else:
            status = "passed"

        # Generate summary
        summary = f"{stats['tests']} tests, {stats['failed']} failed, {stats['skipped']} skipped"

        # Build followups
        followups = []
        if failures:
            failing_test = failures[0]["nodeid"].split("::")[-1]
            followups.append(f"Re-run locally: pytest -k '{failing_test}' -vv")
        if "fault_detection" in str(failures):
            followups.append("Check FDI system configuration and random seed")

        # Generate final JSON
        result = {
            "summary": summary,
            "status": status,
            "stats": stats,
            "artifacts": {
                "junit_xml": "reports/junit.xml",
                "raw_log": "reports/pytest.log",
                "coverage_xml": "reports/coverage.xml" if (base_dir / "coverage.xml").exists() else None
            },
            "slow_tests": slow_tests,
            "failures": failures,
            "followups": followups
        }

        # Save and print JSON
        with open(base_dir / "summary.json", 'w') as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))

    except Exception as e:
        # Error fallback
        error_result = {
            "summary": f"Test run failed with error: {str(e)}",
            "status": "error",
            "stats": {"tests": 0, "passed": 0, "failed": 0, "errors": 1, "skipped": 0, "xfail": 0, "xpass": 0, "duration_seconds": 0.0},
            "artifacts": {"junit_xml": "reports/junit.xml", "raw_log": "reports/pytest.log", "coverage_xml": None},
            "slow_tests": [],
            "failures": [],
            "followups": ["Check pytest.log for detailed error information"]
        }

        with open(base_dir / "summary.json", 'w') as f:
            json.dump(error_result, f, indent=2)

        print(json.dumps(error_result, indent=2))


if __name__ == "__main__":
    main()