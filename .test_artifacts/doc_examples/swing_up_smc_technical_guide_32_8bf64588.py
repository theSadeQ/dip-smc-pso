# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 32
# Runnable: False
# Hash: 8bf64588

def analyze_transitions(history_list):
    """Analyze mode switching behavior."""
    transitions = []
    prev_mode = history_list[0].get("mode", "swing")

    for i, h in enumerate(history_list[1:], 1):
        mode = h.get("mode", "swing")
        if mode != prev_mode:
            transitions.append({
                'time': h.get("t", 0),
                'from': prev_mode,
                'to': mode,
                'E_ratio': h.get("E_ratio", 0)
            })
        prev_mode = mode

    print(f"Total transitions: {len(transitions)}")
    for t in transitions:
        print(f"  t={t['time']:.2f}s: {t['from']} → {t['to']} (E_ratio={t['E_ratio']:.3f})")