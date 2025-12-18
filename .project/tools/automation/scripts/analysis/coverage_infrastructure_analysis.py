#======================================================================================\\\
#======================== coverage_infrastructure_analysis.py =========================\\\
#======================================================================================\\\

"""
Coverage Infrastructure Analysis for GitHub Issue #9
Analyzes current coverage gaps and generates strategic improvement plan.
"""

import subprocess
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

class CoverageInfrastructureAnalyzer:
    """Comprehensive coverage infrastructure analysis."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.tests_dir = self.project_root / "tests"

    def analyze_module_coverage(self, module_path: str, timeout: int = 30) -> Dict:
        """Analyze coverage for a specific module."""
        try:
            cmd = [
                sys.executable, '-m', 'pytest',
                f'tests/test_{module_path.replace("/", "_")}/',
                f'--cov=src/{module_path}',
                '--cov-report=xml:temp_coverage.xml',
                '--cov-report=term-missing',
                '--tb=no', '-q', '--disable-warnings'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            coverage_data = {
                'module': module_path,
                'exit_code': result.returncode,
                'has_tests': True,
                'coverage_percentage': 0,
                'lines_covered': 0,
                'lines_total': 0,
                'missing_lines': []
            }

            # Parse coverage from XML if available
            if os.path.exists('temp_coverage.xml'):
                coverage_data.update(self._parse_coverage_xml('temp_coverage.xml'))
                os.remove('temp_coverage.xml')

            return coverage_data

        except subprocess.TimeoutExpired:
            return {
                'module': module_path,
                'error': 'timeout',
                'has_tests': True,
                'coverage_percentage': 0
            }
        except Exception as e:
            return {
                'module': module_path,
                'error': str(e),
                'has_tests': False,
                'coverage_percentage': 0
            }

    def _parse_coverage_xml(self, xml_file: str) -> Dict:
        """Parse coverage data from XML file."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            total_lines = int(root.attrib.get('lines-valid', 0))
            covered_lines = int(root.attrib.get('lines-covered', 0))
            coverage_percent = (covered_lines / total_lines * 100) if total_lines > 0 else 0

            return {
                'coverage_percentage': round(coverage_percent, 2),
                'lines_covered': covered_lines,
                'lines_total': total_lines
            }
        except Exception:
            return {}

    def find_untested_modules(self) -> List[str]:
        """Find modules without corresponding tests."""
        untested = []

        for py_file in self.src_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            rel_path = py_file.relative_to(self.src_dir)
            module_path = str(rel_path.with_suffix(''))

            # Check if corresponding test exists
            test_patterns = [
                self.tests_dir / f"test_{module_path.replace('/', '_')}.py",
                self.tests_dir / f"test_{rel_path.parent}" / f"test_{py_file.stem}.py",
                self.tests_dir / rel_path.parent / f"test_{py_file.stem}.py"
            ]

            has_test = any(pattern.exists() for pattern in test_patterns)
            if not has_test:
                untested.append(module_path)

        return untested

    def analyze_large_modules(self) -> List[Tuple[str, int]]:
        """Identify large modules that need coverage attention."""
        large_modules = []

        for py_file in self.src_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            try:
                line_count = len(py_file.read_text(encoding='utf-8').splitlines())
                if line_count > 200:  # Focus on substantial modules
                    rel_path = py_file.relative_to(self.src_dir)
                    module_path = str(rel_path.with_suffix(''))
                    large_modules.append((module_path, line_count))
            except Exception:
                continue

        return sorted(large_modules, key=lambda x: x[1], reverse=True)

    def generate_coverage_strategy(self) -> Dict:
        """Generate strategic coverage improvement plan."""
        untested_modules = self.find_untested_modules()
        large_modules = self.analyze_large_modules()

        # Prioritize by impact
        high_impact_targets = []
        medium_impact_targets = []
        low_impact_targets = []

        for module, lines in large_modules[:10]:  # Top 10 largest
            if module in untested_modules:
                high_impact_targets.append({'module': module, 'lines': lines, 'reason': 'large_untested'})
            else:
                medium_impact_targets.append({'module': module, 'lines': lines, 'reason': 'large_undertested'})

        for module in untested_modules:
            if not any(t['module'] == module for t in high_impact_targets):
                low_impact_targets.append({'module': module, 'reason': 'untested'})

        return {
            'high_impact_targets': high_impact_targets,
            'medium_impact_targets': medium_impact_targets,
            'low_impact_targets': low_impact_targets[:20],  # Limit for focus
            'total_untested': len(untested_modules),
            'total_large_modules': len(large_modules)
        }

    def run_quick_coverage_assessment(self) -> Dict:
        """Run quick coverage assessment on key modules."""
        key_modules = [
            'controllers',
            'optimization',
            'simulation',
            'core',
            'plant',
            'utils'
        ]

        results = {}
        for module in key_modules:
            print(f"Analyzing {module} coverage...")
            results[module] = self.analyze_module_coverage(module, timeout=20)

        return results

