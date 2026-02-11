"""
Structural Tests - Validate admissibility acceptance/rejection
NO performance tests, NO optimization tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine

class TestStructuralAdmissibility(unittest.TestCase):
    """Test admissibility acceptance/rejection"""
    
    def setUp(self):
        self.lexer = QGLLexer()
        self.parser = QGLParser()
        self.engine = AdmissibilityEngine()
    
    def test_valid_structure(self):
        """Valid structure should be admissible"""
        qgl_code = """
        boundary Outer {
            Inner, element1
        }
        
        boundary Inner {
            element2, element3
        }
        """
        
        tokens = self.lexer.tokenize(qgl_code)
        program = self.parser.parse(tokens)
        admissible, reason = self.engine.check_structure(program)
        
        self.assertTrue(admissible)
        self.assertIn("admissible", reason.lower())
    
    def test_self_containment_rejection(self):
        """Boundary containing itself should be rejected"""
        qgl_code = """
        boundary SelfContaining {
            SelfContaining  // Should cause parse error
        }
        """
        
        with self.assertRaises(ValueError) as context:
            tokens = self.lexer.tokenize(qgl_code)
            program = self.parser.parse(tokens)
            self.engine.check_structure(program)
        
        self.assertIn("cannot contain itself", str(context.exception))
    
    def test_circular_containment_rejection(self):
        """Circular containment should be rejected"""
        qgl_code = """
        boundary A {
            B
        }
        
        boundary B {
            A
        }
        """
        
        tokens = self.lexer.tokenize(qgl_code)
        program = self.parser.parse(tokens)
        admissible, reason = self.engine.check_structure(program)
        
        self.assertFalse(admissible)
        self.assertIn("circular", reason.lower())
    
    def test_forbidden_syntax_rejection(self):
        """Forbidden syntax should be rejected at lexer stage"""
        qgl_code = """
        boundary Test {
            elements
        }
        
        for i in elements  // FORBIDDEN: iteration
        """
        
        with self.assertRaises(SyntaxError) as context:
            self.lexer.tokenize(qgl_code)
        
        self.assertIn("forbidden", str(context.exception).lower())
        self.assertIn("iteration", str(context.exception).lower())
    
    def test_time_reference_rejection(self):
        """Time references should be rejected"""
        qgl_code = """
        boundary System {
            states
        }
        
        // Time step - FORBIDDEN
        time = 0
        """
        
        with self.assertRaises(SyntaxError) as context:
            self.lexer.tokenize(qgl_code)
        
        self.assertIn("forbidden", str(context.exception).lower())
        self.assertIn("time", str(context.exception).lower())
    
    def test_qubit_domain_validation(self):
        """Qubit states must be in domains"""
        qgl_code = """
        boundary System {
            my_domain, my_qubit
        }
        
        domain MyDomain {
            state1, state2
        }
        
        qubit my_qubit = { state1 ⊕ state2 }
        """
        
        tokens = self.lexer.tokenize(qgl_code)
        program = self.parser.parse(tokens)
        admissible, reason = self.engine.check_structure(program)
        
        self.assertTrue(admissible, f"Should be admissible: {reason}")
    
    def test_qubit_missing_domain_rejection(self):
        """Qubit with state not in domain should be rejected"""
        qgl_code = """
        boundary System {
            my_domain, my_qubit
        }
        
        domain MyDomain {
            state1  // Missing state2
        }
        
        qubit my_qubit = { state1 ⊕ state2 }  // state2 not in domain
        """
        
        tokens = self.lexer.tokenize(qgl_code)
        program = self.parser.parse(tokens)
        admissible, reason = self.engine.check_structure(program)
        
        self.assertFalse(admissible)
        self.assertIn("not in any domain", reason)
    
    def test_inversion_preserves_admissibility(self):
        """Inversion should transform admissible → admissible"""
        from engine.inversion import InversionEngine
        
        qgl_code = """
        boundary Outer {
            Inner, element
        }
        
        boundary Inner {
            sub_element
        }
        """
        
        tokens = self.lexer.tokenize(qgl_code)
        program = self.parser.parse(tokens)
        
        # Check initial admissibility
        admissible, reason = self.engine.check_structure(program)
        self.assertTrue(admissible)
        
        # Create inversion engine
        inversion_engine = InversionEngine(self.engine)
        
        # Perform inversion
        new_program, success, inv_reason = inversion_engine.invert(program, "Outer")
        
        self.assertTrue(success)
        self.assertIn("successful", inv_reason.lower())
        
        # Check new structure is admissible
        admissible_after, reason_after = self.engine.check_structure(new_program)
        self.assertTrue(admissible_after, f"After inversion: {reason_after}")

class TestInvariance(unittest.TestCase):
    """Test invariance under different representations"""
    
    def test_representation_invariance(self):
        """Same structure with different formatting should give same result"""
        qgl_code1 = """
        boundary A{b,c}
        boundary B{d,e}
        """
        
        qgl_code2 = """
        boundary A {
            b, c
        }
        
        boundary B {
            d, e
        }
        """
        
        lexer = QGLLexer()
        parser = QGLParser()
        engine = AdmissibilityEngine()
        
        # Parse both
        tokens1 = lexer.tokenize(qgl_code1)
        program1 = parser.parse(tokens1)
        
        tokens2 = lexer.tokenize(qgl_code2)
        program2 = parser.parse(tokens2)
        
        # Check both are admissible
        admissible1, reason1 = engine.check_structure(program1)
        admissible2, reason2 = engine.check_structure(program2)
        
        self.assertEqual(admissible1, admissible2)
        
        # Reset engine for second check
        engine2 = AdmissibilityEngine()
        admissible2_2, reason2_2 = engine2.check_structure(program2)
        
        self.assertEqual(admissible1, admissible2_2)

if __name__ == '__main__':
    unittest.main()