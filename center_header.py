# -*- coding: utf-8 -*-
"""테이블 헤더(구분, 세부 항목, 주요 내용) 가운데 정렬 스타일 추가"""
import re
from pathlib import Path

HEADER_RULE = """
        table tr:first-child td {
            text-align: center;
        }
"""

def process_file(path):
    path = Path(path)
    if path.suffix.lower() != ".html":
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Read error {path}: {e}")
        return False
    if "table tr:first-child td" in content:
        # 이미 있으면 포맷만 정리 (} 다음 줄바꿈, 앞 공백 제거)
        content = re.sub(
            r"(\})\s*\n\s*table tr:first-child td",
            r"\1\n        table tr:first-child td",
            content,
            count=1
        )
        content = re.sub(
            r"(\}\s{2,})table tr:first-child td",
            r"}\n        table tr:first-child td",
            content,
            count=1
        )
        path.write_text(content, encoding="utf-8")
        return True
    # </style> 직전에 헤더 스타일 추가
    content = re.sub(
        r"(\s*)</style>",
        HEADER_RULE + r"\1</style>",
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
