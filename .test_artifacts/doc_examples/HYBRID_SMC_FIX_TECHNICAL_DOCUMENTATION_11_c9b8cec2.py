# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 11
# Runnable: True
# Hash: c9b8cec2

# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: return-statement-check
        name: Return Statement Validation
        entry: python scripts/validate_return_statements.py
        language: system
        files: ^src/controllers/.*\.py$