def main():
    """Main coverage infrastructure analysis."""
    analyzer = CoverageInfrastructureAnalyzer()

    print("="*80)
    print("COVERAGE INFRASTRUCTURE ANALYSIS - GitHub Issue #9")
    print("="*80)

    # 1. Quick assessment
    print("\n1. QUICK COVERAGE ASSESSMENT")
    print("-" * 40)
    coverage_results = analyzer.run_quick_coverage_assessment()

    total_coverage = 0
    valid_modules = 0

    for module, data in coverage_results.items():
        if 'coverage_percentage' in data and not data.get('error'):
            print(f"{module:15}: {data['coverage_percentage']:6.1f}% coverage")
            total_coverage += data['coverage_percentage']
            valid_modules += 1
        else:
            print(f"{module:15}: ERROR - {data.get('error', 'unknown')}")

    avg_coverage = total_coverage / valid_modules if valid_modules > 0 else 0
    print(f"\nAverage Coverage: {avg_coverage:.1f}%")

    # 2. Coverage strategy
    print("\n2. COVERAGE IMPROVEMENT STRATEGY")
    print("-" * 40)
    strategy = analyzer.generate_coverage_strategy()

    print(f"High Impact Targets ({len(strategy['high_impact_targets'])}):")
    for target in strategy['high_impact_targets']:
        print(f"  - {target['module']} ({target['lines']} lines) - {target['reason']}")

    print(f"\nMedium Impact Targets ({len(strategy['medium_impact_targets'])}):")
    for target in strategy['medium_impact_targets'][:5]:  # Top 5
        print(f"  - {target['module']} ({target['lines']} lines) - {target['reason']}")

    print(f"\nTotal Untested Modules: {strategy['total_untested']}")
    print(f"Total Large Modules (>200 lines): {strategy['total_large_modules']}")

    # 3. Coverage gap analysis
    print("\n3. COVERAGE GAP ANALYSIS")
    print("-" * 40)

    gap_to_85 = max(0, 85 - avg_coverage)
    gap_to_95 = max(0, 95 - avg_coverage)

    print(f"Gap to 85% target: {gap_to_85:.1f} percentage points")
    print(f"Gap to 95% target: {gap_to_95:.1f} percentage points")

    # Estimate lines needed
    total_src_lines = sum(len(f.read_text(encoding='utf-8').splitlines())
                         for f in Path('src').rglob("*.py")
                         if f.name != "__init__.py")

    current_covered_lines = int(total_src_lines * avg_coverage / 100)
    lines_for_85 = int(total_src_lines * 0.85) - current_covered_lines
    lines_for_95 = int(total_src_lines * 0.95) - current_covered_lines

    print(f"Estimated lines to cover for 85%: {lines_for_85}")
    print(f"Estimated lines to cover for 95%: {lines_for_95}")

    # 4. Recommendations
    print("\n4. RECOMMENDATIONS")
    print("-" * 40)
    print("Priority Actions:")
    print("1. Add pytest-cov to requirements.txt")
    print("2. Create coverage configuration (.coveragerc)")
    print("3. Focus on high-impact targets first")
    print("4. Implement quality gates in CI/CD")
    print("5. Set up coverage regression detection")

    # Save results
    report = {
        'coverage_results': coverage_results,
        'strategy': strategy,
        'metrics': {
            'average_coverage': avg_coverage,
            'gap_to_85': gap_to_85,
            'gap_to_95': gap_to_95,
            'lines_for_85': lines_for_85,
            'lines_for_95': lines_for_95
        }
    }

    with open('coverage_infrastructure_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: coverage_infrastructure_report.json")

    return avg_coverage >= 85  # Return success if meeting target

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)