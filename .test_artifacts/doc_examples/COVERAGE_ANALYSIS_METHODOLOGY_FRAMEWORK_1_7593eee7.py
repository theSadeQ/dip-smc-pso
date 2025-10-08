# Example from: docs\analysis\COVERAGE_ANALYSIS_METHODOLOGY_FRAMEWORK.md
# Index: 1
# Runnable: True
# Hash: 7593eee7

# scripts/coverage_validator.py
#==========================================================================================\\\
#=================================== coverage_validator.py ==============================\\\
#==========================================================================================\\\

"""Advanced coverage validation with mathematical threshold enforcement."""

import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
from pathlib import Path
import sys

class CoverageValidator:
    """Mathematical coverage validation with multi-tier enforcement."""

    def __init__(self, coverage_xml: Path):
        """Initialize coverage validator with XML report."""
        self.coverage_xml = coverage_xml
        self.tree = ET.parse(coverage_xml)
        self.root = self.tree.getroot()

    def get_component_coverage(self, component_pattern: str) -> float:
        """Calculate coverage for specific component pattern.

        Args:
            component_pattern: Pattern to match component files

        Returns:
            Coverage percentage for matched components
        """
        total_lines = 0
        covered_lines = 0

        for package in self.root.findall('.//package'):
            for class_elem in package.findall('.//class'):
                filename = class_elem.get('filename', '')
                if component_pattern in filename:
                    lines = class_elem.findall('.//line')
                    total_lines += len(lines)
                    covered_lines += sum(1 for line in lines if int(line.get('hits', 0)) > 0)

        return (covered_lines / total_lines * 100) if total_lines > 0 else 0.0

    def validate_quality_gates(self) -> Dict[str, Tuple[float, float, bool]]:
        """Validate all quality gate thresholds.

        Returns:
            Dict mapping gate name to (actual, required, passed) tuple
        """
        gates = {
            'safety_critical': (self.get_component_coverage('safety_guards'), 100.0),
            'controllers_smc': (self.get_component_coverage('controllers/smc'), 95.0),
            'core_dynamics': (self.get_component_coverage('core/dynamics'), 95.0),
            'pso_optimizer': (self.get_component_coverage('optimizer/pso'), 95.0),
            'overall_system': (float(self.root.get('line-rate', 0)) * 100, 85.0)
        }

        results = {}
        for gate_name, (actual, required) in gates.items():
            passed = actual >= required
            results[gate_name] = (actual, required, passed)

        return results

    def generate_coverage_report(self) -> str:
        """Generate comprehensive coverage analysis report."""
        results = self.validate_quality_gates()

        report = "## Coverage Quality Gate Analysis\n\n"
        report += "| **Component** | **Actual** | **Required** | **Status** |\n"
        report += "|---------------|------------|--------------|------------|\n"

        for gate_name, (actual, required, passed) in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            report += f"| {gate_name.replace('_', ' ').title()} | {actual:.1f}% | {required:.1f}% | {status} |\n"

        overall_pass = all(passed for _, _, passed in results.values())
        report += f"\n**Overall Quality Gate Status**: {'✅ PASS' if overall_pass else '❌ FAIL'}\n"

        return report

if __name__ == "__main__":
    validator = CoverageValidator(Path("coverage.xml"))
    results = validator.validate_quality_gates()

    # Enforcement logic
    failed_gates = [name for name, (_, _, passed) in results.items() if not passed]

    if failed_gates:
        print(f"❌ Coverage quality gates FAILED: {', '.join(failed_gates)}")
        print(validator.generate_coverage_report())
        sys.exit(1)
    else:
        print("✅ All coverage quality gates PASSED")
        sys.exit(0)