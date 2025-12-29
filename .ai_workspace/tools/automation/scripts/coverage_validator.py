#======================================================================================\\\
#=========================== scripts/coverage_validator.py ============================\\\
#======================================================================================\\\

"""Advanced coverage validation with mathematical threshold enforcement for GitHub Issue #9."""

import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import sys
import json
import argparse
from datetime import datetime

class CoverageValidator:
    """Mathematical coverage validation with multi-tier enforcement.

    Implements the coverage methodology framework for DIP SMC PSO project,
    enforcing 85%/95%/100% quality gate thresholds with scientific rigor.
    """

    # Component classification for coverage requirements
    SAFETY_CRITICAL_PATTERNS = [
        'safety_guards',
        'parameter_bounds',
        'gain_validation',
        'bounds_checking'
    ]

    CRITICAL_COMPONENT_PATTERNS = [
        'controllers/smc',
        'controllers/adaptive_smc',
        'controllers/classic_smc',
        'controllers/sta_smc',
        'core/dynamics',
        'core/dynamics_full',
        'optimizer/pso_optimizer',
        'core/simulation_runner'
    ]

    def __init__(self, coverage_xml: Path):
        """Initialize coverage validator with XML report.

        Args:
            coverage_xml: Path to coverage.xml report from pytest-cov
        """
        self.coverage_xml = coverage_xml
        if not coverage_xml.exists():
            raise FileNotFoundError(f"Coverage XML not found: {coverage_xml}")

        self.tree = ET.parse(coverage_xml)
        self.root = self.tree.getroot()

        # Extract overall metrics
        self.total_lines = int(self.root.get('lines-valid', 0))
        self.covered_lines = int(self.root.get('lines-covered', 0))
        self.overall_coverage = float(self.root.get('line-rate', 0)) * 100

    def get_component_coverage(self, component_patterns: List[str]) -> Tuple[float, Dict[str, float]]:
        """Calculate coverage for components matching patterns.

        Args:
            component_patterns: List of patterns to match component files

        Returns:
            Tuple of (overall_component_coverage, detailed_file_coverage)
        """
        total_lines = 0
        covered_lines = 0
        file_details = {}

        for package in self.root.findall('.//package'):
            for class_elem in package.findall('.//class'):
                filename = class_elem.get('filename', '')

                # Check if file matches any pattern
                if any(pattern in filename for pattern in component_patterns):
                    lines = class_elem.findall('.//line')
                    file_total = len(lines)
                    file_covered = sum(1 for line in lines if int(line.get('hits', 0)) > 0)

                    if file_total > 0:
                        file_coverage = (file_covered / file_total) * 100
                        file_details[filename] = file_coverage

                        total_lines += file_total
                        covered_lines += file_covered

        component_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0.0
        return component_coverage, file_details

    def validate_quality_gates(self) -> Dict[str, Dict]:
        """Validate all quality gate thresholds with detailed analysis.

        Returns:
            Dictionary with validation results for each quality gate
        """
        results = {}

        # Safety-critical components (100% requirement)
        safety_coverage, safety_details = self.get_component_coverage(self.SAFETY_CRITICAL_PATTERNS)
        results['safety_critical'] = {
            'actual': safety_coverage,
            'required': 100.0,
            'passed': safety_coverage >= 100.0,
            'details': safety_details,
            'category': 'SAFETY-CRITICAL'
        }

        # Critical components (95% requirement)
        critical_coverage, critical_details = self.get_component_coverage(self.CRITICAL_COMPONENT_PATTERNS)
        results['critical_components'] = {
            'actual': critical_coverage,
            'required': 95.0,
            'passed': critical_coverage >= 95.0,
            'details': critical_details,
            'category': 'CRITICAL'
        }

        # Overall system (85% requirement)
        results['overall_system'] = {
            'actual': self.overall_coverage,
            'required': 85.0,
            'passed': self.overall_coverage >= 85.0,
            'details': {'total_lines': self.total_lines, 'covered_lines': self.covered_lines},
            'category': 'GENERAL'
        }

        return results

    def calculate_improvement_metrics(self, results: Dict) -> Dict:
        """Calculate mathematical metrics for coverage improvement.

        Args:
            results: Results from validate_quality_gates()

        Returns:
            Dictionary with improvement metrics and recommendations
        """
        metrics = {
            'gaps': {},
            'effort_estimation': {},
            'priority_ranking': []
        }

        for gate_name, gate_data in results.items():
            if not gate_data['passed']:
                gap = gate_data['required'] - gate_data['actual']
                metrics['gaps'][gate_name] = {
                    'percentage_gap': gap,
                    'priority': 'CRITICAL' if gate_data['category'] == 'SAFETY-CRITICAL' else
                               'HIGH' if gate_data['category'] == 'CRITICAL' else 'MEDIUM'
                }

        # Calculate total effort estimation
        total_gap = max(0, 85 - self.overall_coverage)
        estimated_lines_needed = (total_gap / 100) * self.total_lines
        estimated_effort_hours = estimated_lines_needed / 50  # 50 lines per hour average

        metrics['effort_estimation'] = {
            'total_gap_percentage': total_gap,
            'estimated_lines_needed': int(estimated_lines_needed),
            'estimated_effort_hours': int(estimated_effort_hours),
            'estimated_weeks': max(1, int(estimated_effort_hours / 40))
        }

        return metrics

    def generate_coverage_report(self, include_details: bool = True) -> str:
        """Generate comprehensive coverage analysis report.

        Args:
            include_details: Include detailed file-by-file analysis

        Returns:
            Formatted coverage report string
        """
        results = self.validate_quality_gates()
        metrics = self.calculate_improvement_metrics(results)

        report = f"""# Coverage Quality Gate Analysis Report
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Repository**: https://github.com/theSadeQ/dip-smc-pso.git
**Issue**: GitHub Issue #9 - Coverage Analysis Framework

## Executive Summary
| **Quality Gate** | **Actual** | **Required** | **Status** | **Gap** |
|------------------|------------|--------------|------------|---------|
"""

        for gate_name, gate_data in results.items():
            status = "✅ PASS" if gate_data['passed'] else "❌ FAIL"
            gap = gate_data['required'] - gate_data['actual']
            gate_display = gate_name.replace('_', ' ').title()

            report += f"| {gate_display} | {gate_data['actual']:.1f}% | {gate_data['required']:.1f}% | {status} | {gap:+.1f}% |\n"

        # Overall assessment
        overall_pass = all(gate_data['passed'] for gate_data in results.values())
        total_gates = len(results)
        passed_gates = sum(1 for gate_data in results.values() if gate_data['passed'])

        report += f"\n**Overall Assessment**: {passed_gates}/{total_gates} quality gates passed\n"
        report += f"**System Status**: {'✅ PRODUCTION READY' if overall_pass else '❌ PRODUCTION BLOCKED'}\n"

        # Mathematical analysis
        report += f"\n## Mathematical Analysis\n"
        report += f"**Coverage Efficiency**: C_eff = C_achieved/C_target = {self.overall_coverage/85:.3f}\n"
        report += f"**Lines Covered**: {self.covered_lines:,}/{self.total_lines:,}\n"

        if metrics['effort_estimation']['total_gap_percentage'] > 0:
            report += f"**Improvement Required**: {metrics['effort_estimation']['total_gap_percentage']:.1f}%\n"
            report += f"**Estimated Effort**: {metrics['effort_estimation']['estimated_effort_hours']} hours (~{metrics['effort_estimation']['estimated_weeks']} weeks)\n"

        # Detailed component analysis
        if include_details:
            report += f"\n## Component Coverage Details\n"

            for gate_name, gate_data in results.items():
                if gate_data['details'] and isinstance(gate_data['details'], dict):
                    report += f"\n### {gate_name.replace('_', ' ').title()}\n"

                    if gate_name == 'overall_system':
                        report += f"- **Total Lines**: {gate_data['details']['total_lines']:,}\n"
                        report += f"- **Covered Lines**: {gate_data['details']['covered_lines']:,}\n"
                    else:
                        # File-by-file breakdown
                        sorted_files = sorted(gate_data['details'].items(), key=lambda x: x[1])
                        for filename, coverage in sorted_files:
                            status_icon = "✅" if coverage >= gate_data['required'] else "❌"
                            report += f"- {filename}: {coverage:.1f}% {status_icon}\n"

        # Recommendations
        report += f"\n## Improvement Recommendations\n"

        if metrics['gaps']:
            report += f"### Priority Actions\n"

            # Sort by priority
            priority_order = {'CRITICAL': 1, 'HIGH': 2, 'MEDIUM': 3}
            sorted_gaps = sorted(metrics['gaps'].items(),
                               key=lambda x: priority_order.get(x[1]['priority'], 4))

            for gate_name, gap_data in sorted_gaps:
                priority = gap_data['priority']
                gap_pct = gap_data['percentage_gap']

                report += f"\n**{priority} Priority**: {gate_name.replace('_', ' ').title()}\n"
                report += f"- Coverage gap: {gap_pct:.1f}%\n"

                if gate_name == 'safety_critical':
                    report += f"- **Action**: Immediately add tests for safety-critical components\n"
                    report += f"- **Requirement**: 100% coverage mandatory for production\n"
                elif gate_name == 'critical_components':
                    report += f"- **Action**: Enhance controller and dynamics testing\n"
                    report += f"- **Focus**: SMC algorithms, PSO optimization, dynamics models\n"
                else:
                    report += f"- **Action**: Systematic test development for general components\n"
                    report += f"- **Approach**: Incremental improvement to 85% threshold\n"
        else:
            report += "✅ **All quality gates passed!** Maintain current coverage levels and focus on quality improvement.\n"

        # Integration instructions
        report += f"\n## Integration with CLAUDE.md\n"
        report += f"This report aligns with established quality standards:\n"
        report += f"- **Coverage Targets**: 85%/95%/100% thresholds maintained\n"
        report += f"- **Quality Gates**: Automated enforcement in CI/CD pipeline\n"
        report += f"- **Production Readiness**: Coverage directly impacts deployment score\n"

        return report

    def export_json_metrics(self, output_path: Path) -> None:
        """Export coverage metrics to JSON for automation integration."""
        results = self.validate_quality_gates()
        metrics = self.calculate_improvement_metrics(results)

        export_data = {
            'timestamp': datetime.now().isoformat(),
            'repository': 'https://github.com/theSadeQ/dip-smc-pso.git',
            'issue': 'GitHub Issue #9',
            'overall_coverage': self.overall_coverage,
            'quality_gates': results,
            'improvement_metrics': metrics,
            'production_ready': all(gate_data['passed'] for gate_data in results.values())
        }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

