# -*- coding: utf-8 -*-
"""Step-by-step debug for TC-CQ-001 wizard using form login."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "selenium" / "scripts"))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
)
from conftest import APP_URL, TEST_ACCOUNTS

opts = Options()
# opts.add_argument("--headless=new")   # comment out to see browser
opts.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 20)

def safe_click(el):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.15)
    except StaleElementReferenceException:
        raise
    try:
        el.click()
    except ElementClickInterceptedException:
        time.sleep(0.4)
        driver.execute_script("arguments[0].click();", el)

try:
    # ── Step 0: Login ─────────────────────────────────────────────────────────
    print("[1] Logging in as creator...")
    driver.get(APP_URL + "/login")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(TEST_ACCOUNTS["creator"]["email"])
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(TEST_ACCOUNTS["creator"]["password"])
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-blue-600.w-full")))
    safe_click(btn)
    wait.until(lambda d: "/login" not in d.current_url)
    time.sleep(1.5)
    print(f"    Login OK → {driver.current_url}")

    # ── Step 1: Navigate to /creator/new ─────────────────────────────────────
    print("[2] Navigating to /creator/new...")
    driver.get(APP_URL + "/creator/new")
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))
        print("    div.grid found ✓")
    except TimeoutException:
        print("    div.grid NOT found — body text:")
        print("   ", driver.find_element(By.TAG_NAME, "body").text[:300])
        raise
    time.sleep(1)

    # ── Step 2: Select quiz type card ────────────────────────────────────────
    print("[3] Finding type-card buttons...")
    btns = driver.find_elements(By.XPATH, "//div[contains(@class,'grid')]//button[.//h3]")
    print(f"    Found {len(btns)} buttons with h3")
    if not btns:
        all_btns = driver.find_elements(By.XPATH, "//button[.//h3]")
        print(f"    Fallback: //button[.//h3] found {len(all_btns)}")
        for b in all_btns[:5]:
            print(f"      btn text: {b.text[:60]!r}")
    else:
        for i, b in enumerate(btns[:5]):
            print(f"      btn[{i}] text: {b.text[:60]!r}")

    if len(btns) >= 2:
        driver.execute_script("arguments[0].click();", btns[1])
        print("    Clicked standard card (index 1) ✓")
    elif len(btns) == 1:
        driver.execute_script("arguments[0].click();", btns[0])
        print("    Only 1 card found, clicked it ✓")
    else:
        print("    ERROR: No type-card buttons found!")
    time.sleep(0.3)

    # ── Step 3: Click Continue → ─────────────────────────────────────────────
    print("[4] Clicking Continue →...")
    xp = "//button[contains(.,'→') and not(contains(.,'←'))]"

    def click_continue_btn():
        from selenium.webdriver.common.action_chains import ActionChains
        b = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
        print(f"    Continue btn text: {b.text!r}, location: {b.location}")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", b)
        time.sleep(0.4)
        try:
            ActionChains(driver).move_to_element(b).click().perform()
        except Exception as ex:
            print(f"    ActionChains failed: {ex.__class__.__name__}: {str(ex)[:80]}")
            b = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            driver.execute_script(
                "arguments[0].dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));",
                b
            )
        time.sleep(1.0)
        print(f"    After click → url: {driver.current_url}")
        print(f"    Body (first 200): {driver.find_element(By.TAG_NAME, 'body').text[:200]!r}")

    click_continue_btn()

    # ── Step 4: Fill quiz info ───────────────────────────────────────────────
    print("[5] Filling quiz info (Step 1)...")
    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
        ))
        print("    Title input found ✓")
    except TimeoutException:
        print("    Title input NOT found! Body text:")
        print("   ", driver.find_element(By.TAG_NAME, "body").text[:400])
        raise

    # Print ALL inputs on page to diagnose duration field
    print("    --- All inputs on quiz info page ---")
    for inp in driver.find_elements(By.TAG_NAME, "input"):
        print(f"      type={inp.get_attribute('type')!r} class={inp.get_attribute('class')[:60]!r} placeholder={inp.get_attribute('placeholder')!r}")
    print("    --- All selects ---")
    for sel in driver.find_elements(By.TAG_NAME, "select"):
        print(f"      class={sel.get_attribute('class')[:60]!r}")
    print("    ---")

    title = f"TC-CQ-001_Debug_{int(time.time())}"
    t_inp = driver.find_element(By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
    t_inp.clear()
    t_inp.send_keys(title)
    print(f"    Title filled: {title}")
    time.sleep(0.3)

    def react_select(sel_elem, value=None, index=1):
        sel = Select(sel_elem)
        try:
            if value:
                sel.select_by_value(value)
            else:
                sel.select_by_index(index)
        except Exception:
            sel.select_by_index(index)
        target_val = sel.first_selected_option.get_attribute("value")
        driver.execute_script("""
            var setter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, 'value').set;
            setter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
        """, sel_elem, target_val)
        # Re-query to get current value after React re-render
        time.sleep(0.3)
        return target_val

    # Category
    selects = driver.find_elements(By.CSS_SELECTOR, "select.w-full.p-4.border-2.border-gray-200.rounded-xl")
    print(f"    Found {len(selects)} selects")
    if selects:
        chosen = react_select(selects[0], index=1)
        print(f"    Category nativeValueSetter: {chosen!r} ✓")
        # Verify via DOM
        time.sleep(0.4)
        selects2 = driver.find_elements(By.CSS_SELECTOR, "select.w-full.p-4.border-2.border-gray-200.rounded-xl")
        if selects2:
            actual = selects2[0].get_attribute("value")
            print(f"    Category actual DOM value after: {actual!r}")
    time.sleep(0.4)
    selects = driver.find_elements(By.CSS_SELECTOR, "select.w-full.p-4.border-2.border-gray-200.rounded-xl")
    if len(selects) >= 2:
        chosen2 = react_select(selects[1], value="easy")
        print(f"    Difficulty set to: {chosen2!r} ✓")

    # Duration
    dur = driver.find_element(By.CSS_SELECTOR, "input[type='number'].w-full.p-4.border-2.rounded-xl")
    driver.execute_script("arguments[0].value='';", dur)
    dur.clear()
    dur.send_keys("10")
    dur.send_keys("\t")
    time.sleep(0.3)
    print("    Duration filled ✓")

    # Verify form state + check buttons
    print("    --- Form state after fill ---")
    for sel in driver.find_elements(By.CSS_SELECTOR, "select.w-full.p-4.border-2.border-gray-200.rounded-xl"):
        try:
            print(f"      select value={sel.get_attribute('value')!r} selected={Select(sel).first_selected_option.text!r}")
        except Exception as ex:
            print(f"      select error: {ex}")
    for inp in driver.find_elements(By.CSS_SELECTOR, "input[type='number']"):
        print(f"      number value={inp.get_attribute('value')!r}")
    print("    --- Buttons on page ---")
    for b in driver.find_elements(By.TAG_NAME, "button")[:25]:
        txt = b.text.strip()[:60]
        dis = b.get_attribute("disabled")
        if "→" in txt or "←" in txt or "Tiếp" in txt or "Continue" in txt or "Publish" in txt or "Draft" in txt:
            print(f"      btn: {txt!r} disabled={dis!r} class={b.get_attribute('class')[:50]!r}")
    print("    ---")

    # ── Step 5: Continue to questions ─────────────────────────────────────────
    print("[6] Clicking Continue → (to questions)...")
    try:
        cont2 = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
        cont2.click()
        time.sleep(0.8)
        print("    Clicked ✓")
    except TimeoutException:
        print("    ERROR: Continue → not found at quiz info step!")
        print("    Buttons:", [b.text[:40] for b in driver.find_elements(By.TAG_NAME, "button")[:10]])
        raise

    # ── Step 6: Add MCQ question ─────────────────────────────────────────────
    print("[7] Adding MCQ question...")
    try:
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "//button[contains(@class,'bg-blue-600') and "
             "(contains(.,'Add') or contains(.,'Thêm') or contains(.,'câu hỏi'))]")
        ))
        print(f"    Add btn text: {add_btn.text!r}")
        safe_click(add_btn)
        time.sleep(0.8)
        print("    Add Question clicked ✓")
    except TimeoutException:
        print("    Add Question button NOT found! Body:")
        print("   ", driver.find_element(By.TAG_NAME, "body").text[:400])
        raise

    q_block = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.border.rounded-lg.p-4.mb-4.bg-gray-50")
    ))
    all_inputs = q_block.find_elements(By.CSS_SELECTOR, "input.flex-1.border.p-2.rounded")
    print(f"    Question inputs found: {len(all_inputs)}")
    if all_inputs:
        all_inputs[0].clear()
        all_inputs[0].send_keys("What is 1+1?")
    for i, inp in enumerate(all_inputs[1:5], 1):
        inp.clear()
        inp.send_keys(f"Option {i}")
    time.sleep(0.2)
    print("    MCQ filled ✓")

    # ── Step 7: Continue to review ────────────────────────────────────────────
    print("[8] Clicking Continue → (to review)...")
    try:
        cont3 = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
        cont3.click()
        time.sleep(0.8)
        print("    Clicked ✓")
    except TimeoutException:
        print("    ERROR: Continue → not found at questions step!")
        raise

    # ── Step 8: Save as Draft ─────────────────────────────────────────────────
    print("[9] Clicking Save Draft...")
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(.,'🚀') or contains(.,'Publish')]")
        ))
        draft_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(.,'Draft') or contains(.,'Nháp') or contains(.,'💾')]")
        ))
        print(f"    Draft btn text: {draft_btn.text!r}")
        safe_click(draft_btn)
        print("    Save Draft clicked ✓")
    except TimeoutException:
        print("    ERROR: Publish/Draft buttons not found! Body:")
        print("   ", driver.find_element(By.TAG_NAME, "body").text[:400])
        raise

    time.sleep(3)
    print("[10] Final URL:", driver.current_url)
    print("[10] Body (first 300):", driver.find_element(By.TAG_NAME, "body").text[:300])

    print("\n=== TC-CQ-001 Debug COMPLETE ===")

except Exception:
    print("\n=== FAILED AT STEP ABOVE ===")
    print(traceback.format_exc())
    print("Current URL:", driver.current_url)
    try:
        print("Body:", driver.find_element(By.TAG_NAME, "body").text[:400])
    except Exception:
        pass

finally:
    input("\nPress Enter to close browser...")
    driver.quit()
