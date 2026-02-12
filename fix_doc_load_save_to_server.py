# doc_load: 저장 시 baseUrl 사용, 서버 실패 시 다운로드 대신 안내 메시지
import os
import re

DOC_LOAD = os.path.join(os.path.dirname(__file__), "doc_load")

# (1) scheduleAutoSave 내: origin -> baseUrl, r.json()에 .catch 추가
OLD_ORIGIN_FETCH = """            var origin = location.origin || (location.protocol + '//' + location.host);
            fetch(origin + '/save', {"""

NEW_BASEURL_FETCH = """            var baseUrl = location.origin + ((location.pathname || '').split('/doc_load')[0] || '');
            if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);
            fetch(baseUrl + '/save', {"""

OLD_JSON_THEN = """}).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }); })"""
NEW_JSON_THEN = """}).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }).catch(function() { return { ok: false, data: null }; }); })"""

# (2) btnSave: fallbackWithDialog 블록 + origin fetch -> baseUrl fetch + 실패 시 안내만
OLD_SAVE_BLOCK = r"""        function fallbackWithDialog\(\) \{
            if \('showSaveFilePicker' in window\) \{
                window\.showSaveFilePicker\(\{
                    suggestedName: filename,
                    types: \[\{ description: 'HTML file', accept: \{ 'text/html': \[\.html'\] \} \}\]
                \}\)\.then\(function\(fileHandle\) \{ return fileHandle\.createWritable\(\); \}\)
                  \.then\(function\(writable\) \{ return writable\.write\(html\)\.then\(function\(\) \{ return writable\.close\(\); \}\); \}\)
                  \.then\(doRefresh\)\.catch\(function\(err\) \{
                    if \(err\.name !== 'AbortError'\) alert\('저장 실패: ' \+ \(err\.message \|\| err\)\);
                    btnSave\.disabled = false;
                  \}\);
            \} else \{
                var blob = new Blob\(\[html\], \{ type: 'text/html;charset=utf-8' \}\);
                var a = document\.createElement\('a'\);
                a\.href = URL\.createObjectURL\(blob\);
                a\.download = filename;
                a\.style\.display = 'none';
                document\.body\.appendChild\(a\);
                a\.click\(\);
                document\.body\.removeChild\(a\);
                URL\.revokeObjectURL\(a\.href\);
                setTimeout\(doRefresh, 300\);
            \}
        \}

        var origin = location\.origin \|\| \(location\.protocol \+ '//' \+ location\.host\);
        fetch\(origin \+ '/save', \{
            method: 'POST',
            headers: \{ 'Content-Type': 'application/json' \},
            body: JSON\.stringify\(\{ filename: filename, content: html \}\)
        \}\)\.then\(function\(r\) \{ return r\.json\(\)\.then\(function\(d\) \{ return \{ ok: r\.ok, data: d \}; \}\); \}\)
          \.then\(function\(result\) \{
              if \(result\.ok && result\.data && result\.data\.ok\) \{ showToast\('저장되었습니다\.'\); doRefresh\(\); \}
              else fallbackWithDialog\(\);
          \}\)
          \.catch\(function\(\) \{ fallbackWithDialog\(\); \}\);"""

# Use non-regex string replace for reliability
OLD_SAVE_PART1 = """        function fallbackWithDialog() {
            if ('showSaveFilePicker' in window) {
                window.showSaveFilePicker({
                    suggestedName: filename,
                    types: [{ description: 'HTML file', accept: { 'text/html': ['.html'] } }]
                }).then(function(fileHandle) { return fileHandle.createWritable(); })
                  .then(function(writable) { return writable.write(html).then(function() { return writable.close(); }); })
                  .then(doRefresh).catch(function(err) {
                    if (err.name !== 'AbortError') alert('저장 실패: ' + (err.message || err));
                    btnSave.disabled = false;
                  });
            } else {
                var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
                var a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = filename;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(a.href);
                setTimeout(doRefresh, 300);
            }
        }

        var origin = location.origin || (location.protocol + '//' + location.host);
        fetch(origin + '/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename, content: html })
        }).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }); })
          .then(function(result) {
              if (result.ok && result.data && result.data.ok) { showToast('저장되었습니다.'); doRefresh(); }
              else fallbackWithDialog();
          })
          .catch(function() { fallbackWithDialog(); });"""

NEW_SAVE_PART1 = """        var baseUrl = location.origin + ((location.pathname || '').split('/doc_load')[0] || '');
        if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);
        fetch(baseUrl + '/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename, content: html })
        }).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }).catch(function() { return { ok: false, data: null }; }); })
          .then(function(result) {
              if (result.ok && result.data && result.data.ok) { showToast('저장되었습니다.'); doRefresh(); }
              else { showToast('서버에 저장할 수 없습니다. Replit 또는 Node 서버 주소에서 열어 주세요.'); btnSave.disabled = false; }
          })
          .catch(function() { showToast('서버에 저장할 수 없습니다. Replit 또는 Node 서버 주소에서 열어 주세요.'); btnSave.disabled = false; });"""

# btnSave 쪽에서 origin 사용하는 다른 패턴 (한 줄로 된 경우)
OLD_ORIGIN_LINE = "        var origin = location.origin || (location.protocol + '//' + location.host);\n        fetch(origin + '/save', {"
NEW_BASEURL_LINE = "        var baseUrl = location.origin + ((location.pathname || '').split('/doc_load')[0] || '');\n        if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);\n        fetch(baseUrl + '/save', {"

count = 0
for name in sorted(os.listdir(DOC_LOAD)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(DOC_LOAD, name)
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    changed = False

    # 123-01-01은 이미 수정됨 (fallbackWithDialog 없음) - scheduleAutoSave만 확인
    if "fallbackWithDialog" in s:
        if OLD_SAVE_PART1 in s:
            s = s.replace(OLD_SAVE_PART1, NEW_SAVE_PART1, 1)
            changed = True
    else:
        # 이미 새 형식일 수 있음 - origin이 남아있는지 확인
        if "var origin = location.origin" in s and "fetch(origin + '/save'" in s:
            s = s.replace(OLD_ORIGIN_LINE, NEW_BASEURL_LINE, 1)
            s = s.replace(
                "}).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }); })",
                "}).then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }).catch(function() { return { ok: false, data: null }; }); })",
                1
            )
            # else fallback -> else { showToast... }
            s = s.replace(
                "else fallbackWithDialog();",
                "else { showToast('서버에 저장할 수 없습니다. Replit 또는 Node 서버 주소에서 열어 주세요.'); btnSave.disabled = false; }",
                1
            )
            s = s.replace(
                ".catch(function() { fallbackWithDialog(); });",
                ".catch(function() { showToast('서버에 저장할 수 없습니다. Replit 또는 Node 서버 주소에서 열어 주세요.'); btnSave.disabled = false; });",
                1
            )
            changed = True

    # scheduleAutoSave: origin -> baseUrl (아직 origin이 있는 파일만)
    if "var origin = location.origin" in s and "fetch(origin + '/save'" in s:
        s = s.replace(OLD_ORIGIN_FETCH, NEW_BASEURL_FETCH, 1)
        if OLD_JSON_THEN in s:
            s = s.replace(OLD_JSON_THEN, NEW_JSON_THEN, 1)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        count += 1

print("수정된 파일 수:", count)
