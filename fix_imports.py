# fix_imports.py
import os
import sys

print("Fixing import paths...")

# Check folder structure
folders = ["qgl", "engine", "engines"]
for folder in folders:
    if os.path.exists(folder):
        print(f"✅ {folder}/ exists")
        # Add __init__.py if missing
        init_file = os.path.join(folder, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write(f"# {folder} package\n")
            print(f"   Created {init_file}")

# Check if main.py tries to import from 'engines' instead of 'engine'
if os.path.exists("main.py"):
    with open("main.py", "r") as f:
        content = f.read()
    
    if "import engines" in content or "from engines" in content:
        print("\n⚠️  main.py imports from 'engines' but folder is 'engine'")
        fix = input("Fix this? (y/n): ")
        if fix.lower() == 'y':
            new_content = content.replace("import engines", "import engine")
            new_content = new_content.replace("from engines", "from engine")
            with open("main.py", "w") as f:
                f.write(new_content)
            print("✅ Fixed imports in main.py")

print("\nCreating test script...")

# Create a simple test
test_code = '''
print("="*60)
print("IMPORT TEST")
print("="*60)

import sys
sys.path.insert(0, '.')

try:
    import qgl.lexer
    print("✅ qgl.lexer")
except ImportError as e:
    print(f"❌ qgl.lexer: {e}")

try:
    import qgl.parser
    print("✅ qgl.parser")  
except ImportError as e:
    print(f"❌ qgl.parser: {e}")

try:
    # Try both engine and engines
    try:
        import engine
        print("✅ engine")
    except:
        import engines
        print("✅ engines")
except ImportError as e:
    print(f"❌ engine/engines: {e}")

print("="*60)
input("Press Enter...")
'''

with open("import_test.py", "w") as f:
    f.write(test_code)

print("✅ Created import_test.py")
print("\nRun: python import_test.py")