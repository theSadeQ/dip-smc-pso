import json
from collections import Counter

data = json.load(open('artifacts/code_claims.json'))
scopes = [c['scope'] for c in data['claims']]
counts = Counter(scopes)

print('Top 15 scope patterns:')
for scope, count in counts.most_common(15):
    print(f'{count:3d}  {scope}')

# Analyze scope depth
print('\nScope depth distribution:')
depth_counts = Counter(len(s.split(':')) for s in scopes)
for depth in sorted(depth_counts.keys()):
    print(f'Depth {depth}: {depth_counts[depth]} claims')

# Sample class and function scopes
print('\nSample class-level scopes:')
class_scopes = [s for s in scopes if 'class:' in s][:5]
for s in class_scopes:
    print(f'  {s}')

print('\nSample function-level scopes:')
func_scopes = [s for s in scopes if 'function:' in s][:5]
for s in func_scopes:
    print(f'  {s}')
