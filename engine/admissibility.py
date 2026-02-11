"""
Admissibility Engine - Validates structural constraints
NO simulation, NO optimization, NO search
"""
from typing import Dict, List, Tuple, Set

class AdmissibilityEngine:
    """
    Core Rule: No boundary may be a member of the system it bounds.
    Answer ONE question: Is this structure admissible?
    """
    
    def __init__(self):
        self.structures: Dict[str, Set[str]] = {}  # name -> contents
        self.constraints: List[callable] = []
        self.accumulation: List[Dict] = []  # Bookkeeping ONLY
        
        # Define global constraints
        self._setup_constraints()
    
    def _setup_constraints(self):
        """Define non-local constraints that must always hold"""
        
        # Constraint 1: No self-membership
        def no_self_membership(structure_name, contents):
            return structure_name not in contents
        
        # Constraint 2: No circular containment
        def no_circular_containment(structures):
            # Check for A contains B, B contains A
            for a_name, a_contents in structures.items():
                for b_name in a_contents:
                    if b_name in structures and a_name in structures[b_name]:
                        return False
            return True
        
        # Constraint 3: All qubits must be in some domain
        def qubits_in_domains(qubits, domains):
            all_domain_states = set()
            for domain in domains:
                for state in domain.states:
                    # Extract individual states from superposition
                    if '⊕' in state:
                        s1, s2 = state.split('⊕')
                        all_domain_states.add(s1)
                        all_domain_states.add(s2)
                    else:
                        all_domain_states.add(state)
            
            for qubit in qubits:
                if qubit.state_a not in all_domain_states:
                    return False, f"Qubit state {qubit.state_a} not in any domain"
                if qubit.state_b not in all_domain_states:
                    return False, f"Qubit state {qubit.state_b} not in any domain"
            return True, ""
        
        self.constraints = [
            no_self_membership,
            no_circular_containment,
            lambda s, q, d: qubits_in_domains(q, d)[0]
        ]
    
    def check_structure(self, program) -> Tuple[bool, str]:
        """
        Main admissibility check
        Returns: (is_admissible, reason_if_not)
        """
        reasons = []
        
        # 1. Check boundary self-containment
        for boundary in program.boundaries:
            if boundary.name in boundary.content:
                return False, f"Boundary '{boundary.name}' contains itself"
        
        # 2. Check circular containment
        structures = {}
        for boundary in program.boundaries:
            structures[boundary.name] = set(boundary.content)
        
        if not self.constraints[1](structures):  # no_circular_containment
            return False, "Circular containment detected"
        
        # 3. Check qubits are in domains
        qubit_domain_check, qubit_reason = self._check_qubit_domains(
            program.qubits, program.domains
        )
        if not qubit_domain_check:
            return False, qubit_reason
        
        # 4. Check all domains are inside some boundary
        all_boundary_contents = set()
        for boundary in program.boundaries:
            all_boundary_contents.update(boundary.content)
        
        for domain in program.domains:
            if domain.name not in all_boundary_contents:
                reasons.append(f"Domain '{domain.name}' not contained in any boundary")
        
        # 5. Check all qubits are inside some boundary
        for qubit in program.qubits:
            if qubit.name not in all_boundary_contents:
                reasons.append(f"Qubit '{qubit.name}' not contained in any boundary")
        
        if reasons:
            return False, "; ".join(reasons)
        
        # Record in accumulation (bookkeeping only)
        self.accumulation.append({
            'type': 'admissibility_check',
            'program': program,
            'result': 'admissible',
            'timestamp': self._get_timestamp()
        })
        
        return True, "Structure is admissible"
    
    def _check_qubit_domains(self, qubits, domains):
        """Check all qubit states exist in domains"""
        # Build set of all states in domains
        domain_states = set()
        for domain in domains:
            for state_str in domain.states:
                if '⊕' in state_str:
                    for state in state_str.split('⊕'):
                        domain_states.add(state)
                else:
                    domain_states.add(state_str)
        
        # Check each qubit
        for qubit in qubits:
            if qubit.state_a not in domain_states:
                return False, f"Qubit state '{qubit.state_a}' not in any domain"
            if qubit.state_b not in domain_states:
                return False, f"Qubit state '{qubit.state_b}' not in any domain"
        
        return True, ""
    
    def _get_timestamp(self):
        """Mock timestamp - in real implementation would use system time"""
        return "no-time-reference"  # QGL has no time
    
    def get_accumulation(self):
        """Return accumulation ledger - READ ONLY"""
        return self.accumulation.copy()