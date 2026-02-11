# showToast/scheduleAutoSave/onEditInput 이 없는 doc_load 파일에만 해당 블록 삽입
import os

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# filename 다음, btnEdit.addEventListener 직전에 넣을 블록 (setTableEditable 없는 파일용)
INSERT_BLOCK = r"""
    var autoSaveTimer = null;
    var AUTO_SAVE_DELAY_MS = 2000;

    function showToast(msg) {
        var t = document.getElementById('docLoadToast');
        if (t) t.remove();
        t = document.createElement('div');
        t.id = 'docLoadToast';
        t.textContent = msg;
        t.style.cssText = 'position:fixed;bottom:20px;right:20px;padding:10px 16px;background:#333;color:#fff;border-radius:8px;font-size:13px;z-index:9999;box-shadow:0 2px 8px rgba(0,0,0,0.2);';
        document.body.appendChild(t);
        setTimeout(function() { if (t.parentNode) t.remove(); }, 2500);
    }

    function scheduleAutoSave() {
        if (autoSaveTimer) clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            autoSaveTimer = null;
            var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
            var origin = location.origin || (location.protocol + '//' + location.host);
            fetch(origin + '/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: filename, content: html })
            }).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }); })
              .then(function(result) {
                  if (result.ok && result.data && result.data.ok) showToast('자동 저장됨');
                  else showToast('자동 저장 불가 (서버에서 열어 주세요)');
              })
              .catch(function() { showToast('자동 저장 불가 (서버 연결 필요)'); });
        }, AUTO_SAVE_DELAY_MS);
    }

    function onEditInput() { scheduleAutoSave(); }

"""

# "function showToast" 가 없고 "onEditInput" 가 있는 파일에서만 삽입
# 삽입 위치: if (!/\.html$/i.test(filename)) filename = filename + '.html'; \n\n    btnEdit.addEventListener
PREFIX = "    if (!/\.html$/i.test(filename)) filename = filename + '.html';\n\n    btnEdit.addEventListener"
TARGET = "    if (!/\.html$/i.test(filename)) filename = filename + '.html';\n\n" + INSERT_BLOCK.strip() + "\n\n    btnEdit.addEventListener"

count = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    if "function showToast" in s:
        continue
    if "onEditInput" not in s:
        continue
    if PREFIX not in s:
        continue
    s = s.replace(PREFIX, TARGET, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    count += 1
print("showToast/scheduleAutoSave/onEditInput 추가된 파일 수:", count)
