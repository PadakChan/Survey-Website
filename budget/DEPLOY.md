# 가계부를 PythonAnywhere에 배포하기 (무료)

배포하면 `https://내아이디.pythonanywhere.com` 주소로 폰이든 컴퓨터든
어디서나 접속되고, 데이터는 서버 한 곳에 저장되며, 구글 시트 백업 버튼도
그대로 작동한다. 소요 시간 약 15분, 카드 등록 불필요.

## 1. 계정 만들기

1. [pythonanywhere.com](https://www.pythonanywhere.com) → **Pricing & signup** → **Create a Beginner account** (무료).
2. 아이디가 곧 주소가 된다: 아이디가 `padakchan`이면 → `padakchan.pythonanywhere.com`.

## 2. 코드 받기

로그인 후 **Consoles** 탭 → **Bash** 클릭. 검은 터미널이 열리면 한 줄씩 입력:

```bash
git clone https://github.com/PadakChan/Survey-Website.git
mkvirtualenv ledger --python=python3.11
pip install flask
```

## 3. 웹 앱 만들기

1. **Web** 탭 → **Add a new web app** → (주소 확인, Next) → **Manual configuration** → **Python 3.11**.
2. 생성된 설정 화면에서 아래 세 가지를 채운다 (`내아이디`는 본인 아이디로!):
   - **Source code**: `/home/내아이디/Survey-Website/budget`
   - **Virtualenv**: `/home/내아이디/.virtualenvs/ledger`
   - **WSGI configuration file**: 파란 링크를 눌러 열고, **내용 전체를 지운 뒤** 아래로 교체:

   ```python
   import os
   import sys

   path = '/home/내아이디/Survey-Website/budget'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['LEDGER_PASSWORD'] = '여기에_원하는_비밀번호'

   from app import app as application
   ```

   저장(Save) 버튼을 누른다. `LEDGER_PASSWORD`는 앱 접속 비밀번호다 —
   인터넷에 공개되는 주소이므로 꼭 설정할 것. 접속하면 로그인 창이 뜨는데,
   **username은 아무거나, password에 이 비밀번호**를 넣으면 된다.

3. **Web** 탭 상단의 초록색 **Reload** 버튼을 누른다.
4. `https://내아이디.pythonanywhere.com` 접속 → 로그인 → 끝!

## 4. 구글 시트 연결 (선택)

`README.md`의 Apps Script 설정을 마쳤다면, Bash 콘솔에서 (URL은 본인 것으로):

```bash
echo '{ "webhook_url": "https://script.google.com/macros/s/…/exec" }' > ~/Survey-Website/budget/sheet_config.json
```

입력 후 **Web** 탭에서 **Reload**. 이제 서버에서도 백업 버튼이 작동한다.

## 5. 폰 홈 화면에 추가

폰 브라우저로 접속한 뒤 — iPhone: 공유 버튼 → "홈 화면에 추가" /
Android: 메뉴(⋮) → "홈 화면에 추가". 앱 아이콘처럼 쓸 수 있다.

## 나중에 코드를 수정하면

1. 내 컴퓨터에서 커밋 + `git push`
2. PythonAnywhere Bash 콘솔: `cd ~/Survey-Website && git pull`
3. **Web** 탭 → **Reload**

## 알아둘 것

- **3개월마다 연장 버튼**: 무료 계정은 Web 탭에 "Run until…" 노란 버튼이 있는데,
  3개월에 한 번 눌러줘야 앱이 계속 돈다 (만료 전 이메일이 온다).
- 데이터(`budget.db`)는 서버에 저장되므로 git pull 해도 지워지지 않는다.
- 컴퓨터의 로컬 앱(`http://localhost:8765`)과 서버 데이터는 서로 별개다 —
  배포 후에는 서버 주소 하나만 쓰는 것을 추천.
