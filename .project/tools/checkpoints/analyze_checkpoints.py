"""Analyze checkpoint status and categorize incomplete work."""
import json
from pathlib import Path

def analyze_checkpoints():
    artifacts = Path('.artifacts')
    checkpoints = {}

    # Find all launched checkpoints
    for f in artifacts.glob('*_launched.json'):
        try:
            data = json.load(open(f))
            task_agent = f.stem.replace('_launched', '')
            complete_file = f.parent / f'{task_agent}_complete.json'

            checkpoints[task_agent] = {
                'launched': data.get('launched_timestamp', 'unknown'),
                'complete': complete_file.exists(),
                'task_id': data.get('task_id', 'unknown'),
                'role': data.get('role', 'unknown')
            }
        except Exception as e:
            print(f'[ERROR] Failed to read {f}: {e}')

    # Categorize
    real_incomplete = []
    test_incomplete = []

    print('CHECKPOINT ANALYSIS:\n')
    print('-' * 80)

    for agent, info in sorted(checkpoints.items()):
        status = '[COMPLETE]' if info['complete'] else '[INCOMPLETE]'

        if not info['complete']:
            agent_lower = agent.lower()
            if 'test' in agent_lower or 'demo' in agent_lower:
                test_incomplete.append(agent)
            else:
                real_incomplete.append(agent)

        print(f'{status} {agent}')
        print(f'  Task: {info["task_id"]}')
        role_truncated = info["role"][:70] + ('...' if len(info["role"]) > 70 else '')
        print(f'  Role: {role_truncated}')
        print(f'  Launched: {info["launched"]}')
        print()

    print('-' * 80)
    print(f'\nSUMMARY:')
    print(f'  Total agents launched: {len(checkpoints)}')
    print(f'  Completed agents: {sum(1 for i in checkpoints.values() if i["complete"])}')
    print(f'  Real incomplete work: {len(real_incomplete)}')
    print(f'  Test/demo incomplete: {len(test_incomplete)}')

    if real_incomplete:
        print(f'\nREAL INCOMPLETE AGENTS (need resumption):')
        for a in real_incomplete:
            print(f'  - {a}')
            print(f'    Task: {checkpoints[a]["task_id"]}')
            print(f'    Role: {checkpoints[a]["role"]}')

    if test_incomplete:
        print(f'\nTEST/DEMO INCOMPLETE (can be cleaned up):')
        for a in test_incomplete:
            print(f'  - {a}')

    return real_incomplete, test_incomplete

if __name__ == '__main__':
    analyze_checkpoints()
