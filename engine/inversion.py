"""
Inversion Engine - ONLY dynamic operation allowed
Atomic boundary ↔ content role swap
"""
from copy import deepcopy

class InversionEngine:
    """
    Inversion is the ONLY operation that changes structure.
    Atomic, non-iterative, preserves global constraints.
    """
    
    def __init__(self, admissibility_engine):
        self.admissibility = admissibility_engine
        self.inversion_log = []
    
    def invert(self, program, boundary_name):
        """
        Perform atomic inversion of a boundary.
        Returns: (new_program, success, reason)
        """
        # 1. Verify structure is admissible BEFORE inversion
        admissible, reason = self.admissibility.check_structure(program)
        if not admissible:
            return program, False, f"Cannot invert inadmissible structure: {reason}"
        
        # 2. Find the boundary to invert
        boundary_to_invert = None
        for boundary in program.boundaries:
            if boundary.name == boundary_name:
                boundary_to_invert = boundary
                break
        
        if not boundary_to_invert:
            return program, False, f"Boundary '{boundary_name}' not found"
        
        # 3. Create deep copy for inversion (atomic operation)
        new_program = deepcopy(program)
        
        # 4. Perform atomic swap: boundary becomes content, content becomes boundary
        inverted_boundary = self._perform_atomic_swap(
            new_program, boundary_to_invert
        )
        
        # 5. Verify admissibility AFTER inversion
        admissible_after, reason_after = self.admissibility.check_structure(new_program)
        if not admissible_after:
            # Roll back - inversion failed
            return program, False, f"Inversion produced inadmissible structure: {reason_after}"
        
        # 6. Log the inversion (bookkeeping ONLY)
        self.inversion_log.append({
            'boundary': boundary_name,
            'before': program,
            'after': new_program,
            'atomic': True,
            'iterations': 0  # Always 0 - inversion is atomic
        })
        
        return new_program, True, "Inversion successful"
    
    def _perform_atomic_swap(self, program, boundary):
        """
        Atomic operation: boundary ↔ content role swap
        No partial operations. No iteration.
        """
        # Remove the boundary from boundaries list
        program.boundaries = [b for b in program.boundaries if b.name != boundary.name]
        
        # Create new boundaries from the content
        for item_name in boundary.content:
            # Each item in content becomes a new boundary containing the old boundary name
            new_boundary = type(boundary)(
                name=item_name,
                content=[boundary.name]
            )
            program.boundaries.append(new_boundary)
        
        # The old boundary name becomes regular content in the new boundaries
        # (Already handled above)
        
        return program
    
    def get_inversion_count(self):
        """Return number of inversions performed"""
        return len(self.inversion_log)
    
    def get_inversion_history(self):
        """Return inversion log - READ ONLY"""
        return self.inversion_log.copy()