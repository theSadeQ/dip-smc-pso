# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 31
# Runnable: False
# Hash: e23521cd

def diagnose_energy(swing_up, state):
    """Print detailed energy diagnostics."""
    E_current = swing_up.dyn.total_energy(state)
    E_about_bottom = swing_up.E_bottom - E_current
    E_ratio = E_about_bottom / swing_up.E_bottom

    print(f"E_current: {E_current:.3f} J")
    print(f"E_bottom: {swing_up.E_bottom:.3f} J")
    print(f"E_about_bottom: {E_about_bottom:.3f} J")
    print(f"E_ratio: {E_ratio:.3f} (target: 0.95)")

    if E_ratio >= swing_up.switch_energy_factor:
        print("✅ Energy sufficient for handoff")
    else:
        shortage = (swing_up.switch_energy_factor - E_ratio) * swing_up.E_bottom
        print(f"❌ Energy shortage: {shortage:.3f} J")