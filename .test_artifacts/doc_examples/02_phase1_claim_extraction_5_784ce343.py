# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 5
# Runnable: False
# Hash: 784ce343

@dataclass
class FormalClaim:
    # Identity
    id: str                    # "FORMAL-THEOREM-001"
    type: str                  # "theorem", "lemma", "proposition"
    number: Optional[int]      # Theorem number (if numbered)

    # Content
    statement: str             # Full theorem statement
    proof: Optional[str]       # Associated proof (if found)
    math_blocks: List[str]     # Extracted LaTeX math

    # Location
    file_path: str             # Relative path from project root
    line_number: int           # Line where claim starts
    section_header: str        # Containing section (e.g., "Super-Twisting Algorithm")

    # Context (for AI research)
    context_before: List[str]  # 5 lines before
    context_after: List[str]   # 5 lines after

    # Metadata
    has_citation: bool         # Already has {cite}?
    confidence: float          # Extraction confidence [0, 1]
    suggested_keywords: List[str]  # For AI research queries