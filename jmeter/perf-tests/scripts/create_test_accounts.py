"""
create_test_accounts.py
=======================
Tạo 200 tài khoản Firebase test cho performance testing.

Yêu cầu:
    pip install firebase-admin

Cách chạy:
    python create_test_accounts.py

Output:
    perf-tests/data/accounts.csv  (uid, email, password)

Idempotent: an toàn khi chạy lại — các tài khoản đã tồn tại sẽ bị bỏ qua.
"""

import csv
import os
import sys

import firebase_admin
from firebase_admin import auth, credentials

# ─────────────────────────────────────────────
# CẤU HÌNH — chỉnh sửa 2 dòng này nếu cần
# ─────────────────────────────────────────────

# Đường dẫn tới file service account JSON tải về từ Firebase Console
SERVICE_ACCOUNT_PATH = r"C:\Users\QUY\Downloads\datn-quizapp-firebase-adminsdk-fbsvc-f51742468d.json"

# File output CSV (đường dẫn tương đối từ thư mục gốc dự án)
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "accounts.csv")

# Số lượng tài khoản cần tạo
TOTAL_ACCOUNTS = 200

# Format email và password cho từng tài khoản test
EMAIL_FORMAT   = "perf_user_{i}@test.com"   # i từ 1 → TOTAL_ACCOUNTS
PASSWORD_FORMAT = "PerfTest@{i}"             # i từ 1 → TOTAL_ACCOUNTS

# In tiến độ mỗi bao nhiêu tài khoản
PROGRESS_INTERVAL = 50

# ─────────────────────────────────────────────


def init_firebase():
    """Khởi tạo Firebase Admin SDK với service account."""
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        sys.exit(
            f"[ERROR] Không tìm thấy service account file:\n  {SERVICE_ACCOUNT_PATH}\n"
            "Tải về tại: Firebase Console → Project Settings → Service Accounts → Generate new private key"
        )
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    # Chỉ khởi tạo 1 lần, tránh lỗi khi chạy lại trong cùng process
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    print(f"[OK] Firebase Admin SDK đã khởi tạo với project: datn-quizapp")


def load_existing_accounts(csv_path: str) -> dict:
    """
    Đọc file CSV đã có (nếu tồn tại) và trả về dict {email: uid}.
    Dùng để bỏ qua các tài khoản đã được tạo từ lần chạy trước.
    """
    existing = {}
    if not os.path.exists(csv_path):
        return existing
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing[row["email"]] = row["uid"]
    print(f"[INFO] Đã load {len(existing)} tài khoản từ file CSV cũ.")
    return existing


def create_account(email: str, password: str) -> str | None:
    """
    Tạo một tài khoản Firebase Auth.
    Trả về uid nếu thành công, None nếu email đã tồn tại (bỏ qua).
    Ném lỗi với các trường hợp khác.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except auth.EmailAlreadyExistsError:
        # Tài khoản đã có → lấy uid hiện tại thay vì báo lỗi
        existing_user = auth.get_user_by_email(email)
        return existing_user.uid
    except Exception as e:
        print(f"[WARN] Không tạo được tài khoản {email}: {e}")
        return None


def main():
    init_firebase()

    # Đảm bảo thư mục output tồn tại
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    # Load các tài khoản đã tạo trước đó (để idempotent)
    existing = load_existing_accounts(OUTPUT_CSV)

    # Mở CSV ở chế độ append để ghi thêm tài khoản mới
    csv_file = open(OUTPUT_CSV, "a", newline="", encoding="utf-8")
    writer   = csv.writer(csv_file)

    # Ghi header chỉ khi file mới (chưa có nội dung)
    if os.path.getsize(OUTPUT_CSV) == 0:
        writer.writerow(["uid", "email", "password"])

    created  = 0   # số tài khoản tạo mới trong lần chạy này
    skipped  = 0   # số tài khoản bỏ qua vì đã tồn tại trong CSV
    failed   = 0   # số tài khoản tạo thất bại

    print(f"\n[START] Bắt đầu tạo {TOTAL_ACCOUNTS} tài khoản test...\n")

    for i in range(1, TOTAL_ACCOUNTS + 1):
        email    = EMAIL_FORMAT.format(i=i)
        password = PASSWORD_FORMAT.format(i=i)

        # Bỏ qua nếu đã có trong CSV từ lần chạy trước
        if email in existing:
            skipped += 1
        else:
            uid = create_account(email, password)
            if uid:
                # Lưu vào CSV ngay sau khi tạo (tránh mất dữ liệu nếu script crash)
                writer.writerow([uid, email, password])
                csv_file.flush()
                created += 1
            else:
                failed += 1

        # In tiến độ định kỳ
        if i % PROGRESS_INTERVAL == 0:
            print(f"  [{i}/{TOTAL_ACCOUNTS}] Đã xử lý — Tạo mới: {created}, Bỏ qua: {skipped}, Lỗi: {failed}")

    csv_file.close()

    # Tổng kết
    print(f"\n[DONE] Hoàn tất!")
    print(f"  Tạo mới : {created}")
    print(f"  Bỏ qua  : {skipped}")
    print(f"  Lỗi     : {failed}")
    print(f"  Output  : {os.path.abspath(OUTPUT_CSV)}")

    if failed > 0:
        print(f"\n[WARN] {failed} tài khoản thất bại — kiểm tra log bên trên.")


if __name__ == "__main__":
    main()
