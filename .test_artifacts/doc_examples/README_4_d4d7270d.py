# Example from: docs\factory\README.md
# Index: 4
# Runnable: True
# Hash: d4d7270d

def quick_health_check():
    from src.controllers.factory import create_controller
    try:
        controller = create_controller('classical_smc', gains=[20]*6)
        print("✅ Factory system healthy")
        return True
    except Exception as e:
        print(f"❌ Factory system issue: {e}")
        return False

quick_health_check()