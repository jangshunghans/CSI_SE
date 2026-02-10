# -*- coding: utf-8 -*-
"""doc_load 내 모든 HTML에 수정/저장 버튼 로직 추가 (123-01-06과 동일)"""
import re
from pathlib import Path

STYLES = """
        .btn-wrap {
            margin: 16px 0;
        }
        .btn-wrap button {
            font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
            padding: 8px 20px;
            margin-right: 10px;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f5f5f5;
            color: #333;
            cursor: pointer;
        }
        .btn-wrap button:hover {
            background: #e8e8e8;
        }
        .btn-wrap button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        #editableArea[contenteditable="true"] {
            outline: 1px dashed #4a90d9;
            padding: 4px;
            min-height: 100px;
        }
"""

BUTTONS_AND_OPEN = """
<div class="btn-wrap">
    <button type="button" id="btnEdit">수정</button>
    <button type="button" id="btnSave" disabled>저장</button>
</div>
<div id="editableArea" contenteditable="false">
"""

SCRIPT = r"""
<script>
(function() {
    var btnEdit = document.getElementById('btnEdit');
    var btnSave = document.getElementById('btnSave');
    var area = document.getElementById('editableArea');
    var pathname = location.pathname || '';
    var filename = pathname.split('/').filter(Boolean).pop() || (document.title || 'document').trim() + '.html';
    if (!/\.html$/i.test(filename)) filename = filename + '.html';

    btnEdit.addEventListener('click', function() {
        area.setAttribute('contenteditable', 'true');
        area.focus();
        btnEdit.disabled = true;
        btnSave.disabled = false;
    });

    btnSave.addEventListener('click', function() {
        area.setAttribute('contenteditable', 'false');
        btnEdit.disabled = false;
        btnSave.disabled = true;
        var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;

        function doRefresh() { location.reload(); }

        function fallbackWithDialog() {
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
              if (result.ok && result.data && result.data.ok) doRefresh();
              else fallbackWithDialog();
          })
          .catch(function() { fallbackWithDialog(); });
    });
})();
</script>
"""

def process(path):
    path = Path(path)
    if path.suffix.lower() != '.html':
        return False
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        print('Read error', path, e)
        return False
    if 'id="btnEdit"' in content or 'id=\'btnEdit\'' in content:
        return True
    if '<body>' not in content or '</table>' not in content or '</body>' not in content:
        print('Skip (wrong structure):', path.name)
        return True
    # 1) 스타일 추가: </style> 직전에
    content = content.replace('    </style>', STYLES + '    </style>', 1)
    # 2) body 직후에 버튼 + editableArea 열기, 첫 <p> 앞에
    content = re.sub(r'<body>\s*<p>', '<body>' + BUTTONS_AND_OPEN + '<p>', content, count=1)
    # 3) 마지막 </table> 다음 </body> 전에 </div> + 스크립트
    content = re.sub(r'</table>\s*</body>', '</table>\n</div>' + SCRIPT + '\n</body>', content, count=1)
    try:
        path.write_text(content, encoding='utf-8')
    except Exception as e:
        print('Write error', path, e)
        return False
    return True

def main():
    doc_load = Path(__file__).resolve().parent / 'doc_load'
    if not doc_load.is_dir():
        print('doc_load folder not found')
        return
    count = 0
    for f in sorted(doc_load.glob('*.html')):
        if process(f):
            count += 1
    print('Processed', count, 'files.')

if __name__ == '__main__':
    main()
