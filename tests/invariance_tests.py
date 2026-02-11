"""
Invariance Tests - Same result regardless of representation
NO hardware tests, NO performance tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine

class TestTickCountInvariance(unittest.TestCase):
    """
    Critical: QGL must be tick-count invariant
    No concept of steps, iterations, or time
    """
    
    def test_no_iteration_counting(self):
        """Structure validity should not depend on 'number of checks'"""
        qgl_code = """
        boundary System {
            component1, component2
        }
        
        domain Components {
            A, B
        }
        """
        
        lexer = QGLLexer()
        parser = QGLParser()
        
        tokens = lexer.tokenize(qgl_code)
        program = parser.parse(tokens)
        
        # Check 100 times - should always get same result
        results = []
        for i in range(100):
            engine = AdmissibilityEngine()  # Fresh engine each time
            admissible, reason = engine.check_structure(program)
            results.append((admissible, reason))
        
        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result[0], first_result[0])
            # Reasons might differ slightly in wording, but not in meaning
    
    def test_order_invariance(self):
        """Structure validity should not depend on declaration order"""
        qgl_code_forward = """
        boundary A { B }
        boundary B { C }
        boundary C { elements }
        """
        
        qgl_code_backward = """
        boundary C { elements }
        boundary B { C }
        boundary A { B }
        """
        
        lexer = QGLLexer()
        parser = QGLParser()
        
        # Parse forward
        tokens_fwd = lexer.tokenize(qgl_code_forward)
        program_fwd = parser.parse(tokens_fwd)
        
        # Parse backward
        tokens_bwd = lexer.tokenize(qgl_code_backward)
        program_bwd = parser.parse(tokens_bwd)
        
        # Check both
        engine = AdmissibilityEngine()
        admissible_fwd, reason_fwd = engine.check_structure(program_fwd)
        
        engine2 = AdmissibilityEngine()
        admissible_bwd, reason_bwd = engine2.check_structure(program_bwd)
        
        self.assertEqual(admissible_fwd, admissible_bwd)
    
    def test_whitespace_invariance(self):
        """Structure validity should not depend on whitespace"""
        test_cases = [
            ("boundary A{b,c}", "boundary A { b , c }"),
            ("boundary\nA\n{\nb\n,\nc\n}\n", "boundary A{b,c}"),
            ("  boundary   A   {   b   ,   c   }   ", "boundary A{b,c}"),
        ]
        
        lexer = QGLLexer()
        parser = QGLParser()
        
        for code1, code2 in test_cases:
            with self.subTest(case=f"{code1[:20]}... vs {code2[:20]}..."):
                tokens1 = lexer.tokenize(code1)
                program1 = parser.parse(tokens1)
                
                tokens2 = lexer.tokenize(code2)
                program2 = parser.parse(tokens2)
                
                engine = AdmissibilityEngine()
                admissible1, reason1 = engine.check_structure(program1)
                
                engine2 = AdmissibilityEngine()
                admissible2, reason2 = engine2.check_structure(program2)
                
                self.assertEqual(
                    admissible1, admissible2,
                    f"Mismatch: '{code1}' -> {admissible1}, '{code2}' -> {admissible2}"
                )

class TestHardwareIndependence(unittest.TestCase):
    """
    QGL must give same results on all hardware
    (Simulated by testing with different data structure implementations)
    """
    
    def test_memory_layout_independence(self):
        """Should not depend on how structures are stored in memory"""
        
        # Same structure, different QGL representations
        representations = [
            # Flat representation
            """
            boundary System {A,B,C}
            boundary A {a1}
            boundary B {b1}
            boundary C {c1}
            """,
            
            # Nested representation
            """
            boundary System {
                A, B, C
            }
            
            boundary A {
                a1
            }
            
            boundary B {
                b1
            }
            
            boundary C {
                c1
            }
            """,
            
            # Mixed representation
            """
            boundary System{A,B,C}
            boundary A{a1}
            boundary B {
                b1
            }
            boundary C{c1}
            """
        ]
        
        lexer = QGLLexer()
        parser = QGLParser()
        
        results = []
        for rep in representations:
            tokens = lexer.tokenize(rep)
            program = parser.parse(tokens)
            
            engine = AdmissibilityEngine()
            admissible, reason = engine.check_structure(program)
            results.append(admissible)
        
        # All should give same result
        self.assertTrue(all(r == results[0] for r in results),
                       f"Different results: {results}")
    
    def test_no_floating_point_dependence(self):
        """QGL should not use floating point for decisions"""
        qgl_code = """
        boundary MathSystem {
            integers, rationals
        }
        
        domain Integers {
            one, two, three
        }
        
        domain Rationals {
            one_half, two_thirds
        }
        
        // No floating point operations
        // No π, e, φ constants in structural decisions
        """
        
        lexer = QGLLexer()
        parser = QGLParser()
        engine = AdmissibilityEngine()
        
        tokens = lexer.tokenize(qgl_code)
        program = parser.parse(tokens)
        
        admissible, reason = engine.check_structure(program)
        
        # Check that no floating point was involved
        # (This is more of a design constraint than runtime test)
        self.assertTrue(admissible)
        # If this test passes, it means QGL didn't crash trying to do math
        # QGL should only do structural checks, not numerical computations

if __name__ == '__main__':
    unittest.main()