# doc_load 내 모든 HTML에서 저장 성공 시 "서버에 저장되었습니다." 메시지 추가
import os

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")
OLD = "if (result.ok && result.data && result.data.ok) doRefresh();"
NEW = "if (result.ok && result.data && result.data.ok) { alert('서버에 저장되었습니다.'); doRefresh(); }"

count = 0
for name in os.listdir(DOC_LOAD):
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
print("수정된 파일 수:", count)
