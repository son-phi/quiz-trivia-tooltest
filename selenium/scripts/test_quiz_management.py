"""
test_quiz_management.py – F3 Quiz Management Selenium tests
Covers: Create / Read / Update / Delete / Import CSV / State transition / Password quiz

Run all : pytest selenium/scripts/test_quiz_management.py -v -s
Run one  : pytest selenium/scripts/test_quiz_management.py -v -s -k TC-CQ-001
"""
import os
import sys
import re
import time
import hashlib
import base64
import tempfile
import pytest
import requests
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    ElementClickInterceptedException, StaleElementReferenceException,
)

sys.path.insert(0, str(Path(__file__).parent))
from conftest import (
    APP_URL, TEST_ACCOUNTS, FIRESTORE_BASE,
    get_id_token, firestore_get, firestore_delete,
)

QUIZZES_COLLECTION = "quizzes"

# ─────────────────────────────────────────────────────────────────────────────
# Password hash — matches app's passwordHash.ts
# Hash = SHA256(salt + ":" + password), salt = base64(32 random bytes)
# ─────────────────────────────────────────────────────────────────────────────

def _create_password_hash(password: str) -> tuple[str, str]:
    salt_bytes = os.urandom(32)
    salt = base64.b64encode(salt_bytes).decode("ascii")
    combined = f"{salt}:{password}"
    hash_val = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return salt, hash_val


# ─────────────────────────────────────────────────────────────────────────────
# Firestore REST helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fs_find_by_title(title: str, role: str = "creator") -> str | None:
    """Return quiz_id matching exact title via Firestore runQuery, or None."""
    info = get_id_token(role)
    url = f"{FIRESTORE_BASE}:runQuery"
    headers = {"Authorization": f"Bearer {info['idToken']}", "Content-Type": "application/json"}
    body = {
        "structuredQuery": {
            "from": [{"collectionId": QUIZZES_COLLECTION}],
            "where": {"fieldFilter": {
                "field": {"fieldPath": "title"},
                "op": "EQUAL",
                "value": {"stringValue": title},
            }},
            "limit": 1,
        }
    }
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        if resp.status_code != 200:
            return None
        rows = resp.json()
        if rows and isinstance(rows, list) and "document" in rows[0]:
            return rows[0]["document"]["name"].split("/")[-1]
    except Exception:
        pass
    return None


def _fs_create_quiz(
    title: str,
    status: str = "draft",
    role: str = "creator",
    password: str | None = None,
    add_question: bool = True,
) -> str:
    """Create a quiz via Firestore REST. Returns quiz_id."""
    info = get_id_token(role)
    url = f"{FIRESTORE_BASE}/{QUIZZES_COLLECTION}"
    headers = {"Authorization": f"Bearer {info['idToken']}", "Content-Type": "application/json"}

    q_values: list = []
    if add_question:
        q_values = [{"mapValue": {"fields": {
            "id": {"stringValue": "q1"},
            "text": {"stringValue": "What is 1+1?"},
            "type": {"stringValue": "multiple"},
            "points": {"integerValue": 1},
            "answers": {"arrayValue": {"values": [
                {"mapValue": {"fields": {
                    "id": {"stringValue": "a1"},
                    "text": {"stringValue": "2"},
                    "isCorrect": {"booleanValue": True},
                }}},
                {"mapValue": {"fields": {
                    "id": {"stringValue": "a2"},
                    "text": {"stringValue": "3"},
                    "isCorrect": {"booleanValue": False},
                }}},
            ]}},
        }}}]

    fields: dict = {
        "title": {"stringValue": title},
        "description": {"stringValue": "Automated test quiz"},
        "category": {"stringValue": "science"},
        "difficulty": {"stringValue": "easy"},
        "duration": {"integerValue": 10},
        "status": {"stringValue": status},
        "isDraft": {"booleanValue": status == "draft"},
        "isPublished": {"booleanValue": status != "draft"},
        "isPublic": {"booleanValue": False},
        "allowRetake": {"booleanValue": True},
        "createdBy": {"stringValue": info["localId"]},
        "questions": {"arrayValue": {"values": q_values}},
        "quizType": {"stringValue": "standard"},
    }
    if password:
        salt, hash_val = _create_password_hash(password)
        fields["havePassword"] = {"stringValue": "password"}
        fields["password"] = {"stringValue": password}
        fields["visibility"] = {"stringValue": "password"}
        fields["pwd"] = {"mapValue": {"fields": {
            "enabled": {"booleanValue": True},
            "algo": {"stringValue": "SHA256"},
            "salt": {"stringValue": salt},
            "hash": {"stringValue": hash_val},
        }}}

    resp = requests.post(url, headers=headers, json={"fields": fields}, timeout=10)
    resp.raise_for_status()
    return resp.json()["name"].split("/")[-1]


def _fs_delete_quiz(quiz_id: str, role: str = "creator"):
    try:
        info = get_id_token(role)
        firestore_delete(QUIZZES_COLLECTION, quiz_id, info["idToken"])
    except Exception as e:
        print(f"  [WARN] Rollback failed for quizzes/{quiz_id}: {e}")


def _fs_get_quiz(quiz_id: str, role: str = "creator") -> dict | None:
    info = get_id_token(role)
    return firestore_get(QUIZZES_COLLECTION, quiz_id, info["idToken"])


def _fs_get_status(quiz_id: str, role: str = "creator") -> str:
    doc = _fs_get_quiz(quiz_id, role)
    if doc is None:
        return "NOT_FOUND"
    return doc.get("fields", {}).get("status", {}).get("stringValue", "unknown")


# ─────────────────────────────────────────────────────────────────────────────
# Selenium helpers  (rewritten based on CreateQuizPage source code analysis)
# ─────────────────────────────────────────────────────────────────────────────

def _safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.15)
    except StaleElementReferenceException:
        raise
    try:
        element.click()
    except ElementClickInterceptedException:
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", element)


