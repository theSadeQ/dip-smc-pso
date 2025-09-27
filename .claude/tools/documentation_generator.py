#==========================================================================================\\\
#========================= .claude/tools/documentation_generator.py =====================\\\
#==========================================================================================\\\

"""
Documentation Generator Tool for DIP_SMC_PSO Project

Automated documentation generation utilities for the Documentation Expert Agent.
Supports API documentation, user guides, mathematical notation, and integration
with the existing multi-agent orchestration system.
"""

import os
import re
import ast
import inspect
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

import numpy as np
try:
    import yaml
except ImportError:
    yaml = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentationType(Enum):
    """Types of documentation that can be generated."""
    API_REFERENCE = "api_reference"
    USER_GUIDE = "user_guide"
    DEVELOPER_GUIDE = "developer_guide"
    THEORY_DOCUMENTATION = "theory_documentation"
    INTEGRATION_GUIDE = "integration_guide"


@dataclass
class DocumentationConfig:
    """Configuration for documentation generation."""
    project_root: Path
    source_dirs: List[Path]
    output_dir: Path
    include_private: bool = False
    generate_examples: bool = True
    mathematical_notation: bool = True
    cross_references: bool = True

    def __post_init__(self):
        """Validate configuration."""
        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {self.project_root}")

        for source_dir in self.source_dirs:
            if not (self.project_root / source_dir).exists():
                logger.warning(f"Source directory not found: {source_dir}")


