# QuizzTrivia — Performance Test Suite

## Cấu trúc thư mục

```
perf-tests/
├── scripts/
│   ├── create_test_accounts.py
│   └── refresh_tokens.py
├── data/
│   ├── accounts.csv       # 200 test accounts (đã có sẵn)
│   ├── users.csv          # ID Tokens — refresh trước mỗi lần test
│   ├── quizzes.csv        # 3 quiz ID thực (đã điền sẵn)
│   └── questions.csv      # 50 câu SQA cho TC-03
├── results/
│   ├── TC01/
│   │   ├── baseline.jtl   # Raw data — JMeter tự ghi
│   │   ├── normal.jtl
│   │   ├── stress.jtl
│   │   ├── breaking.jtl
│   │   └── reports/       # HTML report — tự generate sau khi chạy
│   ├── TC02/
│   └── TC03/
└── quiz_performance_test.jmx
```

---

## Trạng thái file data

| File | Trạng thái |
|---|---|
| `accounts.csv` | ✅ Đã có 200 accounts |
| `quizzes.csv` | ✅ Đã có 3 quiz ID thực |
| `questions.csv` | ✅ Đã có 50 câu SQA |
| `users.csv` | ⚠️ Phải refresh trước mỗi lần test |

---

## Bước 0: Cài đặt

```bash
pip install requests

# JMeter >= 5.6: https://jmeter.apache.org/download_jmeter.cgi
# Giải nén, thêm thư mục bin/ vào PATH
```

---

## Bước 1: Refresh ID Tokens (bắt buộc trước mỗi lần test)

Token hết hạn sau **1 giờ**.

```bash
cd perf-tests/scripts
python refresh_tokens.py
```

Output: `data/users.csv`

---

## Bước 2: Chạy test

Mỗi lệnh chạy **1 TC × 1 load level**. Truyền `-Jtc` và `-Jlevel` để JMeter ghi file vào đúng thư mục.

### TC-01 — Solo Quiz

```bash
jmeter -n -t quiz_performance_test.jmx -Jtc=TC01 -Jlevel=baseline  -Jtc01_users=20  -Jtc01_rampup=30  -Jtc01_duration=300
jmeter -n -t quiz_performance_test.jmx -Jtc=TC01 -Jlevel=normal    -Jtc01_users=50  -Jtc01_rampup=60  -Jtc01_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC01 -Jlevel=stress    -Jtc01_users=100 -Jtc01_rampup=90  -Jtc01_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC01 -Jlevel=breaking  -Jtc01_users=200 -Jtc01_rampup=120 -Jtc01_duration=300
```

### TC-02 — Multiplayer

```bash
jmeter -n -t quiz_performance_test.jmx -Jtc=TC02 -Jlevel=baseline  -Jtc02_hosts=5  -Jtc02_players=20  -Jtc02_rampup=30  -Jtc02_duration=300
jmeter -n -t quiz_performance_test.jmx -Jtc=TC02 -Jlevel=normal    -Jtc02_hosts=10 -Jtc02_players=50  -Jtc02_rampup=60  -Jtc02_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC02 -Jlevel=stress    -Jtc02_hosts=20 -Jtc02_players=100 -Jtc02_rampup=90  -Jtc02_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC02 -Jlevel=breaking  -Jtc02_hosts=40 -Jtc02_players=200 -Jtc02_rampup=120 -Jtc02_duration=300
```

### TC-03 — Chatbot RAG

```bash
jmeter -n -t quiz_performance_test.jmx -Jtc=TC03 -Jlevel=baseline  -Jtc03_users=5  -Jtc03_rampup=30 -Jtc03_duration=300
jmeter -n -t quiz_performance_test.jmx -Jtc=TC03 -Jlevel=normal    -Jtc03_users=15 -Jtc03_rampup=60 -Jtc03_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC03 -Jlevel=stress    -Jtc03_users=30 -Jtc03_rampup=90 -Jtc03_duration=600
jmeter -n -t quiz_performance_test.jmx -Jtc=TC03 -Jlevel=breaking  -Jtc03_users=60 -Jtc03_rampup=60 -Jtc03_duration=300
```

> **Lưu ý Windows**: Viết mỗi lệnh trên **một dòng duy nhất** (không dùng `\` xuống dòng).

---

## Bước 3: Xem kết quả

```bash
# Sinh HTML report từ file .jtl
jmeter -g results/TC01/baseline.jtl -o results/TC01/reports/baseline/

# Mở trong browser
results/TC01/reports/baseline/index.html
```

Làm tương tự cho các TC và level khác (`normal`, `stress`, `breaking`).

---

## Ngưỡng Pass/Fail

| Test Case | P95 | Error Rate | Ghi chú |
|---|---|---|---|
| TC-01 Solo Quiz | ≤ 1000ms | ≤ 1% | |
| TC-02 Multiplayer | ≤ 1500ms | ≤ 2% | |
| TC-03 Chatbot RAG | ≤ 5000ms | ≤ 2% | Fail thêm nếu bất kỳ request nào > 12000ms |

---

## Xử lý sự cố thường gặp

| Triệu chứng | Nguyên nhân | Cách fix |
|---|---|---|
| Lỗi 401 khi chạy | Token hết hạn | Chạy lại `refresh_tokens.py` |
| Lỗi `cannot write to results/...` | Thư mục chưa tồn tại | Chạy `mkdir results/TC01 results/TC02 results/TC03` |
| Nhiều lỗi `[RATE_LIMIT_429]` ở TC-03 | Gemini quota | Giảm `-Jtc03_users` hoặc kiểm tra quota tại Google Cloud Console |
| TC-02 players lỗi 403 | Host chưa tạo phòng kịp | Tăng `delay` trong Player Thread Group lên 10s |

---

## Dọn dẹp sau test

Document test có field `"source": "perf-test"`. Xóa bằng Firebase Console:

```js
db.collection('quiz-results').where('source', '==', 'perf-test').get()
  .then(snap => snap.forEach(d => d.ref.delete()))

db.collection('multiplayer_rooms').where('source', '==', 'perf-test').get()
  .then(snap => snap.forEach(d => d.ref.delete()))
```

---

## Thêm tài khoản test (nếu cần)

```bash
pip install firebase-admin
python scripts/create_test_accounts.py
```

Script idempotent — bỏ qua accounts đã tồn tại, an toàn khi chạy lại.
