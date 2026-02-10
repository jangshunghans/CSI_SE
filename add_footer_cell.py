# -*- coding: utf-8 -*-
"""각 페이지 테이블 마지막에 구분·세부 항목·주요 내용(설명) 병합 셀 추가"""
import re
from pathlib import Path

FOOTER_ROW = """
<tr>
<td colspan="3">구분, 세부 항목, 주요 내용(설명)</td>
</tr>"""

def process_file(path):
    path = Path(path)
    if path.suffix.lower() != ".html":
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Read error {path}: {e}")
        return False
    # 이미 추가된 경우 스킵
    if "colspan=\"3\"" in content and "구분, 세부 항목, 주요 내용(설명)" in content:
        return True
    # </table> 직전에 행 추가
    content = re.sub(
        r"(\s*)(</table>)",
        FOOTER_ROW + r"\n\1\2",
        content,
        count=1
    )
    try:
        path.write_text(content, encoding="utf-8")
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
