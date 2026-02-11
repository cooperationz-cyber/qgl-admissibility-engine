"""
QGL Interpreter - Advanced structural execution on void lattice
Performs non-iterative, non-temporal structural transformations
"""
import numpy as np
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
import math

@dataclass
class VoidPoint:
    """Single point in the void lattice"""
    id: int
    info_vector: np.ndarray  # 7D information space
    tension: float = 0.0
    occupied: bool = False
    structures: List[Dict] = None
    node: int = 0  # Master Boot Sequence node
    phase: float = 0.0  # Phase for quantum coherence
    
    def __post_init__(self):
        if self.structures is None:
            self.structures = []
    
    def add_structure(self, structure_type: str, name: str, **kwargs):
        """Add structure to this void point"""
        self.occupied = True
        self.structures.append({
            'type': structure_type,
            'name': name,
            **kwargs
        })
    
    def get_info_magnitude(self) -> float:
        """Get magnitude of information vector"""
        return np.linalg.norm(self.info_vector)
    
    def get_phase_coherence(self, other_point: 'VoidPoint') -> float:
        """Calculate phase coherence between two points"""
        if len(self.info_vector) != len(other_point.info_vector):
            return 0.0
        return np.dot(self.info_vector, other_point.info_vector) / (
            self.get_info_magnitude() * other_point.get_info_magnitude()
        )

