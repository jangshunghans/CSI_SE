# -*- coding: utf-8 -*-
"""테이블의 설명 열(주요 내용, 3번째 열) 왼쪽 정렬 명시"""
import re
from pathlib import Path

# 이미 있으면 스킵
MARKER = "td:nth-child(3)"
LEFT_RULE = """        table tr td:nth-child(3) {
            text-align: left;
        }"""

def process_file(path):
    path = Path(path)
    if path.suffix.lower() != ".html":
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Read error {path}: {e}")
        return False
    if "td:nth-child(3)" in content and "text-align: left" in content:
        return True
    # 구분·세부 항목 center 규칙 다음에 추가 (또는 </style> 직전)
    if "table tr td:nth-child(2)" in content:
        content = re.sub(
            r"(table tr td:nth-child\(2\) \{\s*text-align: center;\s*\})\s*(\n\s*</style>)",
            r"\1\n        table tr td:nth-child(3) {\n            text-align: left;\n        }\2",
            content,
            count=1
        )
    else:
        content = re.sub(
            r"(\s*)</style>",
            "\n" + LEFT_RULE + "\n    </style>",
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
