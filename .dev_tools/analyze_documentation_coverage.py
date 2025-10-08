#!/usr/bin/env python3
"""
Documentation Coverage vs Type Hint Coverage Analysis

Analyzes Python source files for:
- Missing class docstrings
- Missing method/function docstrings
- Missing parameter documentation
- Missing return documentation
- Type hint coverage (parameters and returns)
- Cross-references with Phase 1.2 findings

Output: Comprehensive JSON + Markdown reports with actionable matrices
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import sys

@dataclass
class TypeHintMetrics:
    """Metrics for type hint coverage in a callable."""
    total_params: int
    annotated_params: int
    has_return_annotation: bool
    coverage_percent: float

@dataclass
class DocstringMetrics:
    """Metrics for docstring quality."""
    has_docstring: bool
    has_parameters_doc: bool
    has_returns_doc: bool
    has_examples: bool
    style: Optional[str]  # "numpy", "google", "sphinx", "unknown"

@dataclass
class ClassMetrics:
    """Complete metrics for a class."""
    module: str
    class_name: str
    line_number: int
    docstring: DocstringMetrics
    type_hints: TypeHintMetrics
    method_count: int
    undocumented_methods: List[str]
    priority: str  # P0, P1, P2, P3

@dataclass
class MethodMetrics:
    """Complete metrics for a method/function."""
    module: str
    class_name: Optional[str]
    method_name: str
    line_number: int
    docstring: DocstringMetrics
    type_hints: TypeHintMetrics
    is_public: bool
    priority: str

@dataclass
class ModuleMetrics:
    """Aggregated metrics for a module."""
    module_path: str
    functions_type_hint_coverage: float
    classes_type_hint_coverage: float
    methods_type_hint_coverage: float
    overall_type_hint_coverage: float
    gap_to_95: float
    undocumented_classes: int
    undocumented_methods: int
    total_classes: int
    total_methods: int

class DocumentationAnalyzer:
    """Analyzes Python files for documentation and type hint coverage."""

    def __init__(self, src_root: Path):
        self.src_root = src_root
        self.all_classes: List[ClassMetrics] = []
        self.all_methods: List[MethodMetrics] = []
        self.module_metrics: Dict[str, ModuleMetrics] = {}

    def analyze_type_hints(self, node: ast.FunctionDef) -> TypeHintMetrics:
        """Analyze type hint coverage for a function/method."""
        args = node.args
        total_params = 0
        annotated_params = 0

        # Count all parameters
        all_args = (
            args.args +
            args.posonlyargs +
            args.kwonlyargs +
            ([args.vararg] if args.vararg else []) +
            ([args.kwarg] if args.kwarg else [])
        )

        for arg in all_args:
            if arg.arg != 'self' and arg.arg != 'cls':
                total_params += 1
                if arg.annotation is not None:
                    annotated_params += 1

        has_return = node.returns is not None
        coverage = (annotated_params / total_params * 100) if total_params > 0 else 100.0

        return TypeHintMetrics(
            total_params=total_params,
            annotated_params=annotated_params,
            has_return_annotation=has_return,
            coverage_percent=coverage
        )

    def analyze_docstring(self, docstring: Optional[str]) -> DocstringMetrics:
        """Analyze docstring quality and style."""
        if not docstring:
            return DocstringMetrics(
                has_docstring=False,
                has_parameters_doc=False,
                has_returns_doc=False,
                has_examples=False,
                style=None
            )

        # Detect style
        style = "unknown"
        if "Parameters\n" in docstring and "----------" in docstring:
            style = "numpy"
        elif "Args:" in docstring:
            style = "google"
        elif ":param" in docstring:
            style = "sphinx"

        # Check for parameter documentation
        has_params = any([
            "Parameters" in docstring,
            "Args:" in docstring,
            ":param" in docstring,
        ])

        # Check for return documentation
        has_returns = any([
            "Returns" in docstring,
            "Return:" in docstring,
            ":return" in docstring,
        ])

        # Check for examples
        has_examples = any([
            "Example" in docstring,
            ">>>" in docstring,
        ])

        return DocstringMetrics(
            has_docstring=True,
            has_parameters_doc=has_params,
            has_returns_doc=has_returns,
            has_examples=has_examples,
            style=style
        )

    def get_priority(self, module: str, name: str, is_class: bool) -> str:
        """Determine priority based on module importance and public API."""
        # P0: Controllers, core simulation, factory patterns
        p0_modules = ['controllers', 'core', 'factory']
        # P1: Plant models, optimization
        p1_modules = ['plant', 'optimization', 'optimizer']
        # P2: Utils, analysis
        p2_modules = ['utils', 'analysis']

        module_lower = module.lower()

        if any(m in module_lower for m in p0_modules):
            return 'P0'
        elif any(m in module_lower for m in p1_modules):
            return 'P1'
        elif any(m in module_lower for m in p2_modules):
            return 'P2'
        else:
            return 'P3'

    def analyze_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=str(file_path))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            return

        module_path = str(file_path.relative_to(self.src_root))

        # Analyze classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, module_path)
            elif isinstance(node, ast.FunctionDef):
                # Top-level functions
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    self._analyze_method(node, module_path, None)

    def _analyze_class(self, node: ast.ClassDef, module_path: str):
        """Analyze a class definition."""
        docstring = ast.get_docstring(node)
        doc_metrics = self.analyze_docstring(docstring)

        # Analyze all methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        undocumented_methods = []

        total_type_hints = []
        for method in methods:
            type_hints = self.analyze_type_hints(method)
            total_type_hints.append(type_hints.coverage_percent)

            method_doc = ast.get_docstring(method)
            if not method_doc and not method.name.startswith('_'):
                undocumented_methods.append(method.name)

            # Record method metrics
            self._analyze_method(method, module_path, node.name)

        # Calculate class type hint coverage
        avg_type_hint = sum(total_type_hints) / len(total_type_hints) if total_type_hints else 0.0

        class_type_hints = TypeHintMetrics(
            total_params=0,
            annotated_params=0,
            has_return_annotation=False,
            coverage_percent=avg_type_hint
        )

        priority = self.get_priority(module_path, node.name, is_class=True)

        class_metrics = ClassMetrics(
            module=module_path,
            class_name=node.name,
            line_number=node.lineno,
            docstring=doc_metrics,
            type_hints=class_type_hints,
            method_count=len(methods),
            undocumented_methods=undocumented_methods,
            priority=priority
        )

        self.all_classes.append(class_metrics)

    def _analyze_method(self, node: ast.FunctionDef, module_path: str, class_name: Optional[str]):
        """Analyze a method or function."""
        docstring = ast.get_docstring(node)
        doc_metrics = self.analyze_docstring(docstring)
        type_hints = self.analyze_type_hints(node)

        is_public = not node.name.startswith('_')
        priority = self.get_priority(module_path, node.name, is_class=False)

        method_metrics = MethodMetrics(
            module=module_path,
            class_name=class_name,
            method_name=node.name,
            line_number=node.lineno,
            docstring=doc_metrics,
            type_hints=type_hints,
            is_public=is_public,
            priority=priority
        )

        self.all_methods.append(method_metrics)

    def calculate_module_metrics(self):
        """Calculate aggregated metrics by module."""
        modules: Dict[str, Dict] = defaultdict(lambda: {
            'functions': [],
            'classes': [],
            'methods': [],
        })

        # Group by module
        for method in self.all_methods:
            module = method.module.split('/')[0] if '/' in method.module else method.module
            if method.class_name is None:
                modules[module]['functions'].append(method.type_hints.coverage_percent)
            else:
                modules[module]['methods'].append(method.type_hints.coverage_percent)

        for cls in self.all_classes:
            module = cls.module.split('/')[0] if '/' in cls.module else cls.module
            modules[module]['classes'].append(cls.type_hints.coverage_percent)

        # Calculate averages
        for module_name, data in modules.items():
            func_coverage = sum(data['functions']) / len(data['functions']) if data['functions'] else 0.0
            class_coverage = sum(data['classes']) / len(data['classes']) if data['classes'] else 0.0
            method_coverage = sum(data['methods']) / len(data['methods']) if data['methods'] else 0.0

            all_coverage = data['functions'] + data['classes'] + data['methods']
            overall = sum(all_coverage) / len(all_coverage) if all_coverage else 0.0

            # Count undocumented
            module_classes = [c for c in self.all_classes if c.module.startswith(module_name)]
            module_methods = [m for m in self.all_methods if m.module.startswith(module_name)]

            undoc_classes = sum(1 for c in module_classes if not c.docstring.has_docstring)
            undoc_methods = sum(1 for m in module_methods if not m.docstring.has_docstring and m.is_public)

            self.module_metrics[module_name] = ModuleMetrics(
                module_path=module_name,
                functions_type_hint_coverage=func_coverage,
                classes_type_hint_coverage=class_coverage,
                methods_type_hint_coverage=method_coverage,
                overall_type_hint_coverage=overall,
                gap_to_95=95.0 - overall,
                undocumented_classes=undoc_classes,
                undocumented_methods=undoc_methods,
                total_classes=len(module_classes),
                total_methods=len([m for m in module_methods if m.is_public])
            )

    def generate_json_report(self, output_path: Path):
        """Generate comprehensive JSON report."""
        report = {
            "metadata": {
                "analysis_date": "2025-10-07",
                "analyzer": "Phase 1.3 Documentation Coverage Analyzer",
                "project": "DIP-SMC-PSO",
                "src_root": str(self.src_root)
            },
            "summary": {
                "total_classes": len(self.all_classes),
                "undocumented_classes": sum(1 for c in self.all_classes if not c.docstring.has_docstring),
                "total_methods": len([m for m in self.all_methods if m.is_public]),
                "undocumented_methods": sum(1 for m in self.all_methods if not m.docstring.has_docstring and m.is_public),
                "overall_type_hint_coverage": self._calculate_overall_type_hint_coverage(),
                "gap_to_95_percent": 95.0 - self._calculate_overall_type_hint_coverage(),
            },
            "undocumented_classes": [
                {
                    "module": c.module,
                    "class": c.class_name,
                    "line": c.line_number,
                    "type_hints_coverage": c.type_hints.coverage_percent,
                    "priority": c.priority,
                    "undocumented_methods_count": len(c.undocumented_methods),
                    "undocumented_methods": c.undocumented_methods
                }
                for c in self.all_classes if not c.docstring.has_docstring
            ],
            "undocumented_methods": [
                {
                    "module": m.module,
                    "class": m.class_name,
                    "method": m.method_name,
                    "line": m.line_number,
                    "has_docstring": m.docstring.has_docstring,
                    "has_returns": m.docstring.has_returns_doc,
                    "type_hints_coverage": m.type_hints.coverage_percent,
                    "priority": m.priority
                }
                for m in self.all_methods if not m.docstring.has_docstring and m.is_public
            ],
            "type_hint_coverage_by_module": {
                module: {
                    "functions": metrics.functions_type_hint_coverage,
                    "classes": metrics.classes_type_hint_coverage,
                    "methods": metrics.methods_type_hint_coverage,
                    "overall": metrics.overall_type_hint_coverage,
                    "gap_to_95": metrics.gap_to_95,
                    "total_classes": metrics.total_classes,
                    "total_methods": metrics.total_methods,
                    "undocumented_classes": metrics.undocumented_classes,
                    "undocumented_methods": metrics.undocumented_methods
                }
                for module, metrics in sorted(self.module_metrics.items())
            },
            "all_classes": [asdict(c) for c in self.all_classes],
            "all_methods": [asdict(m) for m in self.all_methods if m.is_public]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"JSON report written to: {output_path}")

    def _calculate_overall_type_hint_coverage(self) -> float:
        """Calculate overall type hint coverage across all code."""
        all_coverage = []
        for c in self.all_classes:
            all_coverage.append(c.type_hints.coverage_percent)
        for m in self.all_methods:
            all_coverage.append(m.type_hints.coverage_percent)

        return sum(all_coverage) / len(all_coverage) if all_coverage else 0.0

    def generate_markdown_report(self, output_path: Path):
        """Generate comprehensive Markdown report."""
        overall_coverage = self._calculate_overall_type_hint_coverage()
        total_classes = len(self.all_classes)
        undoc_classes = sum(1 for c in self.all_classes if not c.docstring.has_docstring)
        total_methods = len([m for m in self.all_methods if m.is_public])
        undoc_methods = sum(1 for m in self.all_methods if not m.docstring.has_docstring and m.is_public)

        lines = [
            "# Documentation Coverage Matrix",
            "",
            f"**Analysis Date:** 2025-10-07",
            f"**Analyzer:** Phase 1.3 Documentation Coverage Analyzer",
            "",
            "## Executive Summary",
            "",
            f"- **Total Classes:** {total_classes}",
            f"- **Undocumented Classes:** {undoc_classes} ({undoc_classes/total_classes*100:.1f}%)" if total_classes > 0 else "- **Undocumented Classes:** 0",
            f"- **Total Public Methods:** {total_methods}",
            f"- **Undocumented Public Methods:** {undoc_methods} ({undoc_methods/total_methods*100:.1f}%)" if total_methods > 0 else "- **Undocumented Public Methods:** 0",
            f"- **Type Hint Coverage:** {overall_coverage:.1f}% (target: 95%, gap: {95.0 - overall_coverage:.1f}%)",
            "",
            "## A. Undocumented Classes (Target: 0)",
            "",
            "| Module | Class | Has Docstring | Has Parameters Doc | Type Hints % | Priority |",
            "|--------|-------|---------------|-------------------|--------------|----------|",
        ]

        # Undocumented classes sorted by priority
        undoc_classes_list = [c for c in self.all_classes if not c.docstring.has_docstring]
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        undoc_classes_list.sort(key=lambda c: (priority_order.get(c.priority, 4), c.module, c.class_name))

        for cls in undoc_classes_list:
            lines.append(
                f"| {cls.module} | {cls.class_name} | ❌ | ❌ | {cls.type_hints.coverage_percent:.0f}% | {cls.priority} |"
            )

        if not undoc_classes_list:
            lines.append("| - | - | - | - | - | - |")
            lines.append("| *All classes documented* | | | | | |")

        lines.extend([
            "",
            "## B. Undocumented Methods (Target: 0)",
            "",
            "| Module | Class | Method | Has Docstring | Has Returns | Type Hints % | Priority |",
            "|--------|-------|--------|---------------|-------------|--------------|----------|",
        ])

        # Undocumented methods sorted by priority
        undoc_methods_list = [m for m in self.all_methods if not m.docstring.has_docstring and m.is_public]
        undoc_methods_list.sort(key=lambda m: (priority_order.get(m.priority, 4), m.module, m.class_name or '', m.method_name))

        # Limit to top 50 for readability
        for method in undoc_methods_list[:50]:
            class_col = method.class_name if method.class_name else "(module-level)"
            has_returns = "✅" if method.docstring.has_returns_doc else "❌"
            lines.append(
                f"| {method.module} | {class_col} | {method.method_name} | ❌ | {has_returns} | {method.type_hints.coverage_percent:.0f}% | {method.priority} |"
            )

        if len(undoc_methods_list) > 50:
            lines.append(f"| ... | ... | ... | ... | ... | ... | ... |")
            lines.append(f"| *{len(undoc_methods_list) - 50} more undocumented methods* | | | | | | |")

        if not undoc_methods_list:
            lines.append("| - | - | - | - | - | - | - |")
            lines.append("| *All public methods documented* | | | | | | |")

        lines.extend([
            "",
            "## C. Type Hint Coverage by Module (Target: 95%+)",
            "",
            "| Module | Functions | Classes | Methods | Overall % | Gap to 95% |",
            "|--------|-----------|---------|---------|-----------|------------|",
        ])

        # Sort by overall coverage (worst first)
        sorted_modules = sorted(self.module_metrics.items(), key=lambda x: x[1].overall_type_hint_coverage)

        for module, metrics in sorted_modules:
            lines.append(
                f"| {module} | {metrics.functions_type_hint_coverage:.0f}% | "
                f"{metrics.classes_type_hint_coverage:.0f}% | "
                f"{metrics.methods_type_hint_coverage:.0f}% | "
                f"{metrics.overall_type_hint_coverage:.0f}% | "
                f"{metrics.gap_to_95:.0f}% |"
            )

        lines.extend([
            "",
            "## D. Critical Gaps (P0)",
            "",
            "### Undocumented Classes (P0)",
            ""
        ])

        p0_classes = [c for c in undoc_classes_list if c.priority == 'P0']
        if p0_classes:
            for i, cls in enumerate(p0_classes, 1):
                lines.extend([
                    f"{i}. **{cls.module}:{cls.class_name}**",
                    f"   - Impact: High (priority P0)",
                    f"   - Effort: 30 minutes",
                    f"   - Type Hints: {cls.type_hints.coverage_percent:.0f}% coverage",
                    f"   - Line: {cls.line_number}",
                    ""
                ])
        else:
            lines.append("*No P0 undocumented classes*")
            lines.append("")

        lines.extend([
            "### Undocumented Methods (P0 - Top 20)",
            ""
        ])

        p0_methods = [m for m in undoc_methods_list if m.priority == 'P0'][:20]
        if p0_methods:
            for i, method in enumerate(p0_methods, 1):
                class_name = f"{method.class_name}." if method.class_name else ""
                lines.extend([
                    f"{i}. **{method.module}:{class_name}{method.method_name}**",
                    f"   - Impact: High (priority P0)",
                    f"   - Type Hints: {method.type_hints.coverage_percent:.0f}% coverage",
                    f"   - Line: {method.line_number}",
                    ""
                ])
        else:
            lines.append("*No P0 undocumented methods*")
            lines.append("")

        lines.extend([
            "## Implementation Plan",
            "",
            "### Phase 1: Critical Classes (Week 1)",
            f"- Document {len(p0_classes)} P0 priority classes",
            "- Estimated effort: 14 hours",
            "",
            "### Phase 2: Type Hints (Weeks 2-3)",
            "- Module-by-module type hint completion",
            "- Estimated effort: TBD based on gap analysis",
            "",
            "### Phase 3: Method Documentation (Month 2)",
            f"- Document {len(undoc_methods_list)} public methods",
            "- Focus on public APIs first",
            "",
            "## Quality Gates",
            "",
            "- [ ] 0 undocumented public classes",
            "- [ ] <5% undocumented public methods",
            "- [ ] 95%+ type hint coverage",
            "- [ ] All examples pass pytest validation",
            ""
        ])

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"Markdown report written to: {output_path}")


def main():
    """Main entry point."""
    src_root = Path(__file__).parent.parent / 'src'

    if not src_root.exists():
        print(f"Error: Source root not found: {src_root}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing source files in: {src_root}")

    analyzer = DocumentationAnalyzer(src_root)

    # Find all Python files
    python_files = list(src_root.rglob('*.py'))
    print(f"Found {len(python_files)} Python files")

    # Analyze each file
    for i, file_path in enumerate(python_files, 1):
        print(f"[{i}/{len(python_files)}] Analyzing: {file_path.relative_to(src_root)}", end='\r')
        analyzer.analyze_file(file_path)

    print("\n\nCalculating module metrics...")
    analyzer.calculate_module_metrics()

    # Generate reports
    docs_dir = Path(__file__).parent.parent / 'docs'
    json_output = docs_dir / 'DOCUMENTATION_COVERAGE_MATRIX.json'
    md_output = docs_dir / 'DOCUMENTATION_COVERAGE_MATRIX.md'

    print("\nGenerating reports...")
    analyzer.generate_json_report(json_output)
    analyzer.generate_markdown_report(md_output)

    print("\n✅ Phase 1.3 Analysis Complete!")
    print(f"\nReports generated:")
    print(f"  - JSON: {json_output}")
    print(f"  - Markdown: {md_output}")


if __name__ == '__main__':
    main()
