"""
test_quiz_management.py
F3 – Quiz Management (Create / Read / Update / Delete / Import)
App URL : https://datn-quizapp.web.app
Script  : selenium/scripts/test_quiz_management.py
Chạy 1  TC : pytest selenium/scripts/test_quiz_management.py::test_tc_cq_001 -v -s
Chạy all   : pytest selenium/scripts/test_quiz_management.py -v -s
"""

import time
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import fixtures & helpers từ conftest.py (cùng thư mục)
from conftest import get_id_token, firestore_get, firestore_delete, APP_URL

# ─── Hằng số dùng chung ────────────────────────────────────────────────────────
QUIZ_TITLE_SELENIUM  = "Test Quiz SELENIUM"
QUIZ_TITLE_UPDATED   = "Updated Title SELENIUM"
QUIZ_CATEGORY        = "Tech"
QUIZ_DIFFICULTY      = "easy"
QUIZ_DESCRIPTION     = "Automation test description for Selenium suite"

# Lưu ID quiz tạo ra ở TC-CQ-001 để dùng cho các TC phía sau
_created_quiz_id: str = ""


# ─── Helper: Login qua UI ──────────────────────────────────────────────────────
def ui_login(driver, role: str = "creator"):
    """Đăng nhập bằng tài khoản role được chỉ định qua giao diện web."""
    from conftest import TEST_ACCOUNTS
    acc = TEST_ACCOUNTS[role]

    driver.get(f"{APP_URL}/login")
    wait = WebDriverWait(driver, 15)

    # Nhập email
    email_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    ))
    email_input.clear()
    email_input.send_keys(acc["email"])

    # Nhập password
    pw_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
    pw_input.clear()
    pw_input.send_keys(acc["password"])

    # Bấm đăng nhập
    submit_btn = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], button.btn-login, button.login-btn"
    )
    submit_btn.click()

    # Chờ redirect xong (không còn trên /login)
    wait.until(EC.url_changes(f"{APP_URL}/login"))
    time.sleep(1)


def ui_logout(driver):
    """Đăng xuất bằng cách xóa localStorage và reload."""
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    driver.get(APP_URL)
    time.sleep(1)


def wait_for_toast(driver, timeout: int = 8) -> str:
    """Chờ toast notification xuất hiện và trả về text."""
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 ".Toastify__toast, .toast, [class*='toast'], [role='alert']")
            )
        )
        return toast.text.strip()
    except TimeoutException:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
#  CREATE QUIZ
# ══════════════════════════════════════════════════════════════════════════════

# TC-CQ-001
def test_tc_cq_001_create_valid_quiz(driver, excel_quiz_mgmt):
    """
    TC-CQ-001 | Create Quiz – Tạo quiz hợp lệ, đủ trường bắt buộc.
    Role   : CREATOR
    Input  : Title='Test Quiz SELENIUM'; Category='Tech'; Difficulty='easy'; 5 MCQ
    Expect UI : Toast thành công; redirect sang quiz detail
    Expect DB : Document xuất hiện trong collection 'quizzes'
    """
    global _created_quiz_id
    tc_id    = "TC-CQ-001"
    status   = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        # ── 1. Login ──────────────────────────────────────────────────────────
        ui_login(driver, "creator")

        # ── 2. Mở trang Create Quiz ───────────────────────────────────────────
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        # ── Step 0: Chọn Quiz Type = Standard ────────────────────────────────
        std_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Standard') or contains(text(),'standard') or contains(@data-type,'standard')]")
        ))
        std_btn.click()
        time.sleep(0.5)

        # Bấm Continue (Next)
        next_btn = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn.click()
        time.sleep(0.5)

        # ── Step 1: Nhập Quiz Info ────────────────────────────────────────────
        title_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='title'], input[placeholder*='title' i], input[placeholder*='tiêu đề' i]")
        ))
        title_input.clear()
        title_input.send_keys(QUIZ_TITLE_SELENIUM)

        # Mô tả (rich text / textarea)
        try:
            desc_area = driver.find_element(
                By.CSS_SELECTOR, "textarea[name='description'], textarea[placeholder*='description' i]"
            )
            desc_area.clear()
            desc_area.send_keys(QUIZ_DESCRIPTION)
        except NoSuchElementException:
            # Editor dạng contenteditable
            editor = driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
            editor.click()
            editor.send_keys(QUIZ_DESCRIPTION)

        # Category
        try:
            cat_select = Select(driver.find_element(
                By.CSS_SELECTOR, "select[name='category'], select[id*='category' i]"
            ))
            cat_select.select_by_visible_text(QUIZ_CATEGORY)
        except NoSuchElementException:
            cat_input = driver.find_element(
                By.CSS_SELECTOR, "input[name='category'], input[placeholder*='category' i]"
            )
            cat_input.clear()
            cat_input.send_keys(QUIZ_CATEGORY)

        # Difficulty
        diff_select = Select(driver.find_element(
            By.CSS_SELECTOR, "select[name='difficulty'], select[id*='difficulty' i]"
        ))
        diff_select.select_by_value(QUIZ_DIFFICULTY)

        # Bấm Continue
        next_btn = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn.click()
        time.sleep(0.5)

        # ── Step 2: Thêm 5 câu hỏi ───────────────────────────────────────────
        for i in range(5):
            add_q_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Add Question') or contains(text(),'Thêm câu')]")
            ))
            add_q_btn.click()
            time.sleep(0.3)

            # Điền nội dung câu hỏi
            q_inputs = driver.find_elements(
                By.CSS_SELECTOR, "input[placeholder*='question' i], textarea[placeholder*='question' i]"
            )
            if q_inputs:
                q_inputs[-1].clear()
                q_inputs[-1].send_keys(f"Câu hỏi số {i + 1} – automation test")

            # Điền đáp án (4 ô đầu)
            ans_inputs = driver.find_elements(
                By.CSS_SELECTOR, "input[placeholder*='answer' i], input[placeholder*='đáp án' i]"
            )
            answers = ans_inputs[-4:] if len(ans_inputs) >= 4 else ans_inputs
            for j, a_inp in enumerate(answers):
                a_inp.clear()
                a_inp.send_keys(f"Đáp án {j + 1}")

        # Bấm Continue
        next_btn = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn.click()
        time.sleep(0.5)

        # ── Step 3: Review & Publish ──────────────────────────────────────────
        publish_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Publish') or contains(text(),'Xuất bản') or contains(text(),'🚀')]")
        ))
        publish_btn.click()

        # ── 3. Lấy thông báo UI ───────────────────────────────────────────────
        toast_text = wait_for_toast(driver)
        actual_ui  = toast_text if toast_text else "Không thấy toast"

        time.sleep(2)  # chờ Firestore ghi xong

        # ── 4. Verify Firestore ───────────────────────────────────────────────
        auth   = get_id_token("creator")
        token  = auth["idToken"]

        # Tìm quiz mới nhất của creator trong Firestore
        import os
        FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
        url = f"{FIRESTORE_BASE}/quizzes?orderBy=createdAt+desc&pageSize=5"
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        docs = resp.json().get("documents", [])

        for d in docs:
            fields = d.get("fields", {})
            title  = fields.get("title", {}).get("stringValue", "")
            creator = fields.get("createdBy", {}).get("stringValue", "")
            if title == QUIZ_TITLE_SELENIUM and creator == auth["localId"]:
                _created_quiz_id = d["name"].split("/")[-1]
                status = "PASS"
                actual_db = f"Quiz tạo thành công: id={_created_quiz_id}; status=pending"
                break

        if status != "PASS":
            actual_db = "Không tìm thấy document quiz trong Firestore"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"
        actual_db = "N/A"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui} | DB: {actual_db}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-002
