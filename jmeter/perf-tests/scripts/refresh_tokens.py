"""
refresh_tokens.py
=================
Đọc accounts.csv, đăng nhập từng tài khoản qua Firebase Auth REST API,
lưu ID Token vào users.csv để JMeter dùng cho các request cần xác thực.

ID Token Firebase hết hạn sau 1 giờ — chạy script này trước mỗi lần test.

Yêu cầu:
    pip install requests

Cách chạy:
    python refresh_tokens.py

Output:
    perf-tests/data/users.csv  (uid, email, idToken)

Hiệu suất: tối đa 20 luồng song song → hoàn tất 200 tài khoản < 2 phút.
"""

import csv
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ─────────────────────────────────────────────
# CẤU HÌNH
# ─────────────────────────────────────────────

# Firebase Web API Key — lấy từ Firebase Console → Project Settings → General
FIREBASE_API_KEY = "AIzaSyDtBzTHNPQ5PxKhVb-si89kgr5T_3ppwj8"

# File input (output của create_test_accounts.py)
INPUT_CSV  = os.path.join(os.path.dirname(__file__), "..", "data", "accounts.csv")

# File output dùng bởi JMeter CSV Data Set Config
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")

# Số luồng song song tối đa (tăng → nhanh hơn nhưng dễ bị rate limit)
MAX_WORKERS = 20

# Endpoint Firebase Auth REST API để đăng nhập bằng email/password
SIGN_IN_URL = (
    f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    f"?key={FIREBASE_API_KEY}"
)

# Timeout cho mỗi request đăng nhập (giây)
REQUEST_TIMEOUT = 10

# ─────────────────────────────────────────────


def read_accounts(csv_path: str) -> list[dict]:
    """
    Đọc file accounts.csv và trả về danh sách dict {uid, email, password}.
    Dừng chương trình nếu file không tồn tại.
    """
    if not os.path.exists(csv_path):
        sys.exit(
            f"[ERROR] Không tìm thấy {csv_path}\n"
            "Hãy chạy create_test_accounts.py trước."
        )
    accounts = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts.append(row)
    print(f"[INFO] Đọc được {len(accounts)} tài khoản từ {csv_path}")
    return accounts


def fetch_token(account: dict) -> dict:
    """
    Gọi Firebase Auth REST API để lấy ID Token cho một tài khoản.

    Trả về dict {uid, email, idToken} nếu thành công.
    Trả về dict {uid, email, idToken: None} và in cảnh báo nếu thất bại.

    Firebase Auth REST API endpoint:
        POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}
    Body:
        { "email": "...", "password": "...", "returnSecureToken": true }
    Response:
        { "idToken": "...", "localId": "...", ... }
    """
    email    = account["email"]
    password = account["password"]
    uid      = account["uid"]

    try:
        resp = requests.post(
            SIGN_IN_URL,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,  # bắt buộc để nhận idToken
            },
            timeout=REQUEST_TIMEOUT,
        )

        if resp.status_code == 200:
            id_token = resp.json().get("idToken")
            if id_token:
                return {"uid": uid, "email": email, "idToken": id_token}
            # Đăng nhập thành công nhưng không có token (hiếm gặp)
            print(f"[WARN] Không lấy được idToken cho {email} — response thiếu field idToken")
        else:
            # Lỗi phía Firebase (sai password, tài khoản bị khóa, v.v.)
            error_msg = resp.json().get("error", {}).get("message", "UNKNOWN")
            print(f"[WARN] Đăng nhập thất bại cho {email}: {error_msg} (HTTP {resp.status_code})")

    except requests.exceptions.Timeout:
        print(f"[WARN] Timeout khi đăng nhập {email}")
    except requests.exceptions.ConnectionError:
        print(f"[WARN] Lỗi kết nối khi đăng nhập {email}")
    except Exception as e:
        print(f"[WARN] Lỗi không xác định khi đăng nhập {email}: {e}")

    # Trả về None idToken để caller biết cần bỏ qua dòng này
    return {"uid": uid, "email": email, "idToken": None}


def main():
    start_time = time.time()

    accounts = read_accounts(INPUT_CSV)
    if not accounts:
        sys.exit("[ERROR] accounts.csv trống — không có tài khoản để xử lý.")

    # Đảm bảo thư mục output tồn tại
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    success_rows = []  # các dòng sẽ ghi vào users.csv
    failed_count = 0

    print(f"\n[START] Lấy token cho {len(accounts)} tài khoản ({MAX_WORKERS} luồng song song)...\n")

    # Dùng ThreadPoolExecutor để gửi nhiều request đồng thời
    # as_completed() trả về kết quả ngay khi từng future hoàn thành (không theo thứ tự)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_account = {
            executor.submit(fetch_token, acc): acc for acc in accounts
        }

        completed = 0
        for future in as_completed(future_to_account):
            result    = future.result()
            completed += 1

            if result["idToken"]:
                success_rows.append(result)
            else:
                failed_count += 1

            # In tiến độ mỗi 50 tài khoản
            if completed % 50 == 0:
                elapsed = time.time() - start_time
                print(f"  [{completed}/{len(accounts)}] Xong: {len(success_rows)}, Lỗi: {failed_count} ({elapsed:.1f}s)")

    # Ghi kết quả vào users.csv (ghi đè toàn bộ — token mới nhất)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["uid", "email", "idToken"])
        writer.writeheader()
        writer.writerows(success_rows)

    elapsed = time.time() - start_time

    # Tổng kết
    print(f"\n[DONE] Hoàn tất trong {elapsed:.1f}s")
    print(f"  Thành công : {len(success_rows)}")
    print(f"  Thất bại   : {failed_count}")
    print(f"  Output     : {os.path.abspath(OUTPUT_CSV)}")

    if elapsed > 120:
        print(f"\n[WARN] Mất {elapsed:.0f}s > 120s — xem xét tăng MAX_WORKERS hoặc kiểm tra kết nối.")

    if failed_count > 0:
        print(f"\n[WARN] {failed_count} tài khoản không lấy được token.")
        print("  Nguyên nhân thường gặp: sai password, tài khoản bị xóa, hoặc Firebase rate limit.")
        print("  Các tài khoản này sẽ KHÔNG có trong users.csv — JMeter sẽ bỏ qua.")

    if len(success_rows) == 0:
        sys.exit("[ERROR] Không lấy được token nào — kiểm tra FIREBASE_API_KEY và accounts.csv.")


if __name__ == "__main__":
    main()