class PythonAnalyzer:
    """Analyzes Python source code for documentation generation."""

    def __init__(self, config: DocumentationConfig):
        self.config = config
        self.modules: Dict[str, ast.Module] = {}
        self.docstrings: Dict[str, str] = {}
        self.type_hints: Dict[str, Dict[str, Any]] = {}

    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the entire project structure."""
        logger.info("Starting project analysis...")

        analysis = {
            "modules": {},
            "classes": {},
            "functions": {},
            "dependencies": set(),
            "structure": self._analyze_structure()
        }

        for source_dir in self.config.source_dirs:
            source_path = self.config.project_root / source_dir
            if source_path.exists():
                self._analyze_directory(source_path, analysis)

        logger.info(f"Analysis complete. Found {len(analysis['modules'])} modules")
        return analysis

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze project directory structure."""
        structure = {
            "src_directories": [],
            "test_directories": [],
            "docs_directories": [],
            "config_files": [],
            "main_scripts": []
        }

        for item in self.config.project_root.iterdir():
            if item.is_dir():
                if item.name.startswith('.'):
                    continue
                elif item.name in ['src', 'lib', 'package']:
                    structure["src_directories"].append(str(item.relative_to(self.config.project_root)))
                elif item.name in ['tests', 'test']:
                    structure["test_directories"].append(str(item.relative_to(self.config.project_root)))
                elif item.name in ['docs', 'documentation']:
                    structure["docs_directories"].append(str(item.relative_to(self.config.project_root)))
            elif item.is_file():
                if item.suffix == '.py' and not item.name.startswith('_'):
                    structure["main_scripts"].append(str(item.relative_to(self.config.project_root)))
                elif item.suffix in ['.yaml', '.yml', '.json', '.toml']:
                    structure["config_files"].append(str(item.relative_to(self.config.project_root)))

        return structure

    def _analyze_directory(self, directory: Path, analysis: Dict[str, Any]) -> None:
        """Recursively analyze a directory for Python files."""
        for item in directory.rglob("*.py"):
            if item.name.startswith('_') and not self.config.include_private:
                continue

            try:
                module_info = self._analyze_module(item)
                relative_path = str(item.relative_to(self.config.project_root))
                analysis["modules"][relative_path] = module_info

                # Extract classes and functions for cross-referencing
                for class_name, class_info in module_info.get("classes", {}).items():
                    full_name = f"{relative_path}::{class_name}"
                    analysis["classes"][full_name] = class_info

                for func_name, func_info in module_info.get("functions", {}).items():
                    full_name = f"{relative_path}::{func_name}"
                    analysis["functions"][full_name] = func_info

            except Exception as e:
                logger.warning(f"Failed to analyze {item}: {e}")

    def _analyze_module(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python module."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            return {}

        module_info = {
            "path": str(file_path),
            "docstring": ast.get_docstring(tree),
            "imports": self._extract_imports(tree),
            "classes": {},
            "functions": {},
            "constants": {},
            "has_ascii_header": self._check_ascii_header(content)
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                module_info["classes"][node.name] = self._analyze_class(node)
            elif isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_') or self.config.include_private:
                    module_info["functions"][node.name] = self._analyze_function(node)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        module_info["constants"][target.id] = self._get_constant_value(node.value)

        return module_info

    def _analyze_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Analyze a class definition."""
        class_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "bases": [self._get_name(base) for base in node.bases],
            "methods": {},
            "properties": {},
            "decorators": [self._get_name(dec) for dec in node.decorator_list]
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith('_') or self.config.include_private or item.name in ['__init__', '__call__']:
                    class_info["methods"][item.name] = self._analyze_function(item)
            elif isinstance(item, ast.AsyncFunctionDef):
                if not item.name.startswith('_') or self.config.include_private:
                    method_info = self._analyze_function(item)
                    method_info["is_async"] = True
                    class_info["methods"][item.name] = method_info

        return class_info

    def _analyze_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Analyze a function definition."""
        func_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "args": self._extract_arguments(node),
            "returns": self._get_return_annotation(node),
            "decorators": [self._get_name(dec) for dec in node.decorator_list],
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "has_mathematical_content": self._has_mathematical_content(ast.get_docstring(node) or "")
        }

        return func_info

    def _extract_arguments(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract function arguments with type hints."""
        args = []

        # Regular arguments
        for i, arg in enumerate(node.args.args):
            arg_info = {
                "name": arg.arg,
                "type": self._get_annotation(arg.annotation),
                "has_default": i >= len(node.args.args) - len(node.args.defaults),
                "default": None
            }

            if arg_info["has_default"]:
                default_index = i - (len(node.args.args) - len(node.args.defaults))
                if default_index >= 0:
                    arg_info["default"] = self._get_default_value(node.args.defaults[default_index])

            args.append(arg_info)

        # *args
        if node.args.vararg:
            args.append({
                "name": f"*{node.args.vararg.arg}",
                "type": self._get_annotation(node.args.vararg.annotation),
                "is_vararg": True
            })

        # **kwargs
        if node.args.kwarg:
            args.append({
                "name": f"**{node.args.kwarg.arg}",
                "type": self._get_annotation(node.args.kwarg.annotation),
                "is_kwarg": True
            })

        return args

    def _extract_imports(self, tree: ast.Module) -> List[Dict[str, Any]]:
        """Extract import statements."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname
                    })

        return imports

    def _check_ascii_header(self, content: str) -> bool:
        """Check if file has the expected ASCII header format."""
        lines = content.split('\n')[:5]
        header_pattern = r'^#={80,}\\\\\\$'

        for line in lines:
            if re.match(header_pattern, line.strip()):
                return True

        return False

    def _has_mathematical_content(self, docstring: str) -> bool:
        """Check if docstring contains mathematical notation."""
        if not docstring:
            return False

        math_indicators = [
            r'\$.*\$',  # LaTeX inline math
            r'\\[.*\\]',  # LaTeX display math
            r'\\begin\{.*\}',  # LaTeX environments
            r'θ|φ|λ|Δ|∑|∏|∫|∂',  # Greek letters and math symbols
            r'α|β|γ|δ|ε|ζ|η|κ|μ|ν|π|ρ|σ|τ|ω|Ω',  # More Greek letters
            r'x₁|x₂|y₁|y₂|f₁|f₂',  # Subscripts
            r'x²|x³|y²|f²',  # Superscripts
        ]

        for pattern in math_indicators:
            if re.search(pattern, docstring):
                return True

        return False

    def _get_name(self, node) -> Optional[str]:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return None

    def _get_annotation(self, annotation) -> Optional[str]:
        """Get type annotation as string."""
        if annotation is None:
            return None
        return self._get_name(annotation)

    def _get_return_annotation(self, node: ast.FunctionDef) -> Optional[str]:
        """Get return type annotation."""
        if node.returns:
            return self._get_annotation(node.returns)
        return None

    def _get_default_value(self, node) -> Any:
        """Get default value from AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.List):
            return [self._get_default_value(elt) for elt in node.elts]
        return str(node)

    def _get_constant_value(self, node) -> Any:
        """Get constant value from assignment."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return node.id
        return None