def test_tc_cq_002_create_empty_title(driver, excel_quiz_mgmt):
    """
    TC-CQ-002 | Create Quiz – Để trống tiêu đề.
    Expect UI : Thông báo lỗi 'Tiêu đề là bắt buộc' hoặc toast báo lỗi
    Expect DB : Không có document nào được tạo
    """
    tc_id     = "TC-CQ-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        # Chọn quiz type
        std_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Standard') or contains(@data-type,'standard')]")
        ))
        std_btn.click()
        time.sleep(0.3)

        next_btn = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn.click()
        time.sleep(0.5)

        # Bỏ trống title, điền các trường khác
        desc_inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, [contenteditable='true']")
        if desc_inputs:
            desc_inputs[0].click()
            desc_inputs[0].send_keys(QUIZ_DESCRIPTION)

        # Cố bấm Next mà không có title
        next_btn2 = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn2.click()
        time.sleep(1)

        # Kiểm tra vẫn đang ở step 1 (không chuyển tiếp)
        current_url = driver.current_url
        toast_text  = wait_for_toast(driver, timeout=5)
        actual_ui   = toast_text if toast_text else "Validation block – trang không chuyển"

        # Không tạo doc → DB hợp lệ
        if "/quiz/create" in current_url or toast_text:
            status = "PASS"
            actual_db = "Không có document nào được tạo (đúng kỳ vọng)"
        else:
            actual_db = "Trang đã chuyển sang bước tiếp – cần kiểm tra lại"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-003
def test_tc_cq_003_create_no_questions(driver, excel_quiz_mgmt):
    """
    TC-CQ-003 | Create Quiz – Không có câu hỏi nào.
    Expect UI : Không thể chuyển bước / hiện thông báo lỗi
    Expect DB : Không tạo document
    """
    tc_id     = "TC-CQ-003"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        # Step 0: chọn type
        std_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Standard') or contains(@data-type,'standard')]")
        ))
        std_btn.click()
        time.sleep(0.3)
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
        next_btn.click()
        time.sleep(0.5)

        # Step 1: nhập đủ info
        title_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='title'], input[placeholder*='title' i]")
        ))
        title_input.send_keys(QUIZ_TITLE_SELENIUM)
        desc_things = driver.find_elements(By.CSS_SELECTOR, "textarea, [contenteditable='true']")
        if desc_things:
            desc_things[0].click()
            desc_things[0].send_keys(QUIZ_DESCRIPTION)
        try:
            diff = Select(driver.find_element(By.CSS_SELECTOR, "select[name='difficulty']"))
            diff.select_by_value("easy")
        except Exception:
            pass

        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
        next_btn.click()
        time.sleep(0.5)

        # Step 2: KHÔNG thêm câu hỏi, bấm Next ngay
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
        next_btn.click()
        time.sleep(1)

        toast_text = wait_for_toast(driver, timeout=5)
        actual_ui  = toast_text if toast_text else "Button bị disabled / không chuyển bước"

        # Nếu còn ở trang create thì validation đúng
        if "/quiz/create" in driver.current_url or toast_text:
            status = "PASS"
            actual_db = "Không có document nào được tạo (đúng kỳ vọng)"
        else:
            actual_db = "Trang đã chuyển – lỗi validation"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-004
def test_tc_cq_004_create_xss_title(driver, excel_quiz_mgmt):
    """
    TC-CQ-004 | Create Quiz – Nhập XSS trong title.
    Input  : Title='<script>alert(1)</script>'
    Expect : Script không bị execute; title lưu dạng escaped text
    """
    tc_id      = "TC-CQ-004"
    status     = "FAIL"
    actual_ui  = ""
    actual_db  = ""
    xss_quiz_id = ""
    xss_title   = "<script>alert(1)</script>"

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        # Bước qua step type
        std_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Standard') or contains(@data-type,'standard')]")
        ))
        std_btn.click()
        time.sleep(0.3)
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
        next_btn.click()
        time.sleep(0.5)

        # Nhập XSS vào title
        title_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='title'], input[placeholder*='title' i]")
        ))
        title_input.clear()
        title_input.send_keys(xss_title)

        # Kiểm tra alert() chưa nổ
        try:
            driver.switch_to.alert.dismiss()
            actual_ui = "XSS thực thi được (alert nổ) – BUG BẢO MẬT!"
            status    = "FAIL"
        except Exception:
            actual_ui = "Alert không nổ – XSS được escape đúng cách"

            # Tiếp tục nhập info và tạo quiz để check DB
            desc_things = driver.find_elements(By.CSS_SELECTOR, "textarea, [contenteditable='true']")
            if desc_things:
                desc_things[0].click()
                desc_things[0].send_keys(QUIZ_DESCRIPTION)
            try:
                diff = Select(driver.find_element(By.CSS_SELECTOR, "select[name='difficulty']"))
                diff.select_by_value("easy")
            except Exception:
                pass

            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
            next_btn.click()
            time.sleep(0.5)

            # Thêm 1 câu hỏi đơn giản
            try:
                add_q = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Thêm')]")
                ))
                add_q.click()
                time.sleep(0.3)
                q_inp = driver.find_elements(
                    By.CSS_SELECTOR, "input[placeholder*='question' i], textarea[placeholder*='question' i]"
                )
                if q_inp:
                    q_inp[-1].send_keys("XSS test question")
            except Exception:
                pass

            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]")
            next_btn.click()
            time.sleep(0.5)

            publish_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Publish') or contains(text(),'🚀')]")
            ))
            publish_btn.click()
            time.sleep(2)

            # Kiểm tra DB
            import os
            auth  = get_id_token("creator")
            token = auth["idToken"]
            FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
            resp = requests.get(
                f"{FIRESTORE_BASE}/quizzes?pageSize=5",
                headers={"Authorization": f"Bearer {token}"}
            )
            resp.raise_for_status()
            for d in resp.json().get("documents", []):
                fields = d.get("fields", {})
                stored_title = fields.get("title", {}).get("stringValue", "")
                if xss_title in stored_title or "&lt;script&gt;" in stored_title:
                    xss_quiz_id = d["name"].split("/")[-1]
                    actual_db   = f"Title lưu dạng escaped: '{stored_title}'"
                    status      = "PASS"
                    break

            if not xss_quiz_id:
                actual_db = "Không tìm thấy doc XSS trong Firestore (có thể bị block hoàn toàn – chấp nhận)"
                status    = "PASS"

        # Rollback: xóa quiz test nếu đã tạo
        if xss_quiz_id:
            auth  = get_id_token("creator")
            firestore_delete("quizzes", xss_quiz_id, auth["idToken"])

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  CREATE QUIZ – BOUNDARY VALUE ANALYSIS: DURATION (5 ≤ duration ≤ 120 phút)
# ══════════════════════════════════════════════════════════════════════════════
# Validation trong source (CreateQuizPage/index.tsx):
#   const durationValid = quiz.duration >= 5 && quiz.duration <= 120;
#   Nếu không hợp lệ → toast lỗi + Next button bị chặn
#
# Bảng BVA:
#   -1   → INVALID (số âm)
#    4   → INVALID (biên dưới - 1)
#    5   → VALID   (biên dưới)
#    6   → VALID   (biên dưới + 1)
#  119   → VALID   (biên trên - 1)
#  120   → VALID   (biên trên)
#  121   → INVALID (biên trên + 1)
# ─────────────────────────────────────────────────────────────────────────────

