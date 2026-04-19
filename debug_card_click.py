# -*- coding: utf-8 -*-
"""Debug card selection specifically."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "selenium" / "scripts"))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from conftest import APP_URL, TEST_ACCOUNTS

opts = Options()
opts.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 20)

CARD_XPATH = "//div[contains(@class,'grid')]//button[.//h3]"

def login():
    driver.get(APP_URL + "/login")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(TEST_ACCOUNTS["creator"]["email"])
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(TEST_ACCOUNTS["creator"]["password"])
    driver.find_element(By.CSS_SELECTOR, "button.bg-blue-600.w-full").click()
    wait.until(lambda d: "/login" not in d.current_url)
    time.sleep(1.5)
    print(f"Logged in → {driver.current_url}")

def wait_stable():
    """Wait for auth/loading overlays."""
    xp = "//*[contains(text(),'Đang tải') or contains(text(),'Đang kiểm tra') or contains(text(),'xác thực') or contains(text(),'Vui lòng đợi')]"
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, xp)))
        print("  Loading detected, waiting...")
        WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, xp)))
        print("  Loading done ✓")
    except Exception:
        pass

def check_card_state():
    btns = driver.find_elements(By.XPATH, CARD_XPATH)
    for i, b in enumerate(btns):
        cls = b.get_attribute("class") or ""
        selected = "border-transparent" in cls
        print(f"  Card[{i}]: selected={selected} text={b.text[:30]!r}")

def invoke_react_onclick(el):
    return driver.execute_script("""
        var el = arguments[0];
        var fiberKey = Object.keys(el).find(function(k) {
            return k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance');
        });
        console.log('fiberKey:', fiberKey);
        if (!fiberKey) return {found: false, msg: 'no fiber key'};
        var fiber = el[fiberKey];
        var node = fiber;
        for (var i = 0; i < 10; i++) {
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
                return {found: true, level: i};
            }
            node = node.return;
        }
        return {found: false, msg: 'onClick not found in 10 levels'};
    """, el)

try:
    login()
    driver.get(APP_URL + "/creator/new")
    print("\n[Step 1] Waiting for page stable...")
    wait_stable()
    time.sleep(2.0)  # extra settle
    print("[Step 1] Done")

    print("\n[Step 2] Finding cards...")
    btns = wait.until(EC.presence_of_all_elements_located((By.XPATH, CARD_XPATH)))
    print(f"  Found {len(btns)} cards")
    check_card_state()

    print("\n[Step 3] Trying React fiber onClick on card[1] (standard)...")
    btn = btns[1]
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    result = invoke_react_onclick(btn)
    print(f"  React onClick result: {result}")
    time.sleep(0.8)
    print("  After React onClick:")
    check_card_state()

    print("\n[Step 4] If not selected, trying ActionChains...")
    btns_fresh = driver.find_elements(By.XPATH, CARD_XPATH)
    if btns_fresh:
        cls = btns_fresh[1].get_attribute("class") or ""
        if "border-transparent" not in cls:
            print("  Card still not selected, trying ActionChains...")
            try:
                ActionChains(driver).move_to_element(btns_fresh[1]).click().perform()
                time.sleep(0.8)
                print("  ActionChains clicked")
                check_card_state()
            except Exception as e:
                print(f"  ActionChains failed: {e.__class__.__name__}: {str(e)[:80]}")

    print("\n[Step 5] Checking Continue button state...")
    xp_cont = "//button[contains(.,'→') and not(contains(.,'←'))]"
    cont_btns = driver.find_elements(By.XPATH, xp_cont)
    for b in cont_btns:
        cls = b.get_attribute("class") or ""
        dis = b.get_attribute("disabled")
        print(f"  Continue btn: text={b.text!r} disabled={dis!r} opacity50={'opacity-50' in cls}")

    print("\n[Step 6] Body text (first 400):")
    print(driver.find_element(By.TAG_NAME, "body").text[:400])

    print("\n=== Debug complete ===")

except Exception:
    print(f"\nFAILED:\n{traceback.format_exc()}")
    try:
        print("Body:", driver.find_element(By.TAG_NAME, "body").text[:300])
    except Exception:
        pass

finally:
    input("\nPress Enter to close...")
    driver.quit()
