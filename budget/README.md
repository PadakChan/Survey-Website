# 가계부 (Between Seeing & Feeling — Ledger)

작은 Flask 가계부 앱 (화면은 영어). 지출/수입 내역과 월 예산·시작 잔액은
SQLite(`budget/budget.db`)에 저장되고, "Back up to Google Sheets" 버튼으로
전체 내역을 구글 시트에 복사할 수 있다.

## 실행

```bash
.venv/bin/python budget/app.py
# → http://localhost:8765
```

폰에서 쓰려면 컴퓨터와 같은 와이파이에서 `http://<컴퓨터 IP>:8765` 로 접속.
(컴퓨터 IP는 시스템 설정 → Wi-Fi에서 확인)

## 구글 시트 연결 (한 번만 하면 됨)

구글 계정 인증 파일 없이, 시트에 붙이는 작은 스크립트(Apps Script)로 연결한다.

1. [sheets.google.com](https://sheets.google.com)에서 새 시트를 만든다 (이름 예: `가계부 백업`).
2. 시트 메뉴에서 **확장 프로그램 → Apps Script**를 연다.
3. 열려 있는 코드를 전부 지우고 아래 코드를 붙여넣는다:

   ```javascript
   function doPost(e) {
     var entries = JSON.parse(e.postData.contents).entries;
     var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
     sheet.clearContents();
     var rows = [["ID", "Type", "Date", "Category", "Amount", "Tip", "Total", "Note"]];
     entries.forEach(function (x) {
       rows.push([x.id, x.kind, x.date, x.category, x.amount, x.tip, x.total, x.memo]);
     });
     sheet.getRange(1, 1, rows.length, 8).setValues(rows);
     return ContentService
       .createTextOutput(JSON.stringify({ ok: true, rows: entries.length }))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```

4. 오른쪽 위 **배포 → 새 배포**를 누르고:
   - 유형 선택(⚙️): **웹 앱**
   - 다음 사용자 인증 정보로 실행: **나**
   - 액세스 권한이 있는 사용자: **모든 사용자** ← 중요!
   - **배포** → 권한 승인 (내 계정 선택 → "고급" → "이동" → 허용)
5. 나오는 **웹 앱 URL**(`https://script.google.com/macros/s/…/exec`)을 복사한다.
6. `budget/sheet_config.json` 파일을 만들어 URL을 넣는다:

   ```json
   { "webhook_url": "https://script.google.com/macros/s/여기에_복사한_URL/exec" }
   ```

이제 앱에서 **구글 시트로 백업** 버튼을 누르면 시트 전체가 최신 내역으로 다시 채워진다.
(백업은 전체 덮어쓰기 방식이라 여러 번 눌러도 중복이 생기지 않는다.)

스크립트 코드를 수정했다면 **배포 → 배포 관리 → ✏️ → 새 버전**으로 다시 배포해야 반영된다.
