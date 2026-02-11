"""
Structural Qubits - Classical implementation of quantum concepts
Non-local, non-probabilistic, collapse only via inversion
"""
from dataclasses import dataclass
from typing import Set, List

@dataclass
class StructuralQubit:
    """A QGL qubit: {A ⊕ B} - unresolved superposition"""
    name: str
    state_a: str
    state_b: str
    entangled_with: Set[str] = None  # Names of other qubits
    
    def __post_init__(self):
        if self.entangled_with is None:
            self.entangled_with = set()
    
    def is_entangled(self):
        return len(self.entangled_with) > 0
    
    def entangle_with(self, other_qubit_name):
        """Create entanglement = shared admissibility constraint"""
        self.entangled_with.add(other_qubit_name)
    
    def collapse_via_inversion(self, choice):
        """
        Collapse occurs ONLY via inversion
        Returns collapsed state (A or B)
        """
        if choice == 'A':
            return self.state_a
        elif choice == 'B':
            return self.state_b
        else:
            raise ValueError("Qubit collapse must choose A or B")
    
    def to_string(self):
        """String representation: {A ⊕ B}"""
        return f"{{{self.state_a} ⊕ {self.state_b}}}"

class QubitRegistry:
    """Global registry of all qubits (non-local)"""
    
    def __init__(self):
        self.qubits: Dict[str, StructuralQubit] = {}
        self.entanglement_groups: List[Set[str]] = []
    
    def register_qubit(self, qubit):
        """Register a qubit in global registry"""
        self.qubits[qubit.name] = qubit
    
    def create_entanglement(self, qubit_name_1, qubit_name_2):
        """Create entanglement between two qubits"""
        if qubit_name_1 in self.qubits and qubit_name_2 in self.qubits:
            self.qubits[qubit_name_1].entangle_with(qubit_name_2)
            self.qubits[qubit_name_2].entangle_with(qubit_name_1)
            
            # Update entanglement groups
            self._update_entanglement_groups(qubit_name_1, qubit_name_2)
    
    def _update_entanglement_groups(self, q1, q2):
        """Update global entanglement groups"""
        found_group = None
        for group in self.entanglement_groups:
            if q1 in group or q2 in group:
                found_group = group
                break
        
        if found_group:
            found_group.add(q1)
            found_group.add(q2)
        else:
            self.entanglement_groups.append({q1, q2})
    
    def get_entanglement_group(self, qubit_name):
        """Get all qubits entangled with given qubit"""
        for group in self.entanglement_groups:
            if qubit_name in group:
                return group.copy()
        return {qubit_name}
    
    def collapse_entangled_group(self, group, choices):
        """
        Collapse an entire entanglement group via inversion
        choices: dict of qubit_name -> 'A' or 'B'
        """
        collapsed_states = {}
        
        for qubit_name in group:
            if qubit_name not in choices:
                raise ValueError(f"No collapse choice for qubit {qubit_name}")
            
            qubit = self.qubits[qubit_name]
            collapsed_states[qubit_name] = qubit.collapse_via_inversion(
                choices[qubit_name]
            )
        
        return collapsed_states