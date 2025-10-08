# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 9
# Runnable: False
# Hash: 2e94f962

# example-metadata:
# runnable: false

@dataclass
class CodeClaim:
    id: str
    type: str  # "implementation", "doi_reference", "algorithm_reference"
    scope: str  # "module" | "class:ClassName" | "function:method_name"
    claim_text: str
    algorithm_name: Optional[str]
    source_attribution: Optional[str]
    file_path: str
    line_number: int
    has_citation: bool
    citation_format: Optional[str]  # "numbered", "doi", "author_year", "none"
    confidence: float