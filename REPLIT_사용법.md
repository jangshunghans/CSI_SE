# replit.com에서 하는 방법 (처음부터 끝까지)

replit.com 웹사이트만 열어서 CSI_SE 프로젝트를 올리고, 실행·편집·자동 저장까지 하는 순서입니다.

---

## 1. replit.com 접속

1. 브라우저에서 **https://replit.com** 입력 후 접속합니다.
2. **Log in** 또는 **Sign up** 으로 로그인합니다.  
   - Google, GitHub, Apple 등으로 가입 가능합니다.

---

## 2. 프로젝트 만들기 (두 가지 중 하나)

### 방법 A – GitHub에 이미 올려둔 경우 (추천)

1. 왼쪽 메뉴에서 **Import code or design** (또는 **Import from GitHub**) 클릭.
2. **GitHub URL** 입력란에 저장소 주소 넣기.  
   - 예: `https://github.com/jangshunghans/CSI_SE`  
   - 본인 계정이면 본인 저장소 주소로 바꿉니다.
3. **Import** 실행 후, Replit이 파일을 받아옵니다.  
   - 곧 에디터 화면으로 넘어가면 성공입니다.
4. **3단계(파일 확인)** 로 넘어갑니다.

### 방법 B – 새로 만드는 경우

1. 왼쪽 메뉴에서 **Create App** (또는 **+ Create Repl**) 클릭.
2. **Template**에서 **Node.js** 선택.  
   - 검색창에 `Node.js` 입력 후, “Node.js” 템플릿(JavaScript, npm) 선택.
3. **Title**에 프로젝트 이름 입력 (예: `CSI_SE`).
4. **Create** (또는 **Create Repl**) 클릭.
5. 에디터가 열리면, **파일 올리기**를 합니다.  
   - 왼쪽 **Files** 패널에서 **⋮(더보기)** → **Upload file**  
   - 또는 폴더 아이콘 옆 **+** → **Upload file**  
   - 올릴 것: `index.html`, `server.js`, `package.json`, `csi.json`  
   - **doc_load** 폴더: 먼저 **New folder** 로 `doc_load` 만들고, 그 안에 HTML 파일들 업로드.
6. **3단계(파일 확인)** 로 넘어갑니다.

---

## 3. 파일 확인

왼쪽 **Files**에 아래가 있는지 봅니다.

- `index.html`
- `server.js`
- `package.json`
- `csi.json` (없어도 됨. 4단계에서 만들 수 있음)
- `doc_load` 폴더 (그 안에 여러 개의 `.html` 파일)

- **server.js**를 열어서 포트 설정이 다음처럼 되어 있는지 확인합니다.  
  ```javascript
  const PORT = process.env.PORT || 3840;
  ```  
  이미 이렇게 되어 있으면 수정할 필요 없습니다.

---

## 4. csi.json이 없을 때

- **csi.json**이 없으면 메인 페이지에서 목록이 비어 보입니다.  
- **방법 1**: 로컬 PC에서 `python build_csi_json.py` 로 만든 **csi.json**을 Replit에 **Upload file**로 올립니다.  
- **방법 2**: Replit에 **CSI.xlsx**, **build_csi_json.py**를 올린 뒤, 아래 **Shell**에서 실행합니다.  
  ```bash
  pip install openpyxl
  python build_csi_json.py
  ```  
  생성된 **csi.json**이 프로젝트 루트에 생깁니다.

---

## 5. 서버 실행 (replit.com에서)

1. 아래쪽 **Shell** 탭을 엽니다.  
   - 없으면 상단 메뉴에서 **Tools** → **Shell** 로 열 수 있습니다.
2. Shell에 다음 입력 후 Enter.  
   ```bash
   npm install
   ```
3. 설치가 끝나면 **Run** 버튼(▶)을 누르거나, Shell에서 다음 입력.  
   ```bash
   npm start
   ```
4. 오른쪽 **Webview**에 사이트가 뜨고, 상단에 **주소**가 표시됩니다.  
   - 예: `https://xxxxxx-xxxx-xxxx.repl.co`  
   - 이 주소가 **실제 접속 주소**입니다. 브라우저 새 탭에서 이 주소로 들어가도 됩니다.

---

## 6. 사용 방법 (replit.com에서 연 상태로)

1. 위에서 나온 **Replit 주소**로 접속합니다.  
   - 예: `https://xxxxxx-xxxx-xxxx.repl.co`
2. **메인 페이지**에서 문항 번호를 클릭하면 **doc_load** 문항 페이지로 이동합니다.  
   - 또는 주소 끝에 직접 입력: `.../doc_load/123-01-01.html`
3. 문항 페이지에서 **수정** 버튼을 누릅니다.
4. 본문·테이블을 편집합니다.
5. **자동 저장**:  
   - 입력을 멈추면 **약 2초 뒤** 서버에 자동 저장됩니다.  
   - 화면 우측 하단에 **「자동 저장됨」** 이 잠깐 뜹니다.  
   - Replit 서버가 켜져 있는 동안만 자동 저장됩니다.
6. **저장** 버튼을 누르면 서버에 저장된 뒤 페이지가 새로고침됩니다.

---

## 7. 요약 (replit.com에서 하는 순서)

| 순서 | 할 일 |
|------|--------|
| 1 | replit.com 접속, 로그인 |
| 2 | **Import code or design** 으로 GitHub 저장소 가져오기 **또는** **Create App** → Node.js 선택 후 파일 업로드 |
| 3 | `index.html`, `server.js`, `package.json`, `doc_load` 등 필요한 파일 있는지 확인 |
| 4 | `csi.json` 없으면 업로드하거나 `build_csi_json.py` 로 생성 |
| 5 | Shell에서 `npm install` → **Run** 또는 `npm start` |
| 6 | 나온 URL로 접속 → 문항 페이지에서 **수정** 후 편집하면 **자동 저장** |

이 순서대로 하면 **replit.com에서만** CSI_SE를 올리고, 실행하고, 편집·자동 저장까지 할 수 있습니다.