def main():
    """Main entry point for coverage validation."""
    parser = argparse.ArgumentParser(description='Coverage Quality Gate Validator for GitHub Issue #9')
    parser.add_argument('--coverage-xml', type=Path, default=Path('coverage.xml'),
                       help='Path to coverage XML report')
    parser.add_argument('--output-report', type=Path, default=Path('coverage_quality_report.md'),
                       help='Output path for coverage report')
    parser.add_argument('--output-json', type=Path, default=Path('coverage_metrics.json'),
                       help='Output path for JSON metrics')
    parser.add_argument('--fail-below-threshold', action='store_true',
                       help='Exit with error code if quality gates fail')
    parser.add_argument('--verbose', action='store_true',
                       help='Include detailed component analysis')

    args = parser.parse_args()

    try:
        # Initialize validator
        validator = CoverageValidator(args.coverage_xml)

        # Generate reports
        report = validator.generate_coverage_report(include_details=args.verbose)

        # Save report
        with open(args.output_report, 'w') as f:
            f.write(report)

        # Export JSON metrics
        validator.export_json_metrics(args.output_json)

        # Validate quality gates
        results = validator.validate_quality_gates()
        failed_gates = [name for name, data in results.items() if not data['passed']]

        # Print summary
        if failed_gates:
            print(f"❌ Coverage quality gates FAILED: {', '.join(failed_gates)}")
            print(f"📊 Current overall coverage: {validator.overall_coverage:.1f}%")
            print(f"📄 Detailed report saved to: {args.output_report}")

            if args.fail_below_threshold:
                sys.exit(1)
        else:
            print("✅ All coverage quality gates PASSED")
            print(f"📊 Overall coverage: {validator.overall_coverage:.1f}%")

        print(f"📈 Metrics exported to: {args.output_json}")

    except Exception as e:
        print(f"❌ Coverage validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()