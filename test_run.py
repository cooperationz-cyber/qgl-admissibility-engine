# test_run.py - Simple test to see what's happening
import sys
import os

print("=" * 60)
print("TESTING QGL ADMISSIBILITY ENGINE")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Try to import basic modules
try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ numpy import failed: {e}")

# Check if main.py exists
if os.path.exists("main.py"):
    print("✅ main.py found")
else:
    print("❌ main.py NOT found!")
    
# Check for qgl folder
if os.path.exists("qgl"):
    print("✅ qgl/ folder found")
    print(f"   Contents: {os.listdir('qgl')}")
else:
    print("❌ qgl/ folder NOT found!")

print("=" * 60)
input("Press Enter to exit...")