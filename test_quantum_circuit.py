# test_quantum_circuit.py
print("="*60)
print("QUANTUM CIRCUIT VALIDATION")
print("="*60)

# Is this quantum circuit physically realizable?
qgl_code = """
boundary QuantumComputer {
    qubits, gates, measurement
}

domain Qubits {
    q0, q1, q2, q3
}

// Quantum gates as boundaries
boundary HadamardGate {
    q0, q1
}

boundary CNOTGate {
    control_q0, target_q1
}

boundary ToffoliGate {
    control_q0, control_q1, target_q2
}

// Structural constraint: No cloning theorem
// Cannot have gate that copies quantum states
constraint NoCloning {
    cannot_copy_qubit
}

// Entanglement constraint
qubit bell_pair = { q0_plus_q1 ⊕ q0_minus_q1 }
"""

print("\nChecking quantum circuit structure...")
try:
    tokens = lexer.tokenize(qgl_code)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("✅ Quantum circuit is structurally valid")
        print("   No violation of quantum principles")
        
        # Count components
        print(f"   Qubits: {len([d for d in program.domains if d.name == 'Qubits'][0].states)}")
        print(f"   Gates: {len([b for b in program.boundaries if 'Gate' in b.name])}")
        
    else:
        print(f"❌ Quantum principles violated: {reason}")
        
except Exception as e:
    print(f"❌ Error: {e}")