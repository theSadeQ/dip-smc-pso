# Example from: docs\plans\orchestration\ci_agent_framework.md
# Index: 3
# Runnable: False
# Hash: c5c7bd7a

def integrate_artifacts(agent_outputs: List[Dict]) -> Dict:
    """
    Reconcile multiple agent outputs.

    Conflict resolution order:
    1. Domain expert wins (Control Specialist > Integration Coordinator for SMC)
    2. Higher confidence wins (confidence > 0.8 overrides < 0.8)
    3. More specific wins (file-level > directory-level)
    4. Manual review required (flag for human)
    """

    DOMAIN_PRIORITY = {
        'Academic Research Automation Engineer': 90,
        'Control Systems Specialist': 80,
        'PSO Optimization Engineer': 70,
        'Documentation Expert': 60,
        'Integration Coordinator': 50
    }

    merged = {
        'changes': [],
        'conflicts': []
    }

    # Group changes by file
    by_file = defaultdict(list)
    for output in agent_outputs:
        for change in output['changes']:
            by_file[change['file']].append((output['metadata']['agent_name'], change))

    # Detect and resolve conflicts
    for file_path, changes in by_file.items():
        if len(changes) > 1:
            # Multiple agents modified same file - resolve conflict
            winner = max(changes, key=lambda x: (
                DOMAIN_PRIORITY.get(x[0], 0),  # Domain expert priority
                x[1].get('confidence', 0.0)     # Confidence tiebreaker
            ))

            merged['changes'].append(winner[1])
            merged['conflicts'].append({
                'file': file_path,
                'agents': [c[0] for c in changes],
                'resolution': f"Used {winner[0]} (domain priority + confidence)"
            })
        else:
            merged['changes'].append(changes[0][1])

    return merged