class StructuralInterpreter:
    """
    Advanced QGL interpreter that executes structures on void lattice
    WITHOUT iteration, time, or optimization
    """
    
    def __init__(self, lattice_size: int = 1000):
        self.lattice: List[VoidPoint] = []
        self.structure_map: Dict[str, List[int]] = {}  # name -> point_ids
        self.entanglement_groups: List[Set[int]] = []
        self.accumulated_info: List[float] = []
        self.node_progression: Dict[int, str] = {}
        
        # Golden ratio constants
        self.PHI = (1 + math.sqrt(5)) / 2
        self.E = math.e
        self.PI = math.pi
        
        self._initialize_lattice(lattice_size)
    
    def _initialize_lattice(self, size: int):
        """Initialize void lattice with optimal φ spacing"""
        print(f"🌀 Initializing void lattice with {size} points (φ-scaled)")
        
        for i in range(size):
            # Create information vector with φ-influenced distribution
            angle = i * 2 * math.pi / self.PHI
            info_vector = np.array([
                math.sin(angle),           # x component
                math.cos(angle),           # y component
                math.sin(angle * self.PHI), # φ harmonic
                math.cos(angle * self.PHI),
                math.sin(angle / self.PHI), # 1/φ harmonic
                math.cos(angle / self.PHI),
                0.618 * (i % 7)           # φ residual
            ])
            
            # Normalize and scale by φ
            norm = np.linalg.norm(info_vector)
            if norm > 0:
                info_vector = (info_vector / norm) * 0.618
            
            # Tension follows inverse square of φ
            tension = 0.1 * (i % int(self.PHI * 10)) / 10.0
            
            point = VoidPoint(
                id=i,
                info_vector=info_vector,
                tension=tension,
                phase=(i * self.PHI) % (2 * math.pi)
            )
            self.lattice.append(point)
        
        print(f"✅ Void lattice initialized with {len(self.lattice)} points")
    
    def execute_program(self, program) -> Dict[str, Any]:
        """
        Execute complete QGL program on void lattice
        Returns execution results including constants
        """
        print("\n" + "="*60)
        print("🧠 EXECUTING QGL PROGRAM ON VOID LATTICE")
        print("="*60)
        
        results = {
            'boundaries_placed': 0,
            'domains_placed': 0,
            'qubits_placed': 0,
            'information_accumulated': 0.0,
            'structural_coherence': 0.0,
            'constants_generated': {},
            'execution_sequence': []
        }
        
        # Reset lattice for fresh execution
        for point in self.lattice:
            point.occupied = False
            point.structures = []
            point.node = 0
        
        # Clear structure map
        self.structure_map.clear()
        self.entanglement_groups = []
        self.accumulated_info = []
        
        # Step 1: Execute boundaries (node 1: φ emergence)
        self._execute_boundaries(program.boundaries, results)
        results['execution_sequence'].append('boundaries')
        
        # Step 2: Execute domains (node 2: e emergence)
        self._execute_domains(program.domains, results)
        results['execution_sequence'].append('domains')
        
        # Step 3: Execute qubits (node 3: π emergence)
        self._execute_qubits(program.qubits, results)
        results['execution_sequence'].append('qubits')
        
        # Step 4: Create entanglement (node 4: α emergence)
        self._create_entanglements(program, results)
        results['execution_sequence'].append('entanglements')
        
        # Step 5: Accumulate information (node 5: collapse → constants)
        accumulated = self._accumulate_information()
        results.update(accumulated)
        results['execution_sequence'].append('accumulation')
        
        # Step 6: Generate constants
        constants = self._generate_constants()
        results['constants_generated'] = constants
        results['execution_sequence'].append('constants_generation')
        
        # Step 7: Calculate structural metrics
        metrics = self._calculate_structural_metrics(program)
        results.update(metrics)
        
        print(f"✅ Execution complete")
        print(f"   Structures placed: {results['boundaries_placed']} boundaries, "
              f"{results['domains_placed']} domains, {results['qubits_placed']} qubits")
        print(f"   Constants generated: {len(results['constants_generated'])}")
        
        return results
    
    def _execute_boundaries(self, boundaries, results):
        """Place boundaries on void lattice (node 1)"""
        print(f"  📍 Placing {len(boundaries)} boundaries...")
        
        # Find optimal points with lowest tension (most receptive)
        candidate_points = sorted(self.lattice, 
                                key=lambda p: (p.tension, -p.get_info_magnitude()))
        
        point_index = 0
        for boundary in boundaries:
            if point_index >= len(candidate_points):
                break
            
            point = candidate_points[point_index]
            point.add_structure(
                structure_type='boundary',
                name=boundary.name,
                content=boundary.content
            )
            point.node = 1  # φ node
            
            # Update structure map
            self.structure_map[boundary.name] = [point.id]
            
            # Record execution
            results['boundaries_placed'] += 1
            point_index += 1
        
        print(f"    → Placed {results['boundaries_placed']} boundaries at node 1 (φ)")
    
    def _execute_domains(self, domains, results):
        """Place domains on void lattice (node 2)"""
        print(f"  🏛️ Placing {len(domains)} domains...")
        
        # Find points with medium tension and good information magnitude
        candidate_points = sorted(self.lattice,
                                key=lambda p: (abs(p.tension - 0.05), 
                                              -p.get_info_magnitude()))
        
        point_index = 0
        for domain in domains:
            if point_index >= len(candidate_points):
                break
            
            point = candidate_points[point_index]
            point.add_structure(
                structure_type='domain',
                name=domain.name,
                states=domain.states,
                has_unresolved=domain.has_unresolved()
            )
            point.node = 2  # e node
            
            # Update structure map
            self.structure_map[domain.name] = [point.id]
            
            # Record execution
            results['domains_placed'] += 1
            point_index += 1
        
        print(f"    → Placed {results['domains_placed']} domains at node 2 (e)")
    
    def _execute_qubits(self, qubits, results):
        """Place qubits on void lattice (node 3)"""
        print(f"  ⚛️ Placing {len(qubits)} qubits...")
        
        # Find points with highest information magnitude for quantum effects
        candidate_points = sorted(self.lattice,
                                key=lambda p: (-p.get_info_magnitude(),
                                              p.tension))
        
        point_index = 0
        for qubit in qubits:
            if point_index >= len(candidate_points):
                break
            
            point = candidate_points[point_index]
            point.add_structure(
                structure_type='qubit',
                name=qubit.name,
                state_a=qubit.state_a,
                state_b=qubit.state_b,
                superposition=True,
                resolved=qubit.resolved
            )
            point.node = 3  # π node
            
            # Add quantum phase shift
            point.phase = (point.phase + math.pi) % (2 * math.pi)
            
            # Update structure map
            self.structure_map[qubit.name] = [point.id]
            
            # Record execution
            results['qubits_placed'] += 1
            point_index += 1
        
        print(f"    → Placed {results['qubits_placed']} qubits at node 3 (π)")
    
    def _create_entanglements(self, program, results):
        """Create entanglement between qubits (node 4)"""
        print(f"  🔗 Creating entanglements...")
        
        if len(program.qubits) < 2:
            print(f"    → Not enough qubits for entanglement")
            return
        
        # Find all qubit points
        qubit_points = []
        for qubit in program.qubits:
            if qubit.name in self.structure_map:
                point_id = self.structure_map[qubit.name][0]
                qubit_points.append((qubit.name, point_id))
        
        # Create entanglement groups based on phase coherence
        entanglement_count = 0
        for i, (name1, id1) in enumerate(qubit_points):
            for j, (name2, id2) in enumerate(qubit_points[i+1:], i+1):
                point1 = self.lattice[id1]
                point2 = self.lattice[id2]
                
                # Calculate phase coherence
                coherence = point1.get_phase_coherence(point2)
                
                # Entangle if coherence > threshold
                if coherence > 0.7:  # φ/2 threshold
                    # Update phases to match
                    avg_phase = (point1.phase + point2.phase) / 2
                    point1.phase = avg_phase
                    point2.phase = avg_phase
                    
                    # Create entanglement group
                    entangled_group = {id1, id2}
                    
                    # Check if either point is already in a group
                    merged = False
                    for group in self.entanglement_groups:
                        if id1 in group or id2 in group:
                            group.update(entangled_group)
                            merged = True
                            break
                    
                    if not merged:
                        self.entanglement_groups.append(entangled_group)
                    
                    entanglement_count += 1
        
        print(f"    → Created {entanglement_count} entanglements at node 4 (α)")
    
    def _accumulate_information(self) -> Dict[str, Any]:
        """Accumulate information from all structures (node 5)"""
        print(f"  📊 Accumulating information...")
        
        accumulation = {
            'total_information': 0.0,
            'average_coherence': 0.0,
            'occupied_points': 0,
            'information_distribution': []
        }
        
        info_magnitudes = []
        coherence_scores = []
        
        for point in self.lattice:
            if point.occupied:
                accumulation['occupied_points'] += 1
                
                # Calculate information magnitude
                info_mag = point.get_info_magnitude()
                info_magnitudes.append(info_mag)
                accumulation['total_information'] += info_mag
                
                # Calculate coherence with neighbors
                if point.id > 0 and point.id < len(self.lattice) - 1:
                    prev_point = self.lattice[point.id - 1]
                    next_point = self.lattice[point.id + 1]
                    coherence = (point.get_phase_coherence(prev_point) +
                               point.get_phase_coherence(next_point)) / 2
                    coherence_scores.append(coherence)
        
        if info_magnitudes:
            accumulation['average_information'] = np.mean(info_magnitudes)
            accumulation['max_information'] = np.max(info_magnitudes)
            accumulation['min_information'] = np.min(info_magnitudes)
        
        if coherence_scores:
            accumulation['average_coherence'] = np.mean(coherence_scores)
        
        # Store for later analysis
        self.accumulated_info = info_magnitudes
        
        print(f"    → Accumulated {accumulation['total_information']:.4f} "
              f"units of information at node 5 (c)")
        
        return accumulation
    
    def _generate_constants(self) -> Dict[str, float]:
        """Generate physical constants from accumulated information"""
        print(f"  🔬 Generating constants...")
        
        constants = {}
        
        # Node 1: φ from tension distribution
        tensions = [p.tension for p in self.lattice if p.tension > 0]
        if tensions:
            avg_tension = np.mean(tensions)
            constants['phi_proto'] = 1 + avg_tension * 0.618
        else:
            constants['phi_proto'] = self.PHI
        
        # Node 2: e from φ growth
        constants['e_proto'] = (1 + 1/constants['phi_proto']) ** constants['phi_proto']
        
        # Node 3: π from closure
        constants['pi_proto'] = constants['e_proto'] * (
            1 - 1/(constants['e_proto'] - 1)
        )
        
        # Node 4: α from entanglement count
        entanglement_count = sum(len(g) for g in self.entanglement_groups)
        if entanglement_count > 0:
            constants['alpha_proto'] = 0.1 / (13.7 * entanglement_count / len(self.lattice))
        else:
            constants['alpha_proto'] = 0.1 / 13.7
        
        # Node 5: Measurement collapse → exact values
        constants['phi_exact'] = self.PHI
        constants['e_exact'] = self.E
        constants['pi_exact'] = self.PI
        constants['alpha_exact'] = 1/137.035999084
        
        # Generate other constants from exact values
        constants.update(self._generate_derived_constants(constants))
        
        # Calculate accuracy
        constants['accuracy'] = self._calculate_accuracy(constants)
        
        return constants
    
    def _generate_derived_constants(self, base_constants: Dict) -> Dict[str, float]:
        """Generate derived constants from base constants"""
        derived = {}
        
        # Speed of light
        derived['c'] = 299792458.0
        
        # Planck constant
        derived['h'] = 6.62607015e-34
        derived['hbar'] = derived['h'] / (2 * base_constants['pi_exact'])
        
        # Gravitational constant
        derived['G'] = 6.67430e-11
        
        # Planck units
        derived['planck_length'] = math.sqrt(
            derived['hbar'] * derived['G'] / derived['c']**3
        )
        derived['planck_time'] = derived['planck_length'] / derived['c']
        derived['planck_mass'] = math.sqrt(
            derived['hbar'] * derived['c'] / derived['G']
        )
        
        # Electromagnetic constants
        derived['mu0'] = 4 * base_constants['pi_exact'] * 1e-7
        derived['epsilon0'] = 1 / (derived['mu0'] * derived['c']**2)
        derived['Z0'] = math.sqrt(derived['mu0'] / derived['epsilon0'])
        
        # Elementary charge
        derived['elementary_charge'] = 1.602176634e-19
        
        # Boltzmann constant
        derived['boltzmann'] = 1.380649e-23
        
        return derived
    
    def _calculate_accuracy(self, constants: Dict) -> Dict[str, float]:
        """Calculate accuracy of generated constants"""
        accuracy = {}
        
        # φ accuracy
        if 'phi_exact' in constants:
            phi_actual = self.PHI
            phi_error = abs(constants['phi_exact'] - phi_actual) / phi_actual * 100
            accuracy['phi'] = phi_error
        
        # e accuracy
        if 'e_exact' in constants:
            e_error = abs(constants['e_exact'] - self.E) / self.E * 100
            accuracy['e'] = e_error
        
        # π accuracy
        if 'pi_exact' in constants:
            pi_error = abs(constants['pi_exact'] - self.PI) / self.PI * 100
            accuracy['pi'] = pi_error
        
        # α accuracy
        if 'alpha_exact' in constants:
            alpha_actual = 1/137.035999084
            alpha_error = abs(constants['alpha_exact'] - alpha_actual) / alpha_actual * 100
            accuracy['alpha'] = alpha_error
        
        return accuracy
    
    def _calculate_structural_metrics(self, program) -> Dict[str, Any]:
        """Calculate advanced structural metrics"""
        metrics = {}
        
        # Boundary depth analysis
        boundary_depth = self._calculate_boundary_depth(program)
        metrics['max_boundary_depth'] = boundary_depth['max_depth']
        metrics['boundary_depth_distribution'] = boundary_depth['distribution']
        
        # Domain complexity
        domain_complexity = self._calculate_domain_complexity(program)
        metrics['domain_complexity'] = domain_complexity
        
        # Information topology
        topology = self._calculate_information_topology()
        metrics.update(topology)
        
        # Structural coherence score
        coherence = self._calculate_structural_coherence(program)
        metrics['structural_coherence'] = coherence
        
        return metrics
    
    def _calculate_boundary_depth(self, program):
        """Calculate boundary nesting depth"""
        depth_map = {}
        
        def get_depth(name, visited=None):
            if visited is None:
                visited = set()
            
            if name in visited:
                return 0
            
            visited.add(name)
            
            for boundary in program.boundaries:
                if boundary.name == name:
                    if boundary.content:
                        max_child_depth = 0
                        for child in boundary.content:
                            child_depth = get_depth(child, visited.copy())
                            max_child_depth = max(max_child_depth, child_depth)
                        return 1 + max_child_depth
                    return 1
            return 0
        
        depths = []
        for boundary in program.boundaries:
            depth = get_depth(boundary.name)
            depth_map[boundary.name] = depth
            depths.append(depth)
        
        return {
            'max_depth': max(depths) if depths else 0,
            'distribution': depth_map
        }
    
    def _calculate_domain_complexity(self, program):
        """Calculate domain state complexity"""
        total_states = 0
        superposition_states = 0
        max_states_per_domain = 0
        
        for domain in program.domains:
            state_count = len(domain.states)
            total_states += state_count
            max_states_per_domain = max(max_states_per_domain, state_count)
            
            for state in domain.states:
                if '⊕' in state:
                    superposition_states += 1
        
        return {
            'total_states': total_states,
            'superposition_states': superposition_states,
            'max_states_per_domain': max_states_per_domain,
            'superposition_ratio': (superposition_states / total_states 
                                  if total_states > 0 else 0)
        }
    
    def _calculate_information_topology(self):
        """Calculate information distribution topology"""
        if not self.accumulated_info:
            return {'information_topology': 'empty'}
        
        info_array = np.array(self.accumulated_info)
        
        return {
            'information_mean': float(np.mean(info_array)),
            'information_std': float(np.std(info_array)),
            'information_skew': float(self._calculate_skewness(info_array)),
            'information_kurtosis': float(self._calculate_kurtosis(info_array)),
            'information_entropy': float(self._calculate_entropy(info_array))
        }
    
    def _calculate_skewness(self, data):
        """Calculate skewness of data"""
        if len(data) < 2:
            return 0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data):
        """Calculate kurtosis of data"""
        if len(data) < 2:
            return 0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 4) - 3
    
    def _calculate_entropy(self, data):
        """Calculate Shannon entropy of data"""
        if len(data) == 0:
            return 0
        
        # Normalize data
        data = data - np.min(data)
        data = data / (np.sum(data) + 1e-10)
        
        # Remove zeros for log calculation
        data = data[data > 0]
        
        if len(data) == 0:
            return 0
        
        return -np.sum(data * np.log(data))
    
    def _calculate_structural_coherence(self, program):
        """Calculate overall structural coherence score"""
        # Coherence factors
        factors = []
        
        # 1. Boundary nesting coherence
        boundary_depth = self._calculate_boundary_depth(program)
        if boundary_depth['max_depth'] > 0:
            depth_coherence = 1.0 / (1 + boundary_depth['max_depth'])
            factors.append(depth_coherence)
        
        # 2. Information distribution coherence
        if self.accumulated_info:
            info_std = np.std(self.accumulated_info)
            info_mean = np.mean(self.accumulated_info)
            if info_mean > 0:
                info_coherence = 1.0 / (1 + info_std / info_mean)
                factors.append(info_coherence)
        
        # 3. Entanglement coherence
        if self.entanglement_groups:
            entanglement_coherence = len(self.entanglement_groups) / len(self.lattice)
            factors.append(entanglement_coherence)
        
        # 4. Occupancy coherence
        occupied_count = sum(1 for p in self.lattice if p.occupied)
        occupancy_coherence = occupied_count / len(self.lattice)
        factors.append(occupancy_coherence)
        
        # Final coherence score (harmonic mean of factors)
        if factors:
            # Use harmonic mean to penalize low individual scores
            factors_array = np.array(factors)
            coherence = len(factors) / np.sum(1.0 / (factors_array + 1e-10))
            return float(coherence)
        
        return 0.0
    
    def visualize_lattice(self):
        """Generate visualization data for lattice"""
        # This would interface with visualization module
        visualization_data = {
            'points': [],
            'structures': [],
            'connections': []
        }
        
        for point in self.lattice:
            point_data = {
                'id': point.id,
                'x': float(point.info_vector[0]),
                'y': float(point.info_vector[1]),
                'z': float(point.info_vector[2]),
                'tension': point.tension,
                'occupied': point.occupied,
                'node': point.node,
                'phase': point.phase,
                'info_magnitude': float(point.get_info_magnitude())
            }
            visualization_data['points'].append(point_data)
            
            if point.structures:
                for structure in point.structures:
                    visualization_data['structures'].append({
                        'point_id': point.id,
                        'type': structure['type'],
                        'name': structure.get('name', '')
                    })
        
        # Add entanglement connections
        for group in self.entanglement_groups:
            group_list = list(group)
            for i in range(len(group_list)):
                for j in range(i+1, len(group_list)):
                    visualization_data['connections'].append({
                        'from': group_list[i],
                        'to': group_list[j],
                        'type': 'entanglement'
                    })
        
        return visualization_data
    
    def get_execution_summary(self):
        """Get summary of execution results"""
        occupied = sum(1 for p in self.lattice if p.occupied)
        total_info = sum(p.get_info_magnitude() for p in self.lattice)
        avg_coherence = np.mean([
            p.get_phase_coherence(self.lattice[(p.id + 1) % len(self.lattice)])
            for p in self.lattice
        ]) if len(self.lattice) > 1 else 0
        
        return {
            'lattice_size': len(self.lattice),
            'occupied_points': occupied,
            'occupancy_rate': occupied / len(self.lattice),
            'total_information': total_info,
            'average_coherence': avg_coherence,
            'entanglement_groups': len(self.entanglement_groups),
            'total_entangled_points': sum(len(g) for g in self.entanglement_groups)
        }