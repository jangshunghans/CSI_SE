# Replit 무료 호스팅 + HTML 편집 시 자동 저장 안내

Replit에 배포하면 **doc_load 문항 페이지에서 편집 시 자동으로 서버에 저장**됩니다.

---

## 1. Replit 배포 절차

### 1) Replit 계정 및 새 Repl 생성 (자세한 단계)

#### ① replit.com 접속 및 로그인

1. 브라우저에서 **https://replit.com** 주소로 이동합니다.
2. **Sign up** 또는 **Log in** 으로 가입/로그인합니다.  
   - Google, GitHub, Facebook 등으로 로그인할 수 있습니다.
3. 로그인 후 **대시보드(홈)** 화면이 나옵니다.  
   - 왼쪽에 내 Repl 목록, 오른쪽이나 상단에 **+ Create Repl** 버튼이 보입니다.

#### ② Create Repl 열기

1. 화면에서 **+ Create Repl** (또는 **Create Repl**) 버튼을 클릭합니다.  
   - 버튼이 보이지 않으면 상단 메뉴의 **Create** 를 눌러도 됩니다.
2. **Create a new Repl** 이라는 제목의 창(모달)이 뜹니다.  
   - 이 창에서 **언어/템플릿**, **제목**, **공개 여부** 등을 정합니다.

#### ③ Template에서 Node.js 선택

1. **Template** 영역에서 사용할 환경을 고릅니다.  
   - 상단에 **All templates**, **Popular** 등 탭이 있을 수 있습니다.
2. **검색창**에 `Node.js` 를 입력하거나, 목록을 스크롤해서 **Node.js** 를 찾습니다.  
   - **Node.js** 아이콘/카드에는 보통 Node 로고(초록색 아이콘)와 "Node.js" 라는 이름이 적혀 있습니다.  
   - 설명에 "JavaScript, npm" 같은 문구가 있는 것을 선택하면 됩니다.
3. **Node.js** 카드를 클릭해 선택합니다.  
   - 한 번 클릭하면 선택된 상태(테두리/강조)로 바뀝니다.  
   - "Node.js" 만 있고 "Express", "Fastify" 등이 붙은 다른 템플릿은 쓰지 않아도 됩니다. **순수 Node.js** 템플릿을 선택합니다.

#### ④ Title(프로젝트 이름) 입력

1. **Title** 입력칸을 찾습니다.  
   - 보통 "Untitled" 로 되어 있거나, 비어 있습니다.
2. 원하는 이름을 입력합니다. 예: **CSI_SE**  
   - 이 이름이 Repl URL에 들어갑니다 (예: `https://CSI_SE.사용자이름.repl.co` 형태가 될 수 있음).

#### ⑤ 공개 설정 (선택)

- **Public** / **Private** 중 하나를 선택할 수 있습니다.  
  - **Public** 이면 링크를 아는 사람이 접속할 수 있습니다.  
  - **Private** 이면 본인만 보거나, 팀원만 초대해 쓸 수 있습니다.  
  - 무료로 공개 사이트를 쓰려면 **Public** 을 선택하면 됩니다.

#### ⑥ Repl 생성 완료

1. **Create Repl** (또는 **Create** / **Create Repl** 버튼)을 클릭합니다.  
   - 화면 하단이나 오른쪽에 있는 큰 버튼입니다.
2. 잠시 후 **코드 에디터 화면**으로 넘어갑니다.  
   - 왼쪽: **Files** (파일 목록), 가운데: **에디터**, 오른쪽: **미리보기/콘솔**  
   - Node.js 템플릿이면 기본으로 `index.js`, `package.json` 등이 보일 수 있습니다.
3. 여기까지가 **Replit 접속 → Create Repl → Node.js 선택** 과정입니다.  
   - 다음 단계에서 이 Repl에 CSI_SE 프로젝트 파일(index.html, server.js, doc_load 등)을 올리면 됩니다.

### 2) 프로젝트 파일 올리기

**방법 A – GitHub에서 가져오기 (권장)**

