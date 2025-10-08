# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 2
# Runnable: True
# Hash: ae0a985f

def _get_relative_path(self, source_file: Path, doc_file: Path) -> str:
    """Calculate relative path from doc to source."""
    try:
        relative = os.path.relpath(source_file, doc_file.parent)
        return relative.replace('\\', '/')  # Normalize
    except ValueError:
        return str(source_file)  # Fallback