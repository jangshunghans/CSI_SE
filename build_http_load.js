/**
 * doc_load/*.html → http_load/*.html
 * 암기 학습용 A4 모식도 (인쇄 버튼 없음, 폰트 확대, 가독성 최적화)
 * 실행: node build_http_load.js
 */
const fs = require('fs');
const path = require('path');

const DOC_LOAD = path.join(__dirname, 'doc_load');
const HTTP_LOAD = path.join(__dirname, 'http_load');

if (!fs.existsSync(HTTP_LOAD)) fs.mkdirSync(HTTP_LOAD);

// ── 텍스트 유틸 ───────────────────────────────────────
function stripTags(html) {
    return html
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<[^>]+>/g, '')
        .replace(/&nbsp;/g, ' ')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
        .replace(/&quot;/g, '"')
        .trim();
}

// HTML 특수문자 이스케이프 (태그 미포함)
function escBase(str) {
    return (str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

/**
 * 주요내용 텍스트 정리:
 *  - 소스 HTML 줄바꿈(단순 래핑)을 공백으로 합침
 *  - 불릿(•), 번호(①②③…), 가.나.다. 목록 앞에 <br> 삽입
 */
function formatContent(raw) {
    // 1. 각 줄 trim 후 공백으로 합침 (래핑 아티팩트 제거)
    const joined = raw.split('\n').map(s => s.trim()).filter(Boolean).join(' ');
    // 2. HTML 이스케이프
    const esc = escBase(joined);
    // 3. 목록 마커 앞에 줄바꿈 복원
    return esc
        .replace(/\s+([•·])\s*/g, '<br>• ')
        .replace(/\s+([①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳])/g, '<br>$1')
        .replace(/\s+([가나다라마바사아자차카타파하]\.)\s+/g, '<br>$1 ');
}

// ── 테이블 파싱 (rowspan 처리) ──────────────────────────
function parseTableGrid(tableHtml) {
    const rows = [...tableHtml.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)];
    const R = rows.length;
    const C = 5;
    const grid = Array.from({ length: R }, () => new Array(C).fill(null));

    for (let ri = 0; ri < R; ri++) {
        const cells = [...rows[ri][1].matchAll(/<td([^>]*)>([\s\S]*?)<\/td>/gi)];
        let ci = 0;
        for (const cell of cells) {
            while (ci < C && grid[ri][ci] !== null) ci++;
            const attrs = cell[1];
            const inner = cell[2];
            const rs = parseInt((attrs.match(/rowspan="(\d+)"/) || [, 1])[1]);
            const cs = parseInt((attrs.match(/colspan="(\d+)"/) || [, 1])[1]);
            const text = stripTags(inner);
            for (let r = ri; r < Math.min(ri + rs, R); r++) {
                for (let c = ci; c < Math.min(ci + cs, C); c++) {
                    grid[r][c] = { text, isOrigin: r === ri && c === ci, rs, cs };
                }
            }
            ci += cs;
        }
    }
    return grid;
}

// ── 데이터 추출 ────────────────────────────────────────
function extractData(html) {
    // 1차: editableArea + script 패턴
    let areaM = html.match(/<div[^>]+id="editableArea"[^>]*>([\s\S]*?)<\/div>\s*<script/i);
    // 2차: editableArea div (첫 번째 닫힘 태그까지)
    if (!areaM) areaM = html.match(/<div[^>]+id="editableArea"[^>]*>([\s\S]+?)<\/div>/i);
    // 3차: body 전체
    if (!areaM) {
        const bM = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        if (bM) areaM = [null, bM[1]];
    }
    if (!areaM) return null;
    const area = areaM[1];

    // 제목 (<p> 태그)
    const titles = [...area.matchAll(/<p[^>]*>([\s\S]*?)<\/p>/gi)]
        .map(m => stripTags(m[1]))
        .filter(t => t.length > 0);

    // 테이블
    const tableM = area.match(/<table[^>]*>([\s\S]*?)<\/table>/i);
    if (!tableM) return { titles, categories: [] };

    const grid = parseTableGrid(tableM[1]);
    const categories = [];
    let currentCat = null;

    for (let ri = 1; ri < grid.length; ri++) {
        const row = grid[ri];
        const c0 = row[0], c1 = row[1], c2 = row[2];

        // 스페이서 행 (colspan=3 빈 행) 건너뜀
        if (c0 && c0.isOrigin && c0.cs >= 3 && !c0.text) continue;

        // 새 구분(카테고리)
        if (c0 && c0.isOrigin) {
            currentCat = { label: c0.text, items: [] };
            categories.push(currentCat);
        }

        // 세부항목 + 주요내용
        const itemLabel   = (c1 && c1.isOrigin) ? c1.text : '';
        const itemContent = (c2 && c2.isOrigin) ? c2.text : '';
        if ((itemLabel || itemContent) && currentCat) {
            currentCat.items.push({ label: itemLabel, content: itemContent });
        }
    }

    return { titles, categories: categories.filter(c => c.items.length > 0) };
}

// ── HTML 생성 ──────────────────────────────────────────
function generateHtml(id, data) {
    const { titles, categories } = data;

    const titleHtml = titles.map(t => `<div class="tline">${escBase(t)}</div>`).join('');

    const treeHtml = categories.map(cat => {
        const itemsHtml = cat.items.map(item => `
      <div class="item">
        <div class="ilabel">${escBase(item.label)}</div>
        <div class="icontent">${formatContent(item.content)}</div>
      </div>`).join('');

        return `
    <div class="branch">
      <div class="blabel">${escBase(cat.label)}</div>
      <div class="bitems">${itemsHtml}
      </div>
    </div>`;
    }).join('');

    return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>${id}</title>
<style>
/* ── 페이지 설정 (A4) ── */
@page { size: A4 portrait; margin: 14mm 15mm 14mm 15mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
  font-size: 10pt;
  color: #111;
  background: #fff;
  width: 180mm;
}

/* ── 제목 ── */
.tbox {
  background: #1a365d;
  color: #fff;
  text-align: center;
  padding: 9px 12px;
  font-size: 13pt;
  font-weight: bold;
  margin-bottom: 12px;
  border: 2px solid #1a365d;
}
.tline { line-height: 1.55; }

/* ── 모식도 트리 ── */
.diagram { display: flex; flex-direction: column; gap: 5px; }

/* 구분 박스 */
.branch { display: flex; align-items: stretch; }
.blabel {
  width: 64px; min-width: 64px;
  border: 2px solid #2b6cb0;
  background: #bee3f8;
  text-align: center;
  font-weight: bold;
  font-size: 10pt;
  display: flex; align-items: center; justify-content: center;
  padding: 5px 3px;
  word-break: keep-all;
  line-height: 1.45;
}

/* 연결선 */
.bitems {
  flex: 1;
  display: flex; flex-direction: column; gap: 3px;
  padding-left: 7px;
  border-left: 2.5px solid #2b6cb0;
  margin-left: 6px;
}

/* 세부항목 행 */
.item { display: flex; align-items: stretch; border: 1.5px solid #90cdf4; }
.ilabel {
  width: 92px; min-width: 92px;
  border-right: 1.5px solid #90cdf4;
  background: #ebf8ff;
  text-align: center;
  font-size: 9.5pt;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  padding: 5px 3px;
  word-break: keep-all;
  line-height: 1.45;
}

/* 주요내용 */
.icontent {
  flex: 1;
  padding: 5px 9px;
  font-size: 10pt;
  line-height: 1.7;
  word-break: keep-all;
  color: #1a202c;
}

/* 인쇄 시 색상 강제 출력 */
@media print {
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
</head>
<body>
<div class="tbox">${titleHtml}</div>
<div class="diagram">${treeHtml}</div>
</body>
</html>`;
}

// ── 메인 ──────────────────────────────────────────────
const files = fs.readdirSync(DOC_LOAD).filter(f => /\.html$/i.test(f)).sort();
let done = 0, errors = 0;

for (const file of files) {
    try {
        const html = fs.readFileSync(path.join(DOC_LOAD, file), 'utf8');
        const data = extractData(html);
        if (!data) {
            console.warn(`SKIP (구조 파싱 불가): ${file}`);
            errors++;
            continue;
        }
        const id = path.basename(file, '.html');
        fs.writeFileSync(path.join(HTTP_LOAD, file), generateHtml(id, data), 'utf8');
        done++;
    } catch (e) {
        console.error(`ERROR: ${file} → ${e.message}`);
        errors++;
    }
}

console.log(`\n완료: ${done}개 생성, ${errors}개 오류`);
console.log(`출력: ${HTTP_LOAD}`);
