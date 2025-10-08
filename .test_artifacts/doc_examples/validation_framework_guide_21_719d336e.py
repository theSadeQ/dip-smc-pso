# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 21
# Runnable: True
# Hash: 719d336e

# Good error messages
"proportional_gain must be > 0; got -2.5"
"adaptation_rate must be in the interval [0.01, 10.0]; got 15.0"
"twisting_gain_K2 must satisfy K1 > K2 > 0; got K1=4.0, K2=5.0"

# Bad error messages (avoid)
"Invalid value"                       # Missing parameter name
"Error: -2.5"                         # Missing constraint
"Value out of range"                  # Missing actual bounds