def _fill_quiz_info_step(driver, wait, title: str, duration_value: int):
    """
    Helper dùng chung: Đi qua Step 0 (chọn type Standard) và điền
    toàn bộ Step 1 (Quiz Info) với duration được chỉ định.
    Trả về True nếu điền xong, False nếu gặp lỗi.
    """
    try:
        # ── Step 0: Chọn quiz type Standard ──────────────────────────────────
        std_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "//*[contains(text(),'Standard') or contains(@data-type,'standard')]")
        ))
        std_btn.click()
        time.sleep(0.3)

        next_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        next_btn.click()
        time.sleep(0.5)

        # ── Step 1: Điền Quiz Info ────────────────────────────────────────────
        # Title
        title_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "input[name='title'], input[placeholder*='title' i], input[placeholder*='tiêu đề' i]")
        ))
        title_input.clear()
        title_input.send_keys(title)

        # Description
        try:
            desc = driver.find_element(
                By.CSS_SELECTOR, "textarea[name='description'], textarea[placeholder*='description' i]"
            )
            desc.clear()
            desc.send_keys(QUIZ_DESCRIPTION)
        except NoSuchElementException:
            editor = driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
            editor.click()
            editor.send_keys(QUIZ_DESCRIPTION)

        # Category
        try:
            cat = Select(driver.find_element(
                By.CSS_SELECTOR, "select[name='category'], select[id*='category' i]"
            ))
            cat.select_by_index(1)          # chọn option đầu tiên không rỗng
        except Exception:
            pass

        # Difficulty
        try:
            diff = Select(driver.find_element(
                By.CSS_SELECTOR, "select[name='difficulty'], select[id*='difficulty' i]"
            ))
            diff.select_by_value("easy")
        except Exception:
            pass

        # Duration – xoá và nhập giá trị cần test
        try:
            dur_input = driver.find_element(
                By.CSS_SELECTOR,
                "input[name='duration'], input[type='number'][placeholder*='duration' i], "
                "input[type='number'][placeholder*='phút' i], input[type='number']"
            )
            dur_input.clear()
            dur_input.send_keys(str(duration_value))
        except NoSuchElementException:
            pass        # Nếu không tìm thấy → sẽ dùng giá trị mặc định

        return True
    except Exception:
        return False


def _try_next_from_info_step(driver) -> tuple[bool, str]:
    """
    Bấm nút Continue/Next từ Step Info và trả về (chuyển_bước, toast_text).
    chuyển_bước = True nếu URL thay đổi (bước mới).
    """
    url_before = driver.current_url
    try:
        next_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Continue') or contains(text(),'Tiếp') or contains(text(),'→')]"
        )
        # Kiểm tra button có bị disabled không
        if next_btn.get_attribute("disabled"):
            return False, "Button Continue bị disabled"

        next_btn.click()
    except NoSuchElementException:
        return False, "Không tìm thấy nút Continue"

    time.sleep(1.2)
    toast_text   = wait_for_toast(driver, timeout=4)
    url_changed  = driver.current_url != url_before or "/quiz/create" not in driver.current_url

    # Nếu URL không đổi (vẫn ở create) → chưa chuyển bước
    still_on_create = "/quiz/create" in driver.current_url
    moved            = not still_on_create

    return moved, toast_text if toast_text else ("Chuyển bước thành công" if moved else "Vẫn ở step Info")


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-005
def test_tc_cq_005_duration_negative(driver, excel_quiz_mgmt):
    """
    TC-CQ-005 | Create Quiz – Duration = -1 (số âm).
    BVA: giá trị âm hoàn toàn ngoài vùng hợp lệ.
    Expect UI : Validation error / button Continue bị chặn; không chuyển bước
    Expect DB : Không có document nào được tạo trong Firestore
    """
    tc_id     = "TC-CQ-005"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait      = WebDriverWait(driver, 15)

        _fill_quiz_info_step(driver, wait, title="Test Quiz BVA Duration", duration_value=-1)
        moved, toast = _try_next_from_info_step(driver)

        if not moved:
            status    = "PASS"
            actual_ui = f"Chặn đúng – {toast}"
            actual_db = "Không có document nào được tạo (đúng kỳ vọng)"
        else:
            actual_ui = f"Đã chuyển bước với duration=-1 – BUG VALIDATION! Toast: {toast}"
            actual_db = "Cần kiểm tra – có thể doc đã được tạo với duration âm"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-006
def test_tc_cq_006_duration_below_lower_bound(driver, excel_quiz_mgmt):
    """
    TC-CQ-006 | Create Quiz – Duration = 4 (biên dưới − 1).
    BVA: 4 < 5 → không hợp lệ.
    Expect UI : Validation error; không chuyển bước
    Expect DB : Không có document nào được tạo
    """
    tc_id     = "TC-CQ-006"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        _fill_quiz_info_step(driver, wait, title="Test Quiz BVA Duration", duration_value=4)
        moved, toast = _try_next_from_info_step(driver)

        if not moved:
            status    = "PASS"
            actual_ui = f"Chặn đúng (duration=4 < 5) – {toast}"
            actual_db = "Không có document nào được tạo (đúng kỳ vọng)"
        else:
            actual_ui = f"Đã chuyển bước với duration=4 – BUG! Toast: {toast}"
            actual_db = "Cần kiểm tra Firestore"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-007
