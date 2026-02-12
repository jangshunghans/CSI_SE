# Replit에 배포 방법

CSI_SE를 Replit에 올리고 실행·반영하는 방법을 한 문서로 정리했습니다.

---

## 1. 처음 Replit에 배포할 때

### 1) replit.com 접속

1. 브라우저에서 **https://replit.com** 접속
2. **Log in** / **Sign up** (Google, GitHub 등 가능)

---

### 2) 프로젝트 가져오기 (둘 중 하나)

#### 방법 A – GitHub에서 가져오기 (권장)

1. 왼쪽 메뉴 **Import code or design** (또는 **Import from GitHub**) 클릭
2. **GitHub URL** 입력: `https://github.com/jangshunghans/CSI_SE` (본인 저장소면 해당 주소로)
3. **Import** 실행 → Replit이 파일을 받아옴
4. **4단계(실행)** 로 이동

#### 방법 B – 새 앱 만들고 파일 올리기

1. 왼쪽 메뉴 **Create App** (또는 **+ Create Repl**) 클릭
2. **Template**에서 **Node.js** 선택
3. **Title**에 `CSI_SE` 등 입력 후 **Create** 클릭
4. 왼쪽 **Files**에서 **Upload file** / **New folder** 로 다음을 올림  
   - 루트: `index.html`, `server.js`, `package.json`, `csi.json`  
   - `doc_load` 폴더 생성 후, 그 안에 doc_load용 HTML 파일들 업로드
5. **4단계(실행)** 로 이동

---

### 3) 파일·설정 확인

- **Files**에 `index.html`, `server.js`, `package.json`, `doc_load` 폴더 있는지 확인
- **server.js**에서 포트가 아래처럼 되어 있는지 확인 (이미 있으면 수정 불필요)
  ```javascript
  const PORT = process.env.PORT || 3840;
  ```
- **csi.json**이 없으면: 로컬에서 만든 파일을 업로드하거나, Replit에 `CSI.xlsx`·`build_csi_json.py` 올린 뒤 Shell에서:
  ```bash
  pip install openpyxl
  python build_csi_json.py
  ```

---

### 4) 실행 (배포)

1. 아래쪽 **Shell** 탭 열기
2. Shell에서 실행:
   ```bash
   npm install
   ```
3. **Run** 버튼(▶) 클릭 또는 Shell에서:
   ```bash
   npm start
   ```
4. 오른쪽 **Webview** 상단에 나오는 주소가 **배포된 웹 주소**입니다.  
   예: `https://CSI_SE.sunghanjang.repl.co`  
   이 주소로 접속하면 메인·doc_load(수정·저장) 사용 가능합니다.

---

## 2. 이미 Replit 프로젝트가 있을 때 (수정 반영)

로컬에서 수정한 내용을 Replit(예: https://replit.com/@sunghanjang/CSISE)에 반영하는 방법입니다.

### 방법 1 – GitHub 경유 (권장)

1. **로컬에서 GitHub에 푸시**
   ```powershell
   cd d:\whanin_rpa\CSI_SE
   git add .
   git commit -m "수정 내용 요약"
   git push origin main
   ```
2. **Replit에서 가져오기**
   - Replit 프로젝트 열기 (예: replit.com/@sunghanjang/CSISE)
   - 왼쪽 메뉴 **Version control** (또는 **Git**) → **Pull** / **Sync from GitHub** 클릭
   - GitHub와 연결이 안 되어 있으면 **Connect to GitHub**로 CSI_SE 저장소 연결 후 다시 Pull
3. Replit에서 **Run** 하면 반영된 내용으로 실행됩니다.

### 방법 2 – 파일만 올리기

1. Replit 프로젝트 열기
2. 왼쪽 **Files**에서 수정한 파일 선택 (예: `index.html`)
3. **⋮(더보기)** → **Upload file** 또는 **Replace with file**로 로컬 파일로 덮어쓰기  
   또는 로컬에서 내용 복사 → Replit에서 해당 파일 열어 붙여넣기 → 저장
4. **Run** 하면 반영된 내용으로 실행됩니다.

---

## 3. 배포된 웹 주소

- **Replit 편집 화면**: `https://replit.com/@사용자이름/프로젝트이름`  
  예: https://replit.com/@sunghanjang/CSISE
- **실제 웹사이트(사이트 접속 주소)**: Run 후 Webview에 표시되는 주소  
  예: `https://CSI_SE.sunghanjang.repl.co` 또는 `https://xxxxxx.repl.co`  
  - 메인: `https://[주소]/`  
  - 문항: `https://[주소]/doc_load/123-01-01.html`

---

## 4. 요약

| 단계 | 할 일 |
|------|--------|
| **처음 배포** | replit.com 접속 → **Import from GitHub**(저장소 URL) 또는 **Create App** → Node.js → 파일 업로드 |
| **실행** | Shell에서 `npm install` → **Run** 또는 `npm start` |
| **수정 반영** | 로컬에서 `git push` 후 Replit **Version control** → **Pull** 또는 수정 파일만 업로드 |
| **웹 주소** | Run 후 Webview에 표시되는 `https://xxx.repl.co` 주소로 접속 |

이 순서대로 하면 Replit에 배포하고, 수정 내용도 반영할 수 있습니다.
