# -*- coding: utf-8 -*-
"""System Diagnostic"""
import requests
import os
import pickle

print("="*60)
print("CORTEXDESK DIAGNOSTIC")
print("="*60)

# 1. Check API
print("\n[1] API Status:")
try:
    r = requests.get("http://127.0.0.1:8001/", timeout=2)
    if r.status_code == 200:
        print("   [OK] API is running")
    else:
        print(f"   [FAIL] API returned {r.status_code}")
except:
    print("   [FAIL] API not running")
    print("   ACTION: Run 'python src\\api.py' in a terminal")
    exit(1)

# 2. Check vector database
print("\n[2] Vector Database:")
if os.path.exists("data/vectors.pkl"):
    with open("data/vectors.pkl", "rb") as f:
        data = pickle.load(f)
        count = len(data.get("vectors", []))
        print(f"   [OK] Database exists with {count} documents")
        if count == 0:
            print("   [WARN] Database is EMPTY - need to upload documents!")
else:
    print("   [WARN] Database doesn't exist yet")

# 3. Check confirmations
print("\n[3] Confirmations:")
if os.path.exists("data/confirmations.json"):
    import json
    with open("data/confirmations.json") as f:
        data = json.load(f)
        print(f"   [OK] {len(data)} pending confirmations")
else:
    print("   [WARN] No confirmations file")

# 4. Test search endpoint
print("\n[4] Search Endpoint:")
try:
    r = requests.post(
        "http://127.0.0.1:8001/search",
        json={"query": "test"},
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   [OK] Search works - {data.get('count', 0)} results")
        if 'message' in data:
            print(f"   Message: {data['message']}")
    else:
        print(f"   [FAIL] Error: {r.text[:100]}")
except Exception as e:
    print(f"   [FAIL] {str(e)}")

# 5. Check uploads directory
print("\n[5] Uploads:")
if os.path.exists("data/uploads"):
    files = os.listdir("data/uploads")
    print(f"   [OK] {len(files)} files in uploads")
    if files:
        print(f"   Recent: {files[-1] if files else 'none'}")
else:
    print("   [WARN] No uploads directory")

print("\n" + "="*60)
print("DIAGNOSIS COMPLETE")
print("="*60)

print("\nRECOMMENDED ACTIONS:")
print("1. If vector DB is empty:")
print("   - Go to Dashboard in browser")
print("   - Use Manual Entry to add text")
print("   - Wait 5 seconds")
print("   - Try search again")
print("\n2. If search still fails:")
print("   - Check API terminal for errors")
print("   - Restart API: python src\\api.py")
