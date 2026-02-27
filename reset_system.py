# -*- coding: utf-8 -*-
"""Reset and Rebuild System"""
import os
import shutil

print("="*60)
print("RESET CORTEXDESK")
print("="*60)

# Backup and clear vector database
print("\n[1] Resetting vector database...")
if os.path.exists("data/vectors.pkl"):
    if os.path.exists("data/vectors_backup.pkl"):
        os.remove("data/vectors_backup.pkl")
    shutil.copy("data/vectors.pkl", "data/vectors_backup.pkl")
    os.remove("data/vectors.pkl")
    print("   [OK] Old database backed up and removed")
else:
    print("   [OK] No database to remove")

# Create fresh empty database
print("\n[2] Creating fresh database...")
import pickle
with open("data/vectors.pkl", "wb") as f:
    pickle.dump({"vectors": [], "metadata": []}, f)
print("   [OK] Fresh database created")

print("\n" + "="*60)
print("RESET COMPLETE")
print("="*60)

print("\nNEXT STEPS:")
print("1. Restart API:")
print("   python src\\api.py")
print("\n2. Add sample data:")
print("   - Open cortexdesk.html")
print("   - Dashboard > Manual Entry")
print("   - Paste: 'John needs to finish the database migration by Friday'")
print("   - Click Process Text")
print("   - Wait 5 seconds")
print("\n3. Test search:")
print("   - Go to Research page")
print("   - Search for: database")
print("   - Should work now!")
