# test_interpreter.py
import sys
import os
sys.path.insert(0, '.')

print("="*60)
print("TESTING INTERPRETER")
print("="*60)

try:
    from qgl.interpreter import StructuralInterpreter
    
    print("✅ Interpreter imported successfully")
    
    # Create interpreter
    interpreter = StructuralInterpreter(lattice_size=100)
    print(f"✅ Created interpreter with {len(interpreter.lattice)} void points")
    
    # Test Master Boot Sequence
    print("\nTesting Master Boot Sequence...")
    
    # Create a simple program
    from qgl.parser import Boundary, Domain, Qubit, QGLProgram
    
    program = QGLProgram(
        boundaries=[Boundary("test", ["a", "b"])],
        domains=[Domain("states", ["|0>", "|1>", "|0>⊕|1>"])],
        qubits=[Qubit("q1", "|0>", "|1>")]
    )
    
    # Execute
    results = interpreter.execute_program(program)
    print(f"✅ Execution results: {list(results.keys())}")
    
    if 'constants_generated' in results:
        constants = results['constants_generated']
        print(f"\nGenerated constants: {list(constants.keys())[:5]}...")
        
        # Check for key constants
        for const in ['phi_exact', 'e_exact', 'pi_exact']:
            if const in constants:
                value = constants[const]
                print(f"   {const}: {value}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nChecking interpreter.py...")
    
    if os.path.exists("qgl/interpreter.py"):
        with open("qgl/interpreter.py", "r") as f:
            first_line = f.readline()
            print(f"interpreter.py exists, first line: {first_line}")
    else:
        print("interpreter.py not found!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
input("Press Enter to exit...")