# Example from: docs\analysis\COVERAGE_ANALYSIS_METHODOLOGY_FRAMEWORK.md
# Index: 2
# Runnable: False
# Hash: 0263578b

# scripts/coverage_gap_analyzer.py
#==========================================================================================\\\
#=============================== coverage_gap_analyzer.py =============================\\\
#==========================================================================================\\\

"""Systematic analysis of coverage gaps with actionable recommendations."""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple

class CoverageGapAnalyzer:
    """Scientific analysis of coverage gaps with improvement recommendations."""

    def analyze_uncovered_lines(self, module_path: str) -> Dict[str, List[int]]:
        """Identify specific uncovered lines in module.

        Args:
            module_path: Path to module for analysis

        Returns:
            Dictionary mapping files to uncovered line numbers
        """
        cmd = ["coverage", "report", "--show-missing", "--include", f"{module_path}/*"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        uncovered_lines = {}
        for line in result.stdout.split('\n')[2:]:  # Skip header
            if line.strip() and not line.startswith('TOTAL'):
                parts = line.split()
                if len(parts) >= 4:
                    file_path = parts[0]
                    missing_lines = parts[-1] if parts[-1] != '100%' else ''
                    if missing_lines and missing_lines != '0':
                        uncovered_lines[file_path] = self.parse_missing_lines(missing_lines)

        return uncovered_lines

    def parse_missing_lines(self, missing_str: str) -> List[int]:
        """Parse missing lines string into list of line numbers."""
        lines = []
        for part in missing_str.split(','):
            if '-' in part:
                start, end = map(int, part.strip().split('-'))
                lines.extend(range(start, end + 1))
            else:
                lines.append(int(part.strip()))
        return lines

    def generate_improvement_plan(self, uncovered_lines: Dict[str, List[int]]) -> str:
        """Generate actionable improvement plan for coverage gaps."""
        plan = "## Coverage Improvement Action Plan\n\n"

        for file_path, lines in uncovered_lines.items():
            plan += f"### {file_path}\n"
            plan += f"**Uncovered Lines**: {len(lines)} lines\n"
            plan += f"**Line Numbers**: {', '.join(map(str, lines[:10]))}"
            if len(lines) > 10:
                plan += f" ... (+{len(lines) - 10} more)"
            plan += "\n\n"

            # Categorize improvement actions
            if 'controller' in file_path:
                plan += "**Recommended Actions**:\n"
                plan += "- Add unit tests for control law computation\n"
                plan += "- Test boundary conditions and saturation limits\n"
                plan += "- Validate stability properties with edge cases\n\n"
            elif 'dynamics' in file_path:
                plan += "**Recommended Actions**:\n"
                plan += "- Test state integration accuracy\n"
                plan += "- Validate physical parameter ranges\n"
                plan += "- Test numerical stability edge cases\n\n"
            elif 'optimizer' in file_path:
                plan += "**Recommended Actions**:\n"
                plan += "- Test convergence scenarios\n"
                plan += "- Validate parameter bounds enforcement\n"
                plan += "- Test optimization termination conditions\n\n"

        return plan

    def prioritize_coverage_tasks(self, uncovered_lines: Dict[str, List[int]]) -> List[Tuple[str, int, str]]:
        """Prioritize coverage improvement tasks by impact."""
        tasks = []

        for file_path, lines in uncovered_lines.items():
            priority = "HIGH"
            if 'safety' in file_path or 'critical' in file_path:
                priority = "CRITICAL"
            elif 'util' in file_path or 'helper' in file_path:
                priority = "MEDIUM"

            tasks.append((file_path, len(lines), priority))

        # Sort by priority and line count
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
        tasks.sort(key=lambda x: (priority_order[x[2]], -x[1]))

        return tasks