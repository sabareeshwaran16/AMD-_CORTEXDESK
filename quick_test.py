# -*- coding: utf-8 -*-
"""Quick Search Test"""
import requests
import time

API = "http://127.0.0.1:8001"

print("Testing search...")

# 1. Check API
try:
    requests.get(f"{API}/")
    print("[OK] API running")
except:
    print("[FAIL] Start API: python src\\api.py")
    exit(1)

# 2. Upload test data
text = "John needs to complete the database migration by Friday. Sarah will update the API documentation."
files = {'file': ('test.txt', text.encode(), 'text/plain')}
requests.post(f"{API}/upload", files=files)
print("[OK] Data uploaded")

time.sleep(2)

# 3. Search
r = requests.post(f"{API}/search", json={"query": "database"}, headers={"Content-Type": "application/json"})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:200]}")

if r.status_code == 200:
    data = r.json()
    if data['count'] > 0:
        match = data['results'][0]['similarity'] * 100
        print(f"[OK] Search works! Match: {match:.1f}%")
        if match > 50:
            print("[OK] Good similarity!")
        else:
            print("[WARN] Low similarity, but working")
    else:
        print("[FAIL] No results")
else:
    print(f"[FAIL] API error: {r.status_code}")

print("\nNow try in browser:")
print("1. Open cortexdesk.html")
print("2. Go to Research")
print("3. Search for 'database'")
