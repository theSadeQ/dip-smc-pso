# Example from: docs\plans\documentation\week_1_completion_report.md
# Index: 3
# Runnable: True
# Hash: c2024301

def _get_relative_path(self, source_file: Path, doc_file: Path) -> str:
    """Calculate relative path from doc to source."""
    try:
        relative = os.path.relpath(source_file, doc_file.parent)
        return relative.replace('\\', '/')  # Normalize to forward slashes
    except ValueError:
        return str(source_file)