# Quiz Trivia – Tool Test

Bài tập Tool Test cho môn **Đảm bảo Chất lượng Phần mềm** – E22CNPM03 Nhóm 04  
Ứng dụng được kiểm thử: **https://datn-quizapp.web.app/**

---

## 📁 Cấu trúc thư mục

```
quiz-trivia-tooltest/
│
├── data/                          ← File Excel test data (đọc bởi Selenium scripts)
│   ├── TC_Master_Index.xlsx       ← Index tất cả TC của 3 tool
│   ├── TC_Login.xlsx              ← F1 Auth & RBAC (Selenium)
│   ├── TC_QuizCoreFlow.xlsx       ← F2 Quiz Core Flow (Selenium)
│   ├── TC_QuizManagement.xlsx     ← F3 Quiz CRUD & Import (Selenium)
│   ├── TC_AIFeatures.xlsx         ← F4 AI Generator & Chatbot (Selenium)
│   ├── TC_Postman.xlsx            ← F1+F4 API Testing (Postman)
│   └── TC_JMeter.xlsx             ← Performance (JMeter)
│
├── selenium/
│   ├── scripts/
│   │   ├── conftest.py            ← Pytest fixtures (driver, Firebase connect)
│   │   ├── test_login.py          ← F1 Login/Auth (đọc TC_Login.xlsx)
│   │   ├── test_rbac_roles.py     ← F1 RBAC Role Access
│   │   ├── test_quiz_core.py      ← F2 Quiz Core Flow
│   │   ├── test_quiz_management.py← F3 CRUD & Import
│   │   ├── test_ai_generator.py   ← F4 AI Generator
│   │   └── test_ai_chatbot.py     ← F4 AI Chatbot
│   └── reports/                   ← Generated HTML reports (gitignored)
│
├── postman/
│   └── QuizTrivia_API.postman_collection.json
│
├── jmeter/
│   ├── QuizTrivia_LoadTest.jmx
│   └── reports/                   ← Generated JMeter dashboard (gitignored)
│
├── docs/
│   └── tool_test_report.md        ← Báo cáo tổng kết
│
├── .github/workflows/
│   └── selenium_ci.yml            ← GitHub Actions (tùy chọn)
│
├── requirements.txt
└── README.md
```

---

## 🔧 Cài đặt

```bash
git clone https://github.com/<your-org>/quiz-trivia-tooltest.git
cd quiz-trivia-tooltest

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**Cần thêm ChromeDriver:**  
Script dùng `webdriver-manager` – tự động tải đúng version ChromeDriver.

---

## 🚀 Chạy Selenium Tests

```bash
# Chạy toàn bộ
cd selenium/scripts
pytest --html=../reports/report.html -v

# Chạy từng file
pytest test_login.py -v
pytest test_quiz_core.py -v
pytest test_quiz_management.py -v
pytest test_ai_generator.py -v
pytest test_ai_chatbot.py -v
```

Sau khi chạy, kết quả **tự động ghi ngược vào file Excel** (cột Actual UI, Actual DB, Status).

---

## 📮 Chạy Postman Tests

```bash
# Cần Newman CLI
npm install -g newman newman-reporter-htmlextra

# Chạy collection
newman run postman/QuizTrivia_API.postman_collection.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export selenium/reports/postman_report.html
```

---

## ⚡ Chạy JMeter Tests

```bash
# Cần JMeter 5.6+ đã cài
jmeter -n -t jmeter/QuizTrivia_LoadTest.jmx \
  -l jmeter/reports/results.jtl \
  -e -o jmeter/reports/dashboard/
```

Mở `jmeter/reports/dashboard/index.html` để xem kết quả.

---

## 📊 Quy trình kiểm tra (theo hướng dẫn cô)

Mỗi test case thực hiện **3 bước**:

| Bước | Mô tả |
|------|-------|
| **1. Action** | Thực hiện hành động trên UI (Selenium) hoặc gọi API (Postman) |
| **2. Check Interface** | Assert UI message / kết quả hiển thị đúng không |
| **3. Check Database** | Query Firestore REST API xác nhận data thực sự thay đổi |
| **4. Rollback** | Xóa data test đã tạo (delete doc Firestore) |
| **5. Ghi kết quả** | Fill Pass/Fail + Actual Result ngược vào Excel |

---

## 🗂️ Test Accounts

| Role | Email | Password |
|------|-------|----------|
| USER | user_test@datn.com | Test@12345 |
| CREATOR | creator_test@datn.com | Test@12345 |
| ADMIN | admin_test@datn.com | Test@12345 |

> ⚠️ Tạo các tài khoản test này trong Firebase Console trước khi chạy.

---

## 👥 Nhóm

| Thành viên | MSSV | Phụ trách Tool |
|-----------|------|----------------|
| Trần Tiến Dũng | B22DCCN140 | Selenium – F1 Auth/RBAC |
| Nguyễn Thị Thùy Dương | B22DCAT067 | Selenium – F3 Quiz CRUD |
| Phạm Xuân Quý | B22DCAT240 | Postman – API Testing |
| Phí Quốc Tư Sơn | B22DCAT249 | JMeter – Performance |
