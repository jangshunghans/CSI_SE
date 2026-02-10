# CSI_SE

> CSI 자료 조회 웹앱. GitHub Pages, Vercel, Netlify 등에 배포 가능합니다.

---

## 📤 배포 방법

### GitHub Pages에 배포 (https://jangshunghans.github.io/CSI_SE/)

이 저장소를 **jangshunghans/CSI_SE**로 푸시한 뒤, GitHub Pages만 켜면 아래 주소로 공개됩니다.

**배포 URL:** [https://jangshunghans.github.io/CSI_SE/](https://jangshunghans.github.io/CSI_SE/)

**순서:**

1. **데이터 파일 생성** (CSI.xlsx가 있을 때마다 실행)
   ```bash
   python build_csi_json.py
   ```
   → 프로젝트 루트에 `csi.json`이 생성됩니다.

2. **GitHub 저장소에 푸시**
   ```bash
   cd D:\whanin_rpa\CSI_SE
   git add index.html csi.json doc_load
   git commit -m "CSI 조회 배포"
   git push origin main
   ```
   - 아직 원격이 없다면:
     ```bash
     git remote add origin https://github.com/jangshunghans/CSI_SE.git
     git branch -M main
     git push -u origin main
     ```

3. **GitHub Pages 켜기**
   - GitHub에서 **jangshunghans/CSI_SE** 저장소 열기  
   - **Settings** → 왼쪽 메뉴 **Pages**  
   - **Source**: `Deploy from a branch`  
   - **Branch**: `main` (또는 사용 중인 브랜치), 폴더 **/ (root)**  
   - **Save** 클릭

4. **반영 대기**  
   몇 분 후 [https://jangshunghans.github.io/CSI_SE/](https://jangshunghans.github.io/CSI_SE/) 에 접속하면 배포된 페이지가 보입니다.

**주의:** `csi.json`이 없으면 목록이 비어 보입니다. 배포 전에 반드시 `python build_csi_json.py`를 실행하고, 생성된 `csi.json`을 커밋·푸시하세요.

---

### Git에 다시 배포하기 (수정 후 업데이트)

내용을 수정한 뒤 같은 저장소에 다시 올리려면:

```bash
cd D:\whanin_rpa\CSI_SE

# 1) CSI.xlsx를 수정했다면 데이터 다시 생성
python build_csi_json.py

# 2) 변경된 파일 모두 스테이징
git add .

# 3) 커밋 (메시지는 수정 내용에 맞게)
git commit -m "doc_load 테이블 선 개선, 수정 버튼 스크립트 수정 등 반영"

# 4) 원격 저장소로 푸시
git push origin main
```

푸시가 끝나면 GitHub Pages는 자동으로 다시 빌드합니다. 1~2분 뒤 [https://jangshunghans.github.io/CSI_SE/](https://jangshunghans.github.io/CSI_SE/) 에서 변경 내용을 확인하면 됩니다.

- **특정 파일만 올리기:** `git add index.html doc_load` 처럼 경로만 지정 후 `git commit` → `git push origin main`
- **원격이 안 되어 있을 때:** `git remote add origin https://github.com/jangshunghans/CSI_SE.git` 후 `git push -u origin main`

---

### 1. 정적 배포 (권장: GitHub Pages / Vercel / Netlify)

데이터는 **csi.json**으로 제공되며, Excel 파일 없이 동작합니다.

**배포 전 한 번 실행 (CSI.xlsx가 수정되었을 때):**

```bash
python build_csi_json.py
```

**배포에 포함할 것:**

| 항목 | 설명 |
|------|------|
| `index.html` | 메인 화면 (검색 조건 + 조회 결과) |
| `csi.json` | 조회 데이터 (위 스크립트로 생성) |
| `doc_load/` | 문항별 HTML 파일 전체 |

**배포 절차 요약:**

1. **GitHub Pages**  
   - 저장소에 푸시 후: **Settings → Pages → Source**: `main` 브랜치, `/ (root)`  
   - 사이트 URL: `https://<사용자명>.github.io/<저장소명>/`

2. **Vercel**  
   - [vercel.com](https://vercel.com) → **Add New Project** → 저장소 연결  
   - Build 설정 없이 **Deploy** (정적 사이트)

3. **Netlify**  
   - [netlify.com](https://netlify.com) → **Add new site → Import from Git** → 저장소 선택  
   - Publish directory: **`.`** (프로젝트 루트)

> ⚠️ 정적 배포 시 `csi.json`이 없으면 데이터가 안 보입니다. 반드시 `python build_csi_json.py` 실행 후 `csi.json`을 커밋하세요.

---

### 2. Node 서버 배포 (CSI.xlsx 직접 사용)

CSI.xlsx를 서버에서 직접 읽어 `/api/csi`로 제공하는 방식입니다.

```bash
npm install
npm start
```

- 포트: **3840**  
- 메인: `http://서버주소:3840/`  
- 문항 링크: `http://서버주소:3840/doc_load/123-01-01.html` 형태로 동작

**서버 호스팅 시:**  
Node가 설치된 VPS/클라우드에서 위처럼 실행하고, 필요하면 **pm2**, **systemd** 등으로 백그라운드 실행 및 재시작 설정을 하면 됩니다.

---

## 🚀 로컬에서 보기

| 방식 | 명령 |
|------|------|
| **정적** | `npx serve .` → 브라우저에서 `http://localhost:3000/` |
| **Node (CSI.xlsx 사용)** | `npm start` → `http://localhost:3840/` |

`index.html`을 브라우저에서 직접 열면 `csi.json` 로드가 보안 제한으로 실패할 수 있으므로, 로컬에서는 `npx serve .` 또는 `npm start` 사용을 권장합니다.

---

## 📦 GitHub에 올리기

```bash
cd D:\whanin_rpa\CSI_SE

# csi.json 생성 (CSI.xlsx 기준)
python build_csi_json.py

git init
git add .
git commit -m "Initial commit"

# GitHub에서 새 저장소(예: CSI_SE) 생성 후
git remote add origin https://github.com/your-username/CSI_SE.git
git branch -M main
git push -u origin main
```

---

## 🌐 무료 웹 호스팅 요약

| 플랫폼 | 설정 |
|--------|------|
| **GitHub Pages** | Settings → Pages → Source: main, root |
| **Vercel** | Import Git → Deploy (정적) |
| **Netlify** | Import from Git → Publish directory: `.` |