1. Repl 화면에서 **Version control** (왼쪽 메뉴) → **Import from GitHub**
2. 저장소 URL 입력: `https://github.com/jangshunghans/CSI_SE` (본인 저장소로 변경)
3. Import 후 Replit이 파일을 받아옴

**방법 B – 수동 업로드**

1. Replit 왼쪽 **Files** 패널에서 **Upload file** / **New folder** 로 다음 구조 맞추기  
2. 루트에 올릴 것:
   - `index.html`
   - `csi.json` (없으면 아래 3단계에서 생성)
   - `server.js`
   - `package.json`
   - `doc_load` 폴더 (내부 HTML 전부)

### 3) csi.json 없을 때

- Replit에는 `CSI.xlsx`가 없을 수 있음.  
- **로컬 PC**에서 미리 만들어 둔 `csi.json`을 업로드하거나,  
- Replit에 `CSI.xlsx`와 `build_csi_json.py`를 올린 뒤 Replit Shell에서:
  ```bash
  pip install openpyxl
  python build_csi_json.py
  ```
  실행 후 생성된 `csi.json` 사용

### 4) 패키지 설치 및 서버 실행

1. Replit Shell에서:
   ```bash
   npm install
   ```
2. **Run** 버튼 클릭 (또는 Shell에서 `npm start`)
3. Replit이 자동으로 URL 생성 (예: `https://xxxxxx.xxx.repl.co`)

### 5) 포트 설정 (Replit 규칙)

Replit은 내부 포트를 환경 변수로 알려줍니다. `server.js`가 이 포트를 쓰도록 수정해야 합니다.

**server.js 맨 위 (PORT 정의 부분)를 다음처럼 바꿉니다:**

```javascript
const PORT = process.env.PORT || 3840;
```

이렇게 하면 Replit에서는 `process.env.PORT`, 로컬에서는 3840을 사용합니다.  
(이미 `process.env.PORT`를 쓰고 있다면 그대로 두면 됩니다.)

---

## 2. 자동 저장 사용 방법

### 2-1. 자동 저장이 되는 경우

- **Replit 등 Node 서버**로 사이트를 연 경우  
  → 문항 페이지에서 **수정** 후 **입력이 멈추면 약 2초 뒤 자동으로 서버에 저장**됩니다.

### 2-2. 사용 순서

1. Replit에서 **Run** 후 나온 URL로 접속 (예: `https://xxxxxx.xxx.repl.co`)
2. 메인에서 문항 번호 클릭해 doc_load 문항 페이지로 이동  
   (또는 직접 `https://xxxxxx.xxx.repl.co/doc_load/123-01-01.html` 등으로 이동)
3. **수정** 버튼 클릭
4. 본문·테이블 내용 편집
5. **그대로 두면**  
   - 입력이 멈춘 뒤 **약 2초 후** 자동으로 서버에 저장  
   - 화면 우측 하단에 **「자동 저장됨」** 토스트 표시
6. **저장** 버튼을 눌러도 서버에 저장된 뒤 페이지가 새로고침됨 (수동 저장)

### 2-3. 자동 저장이 안 되는 경우

- GitHub Pages 등 **정적 호스팅**으로만 열었을 때  
  → 서버에 `/save` API가 없어 자동 저장 불가  
  → 이때는 **「자동 저장 불가 (서버에서 열어 주세요)」** 같은 안내가 뜸  
- **Replit URL**로 접속했는지 확인하고, Replit에서 서버가 **Run** 상태인지 확인하면 됨.

---

## 3. 요약

| 항목 | 내용 |
|------|------|
| **호스팅** | Replit (Node.js, 무료) |
| **자동 저장** | 수정 버튼 클릭 후 편집 → **입력 멈춤 후 약 2초 뒤** 서버에 자동 저장 |
| **표시** | 우측 하단 **「자동 저장됨」** 토스트 |
| **수동 저장** | **저장** 버튼 클릭 시에도 서버에 저장 후 새로고침 |
| **접속 주소** | Replit Run 후 표시되는 URL (예: `https://xxxxxx.xxx.repl.co`) |

이렇게 설정하면 **무료 호스팅(Replit) 후, HTML 편집 시 자동 저장**되는 방식으로 사용할 수 있습니다.
