# -*- coding: utf-8 -*-
"""테이블의 구분·세부 항목 열만 가운데 정렬 (주요 내용은 왼쪽 유지)"""
import re
from pathlib import Path

OLD_PATTERN = re.compile(
    r"table tr:first-child td \{\s*text-align: center;\s*\}"
)
NEW_RULE = """table tr td:first-child,
        table tr td:nth-child(2) {
            text-align: center;
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
    # 들여쓰기 정리 (이미 적용된 파일)
    content = re.sub(
        r"(\n\s{12,})table tr td:first-child",
        "\n        table tr td:first-child",
        content,
        count=1
    )
    changed = False
    # 기존: table tr:first-child td { ... } → 구분·세부 항목 열 전체 적용으로 교체
    if OLD_PATTERN.search(content):
        content = OLD_PATTERN.sub(NEW_RULE, content, count=1)
        changed = True
    elif "table tr td:first-child" not in content:
        # 아직 헤더만 가운데 규칙도 없으면 </style> 직전에 추가
        content = re.sub(
            r"(\s*)</style>",
            "\n        " + NEW_RULE + "\n    </style>",
            content,
            count=1
        )
        changed = True
    # 들여쓰기 수정 시에도 저장
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
