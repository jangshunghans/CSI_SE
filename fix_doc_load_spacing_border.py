# doc_load HTML: 테이블 간격 넓히기(padding 8px->12px), 선 굵게(border 1px->2px)

import os
import re

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# 1) table, th, td 의 border 1px -> 2px
PAT_BORDER = re.compile(
    r"(table, th, td \{\s*border: )1px( solid #999;\s*\})",
    re.MULTILINE
)
REPL_BORDER = r"\g<1>2px\g<2>"

# 2) th, td 의 padding: 8px -> 12px (th, td 블록 안의 padding만)
PAT_PADDING = re.compile(
    r"(th, td \{\s*padding: )8px(;)",
    re.MULTILINE
)
REPL_PADDING = r"\g<1>12px\g<2>"

fixed = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content
    if PAT_BORDER.search(new_content):
        new_content = PAT_BORDER.sub(REPL_BORDER, new_content)
    if PAT_PADDING.search(new_content):
        new_content = PAT_PADDING.sub(REPL_PADDING, new_content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed += 1

print("간격·선 굵기 적용된 파일 수:", fixed)