class DocumentationGenerator:
    """Main documentation generator class."""

    def __init__(self, config: DocumentationConfig):
        self.config = config
        self.analyzer = PythonAnalyzer(config)
        self.project_analysis: Optional[Dict[str, Any]] = None

    def generate_documentation(self, doc_type: DocumentationType, **kwargs) -> Path:
        """Generate documentation of specified type."""
        logger.info(f"Generating {doc_type.value} documentation...")

        if self.project_analysis is None:
            self.project_analysis = self.analyzer.analyze_project()

        # Ensure output directory exists
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if doc_type == DocumentationType.API_REFERENCE:
            return self._generate_api_reference(**kwargs)
        elif doc_type == DocumentationType.USER_GUIDE:
            return self._generate_user_guide(**kwargs)
        elif doc_type == DocumentationType.DEVELOPER_GUIDE:
            return self._generate_developer_guide(**kwargs)
        elif doc_type == DocumentationType.THEORY_DOCUMENTATION:
            return self._generate_theory_documentation(**kwargs)
        elif doc_type == DocumentationType.INTEGRATION_GUIDE:
            return self._generate_integration_guide(**kwargs)
        else:
            raise ValueError(f"Unsupported documentation type: {doc_type}")

    def _generate_api_reference(self, **kwargs) -> Path:
        """Generate comprehensive API reference documentation."""
        output_file = self.config.output_dir / "api_reference.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# API Reference\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Project Overview\n\n")
            f.write("This API reference provides comprehensive documentation for all public classes, methods, and functions in the DIP_SMC_PSO project.\n\n")

            # Table of contents
            f.write("## Table of Contents\n\n")
            for module_path in sorted(self.project_analysis["modules"].keys()):
                module_name = module_path.replace('/', '.').replace('.py', '')
                f.write(f"- [{module_name}](#{module_name.replace('.', '-')})\n")
            f.write("\n")

            # Module documentation
            for module_path, module_info in sorted(self.project_analysis["modules"].items()):
                self._write_module_documentation(f, module_path, module_info)

        logger.info(f"API reference generated: {output_file}")
        return output_file

    def _write_module_documentation(self, f, module_path: str, module_info: Dict[str, Any]) -> None:
        """Write documentation for a single module."""
        module_name = module_path.replace('/', '.').replace('.py', '')
        f.write(f"## {module_name}\n\n")

        if module_info.get("docstring"):
            f.write(f"{module_info['docstring']}\n\n")

        f.write(f"**File:** `{module_path}`\n\n")

        # Check for ASCII header compliance
        if not module_info.get("has_ascii_header", False):
            f.write("⚠️ **Note:** This module is missing the standard ASCII header.\n\n")

        # Classes
        if module_info.get("classes"):
            f.write("### Classes\n\n")
            for class_name, class_info in sorted(module_info["classes"].items()):
                self._write_class_documentation(f, class_name, class_info)

        # Functions
        if module_info.get("functions"):
            f.write("### Functions\n\n")
            for func_name, func_info in sorted(module_info["functions"].items()):
                self._write_function_documentation(f, func_name, func_info)

        # Constants
        if module_info.get("constants"):
            f.write("### Constants\n\n")
            for const_name, const_value in sorted(module_info["constants"].items()):
                f.write(f"**{const_name}** = `{const_value}`\n\n")

        f.write("---\n\n")

    def _write_class_documentation(self, f, class_name: str, class_info: Dict[str, Any]) -> None:
        """Write documentation for a class."""
        f.write(f"#### `{class_name}`\n\n")

        if class_info.get("docstring"):
            f.write(f"{class_info['docstring']}\n\n")

        # Inheritance
        if class_info.get("bases"):
            f.write(f"**Inherits from:** {', '.join(class_info['bases'])}\n\n")

        # Decorators
        if class_info.get("decorators"):
            f.write(f"**Decorators:** {', '.join(class_info['decorators'])}\n\n")

        # Methods
        if class_info.get("methods"):
            f.write("**Methods:**\n\n")
            for method_name, method_info in sorted(class_info["methods"].items()):
                self._write_method_documentation(f, method_name, method_info)

    def _write_function_documentation(self, f, func_name: str, func_info: Dict[str, Any]) -> None:
        """Write documentation for a function."""
        f.write(f"#### `{func_name}`\n\n")

        # Function signature
        args = func_info.get("args", [])
        arg_strings = []
        for arg in args:
            arg_str = arg["name"]
            if arg.get("type"):
                arg_str += f": {arg['type']}"
            if arg.get("default") is not None:
                arg_str += f" = {arg['default']}"
            arg_strings.append(arg_str)

        signature = f"{func_name}({', '.join(arg_strings)})"
        if func_info.get("returns"):
            signature += f" -> {func_info['returns']}"

        f.write(f"```python\n{signature}\n```\n\n")

        if func_info.get("docstring"):
            f.write(f"{func_info['docstring']}\n\n")

        # Mathematical content indicator
        if func_info.get("has_mathematical_content"):
            f.write("🔬 **Contains mathematical content**\n\n")

        # Async indicator
        if func_info.get("is_async"):
            f.write("⚡ **Async function**\n\n")

        # Decorators
        if func_info.get("decorators"):
            f.write(f"**Decorators:** {', '.join(func_info['decorators'])}\n\n")

    def _write_method_documentation(self, f, method_name: str, method_info: Dict[str, Any]) -> None:
        """Write documentation for a class method."""
        # Use simplified method documentation for class context
        f.write(f"- **`{method_name}`**")

        if method_info.get("is_async"):
            f.write(" (async)")

        if method_info.get("has_mathematical_content"):
            f.write(" 🔬")

        f.write("\n")

        if method_info.get("docstring"):
            # Get first line of docstring as summary
            first_line = method_info["docstring"].split('\n')[0].strip()
            if first_line:
                f.write(f"  {first_line}\n")

        f.write("\n")

    def _generate_user_guide(self, **kwargs) -> Path:
        """Generate user guide documentation."""
        output_file = self.config.output_dir / "user_guide.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# User Guide\n\n")
            f.write("Comprehensive guide for using the DIP_SMC_PSO simulation framework.\n\n")
            # Add user guide content based on project analysis
            # This would be expanded based on specific requirements

        logger.info(f"User guide generated: {output_file}")
        return output_file

    def _generate_developer_guide(self, **kwargs) -> Path:
        """Generate developer guide documentation."""
        output_file = self.config.output_dir / "developer_guide.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Developer Guide\n\n")
            f.write("Architecture and development documentation for the DIP_SMC_PSO project.\n\n")

            # Project structure
            f.write("## Project Structure\n\n")
            structure = self.project_analysis["structure"]
            for category, items in structure.items():
                if items:
                    f.write(f"### {category.replace('_', ' ').title()}\n\n")
                    for item in items:
                        f.write(f"- `{item}`\n")
                    f.write("\n")

        logger.info(f"Developer guide generated: {output_file}")
        return output_file

    def _generate_theory_documentation(self, **kwargs) -> Path:
        """Generate mathematical theory documentation."""
        output_file = self.config.output_dir / "theory.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Mathematical Theory and Foundations\n\n")
            f.write("Mathematical foundations for sliding mode control and optimization.\n\n")

            # Find modules with mathematical content
            math_modules = []
            for module_path, module_info in self.project_analysis["modules"].items():
                has_math = False
                for func_info in module_info.get("functions", {}).values():
                    if func_info.get("has_mathematical_content"):
                        has_math = True
                        break
                if not has_math:
                    for class_info in module_info.get("classes", {}).values():
                        for method_info in class_info.get("methods", {}).values():
                            if method_info.get("has_mathematical_content"):
                                has_math = True
                                break
                        if has_math:
                            break

                if has_math:
                    math_modules.append((module_path, module_info))

            if math_modules:
                f.write("## Modules with Mathematical Content\n\n")
                for module_path, module_info in math_modules:
                    module_name = module_path.replace('/', '.').replace('.py', '')
                    f.write(f"- [{module_name}](#{module_name.replace('.', '-')})\n")
                f.write("\n")

        logger.info(f"Theory documentation generated: {output_file}")
        return output_file

    def _generate_integration_guide(self, **kwargs) -> Path:
        """Generate integration guide documentation."""
        output_file = self.config.output_dir / "integration_guide.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Integration Guide\n\n")
            f.write("Guide for integrating with the multi-agent orchestration system.\n\n")

        logger.info(f"Integration guide generated: {output_file}")
        return output_file


