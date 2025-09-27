#==========================================================================================\\\
#========================== .claude/tools/demo_documentation.py =========================\\\
#==========================================================================================\\\

"""
Documentation Expert Agent Demonstration

Quick demonstration of the documentation generation capabilities for the
DIP_SMC_PSO project. Shows API analysis and documentation generation.
"""

import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from documentation_generator import DocumentationGenerator, DocumentationType, create_documentation_config

def demo_documentation_analysis():
    """Demonstrate documentation analysis capabilities."""

    print("🟢 DOCUMENTATION EXPERT AGENT DEMONSTRATION")
    print("=" * 60)

    # Create configuration for the DIP_SMC_PSO project
    config = create_documentation_config(str(project_root))

    print(f"\nProject Root: {config.project_root}")
    print(f"Source Directories: {[str(d) for d in config.source_dirs]}")
    print(f"Output Directory: {config.output_dir}")

    # Initialize the documentation generator
    generator = DocumentationGenerator(config)

    print("\n🔍 ANALYZING PROJECT STRUCTURE...")

    # Analyze the project
    try:
        analysis = generator.analyzer.analyze_project()

        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   • Modules found: {len(analysis['modules'])}")
        print(f"   • Classes found: {len(analysis['classes'])}")
        print(f"   • Functions found: {len(analysis['functions'])}")

        # Show some example analysis results
        print(f"\n📁 PROJECT STRUCTURE:")
        structure = analysis['structure']
        for category, items in structure.items():
            if items:
                print(f"   • {category.replace('_', ' ').title()}: {len(items)} items")

        # Find modules with mathematical content
        math_modules = []
        for module_path, module_info in analysis['modules'].items():
            has_math = False
            for func_info in module_info.get('functions', {}).values():
                if func_info.get('has_mathematical_content'):
                    has_math = True
                    break
            if not has_math:
                for class_info in module_info.get('classes', {}).values():
                    for method_info in class_info.get('methods', {}).values():
                        if method_info.get('has_mathematical_content'):
                            has_math = True
                            break
                    if has_math:
                        break
            if has_math:
                math_modules.append(module_path)

        print(f"\n🔬 MATHEMATICAL CONTENT:")
        print(f"   • Modules with mathematical content: {len(math_modules)}")
        if math_modules:
            print("   • Examples:")
            for module in math_modules[:3]:  # Show first 3
                print(f"     - {module}")

        # Check ASCII header compliance
        total_modules = len(analysis['modules'])
        compliant_modules = sum(1 for module_info in analysis['modules'].values()
                              if module_info.get('has_ascii_header', False))

        print(f"\n📝 ASCII HEADER COMPLIANCE:")
        print(f"   • Compliant modules: {compliant_modules}/{total_modules}")
        if compliant_modules < total_modules:
            print(f"   • Compliance rate: {compliant_modules/total_modules*100:.1f}%")

        # Show some example classes and functions
        print(f"\n🏗️  SAMPLE COMPONENTS:")

        # Show a few example classes
        example_classes = list(analysis['classes'].items())[:3]
        if example_classes:
            print("   Classes:")
            for class_name, class_info in example_classes:
                print(f"     • {class_name}: {len(class_info.get('methods', {}))} methods")

        # Show a few example functions
        example_functions = list(analysis['functions'].items())[:3]
        if example_functions:
            print("   Functions:")
            for func_name, func_info in example_functions:
                has_math = "🔬" if func_info.get('has_mathematical_content') else ""
                print(f"     • {func_name} {has_math}")

        return True

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def demo_documentation_generation():
    """Demonstrate documentation generation."""

    print(f"\n📚 DOCUMENTATION GENERATION DEMO")
    print("-" * 40)

    # Create a small demo output directory
    demo_output = project_root / '.claude' / 'demo_output'
    demo_output.mkdir(exist_ok=True)

    config = create_documentation_config(str(project_root))
    config.output_dir = demo_output

    generator = DocumentationGenerator(config)

    try:
        # Generate a sample API reference
        print("🚀 Generating API reference documentation...")
        api_file = generator.generate_documentation(DocumentationType.API_REFERENCE)
        print(f"   ✅ Generated: {api_file}")

        # Show a preview of the generated content
        if api_file.exists():
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                preview_lines = lines[:20]  # First 20 lines

            print(f"\n📖 PREVIEW ({len(lines)} total lines):")
            for i, line in enumerate(preview_lines, 1):
                print(f"   {i:2d}: {line}")
            if len(lines) > 20:
                print(f"   ... ({len(lines) - 20} more lines)")

        return True

    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

def demo_integration_ready():
    """Show that the Documentation Expert is ready for integration."""

    print(f"\n🎯 INTEGRATION READINESS")
    print("-" * 40)

    # Check agent file exists
    agent_file = project_root / '.claude' / 'agents' / 'documentation-expert.md'
    tools_file = project_root / '.claude' / 'tools' / 'documentation_generator.py'
    workflow_file = project_root / '.claude' / 'examples' / 'documentation_expert_workflow.py'

    print("📁 Agent System Files:")
    print(f"   • Agent specification: {'✅' if agent_file.exists() else '❌'} {agent_file.name}")
    print(f"   • Documentation tools: {'✅' if tools_file.exists() else '❌'} {tools_file.name}")
    print(f"   • Workflow examples: {'✅' if workflow_file.exists() else '❌'} {workflow_file.name}")

    print(f"\n🔧 Capabilities:")
    capabilities = [
        "API documentation generation with mathematical notation",
        "User guide creation with step-by-step tutorials",
        "Developer documentation for architecture and patterns",
        "Mathematical theory documentation with LaTeX support",
        "Integration with 5-agent orchestration system",
        "ASCII header compliance checking",
        "Cross-reference validation and link checking",
        "Type hint documentation and validation"
    ]

    for capability in capabilities:
        print(f"   ✅ {capability}")

    print(f"\n🚀 Ready for Deployment:")
    print("   • 5th specialist agent in multi-agent orchestration")
    print("   • Triggered automatically for documentation tasks")
    print("   • Collaborates with Control Systems, PSO, and Integration specialists")
    print("   • Maintains scientific rigor and technical accuracy")

def main():
    """Run the complete demonstration."""

    print("Starting Documentation Expert Agent demonstration...")

    # Run analysis demo
    analysis_success = demo_documentation_analysis()

    if analysis_success:
        # Run generation demo
        generation_success = demo_documentation_generation()

        # Show integration readiness
        demo_integration_ready()

        if generation_success:
            print(f"\n🎉 DEMONSTRATION COMPLETE!")
            print("Documentation Expert Agent is ready for integration!")
        else:
            print(f"\n⚠️  Demonstration completed with generation issues.")
    else:
        print(f"\n❌ Demonstration failed during analysis phase.")

if __name__ == "__main__":
    main()