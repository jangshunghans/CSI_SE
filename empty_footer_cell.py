# -*- coding: utf-8 -*-
"""테이블 마지막 병합 셀 내용 비우기 (추후 이미지 삽입용)"""
from pathlib import Path

def process_file(path):
    path = Path(path)
    if path.suffix.lower() != ".html":
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Read error {path}: {e}")
        return False
    old = '<td colspan="3">구분, 세부 항목, 주요 내용(설명)</td>'
    if old not in content:
        return True
    content = content.replace(old, '<td colspan="3"></td>')
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
