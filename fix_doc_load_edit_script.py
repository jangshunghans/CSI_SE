# doc_load 내 HTML에서 수정 버튼이 동작하지 않는 원인 수정:
# var html = '<!DOCTYPE html> 다음에 실제 줄바꿈이 들어가 있으면 JS 구문 오류로 스크립트 전체가 실행되지 않음.
# 이를 var html = '<!DOCTYPE html>\n' + document... 형태의 한 줄로 통일

import os
import re

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# 줄바꿈 포함 두 줄 패턴 (공백/탭/캐리지리턴 허용)
PATTERN = re.compile(
    r"var html = '<!DOCTYPE html>\s*\r?\n\s*' \+ document\.documentElement\.outerHTML\s*;",
    re.MULTILINE
)
# 한 줄로 치환. re.sub는 치환 문자열에서 \n을 줄바꿈으로 해석하므로 \\\\n으로 넘겨야 역슬래시+n 두 문자가 됨.
REPLACEMENT = "var html = '<!DOCTYPE html>\\\\n' + document.documentElement.outerHTML;"

fixed = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8", newline=None) as f:
        content = f.read()
    if PATTERN.search(content):
        new_content = PATTERN.sub(REPLACEMENT, content)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        fixed += 1
        if fixed <= 5:
            print(path)

if fixed > 5:
    print("... (외 %d개)" % (fixed - 5))
print("수정된 파일 수:", fixed)
