# -*- coding: utf-8 -*-
"""
allinone.html 재생성 스크립트
csi.json + http_load/*.html → allinone.html
실행: python build_allinone.py
"""

import json, os, re
from collections import OrderedDict

HTTP_LOAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "http_load")
DOC_LOAD  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_load")
CSI_JSON  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csi.json")
OUT_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allinone.html")

# ── csi.json 로드 ──────────────────────────────────────
with open(CSI_JSON, encoding="utf-8") as f:
    meta_list = json.load(f)

# 주요항목 → 세부항목 → [문항번호] 순서 유지
major_order = OrderedDict()
detail_order = OrderedDict()

for m in meta_list:
    if m.get("사용여부") != "Y":
        continue
    fid = m["문항번호"]
    major = m.get("주요항목", "기타")
    detail = m.get("세부항목", "기타")
    key = (major, detail)
    if major not in major_order:
        major_order[major] = []
    if detail not in major_order[major]:
        major_order[major].append(detail)
    if key not in detail_order:
        detail_order[key] = []
    detail_order[key].append(fid)

# ── 콘텐츠 추출 (http_load 우선, diagram 비어있으면 doc_load fallback) ──
def extract_content(fid):
    html = None
    for folder in [HTTP_LOAD, DOC_LOAD]:
        path = os.path.join(folder, f"{fid}.html")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            candidate = f.read()
        # diagram에 실제 내용 있는지 확인
        diag_inner = re.search(r'<div class="diagram">(.*?)</div>\s*(?:</body>|$)', candidate, re.DOTALL)
        if diag_inner and diag_inner.group(1).strip():
            html = candidate
            break
    if not html:
        return None, None
    tbox = re.search(r'<div class="tbox">(.*?)</div>\s*<div class="diagram">', html, re.DOTALL)
    tbox_html = tbox.group(1) if tbox else f'<div class="tline">[{fid}]</div>'
    diag = re.search(r'(<div class="diagram">.*?</div>)\s*(?:</body>|$)', html, re.DOTALL)
    diag_html = diag.group(1) if diag else '<div class="diagram"></div>'
    return tbox_html, diag_html

# ── CSS ────────────────────────────────────────────────
CSS = """/* ── 기본 리셋 ── */
* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── 카드 내부 구조 (흑백) ── */
.tbox {
  background: #fff;
  color: #000;
  text-align: center;
  padding: 9px 12px;
  font-size: 12pt;
  font-weight: bold;
  margin-bottom: 10px;
  border-top: 1px solid #000;
  border-bottom: 1px solid #000;
}
.tline { line-height: 1.55; }
.diagram { display: flex; flex-direction: column; gap: 4px; padding: 12px 14px 14px; }
.branch { display: flex; align-items: stretch; }
.blabel {
  width: 64px; min-width: 64px;
  border: 1px solid #000;
  background: #fff;
  text-align: center;
  font-weight: bold;
  font-size: 9.5pt;
  display: flex; align-items: center; justify-content: center;
  padding: 4px 3px;
  word-break: keep-all;
  line-height: 1.4;
}
.bitems {
  flex: 1;
  display: flex; flex-direction: column; gap: 3px;
  padding-left: 7px;
  border-left: 1px solid #000;
  margin-left: 5px;
}
.item { display: flex; align-items: stretch; border: 1px solid #000; }
.ilabel {
  width: 92px; min-width: 92px;
  border-right: 1px solid #000;
  background: #fff;
  text-align: center;
  font-size: 9pt;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  padding: 4px 3px;
  word-break: keep-all;
  line-height: 1.4;
}
.icontent {
  flex: 1;
  padding: 4px 8px;
  font-size: 9.5pt;
  line-height: 1.65;
  word-break: keep-all;
  color: #000;
}

@page { size: A4 portrait; margin: 12mm 14mm 12mm 14mm; }

@media print {
  .sidebar, .nav-bar { display: none !important; }
  .main-content { margin-left: 0 !important; padding: 0 !important; }
  .sub-title { page-break-before: always; break-before: page; }
  .sub-title:first-child { page-break-before: avoid; }
  .card { page-break-after: always; break-after: page; padding: 0 !important; box-shadow: none !important; border: none !important; }
  .cards { gap: 0; }
}

html, body { margin: 0; padding: 0; width: auto; font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif; font-size: 10pt; color: #000; background: #e8e8e8; }
.sidebar { position: fixed; top: 0; left: 0; width: 260px; height: 100vh; background: #222; color: #fff; overflow-y: auto; z-index: 100; display: flex; flex-direction: column; }
.sidebar-header { padding: 14px 12px 10px; font-size: 13pt; font-weight: bold; line-height: 1.4; border-bottom: 1px solid rgba(255,255,255,0.2); flex-shrink: 0; }
.sidebar-search { padding: 7px 10px; flex-shrink: 0; }
.sidebar-search input { width: 100%; padding: 5px 8px; border-radius: 3px; border: none; font-size: 10pt; box-sizing: border-box; }
.toc-major { padding: 7px 12px 3px; font-size: 8.5pt; color: #aaa; font-weight: bold; border-top: 1px solid rgba(255,255,255,0.15); margin-top: 3px; }
.toc-list { list-style: none; margin: 0; padding: 0; }
.toc-list li { margin: 0; }
.toc-link { display: block; padding: 5px 12px 5px 16px; color: #ddd; text-decoration: none; font-size: 9pt; line-height: 1.4; word-break: keep-all; }
.toc-link:hover { background: rgba(255,255,255,0.1); color: #fff; }
.toc-link.active { background: #555; color: #fff; }
.toc-link .cnt { font-size: 8pt; color: #aaa; }
.toc-hidden { display: none; }
.main-content { margin-left: 260px; padding: 20px 24px; min-height: 100vh; }
.sub-section { margin-bottom: 32px; width: 180mm; }
.sub-title { font-size: 11pt; color: #000; margin: 0 0 10px 0; padding: 8px 12px; background: #fff; border-left: 4px solid #000; border-bottom: 1px solid #ccc; word-break: keep-all; width: 180mm; box-sizing: border-box; }
.major-tag { display: inline-block; font-size: 8pt; background: #fff; color: #000; border: 1px solid #000; padding: 1px 6px; border-radius: 2px; margin-right: 7px; font-weight: normal; vertical-align: middle; }
.cards { display: flex; flex-direction: column; gap: 16px; }
.card { background: #fff; border: 1px solid #ccc; padding: 0; width: 180mm; overflow: hidden; }"""

