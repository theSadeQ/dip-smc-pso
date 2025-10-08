# Example from: docs\guides\workflows\pso-sta-smc.md
# Index: 3
# Runnable: False
# Hash: 072cfe5c

# Load optimized gains
with open('optimized_gains_sta_smc_phase53.json', 'r') as f:
    gains = json.load(f)['sta_smc']

K1, K2 = gains[0], gains[1]
ratio = K2 / K1

print(f"K1 = {K1:.2f}")
print(f"K2 = {K2:.2f}")
print(f"K2/K1 = {ratio:.3f}")

if ratio > 0.5:
    print("✅ Stability condition satisfied (K2 > 0.5·K1)")
else:
    print("❌ WARNING: Stability condition violated!")