def create_documentation_config(project_root: str) -> DocumentationConfig:
    """Create a default documentation configuration."""
    root_path = Path(project_root)

    # Detect source directories
    source_dirs = []
    for potential_dir in ['src', 'DIP_SMC_PSO/src', 'lib', 'package']:
        if (root_path / potential_dir).exists():
            source_dirs.append(Path(potential_dir))

    if not source_dirs:
        # Fallback to current directory
        source_dirs = [Path('.')]

    return DocumentationConfig(
        project_root=root_path,
        source_dirs=source_dirs,
        output_dir=root_path / 'docs' / 'generated',
        include_private=False,
        generate_examples=True,
        mathematical_notation=True,
        cross_references=True
    )


def main():
    """Main entry point for documentation generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate documentation for DIP_SMC_PSO project")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--type", choices=[t.value for t in DocumentationType],
                       default=DocumentationType.API_REFERENCE.value,
                       help="Type of documentation to generate")
    parser.add_argument("--output", help="Output directory (default: docs/generated)")
    parser.add_argument("--include-private", action="store_true",
                       help="Include private methods and classes")

    args = parser.parse_args()

    # Create configuration
    config = create_documentation_config(args.project_root)
    if args.output:
        config.output_dir = Path(args.output)
    if args.include_private:
        config.include_private = True

    # Generate documentation
    generator = DocumentationGenerator(config)
    doc_type = DocumentationType(args.type)
    output_file = generator.generate_documentation(doc_type)

    print(f"Documentation generated: {output_file}")


if __name__ == "__main__":
    main()