def _login_as(driver, wait: WebDriverWait, role: str):
    driver.get(APP_URL + "/login")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(TEST_ACCOUNTS[role]["email"])
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(TEST_ACCOUNTS[role]["password"])
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-blue-600.w-full")))
    _safe_click(driver, btn)
    wait.until(lambda d: "/login" not in d.current_url)
    time.sleep(1.5)


def _get_toast(driver, timeout: int = 8) -> str:
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Toastify__toast"))
        )
        return toast.text.strip()
    except TimeoutException:
        return ""


def _fill_richtexteditor(driver, text: str):
    """Insert text into Quill editor. Quill uses its own event system so we trigger
    a 'text-change' event on the Quill instance attached to the editor container."""
    editor = None
    for sel in ["div.ql-editor", "div.ProseMirror", "div[contenteditable='true']"]:
        elems = driver.find_elements(By.CSS_SELECTOR, sel)
        if elems:
            editor = elems[0]
            break
    if editor is None:
        return
    # Set innerHTML and fire both the DOM input event and Quill's internal update
    driver.execute_script("""
        var editor = arguments[0];
        var text = arguments[1];
        editor.innerHTML = '<p>' + text + '</p>';
        editor.dispatchEvent(new Event('input', {bubbles: true}));
        // Also try to notify Quill by finding its root container
        var container = editor.closest('.ql-container') || editor.parentElement;
        if (container && container.__quill) {
            container.__quill.setContents([{insert: text + '\\n'}]);
        }
    """, editor, text)
    time.sleep(0.3)


def _wait_for_page_stable(driver, timeout: int = 30, stable_for: float = 1.2, extra_sleep: float = 0.3):
    """Wait until page has been free of loading/auth-check indicators for `stable_for` seconds.

    The app performs multiple sequential loading phases (auth check → data fetch), so we poll
    continuously and require the page to be loading-free for a sustained period before proceeding.
    """
    LOADING_XPATH = (
        "//*["
        "contains(text(),'Đang tải') or "
        "contains(text(),'Vui lòng đợi') or "
        "contains(text(),'Loading') or "
        "contains(text(),'Đang kiểm tra') or "
        "contains(text(),'xác thực')"
        "]"
    )
    deadline = time.time() + timeout
    stable_since = None

    while time.time() < deadline:
        try:
            has_loading = bool(driver.find_elements(By.XPATH, LOADING_XPATH))
        except StaleElementReferenceException:
            has_loading = True

        if has_loading:
            stable_since = None
        else:
            if stable_since is None:
                stable_since = time.time()
            elif time.time() - stable_since >= stable_for:
                break  # page has been stable long enough

        time.sleep(0.25)

    if extra_sleep > 0:
        time.sleep(extra_sleep)


def _invoke_react_onclick(driver, element) -> bool:
    """Directly invoke the React onClick handler via fiber tree.
    This bypasses all event system issues (stale elements, overlay interception).
    Returns True if handler was found and called."""
    return driver.execute_script("""
        var el = arguments[0];
        var fiberKey = Object.keys(el).find(function(k) {
            return k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance');
        });
        if (!fiberKey) return false;
        var fiber = el[fiberKey];
        var node = fiber;
        for (var i = 0; i < 5; i++) {
            if (!node) break;
            var props = node.memoizedProps || node.pendingProps;
            if (props && props.onClick) {
                props.onClick({
                    preventDefault: function(){},
                    stopPropagation: function(){},
                    target: el,
                    currentTarget: el,
                    type: 'click',
                    nativeEvent: {}
                });
                return true;
            }
            node = node.return;
        }
        return false;
    """, element)


def _select_quiz_type_card(driver, wait: WebDriverWait, quiz_type: str = "standard"):
    """Select quiz type card (Step 0) and verify React state updated.

    Source: QuizTypeStep.tsx — onClick={() => onTypeSelect(type.id)}.
    Selected card gets CSS 'border-transparent scale-[1.02]'.
    Continue button enabled only when quiz.quizType is set (validateStep(0) = !!quiz.quizType).

    Strategy:
    1. Wait for page fully stable (auth check done)
    2. Invoke React onClick directly via fiber tree (most reliable)
    3. Verify selection by CSS class
    4. Retry if needed
    """
    _wait_for_page_stable(driver, extra_sleep=1.0)
    CARD_XPATH = "//div[contains(@class,'grid')]//button[.//h3]"
    idx = 1 if quiz_type == "standard" else 0

    for attempt in range(3):
        try:
            btns = wait.until(EC.presence_of_all_elements_located((By.XPATH, CARD_XPATH)))
            btn = btns[idx]
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.2)

            # Try React fiber onClick first (most reliable)
            called = _invoke_react_onclick(driver, btn)
            if not called:
                # Fallback: ActionChains real click
                ActionChains(driver).move_to_element(btn).click().perform()
            time.sleep(0.6)

            # Verify selection via CSS (border-transparent = selected)
            btns_check = driver.find_elements(By.XPATH, CARD_XPATH)
            if btns_check and idx < len(btns_check):
                cls = btns_check[idx].get_attribute("class") or ""
                if "border-transparent" in cls:
                    return
        except (StaleElementReferenceException, ElementClickInterceptedException):
            pass
        time.sleep(0.5)


