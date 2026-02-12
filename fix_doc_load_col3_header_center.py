# doc_load: 3번째 열 헤더(th) 가운데 정렬, 셀(td) 왼쪽 정렬
import os

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

OLD = """        table tr th:nth-child(3),
        table tr td:nth-child(3) {
            text-align: left;
        }"""

NEW = """        table tr th:nth-child(3) {
            text-align: center;
        }
        table tr td:nth-child(3) {
            text-align: left;
        }"""

count = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    if OLD in s:
        s = s.replace(OLD, NEW, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        count += 1
print("3열 헤더 가운데정렬 적용된 파일 수:", count)