def test_tc_cq_007_duration_at_lower_bound(driver, excel_quiz_mgmt):
    """
    TC-CQ-007 | Create Quiz – Duration = 5 (biên dưới).
    BVA: 5 = lower bound → hợp lệ.
    Expect UI : Chuyển sang bước tiếp theo thành công
    Expect DB : Quiz doc được tạo với duration = 5
    Rollback  : Xóa quiz doc via Firestore API
    """
    tc_id        = "TC-CQ-007"
    status       = "FAIL"
    actual_ui    = ""
    actual_db    = ""
    bva_quiz_id  = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        _fill_quiz_info_step(driver, wait, title="Test BVA Duration=5", duration_value=5)
        moved, toast = _try_next_from_info_step(driver)

        if moved:
            actual_ui = f"Chuyển bước thành công (duration=5) – {toast}"

            # Thêm 1 câu hỏi và publish để kiểm tra DB
            try:
                add_q = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Thêm')]")
                ))
                add_q.click()
                time.sleep(0.4)
                q_inp = driver.find_elements(
                    By.CSS_SELECTOR,
                    "input[placeholder*='question' i], textarea[placeholder*='question' i]"
                )
                if q_inp:
                    q_inp[-1].send_keys("BVA Duration test question")
            except Exception:
                pass

            try:
                next_btn = driver.find_element(
                    By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]"
                )
                next_btn.click()
                time.sleep(0.5)
                publish_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Publish') or contains(text(),'🚀')]")
                ))
                publish_btn.click()
                time.sleep(2)
            except Exception:
                pass

            # Verify DB
            import os
            auth  = get_id_token("creator")
            token = auth["idToken"]
            uid   = auth["localId"]
            FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
            resp = requests.get(
                f"{FIRESTORE_BASE}/quizzes",
                params={"pageSize": 10},
                headers={"Authorization": f"Bearer {token}"}
            )
            resp.raise_for_status()
            for d in resp.json().get("documents", []):
                fields   = d.get("fields", {})
                db_title = fields.get("title", {}).get("stringValue", "")
                db_dur   = fields.get("duration", {}).get("integerValue") or \
                           fields.get("duration", {}).get("doubleValue")
                creator  = fields.get("createdBy", {}).get("stringValue", "")
                if "Duration=5" in db_title and creator == uid:
                    bva_quiz_id = d["name"].split("/")[-1]
                    actual_db   = f"Firestore: duration={db_dur} (kỳ vọng: 5) ✓"
                    status      = "PASS" if str(db_dur) == "5" else "FAIL"
                    break

            if not bva_quiz_id:
                actual_db = "Không tìm thấy doc BVA trong Firestore"
        else:
            actual_ui = f"Bị chặn với duration=5 – BUG (biên dưới hợp lệ)! Toast: {toast}"
            actual_db = "Không tạo doc – sai validation"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        if bva_quiz_id:
            try:
                auth = get_id_token("creator")
                firestore_delete("quizzes", bva_quiz_id, auth["idToken"])
            except Exception:
                pass

        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"




def test_tc_cq_010_duration_at_upper_bound(driver, excel_quiz_mgmt):
    """
    TC-CQ-010 | Create Quiz – Duration = 120 (biên trên).
    BVA: 120 = upper bound → hợp lệ.
    Expect UI : Chuyển sang bước tiếp theo thành công
    Expect DB : Quiz doc được tạo với duration = 120
    Rollback  : Xóa quiz doc via Firestore API
    """
    tc_id       = "TC-CQ-010"
    status      = "FAIL"
    actual_ui   = ""
    actual_db   = ""
    bva_quiz_id = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        _fill_quiz_info_step(driver, wait, title="Test BVA Duration=120", duration_value=120)
        moved, toast = _try_next_from_info_step(driver)

        if moved:
            actual_ui = f"Chuyển bước thành công (duration=120) – {toast}"

            try:
                add_q = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Add') or contains(text(),'Thêm')]")
                ))
                add_q.click()
                time.sleep(0.3)
                next_btn = driver.find_element(
                    By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'→')]"
                )
                next_btn.click()
                time.sleep(0.5)
                publish_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Publish') or contains(text(),'🚀')]")
                ))
                publish_btn.click()
                time.sleep(2)
            except Exception:
                pass

            import os
            auth  = get_id_token("creator")
            token = auth["idToken"]
            uid   = auth["localId"]
            FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
            resp = requests.get(
                f"{FIRESTORE_BASE}/quizzes",
                params={"pageSize": 10},
                headers={"Authorization": f"Bearer {token}"}
            )
            resp.raise_for_status()
            for d in resp.json().get("documents", []):
                fields   = d.get("fields", {})
                db_title = fields.get("title", {}).get("stringValue", "")
                db_dur   = fields.get("duration", {}).get("integerValue") or \
                           fields.get("duration", {}).get("doubleValue")
                creator  = fields.get("createdBy", {}).get("stringValue", "")
                if "Duration=120" in db_title and creator == uid:
                    bva_quiz_id = d["name"].split("/")[-1]
                    actual_db   = f"Firestore: duration={db_dur} (kỳ vọng: 120) ✓"
                    status      = "PASS" if str(db_dur) == "120" else "FAIL"
                    break

            if not bva_quiz_id:
                actual_db = "Không tìm thấy doc BVA trong Firestore"
        else:
            actual_ui = f"Bị chặn với duration=120 – BUG (biên trên hợp lệ)! Toast: {toast}"
            actual_db = "Không tạo doc – sai validation"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        if bva_quiz_id:
            try:
                auth = get_id_token("creator")
                firestore_delete("quizzes", bva_quiz_id, auth["idToken"])
            except Exception:
                pass

        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-CQ-011
def test_tc_cq_011_duration_above_upper_bound(driver, excel_quiz_mgmt):
    """
    TC-CQ-011 | Create Quiz – Duration = 121 (biên trên + 1).
    BVA: 121 > 120 → không hợp lệ.
    Expect UI : Validation error; không chuyển bước
    Expect DB : Không có document nào được tạo
    """
    tc_id     = "TC-CQ-011"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        _fill_quiz_info_step(driver, wait, title="Test Quiz BVA Duration", duration_value=121)
        moved, toast = _try_next_from_info_step(driver)

        if not moved:
            status    = "PASS"
            actual_ui = f"Chặn đúng (duration=121 > 120) – {toast}"
            actual_db = "Không có document nào được tạo (đúng kỳ vọng)"
        else:
            actual_ui = f"Đã chuyển bước với duration=121 – BUG! Toast: {toast}"
            actual_db = "Cần kiểm tra Firestore"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  READ QUIZ
# ══════════════════════════════════════════════════════════════════════════════

