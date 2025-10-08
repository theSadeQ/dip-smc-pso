# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 8
# Runnable: False
# Hash: b292fd83

# example-metadata:
# runnable: false

class DocumentationValidator:
    def validate_literalinclude_paths(self) -> ValidationResult:
        ...

    def validate_coverage(self) -> ValidationResult:
        ...

    def validate_toctree(self) -> ValidationResult:
        ...

    def validate_syntax(self) -> ValidationResult:
        ...