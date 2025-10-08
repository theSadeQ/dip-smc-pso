# Example from: docs\api\factory_system_api_reference.md
# Index: 43
# Runnable: True
# Hash: 9809db08

if controller_type == 'sta_smc' and len(gains) >= 2:
    K1, K2 = gains[0], gains[1]
    if K1 <= K2:
        raise ValueError("Super-Twisting stability requires K1 > K2 > 0")