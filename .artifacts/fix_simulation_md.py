#!/usr/bin/env python3
"""Fix Python comments in simulation.md"""

filepath = r'D:\Projects\main\docs\guides\api\simulation.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Python comments # with ## inside code blocks
in_code_block = False
lines = content.split('\n')
fixed_lines = []

for line in lines:
    if line.strip().startswith('```'):
        in_code_block = not in_code_block
        fixed_lines.append(line)
    elif in_code_block and line.lstrip().startswith('# ') and not line.lstrip().startswith('##'):
        # Replace first occurrence of # with ##
        fixed_line = line.replace('# ', '## ', 1)
        fixed_lines.append(fixed_line)
    else:
        fixed_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print(f"Fixed {filepath}")