JS = """<script>
const links = document.querySelectorAll('.toc-link');
const sections = document.querySelectorAll('.sub-section');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const id = e.target.id;
      links.forEach(l => l.classList.remove('active'));
      const active = document.querySelector('.toc-link[href="#' + id + '"]');
      if (active) {
        active.scrollIntoView({block:'nearest', behavior:'smooth'});
        active.classList.add('active');
      }
    }
  });
}, {threshold: 0.1});
sections.forEach(s => observer.observe(s));
function filterToc(val) {
  const v = val.trim().toLowerCase();
  links.forEach(l => {
    const label = l.getAttribute('data-label').toLowerCase();
    l.parentElement.classList.toggle('toc-hidden', v && !label.includes(v));
  });
}
</script>"""

def build_sidebar():
    lines = []
    lines.append('<nav class="sidebar" id="sidebar">')
    lines.append('  <div class="sidebar-header">건설안전기술사<br>기출문제 모음</div>')
    lines.append('  <div class="sidebar-search"><input type="text" id="tocSearch" placeholder="세부항목 검색..." oninput="filterToc(this.value)"></div>')
    sec_idx = 0
    for major, details in major_order.items():
        lines.append(f'  <div class="toc-major">{major}</div>')
        lines.append('  <ul class="toc-list">')
        for detail in details:
            cnt = len(detail_order.get((major, detail), []))
            lines.append(f'    <li><a href="#sec-{sec_idx}" class="toc-link" data-label="{detail}">{detail} <span class="cnt">({cnt})</span></a></li>')
            sec_idx += 1
        lines.append('  </ul>')
    lines.append('</nav>')
    return "\n".join(lines)

def build_main():
    lines = []
    lines.append('<main class="main-content">')
    sec_idx = 0
    total_ok = total_skip = 0
    for major, details in major_order.items():
        lines.append('<section>')
        for detail in details:
            ids = detail_order.get((major, detail), [])
            lines.append(f'  <div class="sub-section" id="sec-{sec_idx}">')
            lines.append(f'    <div class="sub-title"><span class="major-tag">{major}</span>{detail}</div>')
            lines.append('  <div class="cards">')
            for fid in ids:
                tbox_html, diag_html = extract_content(fid)
                if not tbox_html:
                    total_skip += 1
                    continue
                lines.append(f'  <div class="card" id="card-{fid}">')
                lines.append(f'    <div class="tbox">{tbox_html}</div>')
                lines.append(f'    {diag_html}')
                lines.append('  </div>')
                total_ok += 1
            lines.append('  </div>')
            lines.append('  </div>')
            sec_idx += 1
        lines.append('</section>')
    lines.append('</main>')
    print(f"  카드 생성: {total_ok}개 성공, {total_skip}개 건너뜀")
    return "\n".join(lines)

def main():
    print("allinone.html 재생성 중...")
    sidebar = build_sidebar()
    main_content = build_main()
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>건설안전기술사 기출문제 모음</title>
<style>
{CSS}
</style>
</head>
<body>

{sidebar}

{main_content}

{JS}
</body>
</html>"""
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
    print(f"완료: {OUT_FILE} ({size_mb:.1f}MB)")

if __name__ == "__main__":
    main()
