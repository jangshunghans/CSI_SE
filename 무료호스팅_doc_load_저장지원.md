# Replit 외 – doc_load 수정·저장 지원 무료 웹호스팅

doc_load 폴더의 **수정**과 **저장 버튼**(또는 자동 저장)이 동작하려면, **Node 서버**가 돌아가고 **디스크에 파일을 쓸 수 있는** 호스팅이어야 합니다. Replit 말고도 아래 서비스들을 사용할 수 있습니다.

---

## 1. Fly.io (권장 대안)

- **특징**: 무료 tier에서 **Persistent Volume** 지원. Node 서버를 띄우고 Volume에 doc_load를 두면 저장이 유지됩니다.
- **doc_load 저장**: Volume을 `/data` 등에 마운트하고, server.js에서 doc_load 경로를 `/data/doc_load`로 두고 `fs.writeFileSync` 하면 됩니다.
- **제한**: 무료는 VM 3개, 스토리지 3GB 등 제한 있음. Docker/`fly.toml` 설정 필요.
- **절차 요약**:
  1. [fly.io](https://fly.io) 가입 후 `flyctl` 설치
  2. `fly launch` 로 앱 생성
  3. `fly volumes create data --size 3 --region iad` 로 Volume 생성
  4. `fly.toml`에 `[mounts]` 추가해 Volume을 `/data`에 마운트
  5. server.js에서 `DOC_LOAD`를 `/data/doc_load`로 변경하고, 배포 시 doc_load 파일들을 Volume에 넣거나 이미지에 포함
  6. `fly deploy` 로 배포
- **문서**: [Fly.io Volumes](https://fly.io/docs/volumes/), [Deploy Node.js to Fly.io with Persistent Storage](https://www.blle.co/blog/deploy-nodejs-apps-to-flyio) 등 참고.

---

## 2. Koyeb

- **특징**: **Volumes** 기능으로 디스크에 데이터 유지. 기술 프리뷰 기간에는 무료로 사용 가능했다는 안내가 있음(현재 정책은 사이트 확인 필요).
- **doc_load 저장**: Volume을 서비스에 붙이고, Node 앱에서 그 경로에 doc_load를 두고 저장하면 됩니다.
- **제한**: 프리뷰/무료 제한·가용 여부는 [Koyeb 문서](https://www.koyeb.com/docs/reference/volumes)에서 확인하세요.

---

## 3. Replit (기존 사용 중)

- **특징**: 브라우저에서 Node 실행, **파일 쓰기 후 재시작해도 유지**되는 파일 시스템 지원.
- **doc_load 저장**: server.js의 `POST /save`와 doc_load 경로 그대로 사용 가능. Run 후 나오는 URL로 접속하면 수정·저장·자동 저장 모두 동작.
- **문서**: `DEPLOY_REPLIT.md`, `REPLIT_사용법.md` 참고.

---

## 4. 사용하지 않는 것이 좋은 서비스 (무료 tier)

| 서비스 | 이유 |
|--------|------|
| **Render** (무료) | 무료 웹 서비스는 **ephemeral 파일시스템**이라, 서버에 쓴 파일이 재시작·재배포 시 사라짐. doc_load 저장 내용이 유지되지 않음. |
| **Vercel / Netlify** (서버리스) | 정적 + 함수만 제공. 로컬 파일 시스템에 쓰는 방식의 server.js를 그대로 쓰기 어렵고, doc_load를 파일로 저장하려면 Blob/DB 등 별도 저장소 연동이 필요함. |
| **GitHub Pages** | 정적 호스팅만 됨. 백엔드·저장 API 없음. |

---

## 5. 비교 요약

| 호스팅 | 무료 tier | doc_load 저장(영구) | 난이도 |
|--------|-----------|---------------------|--------|
| **Replit** | ✅ | ✅ | 낮음 |
| **Fly.io** | ✅ | ✅ (Volume 사용) | 중간 |
| **Koyeb** | 조건부 | ✅ (Volume 사용) | 중간 |
| **Render** (무료) | ✅ | ❌ (ephemeral) | 저장 비추천 |
| **Railway** | 제한적 | Volume 유료 가능성 | 확인 필요 |

---

## 6. 정리

- **Replit 외에** doc_load 수정·저장이 가능한 무료 웹호스팅으로는 **Fly.io**를 우선 추천합니다. Volume 붙여서 doc_load 경로만 맞추면 현재 server.js 구조와 유사하게 쓸 수 있습니다.
- **Koyeb**은 Volume 정책만 확인하면 같은 방식으로 검토할 수 있습니다.
- **Render 무료**, **Vercel/Netlify 정적**, **GitHub Pages**는 doc_load를 서버 디스크에 저장하는 방식에는 적합하지 않습니다.

Fly.io로 옮길 때는 `DOC_LOAD` 경로를 Volume 마운트 경로(예: `/data/doc_load`)로 바꾸고, 배포 시 doc_load 파일들을 그 경로에 넣는 단계만 추가하면 됩니다.
