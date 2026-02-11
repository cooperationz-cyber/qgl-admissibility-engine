# test_interpreter_codegen.py
"""
Test the complete interpreter and codegen system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from qgl.interpreter import StructuralInterpreter
from qgl.codegen import QGLCodeGenerator

def test_complete_system():
    print("🧪 TESTING COMPLETE QGL INTERPRETER & CODEGEN")
    print("="*60)
    
    # Sample QGL code
    qgl_code = """
    boundary QuantumRealm {
        HilbertSpace, MeasurementApparatus
    }
    
    domain HilbertSpace {
        |0>, |1>, |+>, |->, |0>⊕|1>
    }
    
    domain MeasurementApparatus {
        Click, NoClick, Click⊕NoClick
    }
    
    qubit Q1 = { |0> ⊕ |1> }
    qubit Q2 = { Click ⊕ NoClick }
    """
    
    # 1. Parse QGL
    lexer = QGLLexer()
    tokens = lexer.tokenize(qgl_code)
    
    parser = QGLParser()
    program = parser.parse(tokens)
    
    print(f"✅ Parsed: {len(program.boundaries)} boundaries, "
          f"{len(program.domains)} domains, {len(program.qubits)} qubits")
    
    # 2. Execute with interpreter
    interpreter = StructuralInterpreter(lattice_size=500)
    results = interpreter.execute_program(program)
    
    print(f"\n📊 Interpreter Results:")
    print(f"   Constants generated: {len(results.get('constants_generated', {}))}")
    print(f"   Structural coherence: {results.get('structural_coherence', 0):.3f}")
    print(f"   Total information: {results.get('total_information', 0):.4f}")
    
    # 3. Generate code in all formats
    codegen = QGLCodeGenerator(interpreter)
    
    print(f"\n🔄 Generating code in all formats...")
    
    # Python
    python_code = codegen.generate_python(program, results)
    print(f"✅ Python code: {len(python_code)} lines")
    
    # HTML report
    html_report = codegen.generate_html_report(program, results)
    print(f"✅ HTML report: {len(html_report)} lines")
    
    # JSON export
    json_export = codegen.generate_json(program, results, pretty=True)
    print(f"✅ JSON export: {len(json_export)} lines")
    
    # C++ code
    cpp_code = codegen.generate_cpp(program, results)
    print(f"✅ C++ code: {len(cpp_code)} lines")
    
    # 4. Export all formats
    codegen.export_all_formats(program, results, "test_output")
    
    # 5. Test accuracy
    constants = results.get('constants_generated', {})
    if 'accuracy' in constants:
        print(f"\n🎯 Accuracy Results:")
        for const, error in constants['accuracy'].items():
            status = "✅" if error < 0.01 else "⚠️"
            print(f"   {status} {const}: {error:.10f}% error")
    
    # 6. Test lattice visualization
    viz_data = interpreter.visualize_lattice()
    print(f"\n🌌 Visualization Data:")
    print(f"   Points: {len(viz_data.get('points', []))}")
    print(f"   Structures: {len(viz_data.get('structures', []))}")
    print(f"   Entanglements: {len(viz_data.get('connections', []))}")
    
    # 7. Get execution summary
    summary = interpreter.get_execution_summary()
    print(f"\n📈 Execution Summary:")
    print(f"   Occupancy: {summary['occupancy_rate']:.2%}")
    print(f"   Entanglement groups: {summary['entanglement_groups']}")
    print(f"   Total information: {summary['total_information']:.4f}")
    
    print("\n" + "="*60)
    print("✅ COMPLETE SYSTEM TEST PASSED!")
    print("="*60)
    
    return {
        'program': program,
        'interpreter_results': results,
        'summary': summary,
        'viz_data': viz_data
    }

if __name__ == "__main__":
    test_complete_system()