# CSI.xlsx -> csi.json 변환 (정적 호스팅용)
import json
import openpyxl

def main():
    wb = openpyxl.load_workbook("CSI.xlsx", read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not rows:
        return
    headers = [str(h) for h in rows[0]]
    data = []
    for row in rows[1:]:
        item = {}
        for i, h in enumerate(headers):
            if i < len(row):
                v = row[i]
                item[h] = v if v is None else (int(v) if isinstance(v, float) and v == int(v) else v)
        data.append(item)
    with open("csi.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    print("csi.json 생성 완료:", len(data), "건")

if __name__ == "__main__":
    main()