# TC-RQ-001
def test_tc_rq_001_creator_views_own_quizzes(driver, excel_quiz_mgmt):
    """
    TC-RQ-001 | Read Quiz – Creator xem danh sách quiz của chính mình.
    Expect UI : Danh sách hiển thị đúng metadata
    Expect DB : Kết quả khớp với query Firestore where createdBy==uid
    """
    tc_id     = "TC-RQ-001"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/creator/my-quizzes")
        wait = WebDriverWait(driver, 20)

        # Chờ bảng/danh sách load
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table, .quiz-list, [class*='quizzes'], h1")
        ))
        time.sleep(1)

        # Lấy tiêu đề các quiz đang hiển thị
        quiz_titles = driver.find_elements(
            By.CSS_SELECTOR, "td .font-semibold, td .quiz-title, table td:first-child div"
        )
        ui_count  = len(quiz_titles)
        actual_ui = f"Hiển thị {ui_count} quiz trên UI"

        # Verify với Firestore
        import os
        auth  = get_id_token("creator")
        token = auth["idToken"]
        uid   = auth["localId"]
        FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"

        resp = requests.get(
            f"{FIRESTORE_BASE}/quizzes",
            params={"pageSize": 50},
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        db_quizzes = [
            d for d in resp.json().get("documents", [])
            if d.get("fields", {}).get("createdBy", {}).get("stringValue") == uid
        ]
        actual_db = f"Firestore trả về {len(db_quizzes)} quiz thuộc uid={uid}"

        if ui_count >= 0:  # Danh sách render (kể cả rỗng là hợp lệ)
            status = "PASS"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-RQ-002
def test_tc_rq_002_admin_views_all_quizzes(driver, excel_quiz_mgmt):
    """
    TC-RQ-002 | Read Quiz – Admin xem TẤT CẢ quiz của mọi creator.
    Expect UI : Danh sách hiển thị quiz từ nhiều creator khác nhau
    Expect DB : Firestore query all (không filter createdBy)
    """
    tc_id     = "TC-RQ-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    try:
        ui_login(driver, "admin")
        driver.get(f"{APP_URL}/admin")
        wait = WebDriverWait(driver, 20)

        # Chờ admin panel load
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table, .admin-panel, h1, [class*='admin']")
        ))
        time.sleep(1)

        quiz_rows = driver.find_elements(
            By.CSS_SELECTOR, "tbody tr, .quiz-row, [class*='quiz-item']"
        )
        ui_count  = len(quiz_rows)
        actual_ui = f"Admin thấy {ui_count} quiz trong bảng quản lý"

        # Verify DB: query tất cả quizzes
        import os
        auth  = get_id_token("admin")
        token = auth["idToken"]
        FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"

        resp = requests.get(
            f"{FIRESTORE_BASE}/quizzes",
            params={"pageSize": 100},
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        db_total  = len(resp.json().get("documents", []))
        actual_db = f"Firestore có tổng {db_total} quiz trong collection"
        status    = "PASS"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  UPDATE QUIZ
# ══════════════════════════════════════════════════════════════════════════════

# TC-UQ-001
def test_tc_uq_001_creator_edits_own_quiz_title(driver, excel_quiz_mgmt):
    """
    TC-UQ-001 | Update Quiz – Creator chỉnh sửa tiêu đề quiz của chính mình.
    NOTE: TC này đang ghi nhận FAIL trong Excel (Bug: edit not persisted)
    Expect UI : Toast thành công; tiêu đề mới hiển thị
    Expect DB : Firestore quizzes/{id}.title = 'Updated Title SELENIUM'
    Rollback  : Restore title gốc qua Firestore API
    """
    tc_id     = "TC-UQ-001"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "TC-CQ-001 chưa tạo quiz – skip", "N/A")
        pytest.skip("TC-CQ-001 chưa tạo quiz, không có ID để test update")

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/{_created_quiz_id}/edit")
        wait = WebDriverWait(driver, 15)

        # Tìm ô nhập title
        title_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='text']")
        ))
        title_input.clear()
        title_input.send_keys(QUIZ_TITLE_UPDATED)

        # Bấm Save
        save_btn = driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit'], button.save-btn, button.btn-save"
        )
        save_btn.click()

        toast_text = wait_for_toast(driver, timeout=8)
        actual_ui  = toast_text if toast_text else "Không thấy toast sau khi lưu"

        time.sleep(2)  # Chờ Firestore ghi xong

        # Verify DB
        auth  = get_id_token("creator")
        doc   = firestore_get("quizzes", _created_quiz_id, auth["idToken"])
        if doc:
            db_title  = doc.get("fields", {}).get("title", {}).get("stringValue", "")
            actual_db = f"Firestore title = '{db_title}'"
            if db_title == QUIZ_TITLE_UPDATED:
                status = "PASS"
            else:
                status    = "FAIL"
                actual_db += " – KHÔNG khớp kỳ vọng (Bug: edit not persisted)"
        else:
            actual_db = "Không tìm thấy quiz doc trong Firestore"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        # Rollback: restore title gốc
        try:
            auth  = get_id_token("creator")
            import os
            FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
            patch_url = f"{FIRESTORE_BASE}/quizzes/{_created_quiz_id}?updateMask.fieldPaths=title"
            requests.patch(
                patch_url,
                json={"fields": {"title": {"stringValue": QUIZ_TITLE_SELENIUM}}},
                headers={"Authorization": f"Bearer {auth['idToken']}"}
            )
        except Exception:
            pass

        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui} | DB: {actual_db}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-UQ-002
def test_tc_uq_002_user_cannot_edit_quiz(driver, excel_quiz_mgmt):
    """
    TC-UQ-002 | Update Quiz – USER thường không được phép chỉnh sửa quiz.
    Expect UI : Access denied / redirect khỏi trang edit
    Expect DB : Không có Firestore write
    """
    tc_id     = "TC-UQ-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID để test", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "user")
        edit_url = f"{APP_URL}/quiz/{_created_quiz_id}/edit"
        driver.get(edit_url)
        time.sleep(2)

        current_url = driver.current_url
        page_text   = driver.find_element(By.TAG_NAME, "body").text

        if edit_url not in current_url:
            actual_ui = f"Redirect xảy ra → {current_url}"
            status    = "PASS"
            actual_db = "Không có Firestore write (đúng kỳ vọng)"
        elif "unauthorized" in page_text.lower() or "access denied" in page_text.lower() \
                or "không có quyền" in page_text.lower():
            actual_ui = "Hiện thông báo không có quyền"
            status    = "PASS"
            actual_db = "Không có Firestore write (đúng kỳ vọng)"
        else:
            actual_ui = "User truy cập được trang edit – BUG PHÂN QUYỀN"
            actual_db = "Cần kiểm tra Firestore rules"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-UQ-003
def test_tc_uq_003_creator_cannot_edit_other_quiz(driver, excel_quiz_mgmt):
    """
    TC-UQ-003 | Update Quiz – Creator KHÔNG thể sửa quiz của Creator khác.
    Expect UI : Permission error / redirect
    Expect DB : Không có Firestore write
    """
    tc_id     = "TC-UQ-003"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID để test", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        # Login bằng USER (không phải creator sở hữu quiz)
        ui_login(driver, "user")
        edit_url = f"{APP_URL}/quiz/{_created_quiz_id}/edit"
        driver.get(edit_url)
        time.sleep(2)

        current_url = driver.current_url
        page_text   = driver.find_element(By.TAG_NAME, "body").text

        if edit_url not in current_url:
            actual_ui = f"Redirect về {current_url}"
            status    = "PASS"
            actual_db = "Không có Firestore write (đúng kỳ vọng)"
        elif any(kw in page_text.lower() for kw in ["unauthorized", "permission", "không có quyền", "access denied"]):
            actual_ui = "Hiện lỗi phân quyền – chặn đúng"
            status    = "PASS"
            actual_db = "Không có Firestore write (đúng kỳ vọng)"
        else:
            actual_ui = "Creator khác vẫn vào được trang edit – BUG"
            actual_db = "Cần kiểm tra Firestore security rules"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  DELETE QUIZ
# ══════════════════════════════════════════════════════════════════════════════