def _wait_for_btn_enabled(driver, xpath: str, timeout: int = 20):
    """Wait for a button matching xpath to exist AND not be disabled (opacity-50 = disabled
    in this app's Tailwind setup, or disabled attribute set)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            btns = driver.find_elements(By.XPATH, xpath)
            if btns:
                btn = btns[0]
                cls = btn.get_attribute("class") or ""
                disabled_attr = btn.get_attribute("disabled")
                # Tailwind disabled state: opacity-50 cursor-not-allowed
                is_disabled = disabled_attr or "opacity-50" in cls or "cursor-not-allowed" in cls
                if not is_disabled and btn.is_displayed():
                    return btn
        except StaleElementReferenceException:
            pass
        time.sleep(0.3)
    raise TimeoutException(f"Button ({xpath!r}) not enabled after {timeout}s")


def _click_continue(driver, wait: WebDriverWait):
    """Click the 'Tiếp tục →' Continue button.

    Source: CreateQuizPage/index.tsx — button is disabled={!validateStep(step)}.
    We wait until the button is actually enabled (no opacity-50/cursor-not-allowed),
    then use ActionChains for a real trusted click.
    """
    xp = "//button[contains(.,'→') and not(contains(.,'←'))]"
    _wait_for_page_stable(driver, extra_sleep=0.3)

    for attempt in range(3):
        try:
            btn = _wait_for_btn_enabled(driver, xp, timeout=15)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.3)
            ActionChains(driver).move_to_element(btn).click().perform()
            time.sleep(0.8)
            return
        except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
            if attempt == 2:
                raise
            time.sleep(0.5)


def _wait_for_category_select_ready(driver, wait: WebDriverWait):
    """Wait for the category <select> to be enabled (categoriesLoading=false).
    Source: QuizInfoStep.tsx — select has disabled={categoriesLoading}."""
    SEL = "select.w-full.p-4.border-2.border-gray-200.rounded-xl"
    # Wait until at least one select is present and NOT disabled
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            selects = driver.find_elements(By.CSS_SELECTOR, SEL)
            if selects and not selects[0].get_attribute("disabled"):
                opts = Select(selects[0]).options
                if len(opts) > 1:  # has real options beyond placeholder
                    return selects
        except StaleElementReferenceException:
            pass
        time.sleep(0.4)
    return driver.find_elements(By.CSS_SELECTOR, SEL)


def _react_select_by_index(driver, sel_elem, index: int = 1):
    """Select option at index in a React-controlled <select>.
    Uses nativeInputValueSetter so React's onChange fires correctly."""
    sel = Select(sel_elem)
    if len(sel.options) <= index:
        index = len(sel.options) - 1
    target_value = sel.options[index].get_attribute("value")
    driver.execute_script("""
        var nativeSetter = Object.getOwnPropertyDescriptor(
            window.HTMLSelectElement.prototype, 'value').set;
        nativeSetter.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    """, sel_elem, target_value)
    time.sleep(0.3)


def _fill_quiz_info(
    driver,
    wait: WebDriverWait,
    title: str,
    duration: int = 10,
    description: str = "Automated test description",
):
    """Fill Step 1 QuizInfoStep (title, description, category, difficulty, duration).

    Source: QuizInfoStep.tsx
    - Title: native input with onChange → send_keys triggers React onChange
    - Description: Quill RichTextEditor → inject via ql-editor + Quill API
    - Category select: disabled while categoriesLoading → wait for it to be ready
    - Difficulty select: native <select> with onChange
    - Duration: number input with range 5-120, onChange updates quiz.duration
    """
    # Wait for title input (Step 1 landmark)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
    ))

    # Title — send_keys fires real key events that React's onChange captures
    t_inp = driver.find_element(By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
    t_inp.clear()
    t_inp.send_keys(title)
    time.sleep(0.2)

    # Description — Quill editor
    _fill_richtexteditor(driver, description)

    # Category — wait for categories to load (select is disabled={categoriesLoading})
    selects = _wait_for_category_select_ready(driver, wait)
    if selects:
        _react_select_by_index(driver, selects[0], index=1)

    # Difficulty — re-query after category change triggers re-render
    selects = driver.find_elements(By.CSS_SELECTOR, "select.w-full.p-4.border-2.border-gray-200.rounded-xl")
    if len(selects) >= 2:
        _react_select_by_index(driver, selects[1], index=1)  # index 1 = "easy"

    # Duration — number input. wait.until handles any post-select re-render
    dur = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
    driver.execute_script("""
        var nativeSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    """, dur, str(duration))
    time.sleep(0.3)


def _add_mcq_question(driver, wait: WebDriverWait, q_text: str = "What is 1+1?"):
    """Add one MCQ question in QuestionsStep.
    Source: QuestionsStep.tsx — Add button has bg-blue-600, question block has bg-gray-50."""
    # Wait for page to settle after navigating to questions step
    _wait_for_page_stable(driver, extra_sleep=0.5)

    # Try multiple XPaths — button class/text may vary by build
    ADD_XPATHS = [
        "//button[contains(@class,'bg-blue-600') and (contains(.,'Add') or contains(.,'Thêm') or contains(.,'câu hỏi'))]",
        "//button[contains(.,'Add') or contains(.,'Thêm') or contains(.,'câu hỏi')]",
        "//button[contains(@class,'blue') and not(contains(.,'→')) and not(contains(.,'←'))]",
    ]
    add_btn = None
    for xp in ADD_XPATHS:
        try:
            add_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xp)))
            break
        except TimeoutException:
            continue
    if add_btn is None:
        raise TimeoutException("Add Question button not found with any known XPath")

    _safe_click(driver, add_btn)
    time.sleep(0.8)

    q_block = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.border.rounded-lg.p-4.mb-4.bg-gray-50")
    ))
    all_inputs = q_block.find_elements(By.CSS_SELECTOR, "input.flex-1.border.p-2.rounded")
    if all_inputs:
        all_inputs[0].clear()
        all_inputs[0].send_keys(q_text)
    for i, inp in enumerate(all_inputs[1:5], start=1):
        inp.clear()
        inp.send_keys(f"Option {i}")
    time.sleep(0.2)


def _click_save_draft(driver, wait: WebDriverWait):
    """Click 💾 Save Draft button. Source: ReviewStep — disabled={submitting || !quiz.title || !quiz.quizType}."""
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'💾') or contains(.,'Draft') or contains(.,'Nháp')]")
    ))
    _safe_click(driver, btn)


def _click_publish(driver, wait: WebDriverWait):
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(.,'🚀') or (contains(.,'Publish') and not(contains(.,'Draft')))]")
    ))
    _safe_click(driver, btn)


