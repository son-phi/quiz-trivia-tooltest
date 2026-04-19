# -*- coding: utf-8 -*-
"""Debug TC-CQ-001 to get full exception."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import sys, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "selenium" / "scripts"))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

from conftest import APP_URL, get_id_token, TEST_ACCOUNTS
import requests, os
from dotenv import load_dotenv
load_dotenv()

FIREBASE_API_KEY = os.environ["FIREBASE_API_KEY"]
SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=opts)
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 15)

try:
    # Login as creator
    acc = TEST_ACCOUNTS["creator"]
    resp = requests.post(SIGN_IN_URL, json={
        "email": acc["email"], "password": acc["password"], "returnSecureToken": True
    })
    resp.raise_for_status()
    data = resp.json()
    id_token = data["idToken"]
    local_id = data["localId"]

    # Set cookies via localStorage
    driver.get(APP_URL)
    time.sleep(3)
    driver.execute_script(f"""
        localStorage.setItem('firebase:authUser:AIzaSyDtBzTHNPQ5PxKhVb-si89kgr5T_3ppwj8:[DEFAULT]',
            JSON.stringify({{
                "uid": "{local_id}",
                "email": "{acc['email']}",
                "stsTokenManager": {{
                    "accessToken": "{id_token}",
                    "expirationTime": {int(time.time()) * 1000 + 3600000}
                }}
            }})
        );
    """)
    driver.refresh()
    time.sleep(3)

    print("Page title:", driver.title)
    print("URL:", driver.current_url)

    # Navigate to /creator/new
    driver.get(APP_URL + "/creator/new")
    time.sleep(3)
    print("After nav to /creator/new:", driver.current_url)

    body_text = driver.find_element(By.TAG_NAME, "body").text[:300]
    print("Body text:", body_text)

    # Wait for grid
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid")))
        print("Grid found!")
    except Exception as e:
        print(f"Grid not found: {e}")

    time.sleep(1)

    # Find type buttons
    btns = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@class,'grid')]//button[.//h3]")
    ))
    print(f"Found {len(btns)} type buttons")

    # Click standard (index 1)
    driver.execute_script("arguments[0].click();", btns[1])
    time.sleep(0.3)

    # Click continue
    xp = "//button[contains(.,'→') and not(contains(.,'←'))]"
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
    btn.click()
    time.sleep(0.8)

    print("After continue click:", driver.current_url)
    body_text2 = driver.find_element(By.TAG_NAME, "body").text[:300]
    print("Body text after continue:", body_text2)

    # Wait for title input
    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.w-full.p-4.border-2.border-gray-200.rounded-xl")
        ))
        print("Title input found! Step 1 reached.")
    except Exception as e:
        print(f"Title input NOT found: {e}")

except Exception as e:
    print(f"\nFULL EXCEPTION:\n{traceback.format_exc()}")
finally:
    driver.quit()
    print("Done")
