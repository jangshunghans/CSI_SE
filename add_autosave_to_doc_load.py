# doc_load 내 모든 HTML에 자동 저장(debounce + 토스트) 로직 추가
import os

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# 치환 1: setTableEditable 앞에 자동 저장 관련 코드 추가
OLD1 = """    if (!/\.html$/i.test(filename)) filename = filename + '.html';

    function setTableEditable(editable) {"""

NEW1 = """    if (!/\.html$/i.test(filename)) filename = filename + '.html';

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
            var html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;
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

    function setTableEditable(editable) {"""

# 치환 2: 수정 버튼 클릭 시 input/keyup 리스너 추가, 저장 버튼 클릭 시 제거
OLD2 = """        btnEdit.disabled = true;
        btnSave.disabled = false;
    });

    btnSave.addEventListener('click', function() {
        area.setAttribute('contenteditable', 'false');"""

NEW2 = """        btnEdit.disabled = true;
        btnSave.disabled = false;
        area.addEventListener('input', onEditInput);
        area.addEventListener('keyup', onEditInput);
    });

    btnSave.addEventListener('click', function() {
        area.removeEventListener('input', onEditInput);
        area.removeEventListener('keyup', onEditInput);
        area.setAttribute('contenteditable', 'false');"""

# 치환 3: 저장 성공 시 alert -> showToast
OLD3 = """if (result.ok && result.data && result.data.ok) { alert('서버에 저장되었습니다.'); doRefresh(); }"""
NEW3 = """if (result.ok && result.data && result.data.ok) { showToast('저장되었습니다.'); doRefresh(); }"""

count = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    changed = False
    if OLD1 in s and NEW1 not in s:
        s = s.replace(OLD1, NEW1, 1)
        changed = True
    if OLD2 in s:
        s = s.replace(OLD2, NEW2, 1)
        changed = True
    if OLD3 in s:
        s = s.replace(OLD3, NEW3, 1)
        changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        count += 1
print("자동 저장 로직 적용된 파일 수:", count)
