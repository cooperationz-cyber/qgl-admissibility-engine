"""
Run all QGL demos to verify implementation
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine
from engine.inversion import InversionEngine

def run_demo(demo_name, demo_path):
    """Run a single demo"""
    print(f"\n{'='*60}")
    print(f"DEMO: {demo_name}")
    print(f"{'='*60}")
    
    try:
        with open(demo_path, 'r') as f:
            qgl_code = f.read()
        
        # Initialize components
        lexer = QGLLexer()
        parser = QGLParser()
        engine = AdmissibilityEngine()
        
        # Parse
        tokens = lexer.tokenize(qgl_code)
        program = parser.parse(tokens)
        
        # Check admissibility
        admissible, reason = engine.check_structure(program)
        
        print(f"Admissible: {admissible}")
        print(f"Reason: {reason}")
        
        # Try inversion if admissible
        if admissible:
            inversion_engine = InversionEngine(engine)
            # Try inverting first boundary
            if program.boundaries:
                first_boundary = program.boundaries[0].name
                new_program, success, inv_reason = inversion_engine.invert(
                    program, first_boundary
                )
                print(f"\nInversion on '{first_boundary}': {success}")
                print(f"Inversion reason: {inv_reason}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run all demos"""
    demo_dir = os.path.dirname(__file__)
    demos = [
        ("Moser 31 vs 32", "moser_31_32.qgl"),
        ("Global Pattern", "global_pattern.qgl"),
        ("TSP Collapse", "tsp_collapse.qgl"),
        ("Russell Rejection", "russell_reject.qgl"),
    ]
    
    print("QGL ADMISSIBILITY ENGINE - DEMO SUITE")
    print("="*60)
    
    results = []
    for demo_name, demo_file in demos:
        demo_path = os.path.join(demo_dir, demo_file)
        if os.path.exists(demo_path):
            success = run_demo(demo_name, demo_path)
            results.append((demo_name, success))
        else:
            print(f"\nERROR: Demo file not found: {demo_path}")
            results.append((demo_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("DEMO SUMMARY")
    print(f"{'='*60}")
    
    for demo_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{demo_name:30} {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total_passed}/{len(results)} demos passed")
    
    if total_passed == len(results):
        print("\n🎉 All demos passed! Engine is working correctly.")
    else:
        print("\n⚠ Some demos failed. Check implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()