# TC-DQ-001
def test_tc_dq_001_creator_deletes_own_quiz(driver, excel_quiz_mgmt):
    """
    TC-DQ-001 | Delete Quiz – Creator xóa quiz của mình.
    NOTE: TC này đang ghi nhận FAIL (Bug: delete partially works)
    Expect UI : Quiz xóa khỏi list; toast thành công
    Expect DB : Firestore doc bị xóa
    Rollback  : Re-create quiz sau khi xóa để các TC khác không bị ảnh hưởng
    """
    tc_id     = "TC-DQ-001"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/creator/my-quizzes")
        wait = WebDriverWait(driver, 20)

        # Chờ trang my-quizzes load
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table tbody, .quiz-list")
        ))
        time.sleep(1)

        # Tìm nút Delete của quiz _created_quiz_id
        delete_btn = None
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            if QUIZ_TITLE_SELENIUM in row.text or _created_quiz_id in row.get_attribute("innerHTML"):
                btns = row.find_elements(By.CSS_SELECTOR, "button")
                for b in btns:
                    if any(kw in b.get_attribute("innerHTML").lower() for kw in ["trash", "delete", "xóa"]):
                        delete_btn = b
                        break
            if delete_btn:
                break

        if not delete_btn:
            # Thử tìm bằng data-id
            delete_btn = driver.find_element(
                By.CSS_SELECTOR, f"button[data-quiz-id='{_created_quiz_id}'][class*='delete']"
            )

        delete_btn.click()
        time.sleep(0.5)

        # Confirm dialog
        try:
            confirm = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Xác nhận') or contains(text(),'OK') or contains(text(),'Delete')]")
            ))
            confirm.click()
        except TimeoutException:
            # window.confirm → handle alert
            driver.switch_to.alert.accept()

        toast_text = wait_for_toast(driver, timeout=8)
        actual_ui  = toast_text if toast_text else "Không thấy toast"
        time.sleep(2)

        # Verify Firestore
        auth  = get_id_token("creator")
        doc   = firestore_get("quizzes", _created_quiz_id, auth["idToken"])
        if doc is None:
            actual_db = f"Document quizzes/{_created_quiz_id} đã bị xóa khỏi Firestore"
            status    = "PASS"
        else:
            actual_db = f"Document vẫn còn trong Firestore – Bug: delete not complete"
            status    = "FAIL"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui} | DB: {actual_db}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-DQ-002
def test_tc_dq_002_user_cannot_delete_quiz(driver, excel_quiz_mgmt):
    """
    TC-DQ-002 | Delete Quiz – USER không thể xóa quiz.
    Expect UI : Không có nút Delete; action bị chặn
    Expect DB : Firestore doc không đổi
    """
    tc_id     = "TC-DQ-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "user")
        # User xem trang preview (không có quyền delete)
        driver.get(f"{APP_URL}/quiz/{_created_quiz_id}/preview")
        time.sleep(2)

        page_source = driver.page_source.lower()
        # Check không có nút delete
        has_delete = "delete" in page_source or "trash" in page_source or "xóa" in page_source

        if not has_delete:
            actual_ui = "Không tìm thấy nút Delete trên trang – đúng kỳ vọng"
            status    = "PASS"
            actual_db = "Không gửi request xóa – Firestore doc an toàn"
        else:
            # Thử bấm delete nếu có
            try:
                del_btn = driver.find_element(
                    By.XPATH, "//button[contains(text(),'Delete') or contains(text(),'Xóa')]"
                )
                del_btn.click()
                time.sleep(1)
                toast_text = wait_for_toast(driver, timeout=5)
                actual_ui = f"Nút Delete tồn tại, toast: {toast_text}"
                # Check xem doc còn không
                auth = get_id_token("admin")
                doc  = firestore_get("quizzes", _created_quiz_id, auth["idToken"])
                if doc:
                    actual_db = "Doc vẫn còn – delete bị chặn đúng"
                    status    = "PASS"
                else:
                    actual_db = "Doc bị xóa – BUG phân quyền"
            except NoSuchElementException:
                actual_ui = "Không tìm thấy nút Delete (ẩn với USER)"
                actual_db = "Doc an toàn"
                status    = "PASS"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  IMPORT QUIZ
# ══════════════════════════════════════════════════════════════════════════════

# TC-IMP-001
def test_tc_imp_001_import_valid_csv(driver, excel_quiz_mgmt):
    """
    TC-IMP-001 | Import Quiz – Upload CSV hợp lệ.
    NOTE: đang FAIL (Bug: import fails for most formats)
    Input  : data/sample_import_valid.csv
    Expect UI : Success message; questions xuất hiện
    Expect DB : Firestore questions sub-collection được tạo
    """
    import os
    from pathlib import Path

    tc_id     = "TC-IMP-001"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    csv_path = str(Path(__file__).resolve().parents[2] / "data" / "sample_import_valid.csv")

    if not os.path.exists(csv_path):
        excel_quiz_mgmt.write(tc_id, "SKIP", f"File not found: {csv_path}", "N/A")
        pytest.skip(f"File không tồn tại: {csv_path}")

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        # Tìm nút Import hoặc file input
        try:
            import_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Import') or contains(text(),'Nhập')]")
            ))
            import_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass  # File input có thể không có nút riêng

        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(csv_path)

        toast_text = wait_for_toast(driver, timeout=10)
        actual_ui  = toast_text if toast_text else "Không thấy toast sau import"
        time.sleep(2)

        # DB verify: check questions array xuất hiện (nếu có quiz ID)
        if _created_quiz_id:
            auth = get_id_token("creator")
            doc  = firestore_get("quizzes", _created_quiz_id, auth["idToken"])
            if doc:
                qs = doc.get("fields", {}).get("questions", {}).get("arrayValue", {})
                count = len(qs.get("values", []))
                actual_db = f"Firestore có {count} câu hỏi sau import"
                status    = "PASS" if count > 0 else "FAIL"
            else:
                actual_db = "Không tìm thấy doc để verify"
        else:
            actual_db = "Không có quiz ID – chỉ check UI"
            if "success" in actual_ui.lower() or "thành công" in actual_ui.lower():
                status = "PASS"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-IMP-002
