# -*- coding: utf-8 -*-
"""Check creator/admin Firestore user docs."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os, requests
from dotenv import load_dotenv
load_dotenv()

FIREBASE_API_KEY = os.environ["FIREBASE_API_KEY"]
FIREBASE_PROJECT = os.getenv("FIREBASE_PROJECT", "datn-quizapp")
SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT}/databases/(default)/documents"

for role, email, pwd in [
    ("creator", os.environ["CREATOR_EMAIL"], os.environ["CREATOR_PASSWORD"]),
    ("admin", os.environ["ADMIN_EMAIL"], os.environ["ADMIN_PASSWORD"]),
]:
    print(f"\n=== {role} ({email}) ===")
    try:
        r = requests.post(SIGN_IN_URL, json={"email": email, "password": pwd, "returnSecureToken": True})
        r.raise_for_status()
        data = r.json()
        id_token = data["idToken"]
        local_id = data["localId"]
        print(f"  Auth OK, uid={local_id}")

        # Check Firestore user doc
        url = f"{FIRESTORE_BASE}/users/{local_id}"
        rr = requests.get(url, headers={"Authorization": f"Bearer {id_token}"})
        print(f"  Firestore GET /users/{local_id}: {rr.status_code}")
        if rr.status_code == 200:
            fields = rr.json().get("fields", {})
            print(f"  Fields: {fields}")
        else:
            print(f"  Response: {rr.text[:200]}")
    except Exception as e:
        print(f"  ERROR: {e}")
