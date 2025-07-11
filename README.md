# 🧑‍💼 Benepia 자동 로그인

benepia 홈페이지에 자동 로그인해주는 셀레니움 기반 Python 스크립트입니다.  
크롬 드라이버 최신 버전 자동 다운로드 → 브라우저 자동 실행 → 로그인까지 처리됩니다.

---

## 📦 의존성 설치

먼저 Python 3.x 환경에서 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

## ⚙️ 설정: 사용자 계정 정보

로그인을 위해 사용자 ID와 비밀번호를 benepia_config.json에 아래 형식으로 작성합니다:

```bash
{
  "ID": "your_user_id",
  "PASSWD": "your_password",
  "LOGIN_URL": "benefia address"
}
```

해당 파일은 benepia_login.py와 같은 폴더에 위치해야 합니다.

## ▶️ 실행 방법

```bash
python benepia.py

```

실행하면 다음을 자동으로 처리합니다:

1. 크롬 드라이버 최신 버전 확인 및 다운로드 (필요 시)

2. 셀레니움으로 크롬 브라우저 실행

3. benepia 로그인 페이지로 이동 후 자동 로그인

4. 로그인 완료된 창 그대로 유지

## 🪄 .exe 실행파일로 만들기 (옵션)

Windows 환경에서 .exe 실행파일로 패키징하고 싶다면 다음 명령을 사용하세요:

```bash
pyinstaller --onefile --icon=benepia_icon.ico benepia_login.py
```

빌드 후 dist/benepia_login.exe 파일이 생성됩니다.
.exe 파일은 benepia_config.json과 같은 폴더에 두고 실행해야 정상 작동합니다.

## 🛠 필요 파일 구성

```bash
/프로젝트/
├── benepia_login.py           # 메인 자동화 스크립트
├── benepia_config.json        # 사용자 로그인 정보
├── benepia_icon.ico         # exe 아이콘 (선택)
├── chromedriver.exe        # 크롬 드라이버 (자동 생성/업데이트됨)
├── requirements.txt        # 의존성 목록
```

🔐 보안 주의
benepia_config.json에는 민감한 정보(ID/PW)가 포함되므로 절대 Git에 커밋하지 마세요!

.gitignore에 반드시 아래 항목 포함:

```bash
benepia_config.json
build/
*.spec
__pycache__/
```