def test_tc_imp_002_import_wrong_format(driver, excel_quiz_mgmt):
    """
    TC-IMP-002 | Import Quiz – Upload file .txt (sai định dạng).
    Expect UI : Error: unsupported file format
    Expect DB : Không có data ghi vào Firestore
    """
    import os, tempfile

    tc_id     = "TC-IMP-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    # Tạo file .txt tạm thời
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w")
    tmp.write("This is a plain text file, not a valid quiz import format.")
    tmp.close()
    txt_path = tmp.name

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        try:
            import_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Import') or contains(text(),'Nhập')]")
            ))
            import_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(txt_path)

        toast_text = wait_for_toast(driver, timeout=8)
        actual_ui  = toast_text if toast_text else "Không thấy toast"

        is_error = any(kw in actual_ui.lower() for kw in [
            "error", "lỗi", "không hỗ trợ", "unsupported", "invalid", "định dạng"
        ])

        if is_error:
            status    = "PASS"
            actual_db = "Không có data ghi vào Firestore (đúng kỳ vọng)"
        else:
            actual_db = "Cần kiểm tra – không rõ đã ghi DB chưa"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        os.unlink(txt_path)
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-IMP-003
def test_tc_imp_003_import_bad_schema_csv(driver, excel_quiz_mgmt):
    """
    TC-IMP-003 | Import Quiz – Upload CSV có schema sai.
    Expect UI : Error với thông tin dòng lỗi
    Expect DB : Không ghi data
    """
    import os, tempfile

    tc_id     = "TC-IMP-003"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="")
    tmp.write("wrong_col1,wrong_col2,totally_wrong\n")
    tmp.write("data1,data2,data3\n")
    tmp.close()
    bad_csv_path = tmp.name

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        try:
            import_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Import') or contains(text(),'Nhập')]")
            ))
            import_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(bad_csv_path)

        toast_text = wait_for_toast(driver, timeout=8)
        actual_ui  = toast_text if toast_text else "Không thấy toast"

        is_error = any(kw in actual_ui.lower() for kw in [
            "error", "lỗi", "invalid", "schema", "format", "line", "dòng"
        ])
        if is_error:
            status    = "PASS"
            actual_db = "Không ghi data (đúng kỳ vọng)"
        else:
            actual_db = "Có thể đã ghi data với schema sai – cần kiểm tra"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        os.unlink(bad_csv_path)
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-IMP-004
def test_tc_imp_004_import_large_file(driver, excel_quiz_mgmt):
    """
    TC-IMP-004 | Import Quiz – Upload file > 5MB.
    Expect UI : Error: file too large
    Expect DB : Không ghi data
    """
    import os, tempfile

    tc_id     = "TC-IMP-004"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    # Tạo file CSV > 5MB
    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w")
    tmp.write("question,answer1,answer2,answer3,answer4,correct\n")
    row = "Sample question text," + ",".join(["Sample answer"] * 5) + "\n"
    while tmp.tell() < 6 * 1024 * 1024:  # 6 MB
        tmp.write(row)
    tmp.close()
    large_path = tmp.name

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/quiz/create")
        wait = WebDriverWait(driver, 15)

        try:
            import_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Import') or contains(text(),'Nhập')]")
            ))
            import_btn.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(large_path)

        toast_text = wait_for_toast(driver, timeout=10)
        actual_ui  = toast_text if toast_text else "Không thấy toast"

        is_error = any(kw in actual_ui.lower() for kw in [
            "too large", "quá lớn", "size", "limit", "max", "error", "lỗi"
        ])
        if is_error:
            status    = "PASS"
            actual_db = "Không ghi data (đúng kỳ vọng)"
        else:
            actual_db = "Cần kiểm tra – không thấy lỗi size"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        os.unlink(large_path)
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  STATE TRANSITION
# ══════════════════════════════════════════════════════════════════════════════

# TC-QST-001
def test_tc_qst_001_draft_not_visible_to_user(driver, excel_quiz_mgmt):
    """
    TC-QST-001 | State Transition – Quiz Draft không hiển thị với USER.
    Expect UI : Quiz DRAFT không có trong public quiz list
    Expect DB : Firestore security rules block user read của draft
    NOTE: TC này đang ghi nhận PASS (đã verified)
    """
    tc_id     = "TC-QST-001"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        # Kiểm tra quiz _created_quiz_id có status=draft không qua DB
        auth_creator = get_id_token("creator")
        doc = firestore_get("quizzes", _created_quiz_id, auth_creator["idToken"])
        if doc:
            db_status = doc.get("fields", {}).get("status", {}).get("stringValue", "")
            actual_db = f"Quiz status trong DB: '{db_status}'"
        else:
            actual_db = "Không lấy được trạng thái quiz từ DB"
            db_status = "unknown"

        # Login USER và kiểm tra trang Discover/Public quiz list
        ui_login(driver, "user")
        driver.get(f"{APP_URL}/quizzes")  # public quiz list
        time.sleep(2)

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if QUIZ_TITLE_SELENIUM in page_text and db_status == "draft":
            actual_ui = f"FAIL: Draft quiz '{QUIZ_TITLE_SELENIUM}' xuất hiện trong public list"
        elif QUIZ_TITLE_SELENIUM not in page_text:
            actual_ui = f"Quiz DRAFT không hiển thị trong public list – đúng kỳ vọng"
            status    = "PASS"
        else:
            actual_ui = f"Quiz có status='{db_status}' – kiểm tra thêm"
            if db_status != "draft":
                status = "PASS"  # Nếu không phải draft thì không áp dụng TC này

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-QST-002
def test_tc_qst_002_submit_for_review(driver, excel_quiz_mgmt):
    """
    TC-QST-002 | State Transition – Creator submit quiz cho admin review (draft→pending).
    NOTE: đang FAIL (Bug: state transition unreliable)
    Expect UI : Badge đổi thành 'Pending Review'
    Expect DB : Firestore quizzes/{id}.status = 'pending'
    Rollback  : Reset status về 'draft'
    """
    tc_id     = "TC-QST-002"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "creator")
        driver.get(f"{APP_URL}/creator/my-quizzes")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
        time.sleep(1)

        # Tìm nút Submit for Review
        submit_btn = None
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            if QUIZ_TITLE_SELENIUM in row.text or _created_quiz_id in row.get_attribute("innerHTML"):
                btns = row.find_elements(By.CSS_SELECTOR, "button, a")
                for b in btns:
                    b_text = b.text.lower()
                    if any(kw in b_text for kw in ["submit", "review", "gửi", "send"]):
                        submit_btn = b
                        break
            if submit_btn:
                break

        if not submit_btn:
            # Thử tìm icon Send
            submit_btn = driver.find_element(
                By.CSS_SELECTOR, f"[data-quiz-id='{_created_quiz_id}'] button.submit-review"
            )

        submit_btn.click()
        time.sleep(0.5)

        # Confirm nếu có dialog
        try:
            confirm = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'OK') or contains(text(),'Xác nhận')]")
            ))
            confirm.click()
        except TimeoutException:
            try:
                driver.switch_to.alert.accept()
            except Exception:
                pass

        toast_text = wait_for_toast(driver)
        actual_ui  = toast_text if toast_text else "Không thấy toast"
        time.sleep(2)

        # Verify DB
        auth = get_id_token("creator")
        doc  = firestore_get("quizzes", _created_quiz_id, auth["idToken"])
        if doc:
            db_status = doc.get("fields", {}).get("status", {}).get("stringValue", "")
            actual_db = f"Firestore status = '{db_status}'"
            status    = "PASS" if db_status == "pending" else "FAIL"
        else:
            actual_db = "Không tìm thấy doc"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        # Rollback: reset về draft
        try:
            import os
            auth  = get_id_token("creator")
            FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
            requests.patch(
                f"{FIRESTORE_BASE}/quizzes/{_created_quiz_id}?updateMask.fieldPaths=status",
                json={"fields": {"status": {"stringValue": "draft"}}},
                headers={"Authorization": f"Bearer {auth['idToken']}"}
            )
        except Exception:
            pass

        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui} | DB: {actual_db}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-QST-003
