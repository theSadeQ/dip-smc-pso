# Example from: docs\plans\citation_system\01_initial_analysis.md
# Index: 6
# Runnable: False
# Hash: 8ff66b35

def integrate_artifacts(agent_outputs: List[Dict]) -> Dict:
    """
    Merge outputs from multiple agents.

    Conflict resolution priority:
    1. Domain expert wins (NEW agent for research quality)
    2. Higher confidence wins (confidence > 0.8 overrides < 0.8)
    3. More specific wins (file-level > directory-level)
    4. Manual review (flag for human if unresolvable)
    """

    merged = {'changes': [], 'conflicts': []}

    by_file = defaultdict(list)
    for output in agent_outputs:
        for change in output['changes']:
            by_file[change['file']].append((output['metadata']['agent_name'], change))

    for file_path, changes in by_file.items():
        if len(changes) > 1:
            # Conflict detected
            winner = max(changes, key=lambda x: (
                DOMAIN_PRIORITY.get(x[0], 0),  # NEW agent > DOC > INT
                x[1].get('confidence', 0.0)
            ))
            merged['changes'].append(winner[1])
            merged['conflicts'].append({
                'file': file_path,
                'resolution': f"Used {winner[0]} (domain + confidence)"
            })
        else:
            merged['changes'].append(changes[0][1])

    return merged