# -*- coding: utf-8 -*-
"""Debug actual UI login flow for creator."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, time, traceback
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

APP_URL = "https://datn-quizapp.web.app"
CREATOR_EMAIL = os.environ["CREATOR_EMAIL"]
CREATOR_PASSWORD = os.environ["CREATOR_PASSWORD"]

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=opts)
driver.implicitly_wait(0)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Navigate to login
    driver.get(APP_URL + "/login")
    print(f"URL after /login nav: {driver.current_url}")

    # Wait for email input
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    print("Email input found")

    # Fill credentials
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(CREATOR_EMAIL)
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(CREATOR_PASSWORD)

    # Find login button
    btns = driver.find_elements(By.CSS_SELECTOR, "button.bg-blue-600.w-full")
    print(f"Found {len(btns)} buttons with selector 'button.bg-blue-600.w-full'")

    all_btns = driver.find_elements(By.TAG_NAME, "button")
    print(f"All buttons: {[b.text[:30] for b in all_btns]}")

    if btns:
        btns[0].click()
    else:
        # Try submit button
        submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit.click()

    # Wait for URL change
    try:
        wait.until(lambda d: "/login" not in d.current_url)
        print(f"URL after login: {driver.current_url}")
    except TimeoutException:
        print(f"Still on login after 15s: {driver.current_url}")
        print(f"Body: {driver.find_element(By.TAG_NAME, 'body').text[:300]}")

    time.sleep(1.5)
    print(f"URL after 1.5s sleep: {driver.current_url}")

    # Navigate to /creator/new
    driver.get(APP_URL + "/creator/new")
    time.sleep(3)
    print(f"URL after /creator/new nav: {driver.current_url}")
    print(f"Page body: {driver.find_element(By.TAG_NAME, 'body').text[:400]}")

    # Check for creator form
    grid = driver.find_elements(By.CSS_SELECTOR, "div.grid")
    print(f"Grid elements: {len(grid)}")

    # Check for auth-protected content
    btns2 = driver.find_elements(By.XPATH, "//div[contains(@class,'grid')]//button[.//h3]")
    print(f"Quiz type buttons: {len(btns2)}")

except Exception as e:
    print(f"\nFULL EXCEPTION:\n{traceback.format_exc()}")
finally:
    driver.quit()
    print("Done")