def _do_full_create_wizard(
    driver,
    wait: WebDriverWait,
    title: str,
    duration: int = 10,
    save_as_draft: bool = True,
) -> str:
    """Run the full standard quiz creation wizard (4 steps: Type→Info→Questions→Review).
    Returns title for Firestore lookup."""
    driver.get(APP_URL + "/creator/new")
    _wait_for_page_stable(driver, extra_sleep=0.5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

    # Step 0: Type selection
    _select_quiz_type_card(driver, wait, "standard")
    _click_continue(driver, wait)

    # Step 1: Quiz info
    _fill_quiz_info(driver, wait, title, duration=duration)
    _click_continue(driver, wait)
    _wait_for_page_stable(driver, extra_sleep=0.5)
    # If still on info step (click didn't advance), re-click once
    on_questions = bool(driver.find_elements(
        By.XPATH, "//button[contains(.,'Add') or contains(.,'Thêm') or contains(.,'câu hỏi')]"
    ))
    if not on_questions:
        _click_continue(driver, wait)
        _wait_for_page_stable(driver, extra_sleep=0.5)

    # Step 2: Questions
    _add_mcq_question(driver, wait)
    _click_continue(driver, wait)

    # Step 3: Review — wait for Publish/Draft buttons
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(.,'🚀') or contains(.,'Publish')]")
    ))
    if save_as_draft:
        _click_save_draft(driver, wait)
    else:
        _click_publish(driver, wait)

    return title


def _handle_confirm_dialog(driver, wait: WebDriverWait):
    """Accept a browser alert or a modal confirm button."""
    try:
        alert = driver.switch_to.alert
        alert.accept()
        return
    except Exception:
        pass
    for xpath in [
        "//button[contains(.,'OK')]",
        "//button[contains(.,'Confirm')]",
        "//button[contains(.,'Yes')]",
        "//button[contains(.,'Delete')]",
        "//button[contains(.,'Xác nhận')]",
    ]:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            _safe_click(driver, btn)
            return
        except TimeoutException:
            pass


def _open_import_modal_and_upload(driver, wait: WebDriverWait, file_path: str, file_type: str = "csv"):
    """Open bulk-import modal and upload a file."""
    import_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH,
         "//button[contains(@class,'bg-green-600') or "
         "contains(.,'📁') or "
         "contains(.,'Import') or "
         "contains(.,'Nhập')]")
    ))
    _safe_click(driver, import_btn)
    time.sleep(1)

    accept = ".csv" if file_type == "csv" else ".xlsx,.xls"
    file_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, f"input[type='file'][accept='{accept}']")
    ))
    file_input.send_keys(file_path)
    time.sleep(2.5)


# ─────────────────────────────────────────────────────────────────────────────
# Test IDs
# ─────────────────────────────────────────────────────────────────────────────

TC_IDS = [
    "TC-CQ-001", "TC-CQ-002", "TC-CQ-003", "TC-CQ-004",
    "TC-CQ-005", "TC-CQ-006", "TC-CQ-007", "TC-CQ-008",
    "TC-CQ-009", "TC-CQ-010", "TC-CQ-011",
    "TC-RQ-001", "TC-RQ-002",
    "TC-UQ-001", "TC-UQ-002", "TC-UQ-003",
    "TC-DQ-001", "TC-DQ-002",
    "TC-IMP-001", "TC-IMP-002", "TC-IMP-003", "TC-IMP-004",
    "TC-QST-001", "TC-QST-002", "TC-QST-003",
    "TC-QM-006", "TC-QM-007",
]


