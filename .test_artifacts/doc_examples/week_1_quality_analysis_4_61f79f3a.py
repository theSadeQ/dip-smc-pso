# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 4
# Runnable: False
# Hash: 61f79f3a

# example-metadata:
# runnable: false

# Generator fallback
try:
    relative = os.path.relpath(source_file, doc_file.parent)
except ValueError:
    return str(source_file)

# Validation detailed reporting
@dataclass
class ValidationResult:
    passed: bool
    message: str
    details: List[str] = None