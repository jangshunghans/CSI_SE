# -*- coding: utf-8 -*-
"""
각 HTML 파일의 테이블에서 '구분' 열의 연속된 중복 값을 rowspan으로 하나로 합칩니다.
"""
import re
from pathlib import Path

def normalize_text(s):
    """공백/줄바꿈 정규화하여 비교용 문자열 반환"""
    if s is None:
        return ""
    return " ".join(re.split(r"\s+", s.strip()))

def merge_gubun_in_html(html_content):
    """테이블의 구분 열에서 연속 중복을 rowspan으로 통합"""
    # 헤더 행 찾기: <tr> ... <td>구분</td> ...
    # 데이터 행들에서 첫 번째 td가 구분값
    lines = html_content.split("\n")
    result_lines = []
    i = 0
    in_table = False
    table_start = -1

    while i < len(lines):
        line = lines[i]
        result_lines.append(line)

        # <table> 시작
        if "<table>" in line or "<table " in line:
            in_table = True
            table_start = len(result_lines) - 1

        if in_table and "</table>" in line:
            in_table = False
            i += 1
            continue

        # 테이블 내부에서 <tr><td> 구분 행(헤더) 다음의 데이터 행 처리
        if in_table and "<tr>" in line:
            # 이 tr 블록 전체 수집 (다음 </tr>까지)
            tr_block = [line]
            j = i + 1
            while j < len(lines) and "</tr>" not in lines[j]:
                tr_block.append(lines[j])
                j += 1
            if j < len(lines):
                tr_block.append(lines[j])

            full_tr = "\n".join(tr_block)
            # 헤더 행인지 확인: <td>구분</td>
            if "<td>구분</td>" in full_tr or ">구분</td>" in full_tr:
                result_lines.extend(tr_block[1:])
                i = j
                i += 1
                continue

            # 데이터 행: td들을 추출
            tds = re.findall(r"<td>([\s\S]*?)</td>", full_tr)
            if len(tds) >= 3:  # 구분, 세부 항목, 주요 내용
                gubun = tds[0]
                # 이 행은 그대로 두고, 다음 행들에서 같은 구분이 연속되면 rowspan 처리할 것은
                # 별도 패스에서 처리. 여기서는 한 번에 테이블 전체를 파싱하는 게 나을 수 있음.
                result_lines.extend(tr_block[1:])
                i = j
                i += 1
                continue

            result_lines.extend(tr_block[1:])
            i = j
            i += 1
            continue

        i += 1

    return "\n".join(result_lines)

def merge_gubun_with_rowspan(html_content):
    """
    테이블 전체를 파싱하여 구분 열의 연속 중복을 rowspan으로 통합.
    """
    # 정규식으로 테이블 내용 추출 후 행 단위 처리
    table_match = re.search(
        r"<table[^>]*>([\s\S]*?)</table>",
        html_content,
        re.DOTALL
    )
    if not table_match:
        return html_content

    before_table = html_content[: table_match.start()]
    after_table = html_content[table_match.end() :]
    table_inner = table_match.group(1)

    # 각 <tr>...</tr> 블록 추출
    tr_pattern = re.compile(r"<tr>\s*([\s\S]*?)\s*</tr>", re.DOTALL)
    rows = tr_pattern.findall(table_inner)

    if not rows:
        return html_content

    # 헤더 행
    new_rows = [rows[0]]
    # 데이터 행들
    data_rows = rows[1:]
    if not data_rows:
        return html_content

    # 각 데이터 행의 td 3개 추출
    td_pattern = re.compile(r"<td>\s*([\s\S]*?)\s*</td>", re.DOTALL)
    parsed = []
    for row in data_rows:
        tds = td_pattern.findall(row)
        if len(tds) >= 3:
            parsed.append({
                "gubun": tds[0],
                "gubun_raw": tds[0],  # 원본(공백/줄바꿈 유지)
                "sebu": tds[1],
                "content": tds[2],
                "row_html": row,
            })
        else:
            parsed.append(None)

    # 연속 같은 구분 그룹에 rowspan 적용
    new_table_rows = ["<tr>\n" + rows[0].strip() + "\n</tr>"]
    i = 0
    while i < len(parsed):
        if parsed[i] is None:
            new_table_rows.append("<tr>\n" + data_rows[i] + "\n</tr>")
            i += 1
            continue
        gubun_raw = parsed[i]["gubun_raw"]
        gubun_norm = normalize_text(parsed[i]["gubun"])
        span = 1
        j = i + 1
        while j < len(parsed) and parsed[j] is not None and normalize_text(parsed[j]["gubun"]) == gubun_norm:
            span += 1
            j += 1

        # 첫 행: 구분 td에 rowspan, 나머지 두 td
        if span == 1:
            new_table_rows.append(
                "<tr>\n<td>"
                + gubun_raw.strip()
                + "</td>\n<td>"
                + parsed[i]["sebu"].strip()
                + "</td>\n<td>"
                + parsed[i]["content"].strip()
                + "</td>\n</tr>"
            )
        else:
            new_table_rows.append(
                "<tr>\n<td rowspan=\""
                + str(span)
                + "\">"
                + gubun_raw.strip()
                + "</td>\n<td>"
                + parsed[i]["sebu"].strip()
                + "</td>\n<td>"
                + parsed[i]["content"].strip()
                + "</td>\n</tr>"
            )
        for k in range(i + 1, j):
            # 구분 td 없이 세부항목, 주요내용만
            new_table_rows.append(
                "<tr>\n<td>"
                + parsed[k]["sebu"].strip()
                + "</td>\n<td>"
                + parsed[k]["content"].strip()
                + "</td>\n</tr>"
            )
        i = j

    table_start_tag = re.match(r"<table[^>]*>", html_content[table_match.start() : table_match.start() + 200])
    tag = table_start_tag.group(0) if table_start_tag else "<table>"
    new_table = tag + "\n" + "\n".join(new_table_rows) + "\n</table>"
    return before_table + new_table + after_table

def process_file(path):
    path = Path(path)
    if not path.suffix.lower() == ".html":
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Read error {path}: {e}")
        return False
    new_content = merge_gubun_with_rowspan(content)
    if new_content == content:
        return True
    try:
        path.write_text(new_content, encoding="utf-8")
    except Exception as e:
        print(f"Write error {path}: {e}")
        return False
    return True

def main():
    doc_load = Path(__file__).resolve().parent / "doc_load"
    if not doc_load.is_dir():
        print("doc_load folder not found")
        return
    count = 0
    for f in sorted(doc_load.glob("*.html")):
        if process_file(f):
            count += 1
    print(f"Processed {count} files.")

if __name__ == "__main__":
    main()