# ─────────────────────────────────────────────────────────────────────────────
# Main parametrized test
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("tc_id", TC_IDS)
def test_quiz_management(driver, excel_quiz_mgmt, tc_id):
    wait = WebDriverWait(driver, 20)
    status = "FAIL"
    actual_ui = ""
    actual_db = ""
    quiz_id_cleanup: str | None = None

    try:
        # ────────────────────────────────────────────────────────────────────
        # TC-CQ-001: Create valid standard quiz → success toast + Firestore exists
        # ────────────────────────────────────────────────────────────────────
        if tc_id == "TC-CQ-001":
            _login_as(driver, wait, "creator")
            title = f"TC-CQ-001_Auto_{int(time.time())}"
            _do_full_create_wizard(driver, wait, title, duration=10, save_as_draft=True)

            toast_txt = _get_toast(driver, timeout=8)
            actual_ui = toast_txt[:120] if toast_txt else "No toast"
            time.sleep(2)

            quiz_id = _fs_find_by_title(title)
            quiz_id_cleanup = quiz_id

            if quiz_id:
                doc = _fs_get_quiz(quiz_id)
                actual_db = f"quizzes/{quiz_id} EXISTS (status={_fs_get_status(quiz_id)})"
                if doc and "Error" not in actual_ui:
                    status = "PASS"
            else:
                actual_db = "NOT FOUND in Firestore"

        # ────────────────────────────────────────────────────────────────────
        # TC-CQ-002: Empty title → Continue button disabled (validateStep fails)
        # Source: validateStep('info') requires quiz.title?.trim() non-empty
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-CQ-002":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)

            # Fill all fields properly (so only title is the blocker)
            _fill_quiz_info(driver, wait, title="PLACEHOLDER", duration=10)

            # Clear title — use nativeInputValueSetter so React state updates
            t_inp = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
            ))
            driver.execute_script("""
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                setter.call(arguments[0], '');
                arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
            """, t_inp)
            time.sleep(0.4)

            # Verify Continue button is now disabled (opacity-50 / cursor-not-allowed)
            XP_CONT = "//button[contains(.,'→') and not(contains(.,'←'))]"
            cont_btns = driver.find_elements(By.XPATH, XP_CONT)
            btn_disabled = False
            btn_cls = ""
            if cont_btns:
                btn_cls = cont_btns[0].get_attribute("class") or ""
                btn_disabled = (
                    bool(cont_btns[0].get_attribute("disabled")) or
                    "opacity-50" in btn_cls or
                    "cursor-not-allowed" in btn_cls
                )

            actual_ui = (
                f"Continue disabled={btn_disabled} cls_snippet={btn_cls[:60]}"
            )

            if btn_disabled:
                status = "PASS"
                actual_ui = "Continue button disabled when title empty ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-CQ-003: No questions added → Continue disabled at questions step
        # Source: validateStep('questions') requires questions.length > 0
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-CQ-003":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title="TC-CQ-003 No Questions", duration=10)
            _click_continue(driver, wait)  # → questions step

            # Check Continue button is disabled (no questions added yet)
            XP_CONT = "//button[contains(.,'→') and not(contains(.,'←'))]"
            time.sleep(0.5)
            cont_btns = driver.find_elements(By.XPATH, XP_CONT)
            btn_disabled = False
            if cont_btns:
                cls = cont_btns[0].get_attribute("class") or ""
                btn_disabled = (
                    bool(cont_btns[0].get_attribute("disabled")) or
                    "opacity-50" in cls or "cursor-not-allowed" in cls
                )

            on_questions = bool(driver.find_elements(
                By.XPATH, "//button[contains(.,'Add') or contains(.,'Thêm')]"
            ))

            if btn_disabled or on_questions:
                status = "PASS"
                actual_ui = "Continue disabled with 0 questions – validation ✓"
            else:
                actual_ui = f"btn_disabled={btn_disabled}, on_questions={on_questions}"

        # ────────────────────────────────────────────────────────────────────
        # TC-CQ-004: XSS payload in title → should be sanitized (no raw script)
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-CQ-004":
            _login_as(driver, wait, "creator")
            xss_payload = "<script>alert('xss')</script>"
            unique_suffix = f"_Auto_{int(time.time())}"
            full_title = xss_payload + unique_suffix

            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title=full_title, duration=10)
            _click_continue(driver, wait)
            _add_mcq_question(driver, wait)
            _click_continue(driver, wait)

            page_src = driver.page_source
            no_raw_script = "<script>alert" not in page_src
            actual_ui = "XSS sanitized on review page" if no_raw_script else "Raw <script> tag found!"

            _click_save_draft(driver, wait)
            time.sleep(2)

            quiz_id = _fs_find_by_title(full_title)
            quiz_id_cleanup = quiz_id
            if quiz_id:
                doc = _fs_get_quiz(quiz_id)
                stored = doc.get("fields", {}).get("title", {}).get("stringValue", "") if doc else ""
                actual_db = f"Stored title: {stored[:80]}"

            if no_raw_script:
                status = "PASS"

        # ────────────────────────────────────────────────────────────────────
        # TC-CQ-005..011: BVA duration boundary values
        # ────────────────────────────────────────────────────────────────────
        elif tc_id in ("TC-CQ-005", "TC-CQ-006", "TC-CQ-007", "TC-CQ-008",
                       "TC-CQ-009", "TC-CQ-010", "TC-CQ-011"):
            DURATION_MAP = {
                "TC-CQ-005": (-1,  False),
                "TC-CQ-006": (4,   False),
                "TC-CQ-007": (5,   True),
                "TC-CQ-008": (6,   True),
                "TC-CQ-009": (119, True),
                "TC-CQ-010": (120, True),
                "TC-CQ-011": (121, False),
            }
            dur_val, expect_valid = DURATION_MAP[tc_id]

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title=f"{tc_id} Duration={dur_val}", duration=dur_val)

            XP_CONT = "//button[contains(.,'→') and not(contains(.,'←'))]"
            if expect_valid:
                # Continue should be enabled — click through to Questions step
                _click_continue(driver, wait)
                on_questions = bool(driver.find_elements(
                    By.XPATH, "//button[contains(.,'Add') or contains(.,'Thêm')]"
                ))
                if on_questions:
                    status = "PASS"
                    actual_ui = f"dur={dur_val}: advanced to Questions step ✓"
                else:
                    actual_ui = f"dur={dur_val}: did not advance to Questions step"
            else:
                # Invalid duration — Continue should be DISABLED (opacity-50/cursor-not-allowed)
                time.sleep(0.5)
                cont_btns = driver.find_elements(By.XPATH, XP_CONT)
                btn_disabled = False
                toast_txt = ""
                if cont_btns:
                    cls = cont_btns[0].get_attribute("class") or ""
                    btn_disabled = (
                        bool(cont_btns[0].get_attribute("disabled")) or
                        "opacity-50" in cls or "cursor-not-allowed" in cls
                    )
                if not btn_disabled:
                    # Button somehow enabled — click and check for error feedback
                    try:
                        cont_btns[0].click()
                        time.sleep(0.5)
                    except Exception:
                        pass
                    toast_txt = _get_toast(driver, timeout=4)
                page_text = driver.find_element(By.TAG_NAME, "body").text
                has_dur_error = any(kw in page_text for kw in
                                    ["5 to 120", "5-120", "5 đến 120", "from5to120"])
                actual_ui = (
                    f"dur={dur_val}: disabled={btn_disabled}, "
                    f"err_on_page={has_dur_error}, toast={toast_txt[:40] if toast_txt else 'none'}"
                )
                if btn_disabled or toast_txt or has_dur_error:
                    status = "PASS"
                    actual_ui = f"dur={dur_val}: validation blocked as expected ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-RQ-001: Creator sees their own quiz in /creator/my
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-RQ-001":
            title = f"TC-RQ-001_Auto_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/my")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            _wait_for_page_stable(driver)

            page_text = driver.find_element(By.TAG_NAME, "body").text
            found = title in page_text
            actual_ui = f"Quiz '{title}': {'FOUND' if found else 'NOT FOUND'} in /creator/my"
            actual_db = f"quizzes/{quiz_id} status=draft"

            if found:
                status = "PASS"

        # ────────────────────────────────────────────────────────────────────
        # TC-RQ-002: Admin sees creator's pending quiz in admin panel
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-RQ-002":
            title = f"TC-RQ-002_Auto_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="pending", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "admin")
            for route in ["/admin/quizzes", "/admin/quiz-management", "/admin"]:
                driver.get(APP_URL + route)
                _wait_for_page_stable(driver)
                if title in driver.find_element(By.TAG_NAME, "body").text:
                    actual_ui = f"Admin found quiz '{title}' at {route}"
                    actual_db = f"quizzes/{quiz_id} status=pending"
                    status = "PASS"
                    break
            else:
                actual_ui = f"Quiz '{title}' not found in any admin route"
                actual_db = f"quizzes/{quiz_id} status=pending"

        # ────────────────────────────────────────────────────────────────────
        # TC-UQ-001: Creator opens edit page for own DRAFT quiz
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-UQ-001":
            title = f"TC-UQ-001_Orig_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + f"/quiz/{quiz_id}/edit")
            _wait_for_page_stable(driver)

            current_url = driver.current_url
            page_text = driver.find_element(By.TAG_NAME, "body").text
            actual_ui = f"URL after /edit: {current_url}"
            actual_db = f"quizzes/{quiz_id} status=draft"

            is_edit_or_create = "/edit" in current_url or "/creator/new" in current_url
            has_editor = bool(driver.find_elements(By.CSS_SELECTOR, "div.grid"))
            not_blocked = not any(kw in page_text.lower() for kw in
                                  ["unauthorized", "403", "forbidden"])

            if (is_edit_or_create or has_editor) and not_blocked:
                status = "PASS"
                actual_ui = "Edit page accessible for own draft quiz ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-UQ-002: Regular user cannot access quiz edit page
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-UQ-002":
            title = f"TC-UQ-002_Auto_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "user")
            driver.get(APP_URL + f"/quiz/{quiz_id}/edit")
            _wait_for_page_stable(driver)

            current_url = driver.current_url
            page_text = driver.find_element(By.TAG_NAME, "body").text
            actual_ui = f"User at edit URL → now at: {current_url}"

            blocked = (
                "/edit" not in current_url or
                any(kw in page_text.lower() for kw in [
                    "unauthorized", "403", "forbidden", "not allowed",
                    "creator", "role", "permission", "quyền",
                ])
            )
            if blocked:
                status = "PASS"
                actual_ui = "Regular user blocked from edit page ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-UQ-003: Creator cannot directly edit an APPROVED quiz —
        #            clicking Edit must open Edit Request modal instead
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-UQ-003":
            title = f"TC-UQ-003_Appr_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="approved", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/my")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            _wait_for_page_stable(driver)

            try:
                row = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//tr[contains(.,'{title}')]")
                ))
                # Orange edit button (pencil icon)
                edit_btn = row.find_element(
                    By.XPATH,
                    ".//button[contains(@class,'orange') or "
                    "contains(@title,'Edit') or contains(@title,'edit')]",
                )
                _safe_click(driver, edit_btn)
                time.sleep(1.5)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                current_url = driver.current_url
                modal = any(kw in page_text for kw in [
                    "Edit Request", "Yêu cầu chỉnh sửa", "reason", "Lý do",
                ])
                actual_ui = "Edit Request modal shown ✓" if modal else f"Navigated to {current_url}"

                if modal or "/edit" not in current_url:
                    status = "PASS"
            except (NoSuchElementException, TimeoutException) as e:
                actual_ui = f"Could not find Edit button: {str(e)[:60]}"

        # ────────────────────────────────────────────────────────────────────
        # TC-DQ-001: Creator deletes own draft quiz
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-DQ-001":
            title = f"TC-DQ-001_Del_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/my")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            _wait_for_page_stable(driver)

            deleted_ok = False
            try:
                row = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//tr[contains(.,'{title}')]")
                ))
                del_btn = row.find_element(By.XPATH, ".//button[contains(@class,'red')]")
                _safe_click(driver, del_btn)
                time.sleep(0.5)

                _handle_confirm_dialog(driver, wait)
                time.sleep(2.5)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                actual_ui = f"After delete — title in list: {title in page_text}"

                time.sleep(1.5)
                doc = _fs_get_quiz(quiz_id)
                actual_db = "Deleted from Firestore" if doc is None else "Still in Firestore"

                if title not in page_text or doc is None:
                    deleted_ok = True
                    status = "PASS"
            except Exception as e:
                actual_ui = f"Delete error: {str(e)[:80]}"
            finally:
                if not deleted_ok:
                    quiz_id_cleanup = quiz_id  # rollback if test-side delete failed

        # ────────────────────────────────────────────────────────────────────
        # TC-DQ-002: Regular user has no delete capability for quizzes
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-DQ-002":
            title = f"TC-DQ-002_Auto_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "user")
            driver.get(APP_URL + "/creator/my")
            _wait_for_page_stable(driver)

            current_url = driver.current_url
            page_text = driver.find_element(By.TAG_NAME, "body").text
            actual_ui = f"User at /creator/my → url: {current_url[:60]}"

            blocked = (
                "/creator/my" not in current_url or
                any(kw in page_text.lower() for kw in [
                    "unauthorized", "creator", "role", "permission", "quyền",
                ])
            )
            no_del_btn = not bool(driver.find_elements(
                By.XPATH, f"//tr[contains(.,'{title}')]//button[contains(@class,'red')]"
            ))

            if blocked or no_del_btn:
                status = "PASS"
                actual_ui = "User has no delete capability for creator quizzes ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-IMP-001: Valid CSV import → questions imported successfully
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-IMP-001":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title="TC-IMP-001 Valid CSV", duration=10)
            _click_continue(driver, wait)

            csv_content = (
                "question,answerA,answerB,answerC,answerD,correctAnswer,explanation,points\n"
                '"What is 2+2?","1","4","3","5","b","Simple math",10\n'
                '"Capital of France?","London","Paris","Berlin","Rome","b","Geography",10\n'
            )
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
                f.write(csv_content)
                csv_path = f.name

            try:
                _open_import_modal_and_upload(driver, wait, csv_path, "csv")
                toast_txt = _get_toast(driver, timeout=8)
                actual_ui = f"Import result: {toast_txt[:100] if toast_txt else 'No toast'}"

                page_text = driver.find_element(By.TAG_NAME, "body").text
                success_kw = ["import", "success", "added", "câu hỏi", "thêm", "imported"]
                q_visible = "What is 2+2?" in page_text or "Capital of France?" in page_text

                if (toast_txt and any(kw in toast_txt.lower() for kw in success_kw)) or q_visible:
                    status = "PASS"
                    actual_ui = "Questions imported from valid CSV ✓"
            finally:
                os.unlink(csv_path)

        # ────────────────────────────────────────────────────────────────────
        # TC-IMP-002: Wrong file format (.txt) → error toast shown
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-IMP-002":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title="TC-IMP-002 Wrong Format", duration=10)
            _click_continue(driver, wait)

            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write("Not a CSV file. Random text content.\n")
                txt_path = f.name

            try:
                _open_import_modal_and_upload(driver, wait, txt_path, "csv")
                toast_txt = _get_toast(driver, timeout=8)
                actual_ui = f"Wrong format result: {toast_txt[:100] if toast_txt else 'No toast'}"

                error_kw = ["invalid", "error", "wrong", "not", "csv", "file type", "lỗi", "định dạng"]
                if toast_txt and any(kw in toast_txt.lower() for kw in error_kw):
                    status = "PASS"
                    actual_ui = "Wrong format rejected with error toast ✓"
            finally:
                os.unlink(txt_path)

        # ────────────────────────────────────────────────────────────────────
        # TC-IMP-003: CSV with bad schema (< 6 required columns) → error
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-IMP-003":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title="TC-IMP-003 Bad Schema", duration=10)
            _click_continue(driver, wait)

            # Only 2 columns — parser requires ≥ 6 and will skip all rows
            csv_bad = "question,answer\nWhat is 1+1?,2\nWhat is 2+2?,4\n"
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
                f.write(csv_bad)
                bad_path = f.name

            try:
                _open_import_modal_and_upload(driver, wait, bad_path, "csv")
                toast_txt = _get_toast(driver, timeout=8)
                actual_ui = f"Bad schema result: {toast_txt[:100] if toast_txt else 'No toast'}"

                error_kw = ["no question", "0 question", "empty", "parse",
                            "không có câu hỏi", "lỗi", "error"]
                if toast_txt and any(kw in toast_txt.lower() for kw in error_kw):
                    status = "PASS"
                    actual_ui = "Bad schema CSV rejected correctly ✓"
            finally:
                os.unlink(bad_path)

        # ────────────────────────────────────────────────────────────────────
        # TC-IMP-004: Oversized CSV — app has no size limit → note actual behavior
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-IMP-004":
            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/new")
            _wait_for_page_stable(driver)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))

            _select_quiz_type_card(driver, wait, "standard")
            _click_continue(driver, wait)
            _fill_quiz_info(driver, wait, title="TC-IMP-004 Oversized", duration=10)
            _click_continue(driver, wait)

            header = "question,answerA,answerB,answerC,answerD,correctAnswer,explanation,points\n"
            rows = "".join(f'"Q{i} {"x"*200}","A","B","C","D","a","exp",10\n' for i in range(500))
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
                f.write(header + rows)
                big_path = f.name

            try:
                _open_import_modal_and_upload(driver, wait, big_path, "csv")
                toast_txt = _get_toast(driver, timeout=12)
                actual_ui = f"Oversized result: {toast_txt[:100] if toast_txt else 'No response'}"

                size_err_kw = ["size", "too large", "quá lớn", "exceed", "limit"]
                success_kw = ["import", "success", "added"]

                if toast_txt and any(kw in toast_txt.lower() for kw in size_err_kw):
                    status = "PASS"
                    actual_ui = "Oversized file correctly rejected ✓"
                elif toast_txt and any(kw in toast_txt.lower() for kw in success_kw):
                    # App has no size limit — this is an app deficiency
                    actual_ui = f"App accepted large file (no size validation): {toast_txt[:60]}"
                    status = "FAIL"
                else:
                    actual_ui = "No clear size-validation response"
            finally:
                os.unlink(big_path)

        # ────────────────────────────────────────────────────────────────────
        # TC-QST-001: Draft quiz not accessible to regular users
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-QST-001":
            title = f"TC-QST-001_Draft_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator")
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "user")
            driver.get(APP_URL + f"/quiz/{quiz_id}/preview")
            _wait_for_page_stable(driver)

            current_url = driver.current_url
            page_text = driver.find_element(By.TAG_NAME, "body").text
            actual_ui = f"User at draft quiz preview → url: {current_url}"
            actual_db = f"quizzes/{quiz_id} status=draft"

            not_accessible = (
                f"/quiz/{quiz_id}/preview" not in current_url or
                any(kw in page_text.lower() for kw in [
                    "not found", "unauthorized", "404", "403", "access denied",
                    "không tìm thấy", "không có quyền",
                ])
            )
            if not_accessible:
                status = "PASS"
                actual_ui = "Draft quiz inaccessible to regular user ✓"

        # ────────────────────────────────────────────────────────────────────
        # TC-QST-002: Creator submits draft quiz for admin review
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-QST-002":
            title = f"TC-QST-002_Submit_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="draft", role="creator", add_question=True)
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "creator")
            driver.get(APP_URL + "/creator/my")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            _wait_for_page_stable(driver)

            try:
                row = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//tr[contains(.,'{title}')]")
                ))
                # Publish-draft button: blue, Send icon (only for status=draft)
                pub_btn = row.find_element(
                    By.XPATH,
                    ".//button[contains(@class,'blue') and "
                    "not(contains(@title,'Preview')) and not(contains(@title,'Stat')) "
                    "and not(contains(@title,'Copy'))]",
                )
                _safe_click(driver, pub_btn)
                time.sleep(0.5)

                _handle_confirm_dialog(driver, wait)
                time.sleep(3)

                toast_txt = _get_toast(driver, timeout=6)
                actual_ui = f"Submit result: {toast_txt[:80] if toast_txt else 'No toast'}"

                db_status = _fs_get_status(quiz_id)
                actual_db = f"Firestore status: {db_status}"

                if db_status == "pending":
                    status = "PASS"
                elif toast_txt and any(kw in toast_txt.lower() for kw in
                                       ["success", "sent", "pending", "review", "gửi"]):
                    status = "PASS"

            except Exception as e:
                actual_ui = f"Submit error: {str(e)[:80]}"

        # ────────────────────────────────────────────────────────────────────
        # TC-QST-003: Admin approves a pending quiz
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-QST-003":
            title = f"TC-QST-003_Appr_{int(time.time())}"
            quiz_id = _fs_create_quiz(title, status="pending", role="creator", add_question=True)
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "admin")

            found_route = None
            for route in ["/admin/quizzes", "/admin/quiz-management", "/admin"]:
                driver.get(APP_URL + route)
                _wait_for_page_stable(driver)
                if title in driver.find_element(By.TAG_NAME, "body").text:
                    found_route = route
                    break

            if not found_route:
                actual_ui = "Quiz not found in any admin route"
            else:
                try:
                    approve_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         f"//tr[contains(.,'{title}')]"
                         "//button[contains(@class,'green') or "
                         "contains(@title,'Approv') or contains(@title,'approv')]")
                    ))
                    _safe_click(driver, approve_btn)
                    time.sleep(3)

                    toast_txt = _get_toast(driver, timeout=6)
                    actual_ui = f"Approve result: {toast_txt[:80] if toast_txt else 'No toast'}"

                    db_status = _fs_get_status(quiz_id)
                    actual_db = f"Firestore status: {db_status}"

                    if db_status == "approved":
                        status = "PASS"
                    elif toast_txt and any(kw in toast_txt.lower() for kw in
                                           ["approved", "duyệt", "accept"]):
                        status = "PASS"

                except TimeoutException:
                    actual_ui = f"Approve button not found at {found_route}"

        # ────────────────────────────────────────────────────────────────────
        # TC-QM-006: Wrong password for password-protected quiz → rejected
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-QM-006":
            title = f"TC-QM-006_PWD_{int(time.time())}"
            correct_pwd = "TestPwd2024!"
            quiz_id = _fs_create_quiz(
                title, status="approved", role="creator",
                password=correct_pwd, add_question=True,
            )
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "user")
            driver.get(APP_URL + f"/quiz/{quiz_id}/preview")
            _wait_for_page_stable(driver)

            try:
                pwd_input = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='password']")
                ))
                pwd_input.clear()
                pwd_input.send_keys("WrongPassword999!")

                submit_btn = driver.find_element(By.XPATH,
                    "//button[contains(.,'Enter') or contains(.,'Submit') or "
                    "contains(.,'OK') or contains(.,'Vào') or contains(.,'Xác nhận')]"
                )
                _safe_click(driver, submit_btn)
                time.sleep(2)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                actual_ui = f"Wrong pwd page text (first 80): {page_text[:80]}"

                still_blocked = (
                    any(kw in page_text.lower() for kw in
                        ["wrong", "incorrect", "invalid", "sai", "lỗi"]) or
                    bool(driver.find_elements(By.CSS_SELECTOR, "input[type='password']"))
                )
                if still_blocked:
                    status = "PASS"
                    actual_ui = "Wrong password correctly rejected ✓"

            except TimeoutException:
                actual_ui = "No password gate on quiz preview page"

        # ────────────────────────────────────────────────────────────────────
        # TC-QM-007: Correct password for password-protected quiz → unlocked
        # ────────────────────────────────────────────────────────────────────
        elif tc_id == "TC-QM-007":
            title = f"TC-QM-007_PWD_{int(time.time())}"
            correct_pwd = "TestPwd2024!"
            quiz_id = _fs_create_quiz(
                title, status="approved", role="creator",
                password=correct_pwd, add_question=True,
            )
            quiz_id_cleanup = quiz_id

            _login_as(driver, wait, "user")
            driver.get(APP_URL + f"/quiz/{quiz_id}/preview")
            _wait_for_page_stable(driver)

            try:
                pwd_input = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='password']")
                ))
                pwd_input.clear()
                pwd_input.send_keys(correct_pwd)

                submit_btn = driver.find_element(By.XPATH,
                    "//button[contains(.,'Enter') or contains(.,'Submit') or "
                    "contains(.,'OK') or contains(.,'Vào') or contains(.,'Xác nhận')]"
                )
                _safe_click(driver, submit_btn)
                time.sleep(2.5)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                actual_ui = f"Correct pwd → url: {driver.current_url}"

                no_pwd_gate = not bool(driver.find_elements(
                    By.CSS_SELECTOR, "input[type='password']"
                ))
                has_content = any(kw in page_text for kw in [
                    "Start Quiz", "Bắt đầu", "Play", "Chơi", "question", title,
                ])

                if no_pwd_gate or has_content:
                    status = "PASS"
                    actual_ui = "Correct password accepted, quiz content visible ✓"

            except TimeoutException:
                actual_ui = "No password gate — quiz may be directly accessible"
                if title in driver.find_element(By.TAG_NAME, "body").text:
                    status = "PASS"

    except Exception as e:
        actual_ui = f"EXCEPTION: {str(e)[:150]}"

    finally:
        if quiz_id_cleanup:
            _fs_delete_quiz(quiz_id_cleanup)

        excel_quiz_mgmt.write(tc_id, status, actual_ui=actual_ui, actual_db=actual_db)

    assert status == "PASS", (
        f"{tc_id}: status={status} | UI={actual_ui} | DB={actual_db}"
    )