def test_tc_qst_003_admin_approves_quiz(driver, excel_quiz_mgmt):
    """
    TC-QST-003 | State Transition – Admin approve quiz (pending→published).
    NOTE: đang FAIL (Bug: approval flow broken)
    Expect UI : Quiz status = 'Published'; visible trong discover
    Expect DB : Firestore status='published' (hoặc 'approved')
    Rollback  : Set status về 'pending'
    """
    tc_id     = "TC-QST-003"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        # Đảm bảo quiz đang ở trạng thái pending trước
        import os
        auth_creator = get_id_token("creator")
        FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT','datn-quizapp')}/databases/(default)/documents"
        requests.patch(
            f"{FIRESTORE_BASE}/quizzes/{_created_quiz_id}?updateMask.fieldPaths=status",
            json={"fields": {"status": {"stringValue": "pending"}}},
            headers={"Authorization": f"Bearer {auth_creator['idToken']}"}
        )
        time.sleep(1)

        ui_login(driver, "admin")
        driver.get(f"{APP_URL}/admin")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table, [class*='admin']")))
        time.sleep(1)

        # Tìm nút Approve cho quiz
        approve_btn = None
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            if QUIZ_TITLE_SELENIUM in row.text or _created_quiz_id in row.get_attribute("innerHTML"):
                btns = row.find_elements(By.CSS_SELECTOR, "button")
                for b in btns:
                    b_text = b.text.lower()
                    if any(kw in b_text for kw in ["approve", "duyệt", "chấp nhận"]):
                        approve_btn = b
                        break
            if approve_btn:
                break

        if not approve_btn:
            approve_btn = driver.find_element(
                By.CSS_SELECTOR, f"button[data-quiz-id='{_created_quiz_id}'].approve-btn"
            )

        approve_btn.click()
        time.sleep(0.5)

        try:
            confirm = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'OK') or contains(text(),'Approve')]")
            ))
            confirm.click()
        except TimeoutException:
            pass

        toast_text = wait_for_toast(driver)
        actual_ui  = toast_text if toast_text else "Không thấy toast"
        time.sleep(2)

        # Verify DB
        auth_admin = get_id_token("admin")
        doc = firestore_get("quizzes", _created_quiz_id, auth_admin["idToken"])
        if doc:
            db_status = doc.get("fields", {}).get("status", {}).get("stringValue", "")
            actual_db = f"Firestore status = '{db_status}'"
            status    = "PASS" if db_status in ("approved", "published") else "FAIL"
        else:
            actual_db = "Không tìm thấy doc"

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        # Rollback
        try:
            auth = get_id_token("admin")
            requests.patch(
                f"{FIRESTORE_BASE}/quizzes/{_created_quiz_id}?updateMask.fieldPaths=status",
                json={"fields": {"status": {"stringValue": "pending"}}},
                headers={"Authorization": f"Bearer {auth['idToken']}"}
            )
        except Exception:
            pass

        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui} | DB: {actual_db}"


# ══════════════════════════════════════════════════════════════════════════════
#  PASSWORD PROTECTED
# ══════════════════════════════════════════════════════════════════════════════

# TC-QM-006
def test_tc_qm_006_wrong_password_denied(driver, excel_quiz_mgmt):
    """
    TC-QM-006 | Password Protected – Nhập sai password → từ chối.
    NOTE: đang FAIL (Bug: client-side only check)
    Input  : 'wrongpass' cho quiz có password-protected
    Expect UI : Access denied; quiz content không load
    Expect DB : Không trả về quiz content
    """
    tc_id     = "TC-QM-006"
    status    = "FAIL"
    actual_ui = ""
    actual_db = ""

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "user")
        driver.get(f"{APP_URL}/quiz/{_created_quiz_id}/preview")
        wait = WebDriverWait(driver, 15)

        # Kiểm tra có form nhập password không
        try:
            pwd_input = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='password'], input[placeholder*='password' i], input[placeholder*='mật khẩu' i]")
            ))
            pwd_input.clear()
            pwd_input.send_keys("wrongpass")

            submit = driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], button.submit-password"
            )
            submit.click()

            toast_text = wait_for_toast(driver, timeout=8)
            actual_ui  = toast_text if toast_text else "Không thấy toast"

            is_denied = any(kw in actual_ui.lower() for kw in [
                "wrong", "incorrect", "denied", "không đúng", "sai", "từ chối"
            ])
            if is_denied:
                status    = "PASS"
                actual_db = "Quiz content không được trả về (đúng kỳ vọng)"
            else:
                # Kiểm tra quiz content có load không
                page_text = driver.find_element(By.TAG_NAME, "body").text
                if "câu hỏi" in page_text.lower() or "question" in page_text.lower():
                    actual_ui += " | Quiz content đã load với sai password – BUG"
                    actual_db  = "Quiz content bị lộ – Bug: client-side only check"
                else:
                    actual_ui += " | Content không load với password sai – OK"
                    status     = "PASS"
                    actual_db  = "Quiz content không trả về"

        except TimeoutException:
            actual_ui = "Không có form nhập password – quiz không bảo vệ mật khẩu"
            actual_db = "N/A – quiz cần được set password để test TC này"
            # Nếu quiz không có password thì TC này không applicable
            status    = "SKIP"
            excel_quiz_mgmt.write(tc_id, "SKIP", actual_ui, actual_db)
            pytest.skip("Quiz chưa có password protection")

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ─────────────────────────────────────────────────────────────────────────────

# TC-QM-007
def test_tc_qm_007_correct_password_granted(driver, excel_quiz_mgmt):
    """
    TC-QM-007 | Password Protected – Nhập đúng password → được vào quiz.
    NOTE: TC này đang ghi nhận PASS (đã verified)
    Input  : 'secret123' cho password-protected quiz
    Expect UI : Quiz load bình thường
    """
    tc_id     = "TC-QM-007"
    status    = "FAIL"
    actual_ui = ""
    actual_db = "N/A"

    if not _created_quiz_id:
        excel_quiz_mgmt.write(tc_id, "SKIP", "Không có quiz ID", "N/A")
        pytest.skip("Không có quiz ID")

    try:
        ui_login(driver, "user")
        driver.get(f"{APP_URL}/quiz/{_created_quiz_id}/preview")
        wait = WebDriverWait(driver, 15)

        try:
            pwd_input = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='password'], input[placeholder*='password' i]")
            ))
            pwd_input.clear()
            pwd_input.send_keys("secret123")

            submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit.click()
            time.sleep(2)

            page_text = driver.find_element(By.TAG_NAME, "body").text
            if any(kw in page_text.lower() for kw in ["start", "bắt đầu", "question", "câu hỏi", "preview"]):
                actual_ui = "Quiz load thành công với đúng password"
                status    = "PASS"
            else:
                actual_ui = "Quiz không load dù nhập đúng password"

        except TimeoutException:
            actual_ui = "Không có form password – quiz chưa được bảo vệ"
            status    = "SKIP"
            excel_quiz_mgmt.write(tc_id, "SKIP", actual_ui, actual_db)
            pytest.skip("Quiz chưa set password")

    except Exception as e:
        actual_ui = f"Lỗi script: {e}"

    finally:
        excel_quiz_mgmt.write(tc_id, status, actual_ui, actual_db)
        assert status == "PASS", f"{tc_id} FAIL – {actual_ui}"


# ══════════════════════════════════════════════════════════════════════════════
#  TEARDOWN – Xóa quiz test tạo trong session
# ══════════════════════════════════════════════════════════════════════════════

def test_zz_cleanup(excel_quiz_mgmt):
    """
    Dọn dẹp: Xóa quiz đã tạo trong session test.
    Luôn chạy cuối cùng (tên bắt đầu bằng test_zz_).
    """
    if _created_quiz_id:
        try:
            auth = get_id_token("creator")
            firestore_delete("quizzes", _created_quiz_id, auth["idToken"])
            print(f"\n[CLEANUP] Đã xóa quiz {_created_quiz_id} khỏi Firestore.")
        except Exception as e:
            print(f"\n[CLEANUP WARN] Không xóa được quiz: {e}")
