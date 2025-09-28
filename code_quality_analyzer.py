#!/usr/bin/env python3
"""
Code Quality Analyzer for DIP SMC PSO Project

This script performs comprehensive code quality analysis including:
1. Import statement analysis and optimization
2. Type hint coverage assessment
3. Unused import detection
4. Code complexity analysis
5. Production readiness assessment
"""

import ast
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Union
import json


class ImportAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze import statements and usage."""

    def __init__(self):
        self.imports = set()
        self.from_imports = defaultdict(set)
        self.used_names = set()
        self.function_defs = []
        self.class_defs = []
        self.type_hints = 0
        self.functions_without_hints = []
        self.functions_with_hints = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ''
        for alias in node.names:
            self.from_imports[module].add(alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.function_defs.append(node.name)

        # Check type hints
        has_return_hint = node.returns is not None
        has_param_hints = any(arg.annotation is not None for arg in node.args.args)

        if has_return_hint or has_param_hints:
            self.functions_with_hints.append(node.name)
            self.type_hints += 1
        else:
            # Exclude special methods from type hint requirements
            if not (node.name.startswith('__') and node.name.endswith('__')):
                self.functions_without_hints.append(node.name)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.class_defs.append(node.name)
        self.generic_visit(node)


class CodeQualityAnalyzer:
    """Comprehensive code quality analyzer."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results = {
            'ascii_headers': {},
            'imports': {},
            'type_hints': {},
            'code_complexity': {},
            'unused_imports': {},
            'production_issues': []
        }

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content, filename=str(file_path))

            # Analyze imports and type hints
            analyzer = ImportAnalyzer()
            analyzer.visit(tree)

            # Check ASCII header
            lines = content.split('\n')
            has_ascii_header = (len(lines) >= 3 and
                              lines[0].startswith('#=') and
                              lines[2].startswith('#='))

            # Calculate header width
            header_width = len(lines[0]) if has_ascii_header else 0

            # Import analysis
            all_imported = set()
            for imp in analyzer.imports:
                all_imported.add(imp.split('.')[0])
            for module, names in analyzer.from_imports.items():
                for name in names:
                    all_imported.add(name)

            unused_imports = all_imported - analyzer.used_names

            # Type hint coverage
            total_functions = len(analyzer.function_defs)
            functions_with_hints = len(analyzer.functions_with_hints)
            coverage_percentage = (functions_with_hints / total_functions * 100) if total_functions > 0 else 100

            # Code complexity (simple line count analysis)
            lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('#')])

            return {
                'path': str(file_path.relative_to(self.project_root)),
                'ascii_header': {
                    'present': has_ascii_header,
                    'width': header_width,
                    'compliant': header_width == 95  # 90 chars + \\\
                },
                'imports': {
                    'total_imports': len(all_imported),
                    'unused_imports': list(unused_imports),
                    'unused_count': len(unused_imports)
                },
                'type_hints': {
                    'total_functions': total_functions,
                    'functions_with_hints': functions_with_hints,
                    'functions_without_hints': analyzer.functions_without_hints,
                    'coverage_percentage': coverage_percentage
                },
                'complexity': {
                    'lines_of_code': lines_of_code,
                    'function_count': len(analyzer.function_defs),
                    'class_count': len(analyzer.class_defs)
                },
                'quality_score': self._calculate_quality_score(
                    has_ascii_header, coverage_percentage, len(unused_imports), lines_of_code
                )
            }

        except Exception as e:
            return {
                'path': str(file_path.relative_to(self.project_root)),
                'error': str(e),
                'quality_score': 0
            }

    def _calculate_quality_score(self, has_ascii_header: bool, type_coverage: float,
                               unused_imports: int, lines_of_code: int) -> float:
        """Calculate overall quality score (0-100)."""
        score = 0.0

        # ASCII header (20 points)
        if has_ascii_header:
            score += 20

        # Type hint coverage (40 points)
        score += (type_coverage / 100) * 40

        # Import cleanliness (20 points)
        if unused_imports == 0:
            score += 20
        elif unused_imports <= 2:
            score += 10

        # Code size penalty (20 points)
        if lines_of_code <= 100:
            score += 20
        elif lines_of_code <= 300:
            score += 15
        elif lines_of_code <= 500:
            score += 10
        else:
            score += 5

        return min(100.0, score)

    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the entire project."""
        print("Starting comprehensive code quality analysis...")

        # Find all Python files
        src_files = list(self.project_root.glob('src/**/*.py'))
        test_files = list(self.project_root.glob('tests/**/*.py'))
        root_files = list(self.project_root.glob('*.py'))

        all_files = src_files + test_files + root_files

        print(f"Found {len(all_files)} Python files to analyze")

        file_results = []
        for file_path in all_files:
            if file_path.name.startswith('.'):
                continue
            result = self.analyze_file(file_path)
            file_results.append(result)

        # Aggregate results
        summary = self._generate_summary(file_results)

        return {
            'summary': summary,
            'files': file_results,
            'recommendations': self._generate_recommendations(summary)
        }

    def _generate_summary(self, file_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics."""
        valid_files = [f for f in file_results if 'error' not in f]

        # ASCII header compliance
        ascii_compliant = sum(1 for f in valid_files if f.get('ascii_header', {}).get('compliant', False))
        ascii_present = sum(1 for f in valid_files if f.get('ascii_header', {}).get('present', False))

        # Type hint coverage
        total_functions = sum(f.get('type_hints', {}).get('total_functions', 0) for f in valid_files)
        functions_with_hints = sum(f.get('type_hints', {}).get('functions_with_hints', 0) for f in valid_files)
        overall_type_coverage = (functions_with_hints / total_functions * 100) if total_functions > 0 else 100

        # Import analysis
        total_unused_imports = sum(f.get('imports', {}).get('unused_count', 0) for f in valid_files)
        files_with_unused = sum(1 for f in valid_files if f.get('imports', {}).get('unused_count', 0) > 0)

        # Quality scores
        quality_scores = [f.get('quality_score', 0) for f in valid_files if 'error' not in f]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        return {
            'total_files': len(valid_files),
            'ascii_headers': {
                'compliant': ascii_compliant,
                'present': ascii_present,
                'compliance_rate': (ascii_compliant / len(valid_files) * 100) if valid_files else 0
            },
            'type_hints': {
                'total_functions': total_functions,
                'functions_with_hints': functions_with_hints,
                'coverage_percentage': overall_type_coverage
            },
            'imports': {
                'total_unused_imports': total_unused_imports,
                'files_with_unused': files_with_unused,
                'clean_import_rate': ((len(valid_files) - files_with_unused) / len(valid_files) * 100) if valid_files else 100
            },
            'quality': {
                'average_score': avg_quality_score,
                'files_above_80': sum(1 for score in quality_scores if score >= 80),
                'files_below_60': sum(1 for score in quality_scores if score < 60)
            }
        }

    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # ASCII headers
        if summary['ascii_headers']['compliance_rate'] < 100:
            recommendations.append(
                f"Fix ASCII headers: {summary['ascii_headers']['compliant']}/{summary['total_files']} "
                f"files have compliant 90-character headers"
            )

        # Type hints
        if summary['type_hints']['coverage_percentage'] < 95:
            recommendations.append(
                f"Improve type hint coverage: Currently {summary['type_hints']['coverage_percentage']:.1f}%, "
                f"target is 95%"
            )

        # Unused imports
        if summary['imports']['total_unused_imports'] > 0:
            recommendations.append(
                f"Remove {summary['imports']['total_unused_imports']} unused imports across "
                f"{summary['imports']['files_with_unused']} files"
            )

        # Overall quality
        if summary['quality']['average_score'] < 80:
            recommendations.append(
                f"Improve overall code quality: Average score {summary['quality']['average_score']:.1f}/100, "
                f"target is 80+"
            )

        return recommendations

    def save_results(self, output_file: str = "code_quality_analysis.json"):
        """Save analysis results to file."""
        results = self.analyze_project()

        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Analysis results saved to: {output_path}")
        return results


def main():
    """Main function."""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()

    analyzer = CodeQualityAnalyzer(project_root)
    results = analyzer.save_results()

    # Print summary
    summary = results['summary']
    print("\n" + "="*60)
    print("CODE QUALITY ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total files analyzed: {summary['total_files']}")
    print(f"ASCII header compliance: {summary['ascii_headers']['compliance_rate']:.1f}%")
    print(f"Type hint coverage: {summary['type_hints']['coverage_percentage']:.1f}%")
    print(f"Clean import rate: {summary['imports']['clean_import_rate']:.1f}%")
    print(f"Average quality score: {summary['quality']['average_score']:.1f}/100")

    print("\nRECOMMENDATIONS:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec}")

    print("\nPRODUCTION READINESS ASSESSMENT:")
    if summary['quality']['average_score'] >= 80:
        print("✅ READY FOR PRODUCTION - High code quality standards met")
    elif summary['quality']['average_score'] >= 70:
        print("⚠️  NEEDS MINOR IMPROVEMENTS - Good quality with room for improvement")
    else:
        print("❌ NOT PRODUCTION READY - Significant quality issues need addressing")


if __name__ == "__main__":
    main()