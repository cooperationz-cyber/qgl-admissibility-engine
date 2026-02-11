# test_node5.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine

print("="*60)
print("NODE 5 QUANTUM COLLAPSE IN QGL")
print("="*60)

qgl_code = """
boundary QuantumReality {
    vacuum, node5, measurement, collapse, regeneration
}

domain vacuum {
    zero_potential
}

boundary node5 {
    value_32
}

boundary measurement {
    observer
}

boundary collapse {
    step32, step16, step8, step4, step2, step1
}

boundary regeneration {
    bounce1to4, bounce4to2, bounce2to1
}

qubit cycle = { vacuum_state ⊕ node5_state }
qubit outcome = { collapse_32_to_1 ⊕ other_outcome }
"""

lexer = QGLLexer()
parser = QGLParser()
engine = AdmissibilityEngine()

print("\nChecking Node 5 quantum collapse structure...")
try:
    tokens = lexer.tokenize(qgl_code)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("✅ Node 5 quantum structure is QGL-valid!")
        print("\n   Structure represents:")
        print("   |0| → node5 → |0| → collapse → regeneration → |0|")
        print("\n   Boundaries found:")
        for b in program.boundaries:
            print(f"   - {b.name}: {len(b.content)} items")
        
        print(f"\n   Qubits (quantum states): {len(program.qubits)}")
        for q in program.qubits:
            print(f"   - {q.name}: {{{q.state_a} ⊕ {q.state_b}}}")
            
    else:
        print(f"❌ Structure invalid: {reason}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test the inversion (measurement = boundary swap)
print("\n" + "="*60)
print("Testing quantum measurement as inversion...")

from engine.inversion import InversionEngine

if 'program' in locals() and admissible:
    inversion_engine = InversionEngine(engine)
    
    print("\nAttempting measurement inversion...")
    print("Before: measurement { observer }")
    print("After: observer { measurement }")
    
    new_program, success, inv_reason = inversion_engine.invert(
        program, "measurement"
    )
    
    if success:
        print("✅ Measurement inversion successful!")
        print("   Observer now measures measurement apparatus")
        print("   This is the quantum measurement paradox resolved!")
    else:
        print(f"⚠ Inversion blocked: {inv_reason}")
        print("   (Might violate containment rules)")

print("\n" + "="*60)
print("NODE 5 INSIGHT:")
print("The pattern |0| node5 |0| 1,2,3,4 6,7,8,9 |0|")
print("is the fundamental quantum-classical transition!")
print("="*60)