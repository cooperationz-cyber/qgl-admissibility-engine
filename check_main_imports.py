# check_main_imports.py
import ast
import sys

print("="*60)
print("CHECKING main.py IMPORTS")
print("="*60)

try:
    with open("main.py", "r") as f:
        content = f.read()
    
    # Parse the AST
    tree = ast.parse(content)
    
    print("IMPORT STATEMENTS FOUND:")
    print("-"*40)
    
    imports_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports_found.append(alias.name)
                print(f"  import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [alias.name for alias in node.names]
            import_str = f"  from {module} import {', '.join(names)}"
            imports_found.append(module)
            print(import_str)
    
    print(f"\nTotal imports: {len(imports_found)}")
    
    # Check for problematic imports
    problematic = []
    for imp in imports_found:
        if "engines" in imp and not imp.startswith("engine"):
            problematic.append(imp)
    
    if problematic:
        print(f"\n⚠️  POTENTIAL ISSUE: Found 'engines' imports but your folder is 'engine/'")
        for p in problematic:
            print(f"   - {p}")
        print("\nThis will cause ImportError!")
    
except Exception as e:
    print(f"❌ Error analyzing main.py: {e}")

print("\n" + "="*60)

# Now let's test the actual imports
print("\nTESTING ACTUAL IMPORTS:")
print("-"*40)

modules_to_test = [
    "qgl.lexer",
    "qgl.parser", 
    "qgl.interpreter",
    "qgl.codegen",
    "engine.admissibility_engine",
    "engine.inversion_engine", 
    "engine.qubit_engine",
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module}")
    except ImportError as e:
        print(f"❌ {module}: {str(e)[:80]}...")

print("\n" + "="*60)
input("Press Enter to exit...")