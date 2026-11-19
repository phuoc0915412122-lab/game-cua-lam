with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
s2 = scripts[1]

# Balance check for braces and brackets
stack = []
pairs = {')': '(', ']': '[', '}': '{'}
in_string = False
str_char = ''
in_line_comment = False
in_block_comment = False
escaped = False

errors = []
for idx, ch in enumerate(s2):
    if in_line_comment:
        if ch == '\n': in_line_comment = False
        continue
    if in_block_comment:
        if ch == '/' and s2[idx-1] == '*': in_block_comment = False
        continue
    if in_string:
        if escaped: escaped = False
        elif ch == '\\': escaped = True
        elif ch == str_char: in_string = False
        continue
    if ch in '"\'`':
        in_string = True
        str_char = ch
        continue
    if ch == '/' and idx + 1 < len(s2) and s2[idx+1] == '/':
        in_line_comment = True
        continue
    if ch == '/' and idx + 1 < len(s2) and s2[idx+1] == '*':
        in_block_comment = True
        continue
    if ch in '([{':
        stack.append((ch, idx))
    elif ch in ')]}':
        if not stack:
            errors.append(f'Unmatched closing {ch} at {idx}')
        else:
            top, pos = stack.pop()
            if top != pairs[ch]:
                errors.append(f'Mismatched {top} at {pos} closed by {ch} at {idx}')

if not stack and not errors:
    print('Script 2 bracket/brace balance: 100% PERFECT!')
else:
    print('Errors:', errors[:5])
    print('Unclosed:', len(stack))
