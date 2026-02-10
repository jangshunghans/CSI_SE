# doc_load 내 HTML 테이블 선을 잘 보이도록 border 색상을 #ddd -> #999 로 변경

import os
import re

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# table, th, td { ... border: 1px solid #ddd; ... } 블록만 #999로 변경
PATTERN = re.compile(
    r"(table, th, td \{\s*border: )1px solid #ddd(;\s*\})",
    re.MULTILINE
)
REPLACEMENT = r"\g<1>1px solid #999\g<2>"

fixed = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if PATTERN.search(content):
        new_content = PATTERN.sub(REPLACEMENT, content)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed += 1

print("테이블 선 스타일 변경된 파일 수:", fixed)
