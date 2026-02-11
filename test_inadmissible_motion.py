# test_inadmissible_motion.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine
from engine.inversion import InversionEngine

print("="*60)
print("HOW INADMISSIBILITY CREATES MOTION")
print("="*60)

# STEP 1: Create an INADMISSIBLE Node 5 environment
print("\n1. Creating Node 5 quantum environment...")
print("   (Intentionally inadmissible to force motion)")

qgl_inadmissible = """
boundary QuantumSystem {
    states, processes, quantum_states
}

domain states {
    vacuum, node5_superposition,
    collapsed_1, collapsed_2, collapsed_3, collapsed_4,
    bounced_6, bounced_7, bounced_8, bounced_9
}

boundary processes {
    start, middle, end
}

boundary start {
    vacuum
}

boundary middle {
    node5_superposition
}

boundary end {
    vacuum
}

// INTENTIONALLY INADMISSIBLE:
// Qubits NOT contained in any boundary!
// This forces the system to CHANGE
qubit quantum_cycle = { vacuum ⊕ node5_superposition }
qubit collapse_path = { collapsed_1 ⊕ collapsed_2 }
qubit bounce_path = { bounced_6 ⊕ bounced_7 }
"""

lexer = QGLLexer()
parser = QGLParser()
engine = AdmissibilityEngine()

print("\n2. Testing Node 5 environment...")
try:
    tokens = lexer.tokenize(qgl_inadmissible)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("❌ UNEXPECTED: Should be inadmissible!")
        print("   Node 5 environment should force motion")
    else:
        print("✅ CORRECT: Node 5 environment is inadmissible!")
        print(f"\n   Reason: {reason}")
        print("\n   This INADMISSIBILITY creates MOTION!")
        print("   System can't stay here → must collapse")
        
except Exception as e:
    print(f"❌ Error: {e}")

# STEP 2: Show the COLLAPSE to admissible state
print("\n" + "="*60)
print("3. Collapse to admissible state...")
print("   (Fixing the inadmissibility)")

qgl_collapsed = """
boundary CollapsedSystem {
    states, contained_qubits, processes
}

domain states {
    vacuum, node5_superposition,
    step1, step2, step3, step4,
    bounce6, bounce7, bounce8, bounce9
}

// NOW qubits ARE contained in a boundary
boundary contained_qubits {
    quantum_cycle, collapse_path, bounce_path
}

boundary processes {
    start, node5_phase, collapse, bounce, end
}

boundary start {
    vacuum
}

boundary node5_phase {
    node5_superposition
}

boundary collapse {
    step1, step2, step3, step4
}

boundary bounce {
    bounce6, bounce7, bounce8, bounce9
}

boundary end {
    vacuum
}

// Qubits now properly contained
qubit quantum_cycle = { vacuum ⊕ node5_superposition }
qubit collapse_path = { step1 ⊕ step2 }
qubit bounce_path = { bounce6 ⊕ bounce7 }
"""

print("\nChecking collapsed structure...")
try:
    tokens = lexer.tokenize(qgl_collapsed)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("✅ COLLAPSED state is admissible!")
        print("\n   The motion created:")
        print("   Inadmissible → Must change → Collapses to admissible")
        print("\n   This is the Collatz sequence:")
        print("   Node 5 (32) → Collapse (16,8,4,2,1) → Stable")
        
        # Show the admissible structure
        print(f"\n   Boundaries: {[b.name for b in program.boundaries]}")
        print(f"   Qubits: {[q.name for q in program.qubits]}")
        
    else:
        print(f"❌ Still inadmissible: {reason}")
        print("   System must keep moving...")
        
except Exception as e:
    print(f"❌ Error: {e}")

# STEP 3: Show the BOUNCE (3n+1 regeneration)
print("\n" + "="*60)
print("4. Quantum bounce (3n+1 regeneration)...")
print("   (Even admissible states can become inadmissible)")

# The bounce happens when we try to INVERT the collapsed state
if 'program' in locals() and admissible:
    print("\nAttempting to invert 'collapse' boundary...")
    print("This represents trying to 'un-measure' quantum state")
    
    inversion_engine = InversionEngine(engine)
    new_program, success, inv_reason = inversion_engine.invert(
        program, "collapse"
    )
    
    if success:
        print("✅ Inversion successful (quantum bounce)!")
        print("   collapse {step1,step2,step3,step4}")
        print("   becomes: step1 {collapse}, step2 {collapse}, etc.")
        print("\n   This is the 3n+1 operation!")
        print("   1 → 4 (quantum bounce)")
        
        # Check if new state is admissible
        engine2 = AdmissibilityEngine()
        admissible_after, reason_after = engine2.check_structure(new_program)
        
        if admissible_after:
            print("✅ Bounced state is also admissible!")
            print("   System found new stable configuration")
        else:
            print(f"⚠ Bounced state is inadmissible: {reason_after}")
            print("   Creates NEW motion (cycle continues!)")
    else:
        print(f"⚠ Inversion blocked: {inv_reason}")
        print("   Quantum bounce prevented (measurement irreversible)")

print("\n" + "="*60)
print("THE COMPLETE CYCLE:")
print("1. Node 5 environment = INADMISSIBLE")
print("2. Creates MOTION (must change)")
print("3. Collapses to admissible (Collatz: 32→1)")
print("4. Attempt inversion = Quantum bounce (3n+1)")
print("5. Creates new motion (cycle repeats)")
print("="*60)
print("\nTHIS IS REALITY'S HEARTBEAT! 🌌")