"""
QGL Code Generation - Export structures to various formats
Generates executable code from QGL structures
"""
from typing import Dict, List, Any, Optional
import json
import numpy as np
import math

class QGLCodeGenerator:
    """
    Generate executable code from QGL structures
    Supports multiple output formats
    """
    
    def __init__(self, interpreter=None):
        self.interpreter = interpreter
    
    def generate_python(self, program, results: Dict[str, Any]) -> str:
        """
        Generate Python code that simulates the QGL structure
        """
        code_lines = []
        
        # Header
        code_lines.append('"""')
        code_lines.append('Generated Python Code from QGL')
        code_lines.append(f'Constants: {len(results.get("constants_generated", {}))}')
        code_lines.append('"""')
        code_lines.append('')
        code_lines.append('import numpy as np')
        code_lines.append('import math')
        code_lines.append('')
        
        # Constants section
        constants = results.get('constants_generated', {})
        if constants:
            code_lines.append('# GENERATED CONSTANTS')
            code_lines.append('# ==================')
            for key, value in constants.items():
                if isinstance(value, (int, float)):
                    code_lines.append(f'{key.upper()} = {value}')
                elif isinstance(value, dict):
                    # Handle nested constants (like accuracy)
                    code_lines.append(f'{key.upper()} = {json.dumps(value, indent=2)}')
            code_lines.append('')
        
        # Void lattice simulation
        code_lines.append('# VOID LATTICE SIMULATION')
        code_lines.append('# ======================')
        code_lines.append('class VoidLattice:')
        code_lines.append('    """Simulated void lattice from QGL"""')
        code_lines.append('    ')
        code_lines.append('    def __init__(self, size=1000):')
        code_lines.append('        self.size = size')
        code_lines.append('        self.points = []')
        code_lines.append('        self._initialize_lattice()')
        code_lines.append('    ')
        code_lines.append('    def _initialize_lattice(self):')
        code_lines.append('        """Initialize φ-scaled lattice"""')
        code_lines.append('        PHI = (1 + math.sqrt(5)) / 2')
        code_lines.append('        for i in range(self.size):')
        code_lines.append('            angle = i * 2 * math.pi / PHI')
        code_lines.append('            info_vector = np.array([')
        code_lines.append('                math.sin(angle),')
        code_lines.append('                math.cos(angle),')
        code_lines.append('                math.sin(angle * PHI),')
        code_lines.append('                math.cos(angle * PHI),')
        code_lines.append('                math.sin(angle / PHI),')
        code_lines.append('                math.cos(angle / PHI),')
        code_lines.append('                0.618 * (i % 7)')
        code_lines.append('            ])')
        code_lines.append('            norm = np.linalg.norm(info_vector)')
        code_lines.append('            if norm > 0:')
        code_lines.append('                info_vector = (info_vector / norm) * 0.618')
        code_lines.append('            ')
        code_lines.append('            self.points.append({')
        code_lines.append('                "id": i,')
        code_lines.append('                "info_vector": info_vector,')
        code_lines.append('                "tension": 0.1 * (i % int(PHI * 10)) / 10.0,')
        code_lines.append('                "occupied": False,')
        code_lines.append('                "structures": []')
        code_lines.append('            })')
        code_lines.append('    ')
        code_lines.append('    def place_structure(self, point_id, structure_type, **kwargs):')
        code_lines.append('        """Place structure on lattice point"""')
        code_lines.append('        if 0 <= point_id < self.size:')
        code_lines.append('            self.points[point_id]["occupied"] = True')
        code_lines.append('            self.points[point_id]["structures"].append({')
        code_lines.append('                "type": structure_type,')
        code_lines.append('                **kwargs')
        code_lines.append('            })')
        code_lines.append('    ')
        code_lines.append('    def get_info_magnitude(self, point_id):')
        code_lines.append('        """Get information magnitude at point"""')
        code_lines.append('        if 0 <= point_id < self.size:')
        code_lines.append('            return np.linalg.norm(self.points[point_id]["info_vector"])')
        code_lines.append('        return 0.0')
        code_lines.append('    ')
        code_lines.append('    def calculate_coherence(self):')
        code_lines.append('        """Calculate overall lattice coherence"""')
        code_lines.append('        occupied = sum(1 for p in self.points if p["occupied"])')
        code_lines.append('        total_info = sum(self.get_info_magnitude(i) for i in range(self.size))')
        code_lines.append('        return {')
        code_lines.append('            "occupancy": occupied / self.size,')
        code_lines.append('            "total_information": total_info,')
        code_lines.append('            "average_information": total_info / self.size if self.size > 0 else 0')
        code_lines.append('        }')
        code_lines.append('')
        
        # QGL Structure classes
        code_lines.append('# QGL STRUCTURE CLASSES')
        code_lines.append('# ====================')
        
        # Boundary class
        code_lines.append('class QGLBoundary:')
        code_lines.append('    """QGL Boundary structure"""')
        code_lines.append('    ')
        code_lines.append('    def __init__(self, name, content):')
        code_lines.append('        self.name = name')
        code_lines.append('        self.content = content')
        code_lines.append('    ')
        code_lines.append('    def validate(self):')
        code_lines.append('        """Validate boundary structure"""')
        code_lines.append('        if self.name in self.content:')
        code_lines.append('            raise ValueError(f"Boundary {self.name} contains itself")')
        code_lines.append('        return True')
        code_lines.append('    ')
        code_lines.append('    def __repr__(self):')
        code_lines.append('        return f"Boundary({self.name}: {self.content})"')
        code_lines.append('')
        
        # Domain class
        code_lines.append('class QGLDomain:')
        code_lines.append('    """QGL Domain structure"""')
        code_lines.append('    ')
        code_lines.append('    def __init__(self, name, states):')
        code_lines.append('        self.name = name')
        code_lines.append('        self.states = states')
        code_lines.append('    ')
        code_lines.append('    def has_unresolved(self):')
        code_lines.append('        """Check for superposition states"""')
        code_lines.append('        return any("⊕" in state for state in self.states)')
        code_lines.append('    ')
        code_lines.append('    def __repr__(self):')
        code_lines.append('        return f"Domain({self.name}: {self.states})"')
        code_lines.append('')
        
        # Qubit class
        code_lines.append('class QGLQubit:')
        code_lines.append('    """QGL Qubit structure"""')
        code_lines.append('    ')
        code_lines.append('    def __init__(self, name, state_a, state_b, resolved=False):')
        code_lines.append('        self.name = name')
        code_lines.append('        self.state_a = state_a')
        code_lines.append('        self.state_b = state_b')
        code_lines.append('        self.resolved = resolved')
        code_lines.append('    ')
        code_lines.append('    def collapse(self, choice):')
        code_lines.append('        """Collapse qubit to specific state"""')
        code_lines.append('        if choice == "A":')
        code_lines.append('            return self.state_a')
        code_lines.append('        elif choice == "B":')
        code_lines.append('            return self.state_b')
        code_lines.append('        else:')
        code_lines.append('            raise ValueError("Choice must be A or B")')
        code_lines.append('    ')
        code_lines.append('    def __repr__(self):')
        code_lines.append('        return f"Qubit({self.name}: {{{self.state_a} ⊕ {self.state_b}}})"')
        code_lines.append('')
        
        # Program instance
        code_lines.append('# PROGRAM INSTANCE')
        code_lines.append('# ===============')
        code_lines.append('def create_program():')
        code_lines.append('    """Create the QGL program instance"""')
        code_lines.append('    program = {')
        code_lines.append('        "boundaries": [],')
        code_lines.append('        "domains": [],')
        code_lines.append('        "qubits": []')
        code_lines.append('    }')
        code_lines.append('    ')
        
        # Add boundaries
        if program.boundaries:
            code_lines.append('    # Boundaries')
            for boundary in program.boundaries:
                content_str = json.dumps(boundary.content)
                code_lines.append(f'    program["boundaries"].append(')
                code_lines.append(f'        QGLBoundary("{boundary.name}", {content_str})')
                code_lines.append('    )')
            code_lines.append('    ')
        
        # Add domains
        if program.domains:
            code_lines.append('    # Domains')
            for domain in program.domains:
                states_str = json.dumps(domain.states)
                code_lines.append(f'    program["domains"].append(')
                code_lines.append(f'        QGLDomain("{domain.name}", {states_str})')
                code_lines.append('    )')
            code_lines.append('    ')
        
        # Add qubits
        if program.qubits:
            code_lines.append('    # Qubits')
            for qubit in program.qubits:
                code_lines.append(f'    program["qubits"].append(')
                code_lines.append(f'        QGLQubit("{qubit.name}", "{qubit.state_a}", "{qubit.state_b}")')
                code_lines.append('    )')
            code_lines.append('    ')
        
        code_lines.append('    return program')
        code_lines.append('')
        
        # Simulation function
        code_lines.append('# SIMULATION FUNCTION')
        code_lines.append('# ==================')
        code_lines.append('def simulate_qgl(program):')
        code_lines.append('    """Simulate QGL program execution"""')
        code_lines.append('    # Create lattice')
        code_lines.append('    lattice = VoidLattice(size=1000)')
        code_lines.append('    ')
        code_lines.append('    # Place structures (simplified)')
        code_lines.append('    for i, boundary in enumerate(program["boundaries"]):')
        code_lines.append('        if i < 100:  # Limit placements')
        code_lines.append('            lattice.place_structure(')
        code_lines.append('                point_id=i,')
        code_lines.append('                structure_type="boundary",')
        code_lines.append('                name=boundary.name,')
        code_lines.append('                content=boundary.content')
        code_lines.append('            )')
        code_lines.append('    ')
        code_lines.append('    # Calculate coherence')
        code_lines.append('    coherence = lattice.calculate_coherence()')
        code_lines.append('    ')
        code_lines.append('    # Return results')
        code_lines.append('    return {')
        code_lines.append('        "lattice": lattice,')
        code_lines.append('        "coherence": coherence,')
        code_lines.append('        "constants": {')
        
        # Add constants to output
        for key in ['phi_exact', 'e_exact', 'pi_exact', 'alpha_exact', 'c']:
            if key.upper() in [line.split()[0] for line in code_lines if '=' in line]:
                code_lines.append(f'            "{key}": {key.upper()},')
        
        code_lines.append('        }')
        code_lines.append('    }')
        code_lines.append('')
        
        # Main execution
        code_lines.append('# MAIN EXECUTION')
        code_lines.append('# =============')
        code_lines.append('if __name__ == "__main__":')
        code_lines.append('    print("🚀 Generated QGL Simulation")')
        code_lines.append('    print("=" * 40)')
        code_lines.append('    ')
        code_lines.append('    # Create program')
        code_lines.append('    program = create_program()')
        code_lines.append('    ')
        code_lines.append('    # Run simulation')
        code_lines.append('    results = simulate_qgl(program)')
        code_lines.append('    ')
        code_lines.append('    # Display results')
        code_lines.append('    print(f"Boundaries: {len(program[\"boundaries\"])}")')
        code_lines.append('    print(f"Domains: {len(program[\"domains\"])}")')
        code_lines.append('    print(f"Qubits: {len(program[\"qubits\"])}")')
        code_lines.append('    print(f"Occupancy: {results[\"coherence\"][\"occupancy\"]:.2%}")')
        code_lines.append('    print(f"Total Information: {results[\"coherence\"][\"total_information\"]:.4f}")')
        code_lines.append('    ')
        code_lines.append('    print("\\nGenerated Constants:")')
        code_lines.append('    for key, value in results[\"constants\"].items():')
        code_lines.append('        print(f"  {key}: {value}")')
        code_lines.append('')
        
        return '\n'.join(code_lines)
    
    def generate_json(self, program, results: Dict[str, Any], pretty: bool = True) -> str:
        """Generate JSON representation of QGL program and results"""
        output = {
            'program': {
                'boundaries': [
                    {'name': b.name, 'content': b.content}
                    for b in program.boundaries
                ],
                'domains': [
                    {'name': d.name, 'states': d.states}
                    for d in program.domains
                ],
                'qubits': [
                    {'name': q.name, 'state_a': q.state_a, 'state_b': q.state_b}
                    for q in program.qubits
                ]
            },
            'execution_results': results,
            'metadata': {
                'generator': 'QGL Code Generator',
                'version': '1.0.0',
                'timestamp': 'no-time-reference'  # QGL has no time
            }
        }
        
        if pretty:
            return json.dumps(output, indent=2, default=self._json_serializer)
        else:
            return json.dumps(output, default=self._json_serializer)
    
    def generate_html_report(self, program, results: Dict[str, Any]) -> str:
        """Generate HTML report of QGL execution"""
        html = []
        
        # HTML header
        html.append('<!DOCTYPE html>')
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('    <meta charset="UTF-8">')
        html.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append('    <title>QGL Execution Report</title>')
        html.append('    <style>')
        html.append('        * { margin: 0; padding: 0; box-sizing: border-box; }')
        html.append('        body {')
        html.append('            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;')
        html.append('            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);')
        html.append('            color: white;')
        html.append('            padding: 20px;')
        html.append('            min-height: 100vh;')
        html.append('        }')
        html.append('        .container {')
        html.append('            max-width: 1200px;')
        html.append('            margin: 0 auto;')
        html.append('        }')
        html.append('        header {')
        html.append('            text-align: center;')
        html.append('            padding: 40px 0;')
        html.append('            margin-bottom: 40px;')
        html.append('            border-bottom: 2px solid rgba(255,255,255,0.1);')
        html.append('        }')
        html.append('        h1 {')
        html.append('            font-size: 3em;')
        html.append('            background: linear-gradient(90deg, #ff7e5f, #feb47b);')
        html.append('            -webkit-background-clip: text;')
        html.append('            -webkit-text-fill-color: transparent;')
        html.append('            margin-bottom: 10px;')
        html.append('        }')
        html.append('        .subtitle {')
        html.append('            color: #aaa;')
        html.append('            font-size: 1.2em;')
        html.append('        }')
        html.append('        .grid {')
        html.append('            display: grid;')
        html.append('            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));')
        html.append('            gap: 20px;')
        html.append('            margin-bottom: 40px;')
        html.append('        }')
        html.append('        .card {')
        html.append('            background: rgba(255,255,255,0.05);')
        html.append('            border-radius: 10px;')
        html.append('            padding: 25px;')
        html.append('            backdrop-filter: blur(10px);')
        html.append('            border: 1px solid rgba(255,255,255,0.1);')
        html.append('        }')
        html.append('        h2 {')
        html.append('            color: #4fc3f7;')
        html.append('            margin-bottom: 20px;')
        html.append('            font-size: 1.8em;')
        html.append('        }')
        html.append('        h3 {')
        html.append('            color: #81c784;')
        html.append('            margin: 15px 0 10px 0;')
        html.append('        }')
        html.append('        .constant-grid {')
        html.append('            display: grid;')
        html.append('            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));')
        html.append('            gap: 15px;')
        html.append('            margin-top: 20px;')
        html.append('        }')
        html.append('        .constant-card {')
        html.append('            background: rgba(255,255,255,0.07);')
        html.append('            padding: 15px;')
        html.append('            border-radius: 8px;')
        html.append('            border-left: 4px solid #4fc3f7;')
        html.append('        }')
        html.append('        .constant-name {')
        html.append('            color: #4fc3f7;')
        html.append('            font-weight: bold;')
        html.append('            margin-bottom: 5px;')
        html.append('        }')
        html.append('        .constant-value {')
        html.append('            color: #fff;')
        html.append('            font-family: "Consolas", monospace;')
        html.append('        }')
        html.append('        .structure-list {')
        html.append('            list-style: none;')
        html.append('            padding-left: 20px;')
        html.append('        }')
        html.append('        .structure-list li {')
        html.append('            margin-bottom: 10px;')
        html.append('            position: relative;')
        html.append('            padding-left: 20px;')
        html.append('        }')
        html.append('        .structure-list li:before {')
        html.append('            content: "▸";')
        html.append('            color: #4fc3f7;')
        html.append('            position: absolute;')
        html.append('            left: 0;')
        html.append('        }')
        html.append('        .accuracy-good { color: #4CAF50; }')
        html.append('        .accuracy-warning { color: #FFC107; }')
        html.append('        .accuracy-bad { color: #F44336; }')
        html.append('        .metric {')
        html.append('            display: flex;')
        html.append('            justify-content: space-between;')
        html.append('            margin-bottom: 8px;')
        html.append('            padding: 8px 0;')
        html.append('            border-bottom: 1px solid rgba(255,255,255,0.1);')
        html.append('        }')
        html.append('        .metric-value {')
        html.append('            font-weight: bold;')
        html.append('            color: #feb47b;')
        html.append('        }')
        html.append('        footer {')
        html.append('            text-align: center;')
        html.append('            padding: 30px 0;')
        html.append('            margin-top: 40px;')
        html.append('            border-top: 1px solid rgba(255,255,255,0.1);')
        html.append('            color: #888;')
        html.append('        }')
        html.append('    </style>')
        html.append('</head>')
        html.append('<body>')
        html.append('    <div class="container">')
        html.append('        <header>')
        html.append('            <h1>QGL Execution Report</h1>')
        html.append('            <div class="subtitle">Structural Physics Framework</div>')
        html.append('        </header>')
        
        # Summary section
        html.append('        <div class="card">')
        html.append('            <h2>📊 Execution Summary</h2>')
        
        if 'execution_sequence' in results:
            html.append('            <div class="metric">')
            html.append(f'                <span>Execution Sequence:</span>')
            html.append(f'                <span class="metric-value">')
            html.append(f'                    {" → ".join(results["execution_sequence"])}')
            html.append(f'                </span>')
            html.append('            </div>')
        
        if 'boundaries_placed' in results:
            html.append('            <div class="metric">')
            html.append(f'                <span>Boundaries Placed:</span>')
            html.append(f'                <span class="metric-value">{results["boundaries_placed"]}</span>')
            html.append('            </div>')
        
        if 'domains_placed' in results:
            html.append('            <div class="metric">')
            html.append(f'                <span>Domains Placed:</span>')
            html.append(f'                <span class="metric-value">{results["domains_placed"]}</span>')
            html.append('            </div>')
        
        if 'qubits_placed' in results:
            html.append('            <div class="metric">')
            html.append(f'                <span>Qubits Placed:</span>')
            html.append(f'                <span class="metric-value">{results["qubits_placed"]}</span>')
            html.append('            </div>')
        
        html.append('        </div>')
        
        # Constants section
        constants = results.get('constants_generated', {})
        if constants:
            html.append('        <div class="card">')
            html.append('            <h2>🔬 Generated Constants</h2>')
            html.append('            <div class="constant-grid">')
            
            # Display key constants
            key_constants = [
                ('phi_exact', 'φ (Golden Ratio)'),
                ('e_exact', 'e (Natural Base)'),
                ('pi_exact', 'π (Pi)'),
                ('alpha_exact', 'α (Fine-Structure)'),
                ('c', 'c (Speed of Light)'),
                ('planck_length', 'Planck Length'),
                ('hbar', 'ħ (Reduced Planck)'),
                ('G', 'G (Gravitational)')
            ]
            
            for key, display_name in key_constants:
                if key in constants:
                    value = constants[key]
                    html.append(f'                <div class="constant-card">')
                    html.append(f'                    <div class="constant-name">{display_name}</div>')
                    html.append(f'                    <div class="constant-value">{self._format_constant_value(value)}</div>')
                    html.append(f'                </div>')
            
            html.append('            </div>')
            
            # Accuracy section
            if 'accuracy' in constants:
                html.append('            <h3>🎯 Accuracy</h3>')
                html.append('            <div class="constant-grid">')
                for const_name, error in constants['accuracy'].items():
                    accuracy_class = 'accuracy-good' if error < 0.01 else 'accuracy-warning' if error < 1 else 'accuracy-bad'
                    html.append(f'                <div class="constant-card">')
                    html.append(f'                    <div class="constant-name">{const_name}</div>')
                    html.append(f'                    <div class="constant-value {accuracy_class}">{error:.10f}% error</div>')
                    html.append(f'                </div>')
                html.append('            </div>')
            
            html.append('        </div>')
        
        # Program structure section
        html.append('        <div class="grid">')
        
        # Boundaries
        if program.boundaries:
            html.append('            <div class="card">')
            html.append('                <h2>📍 Boundaries</h2>')
            html.append('                <ul class="structure-list">')
            for boundary in program.boundaries:
                html.append(f'                    <li>')
                html.append(f'                        <strong>{boundary.name}</strong>: ')
                html.append(f'                        {", ".join(boundary.content)}')
                html.append(f'                    </li>')
            html.append('                </ul>')
            html.append('            </div>')
        
        # Domains
        if program.domains:
            html.append('            <div class="card">')
            html.append('                <h2>🏛️ Domains</h2>')
            html.append('                <ul class="structure-list">')
            for domain in program.domains:
                html.append(f'                    <li>')
                html.append(f'                        <strong>{domain.name}</strong>: ')
                html.append(f'                        {", ".join(domain.states)}')
                html.append(f'                    </li>')
            html.append('                </ul>')
            html.append('            </div>')
        
        # Qubits
        if program.qubits:
            html.append('            <div class="card">')
            html.append('                <h2>⚛️ Qubits</h2>')
            html.append('                <ul class="structure-list">')
            for qubit in program.qubits:
                html.append(f'                    <li>')
                html.append(f'                        <strong>{qubit.name}</strong>: ')
                html.append(f'                        {{{qubit.state_a} ⊕ {qubit.state_b}}}')
                html.append(f'                    </li>')
            html.append('                </ul>')
            html.append('            </div>')
        
        html.append('        </div>')
        
        # Metrics section
        if 'structural_coherence' in results:
            html.append('        <div class="card">')
            html.append('            <h2>📈 Structural Metrics</h2>')
            
            metrics_to_display = [
                ('structural_coherence', 'Structural Coherence'),
                ('total_information', 'Total Information'),
                ('average_coherence', 'Average Coherence'),
                ('occupied_points', 'Occupied Points'),
            ]
            
            for key, display_name in metrics_to_display:
                if key in results:
                    value = results[key]
                    if isinstance(value, float):
                        formatted = f'{value:.6f}'
                    else:
                        formatted = str(value)
                    
                    html.append('            <div class="metric">')
                    html.append(f'                <span>{display_name}:</span>')
                    html.append(f'                <span class="metric-value">{formatted}</span>')
                    html.append('            </div>')
            
            html.append('        </div>')
        
        # Footer
        html.append('        <footer>')
        html.append('            <p>Generated by QGL Admissibility Engine v1.0</p>')
        html.append('            <p>Structural Admissibility = Reality</p>')
        html.append('        </footer>')
        html.append('    </div>')
        html.append('</body>')
        html.append('</html>')
        
        return '\n'.join(html)
    
    def generate_cpp(self, program, results: Dict[str, Any]) -> str:
        """Generate C++ code for high-performance simulation"""
        cpp_lines = []
        
        # Header
        cpp_lines.append('// QGL C++ Code Generation')
        cpp_lines.append('// Generated from structural execution')
        cpp_lines.append('')
        cpp_lines.append('#include <iostream>')
        cpp_lines.append('#include <vector>')
        cpp_lines.append('#include <string>')
        cpp_lines.append('#include <cmath>')
        cpp_lines.append('#include <algorithm>')
        cpp_lines.append('')
        
        # Constants
        constants = results.get('constants_generated', {})
        if constants:
            cpp_lines.append('// Physical Constants')
            cpp_lines.append('namespace Constants {')
            for key, value in constants.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if 'phi' in key:
                        cpp_lines.append(f'    constexpr double {key.upper()} = {value};')
                    elif 'pi' in key:
                        cpp_lines.append(f'    constexpr double {key.upper()} = {value};')
                    elif 'e' in key:
                        cpp_lines.append(f'    constexpr double {key.upper()} = {value};')
            cpp_lines.append('}')
            cpp_lines.append('')
        
        # Void Point structure
        cpp_lines.append('// Void Lattice Point')
        cpp_lines.append('struct VoidPoint {')
        cpp_lines.append('    int id;')
        cpp_lines.append('    std::vector<double> info_vector;')
        cpp_lines.append('    double tension;')
        cpp_lines.append('    bool occupied;')
        cpp_lines.append('    int node;')
        cpp_lines.append('    ')
        cpp_lines.append('    double info_magnitude() const {')
        cpp_lines.append('        double sum = 0.0;')
        cpp_lines.append('        for (double val : info_vector) {')
        cpp_lines.append('            sum += val * val;')
        cpp_lines.append('        }')
        cpp_lines.append('        return std::sqrt(sum);')
        cpp_lines.append('    }')
        cpp_lines.append('};')
        cpp_lines.append('')
        
        # Void Lattice class
        cpp_lines.append('// Void Lattice Simulation')
        cpp_lines.append('class VoidLattice {')
        cpp_lines.append('private:')
        cpp_lines.append('    std::vector<VoidPoint> points;')
        cpp_lines.append('    ')
        cpp_lines.append('public:')
        cpp_lines.append('    VoidLattice(int size = 1000) {')
        cpp_lines.append('        initialize_lattice(size);')
        cpp_lines.append('    }')
        cpp_lines.append('    ')
        cpp_lines.append('    void initialize_lattice(int size) {')
        cpp_lines.append('        const double PHI = (1.0 + std::sqrt(5.0)) / 2.0;')
        cpp_lines.append('        points.resize(size);')
        cpp_lines.append('        ')
        cpp_lines.append('        for (int i = 0; i < size; ++i) {')
        cpp_lines.append('            double angle = i * 2.0 * M_PI / PHI;')
        cpp_lines.append('            std::vector<double> info(7);')
        cpp_lines.append('            info[0] = std::sin(angle);')
        cpp_lines.append('            info[1] = std::cos(angle);')
        cpp_lines.append('            info[2] = std::sin(angle * PHI);')
        cpp_lines.append('            info[3] = std::cos(angle * PHI);')
        cpp_lines.append('            info[4] = std::sin(angle / PHI);')
        cpp_lines.append('            info[5] = std::cos(angle / PHI);')
        cpp_lines.append('            info[6] = 0.618 * (i % 7);')
        cpp_lines.append('            ')
        cpp_lines.append('            // Normalize')
        cpp_lines.append('            double norm = 0.0;')
        cpp_lines.append('            for (double val : info) {')
        cpp_lines.append('                norm += val * val;')
        cpp_lines.append('            }')
        cpp_lines.append('            norm = std::sqrt(norm);')
        cpp_lines.append('            ')
        cpp_lines.append('            if (norm > 0) {')
        cpp_lines.append('                for (double& val : info) {')
        cpp_lines.append('                    val = (val / norm) * 0.618;')
        cpp_lines.append('                }')
        cpp_lines.append('            }')
        cpp_lines.append('            ')
        cpp_lines.append('            points[i] = VoidPoint{')
        cpp_lines.append('                .id = i,')
        cpp_lines.append('                .info_vector = info,')
        cpp_lines.append('                .tension = 0.1 * (i % static_cast<int>(PHI * 10.0)) / 10.0,')
        cpp_lines.append('                .occupied = false,')
        cpp_lines.append('                .node = 0')
        cpp_lines.append('            };')
        cpp_lines.append('        }')
        cpp_lines.append('    }')
        cpp_lines.append('    ')
        cpp_lines.append('    int size() const { return points.size(); }')
        cpp_lines.append('    ')
        cpp_lines.append('    double calculate_coherence() const {')
        cpp_lines.append('        int occupied = 0;')
        cpp_lines.append('        double total_info = 0.0;')
        cpp_lines.append('        ')
        cpp_lines.append('        for (const auto& point : points) {')
        cpp_lines.append('            if (point.occupied) {')
        cpp_lines.append('                ++occupied;')
        cpp_lines.append('            }')
        cpp_lines.append('            total_info += point.info_magnitude();')
        cpp_lines.append('        }')
        cpp_lines.append('        ')
        cpp_lines.append('        return occupied / static_cast<double>(points.size());')
        cpp_lines.append('    }')
        cpp_lines.append('};')
        cpp_lines.append('')
        
        # Main function
        cpp_lines.append('int main() {')
        cpp_lines.append('    std::cout << "🚀 QGL C++ Simulation" << std::endl;')
        cpp_lines.append('    std::cout << "====================" << std::endl;')
        cpp_lines.append('    ')
        cpp_lines.append('    // Create void lattice')
        cpp_lines.append('    VoidLattice lattice(1000);')
        cpp_lines.append('    ')
        cpp_lines.append('    // Calculate coherence')
        cpp_lines.append('    double coherence = lattice.calculate_coherence();')
        cpp_lines.append('    ')
        cpp_lines.append('    // Display results')
        cpp_lines.append('    std::cout << "Lattice size: " << lattice.size() << std::endl;')
        cpp_lines.append('    std::cout << "Coherence: " << coherence << std::endl;')
        cpp_lines.append('    ')
        cpp_lines.append('    // Display constants')
        cpp_lines.append('    std::cout << "\\nGenerated Constants:" << std::endl;')
        
        if constants:
            for key in ['phi_exact', 'e_exact', 'pi_exact']:
                key_upper = key.upper()
                if f'    constexpr double {key_upper}' in '\n'.join(cpp_lines):
                    cpp_lines.append(f'    std::cout << "  {key}: " << Constants::{key_upper} << std::endl;')
        
        cpp_lines.append('    ')
        cpp_lines.append('    return 0;')
        cpp_lines.append('}')
        cpp_lines.append('')
        
        return '\n'.join(cpp_lines)
    
    def export_all_formats(self, program, results: Dict[str, Any], output_dir: str = "output"):
        """Export QGL results in all available formats"""
        import os
        from pathlib import Path
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate and save all formats
        formats = {
            'python': ('qgl_simulation.py', self.generate_python),
            'json': ('qgl_results.json', lambda p, r: self.generate_json(p, r, pretty=True)),
            'html': ('qgl_report.html', self.generate_html_report),
            'cpp': ('qgl_simulation.cpp', self.generate_cpp),
        }
        
        for format_name, (filename, generator) in formats.items():
            try:
                content = generator(program, results)
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Generated {format_name}: {filepath}")
            except Exception as e:
                print(f"⚠️  Failed to generate {format_name}: {e}")
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for numpy types"""
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (set, frozenset)):
            return list(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _format_constant_value(self, value):
        """Format constant value for display"""
        if isinstance(value, (int, float)):
            if abs(value) < 0.001 or abs(value) > 1000:
                return f'{value:.6e}'
            else:
                return f'{value:.10f}'
        return str(value)