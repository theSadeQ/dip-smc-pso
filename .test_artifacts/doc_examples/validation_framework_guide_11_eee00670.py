# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 11
# Runnable: True
# Hash: eee00670

from src.controllers.smc.core.gain_validation import SMCGainValidator

validator = SMCGainValidator()

# Super-twisting gains (requires K1 > K2)
sta_gains = [5.0, 4.0, 10.0, 5.0, 8.0, 3.0]  # [K1, K2, k1, k2, λ1, λ2]

stability = validator.validate_stability_conditions(sta_gains, "super_twisting")

if stability['stable']:
    print("✅ Stability conditions satisfied")
else:
    print(f"⚠️ Stability issues:")
    for issue in stability['issues']:
        print(f"  - {issue}")

# Example output:
# ✅ Stability conditions satisfied (K1=5.0 > K2=4.0 > 0)