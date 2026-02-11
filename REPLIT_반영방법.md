# Replit(https://replit.com/@sunghanjang/CSISE)에 반영하는 방법

로컬에서 수정한 내용을 **Replit 프로젝트(CSISE)** 에 반영하는 두 가지 흐름입니다.

---

## 방법 1: GitHub 경유 (권장)

로컬 → **GitHub** → **Replit** 순서로 반영합니다.

### 1단계: 로컬에서 GitHub에 푸시

로컬 프로젝트 폴더에서 터미널(또는 Cursor 터미널)을 열고:

```powershell
cd d:\whanin_rpa\CSI_SE

git add .
git commit -m "No/주요항목 컬럼 분리 등 수정"
git push origin main
```

- 브랜치가 `master`이면: `git push origin master`
- GitHub 로그인/토큰 입력이 나오면 처리합니다.

### 2단계: Replit에서 GitHub 내용 가져오기

1. **https://replit.com/@sunghanjang/CSISE** 에 접속해 프로젝트를 엽니다.
2. 왼쪽 메뉴에서 **Version control** (또는 **Git** / **소스 제어**) 를 엽니다.
3. **Pull** 또는 **Sync from GitHub** / **Pull from remote** 를 클릭합니다.  
   - Replit이 이 프로젝트를 GitHub 저장소와 연결해 둔 경우, 최신 커밋이 당겨집니다.
4. 연결이 안 되어 있다면:
   - **Connect to GitHub** 또는 **Import from GitHub** 로 **본인 GitHub의 CSI_SE 저장소**를 연결한 뒤,
   - 다시 **Pull** 합니다.

이후 Replit에서 **Run** 하면 반영된 코드로 실행됩니다.

---

## 방법 2: 수정된 파일만 Replit에 업로드

GitHub를 쓰지 않고, 바뀐 파일만 Replit에 올리는 방법입니다.

### 1단계: 로컬에서 어떤 파일이 바뀌었는지 확인

이번에 수정한 것처럼 **No/주요항목 구분**은 **index.html** 한 파일만 바뀌었을 수 있습니다.  
다른 수정(자동 저장, doc_load 등)을 함께 반영하려면 해당 파일들을 함께 올리면 됩니다.

### 2단계: Replit에 파일 올리기

1. **https://replit.com/@sunghanjang/CSISE** 접속 후 프로젝트 열기.
2. 왼쪽 **Files** 패널에서 반영할 파일을 선택합니다.  
   - **index.html** 을 로컬에서 수정했다면, Replit에서 **index.html** 선택.
3. 해당 파일을 **덮어쓰기** 합니다.  
   - **방법 A**: Replit에서 `index.html` 이름 옆 **⋮(더보기)** → **Upload file** 또는 **Replace with file** → 로컬의 `d:\whanin_rpa\CSI_SE\index.html` 선택.  
   - **방법 B**: 로컬에서 `index.html` 내용 전체 복사 → Replit에서 `index.html` 열기 → 기존 내용 전체 선택 후 붙여넣기 → 저장.
4. **doc_load** 안의 HTML이나 **server.js** 등도 수정했다면, 같은 방식으로 해당 파일들도 Replit에 업로드하거나 붙여넣기 합니다.

저장 후 **Run** 하면 반영된 내용으로 동작합니다.

---

## 요약

| 방법 | 순서 |
|------|------|
| **1. GitHub 경유** | 로컬 `git add` → `git commit` → `git push` → Replit에서 **Version control** → **Pull** |
| **2. 파일 업로드** | 로컬에서 수정한 파일만 Replit **Files**에서 업로드 또는 복사·붙여넣기 |

Replit이 이미 GitHub 저장소와 연결되어 있으면 **방법 1**이 가장 간단하고, 연결이 없거나 일부 파일만 올리고 싶으면 **방법 2**를 사용하면 됩니다.
