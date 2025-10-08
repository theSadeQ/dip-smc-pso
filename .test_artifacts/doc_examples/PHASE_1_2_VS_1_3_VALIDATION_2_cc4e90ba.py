# Example from: docs\PHASE_1_2_VS_1_3_VALIDATION.md
# Index: 2
# Runnable: False
# Hash: cc4e90ba

# example-metadata:
# runnable: false

# Type hint detection
def analyze_type_hints(node: ast.FunctionDef):
    args = node.args
    all_args = args.args + args.posonlyargs + args.kwonlyargs
    annotated = sum(1 for arg in all_args if arg.annotation is not None)
    has_return = node.returns is not None
    coverage = (annotated / total) * 100 if total > 0 else 100.0

# Docstring detection
def analyze_docstring(docstring: str):
    has_params = "Parameters" in docstring or "Args:" in docstring
    has_returns = "Returns" in docstring or ":return" in docstring
    style = detect_style(docstring)  # numpy, google, sphinx