# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 9
# Runnable: True
# Hash: 53baa652

class SMCControllerType(Enum):
    CLASSICAL = "classical"           # 6 gains
    ADAPTIVE = "adaptive"             # 5 gains
    SUPER_TWISTING = "super_twisting" # 6 gains
    HYBRID = "hybrid"                 # 4 gains