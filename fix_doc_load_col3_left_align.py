# doc_load: 3번째 열(주요 내용) th, td 왼쪽 정렬로 통일
import os

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# 패턴 1: td만 있는 경우 -> th, td 둘 다
OLD1 = """        table tr td:nth-child(3) {
            text-align: left;
        }"""
NEW1 = """        table tr th:nth-child(3),
        table tr td:nth-child(3) {
            text-align: left;
        }"""

# 패턴 2: 공백이 다른 경우 (일부 파일)
OLD2 = "table tr td:nth-child(3) {\n            text-align: left;\n        }"
NEW2 = "table tr th:nth-child(3),\n        table tr td:nth-child(3) {\n            text-align: left;\n        }"

count = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    changed = False
    if OLD1 in s and "table tr th:nth-child(3)" not in s:
        s = s.replace(OLD1, NEW1, 1)
        changed = True
    elif OLD2 in s and "table tr th:nth-child(3)" not in s:
        s = s.replace(OLD2, NEW2, 1)
        changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        count += 1
print("3번째 열 왼쪽정렬(th+td) 적용된 파일 수:", count)
