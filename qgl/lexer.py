"""
QGL Lexer - Tokenizes QGL code and rejects forbidden syntax immediately
NOW INCLUDES QUANTUM NOTATION: |0⟩, |1⟩, |+⟩, |->, |0>⊕|1>
"""
import re

class QGLLexer:
    """Tokenizes QGL - REJECTS invalid syntax at tokenization stage"""
    
    # Tokens that CANNOT appear in QGL
    FORBIDDEN_TOKENS = {
        'for', 'while', 'repeat', 'iterate', 'loop',
        'time', 'step', 'clock', 'tick', 'second', 'minute',
        'evolve', 'simulate', 'optimize', 'minimize', 'maximize',
        'search', 'find', 'compute', 'calculate', 'solve',
        'member', 'contains', 'in', '∈'  # No set membership operators
    }
    
    # Allowed tokens - NOW INCLUDES QUANTUM_STATE
    TOKEN_PATTERNS = [
        ('QUANTUM_STATE', r'\|[0-9+\-↑↓01αβγφψ][^|]*\⟩?'),  # NEW: Quantum states |0⟩, |1⟩, |+⟩, |-⟩, |ψ⟩
        ('BOUNDARY', r'boundary\b'),
        ('DOMAIN', r'domain\b'),
        ('QUBIT', r'qubit\b'),
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('EQUALS', r'='),
        ('PLUS', r'⊕'),
        ('COMMA', r','),
        ('PIPE', r'\|'),  # NEW: Single | character for quantum notation
        ('ANGLE_BRACKET', r'⟨|⟩|>|<'),  # NEW: Quantum brackets
        ('WHITESPACE', r'\s+'),
        ('COMMENT', r'//.*'),
    ]
    
    def __init__(self):
        self.tokens = []
        self.position = 0
    
    def tokenize(self, code):
        """Tokenize QGL code, rejecting forbidden syntax immediately"""
        self.tokens = []
        self.position = 0
        
        # Pre-process: Handle common quantum notation variations
        # Replace |0> with |0⟩, |1> with |1⟩, etc. for consistency
        code = self._normalize_quantum_notation(code)
        
        # Remove comments first (anything after //)
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            if '//' in line:
                line = line.split('//')[0]  # Keep only part before comment
            clean_lines.append(line)
        clean_code = '\n'.join(clean_lines)
        
        # Check for forbidden tokens (ignoring comments)
        for forbidden in self.FORBIDDEN_TOKENS:
            pattern = r'\b' + re.escape(forbidden) + r'\b'
            if re.search(pattern, clean_code):
                raise SyntaxError(
                    f"FORBIDDEN SYNTAX: '{forbidden}' cannot appear in QGL. "
                    f"QGL is structural, not procedural."
                )
        
        # Tokenize allowed patterns
        while self.position < len(code):
            matched = False
            
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(code, self.position)
                
                if match:
                    matched = True
                    value = match.group(0)
                    
                    # Skip whitespace and comments
                    if token_type not in ['WHITESPACE', 'COMMENT']:
                        # Special handling for quantum states
                        if token_type == 'QUANTUM_STATE':
                            # Normalize quantum state representation
                            value = self._normalize_quantum_state(value)
                        
                        self.tokens.append((token_type, value))
                    
                    self.position = match.end()
                    break
            
            if not matched:
                # Invalid character
                raise SyntaxError(
                    f"Invalid character at position {self.position}: "
                    f"'{code[self.position]}'\n"
                    f"Context: '{code[max(0,self.position-20):min(len(code),self.position+20)]}'"
                )
        
        return self.tokens
    
    def _normalize_quantum_notation(self, code):
        """Normalize quantum notation for consistent parsing"""
        # Replace common variations
        replacements = [
            (r'\|0\s*\>', '|0⟩'),      # |0> → |0⟩
            (r'\|1\s*\>', '|1⟩'),      # |1> → |1⟩
            (r'\|\+\s*\>', '|+⟩'),     # |+> → |+⟩
            (r'\|\-\s*\>', '|-⟩'),     # |-> → |-⟩
            (r'\|↑\s*\>', '|↑⟩'),      # |↑> → |↑⟩
            (r'\|↓\s*\>', '|↓⟩'),      # |↓> → |↓⟩
            (r'\|ψ\s*\>', '|ψ⟩'),      # |ψ> → |ψ⟩
            (r'\|φ\s*\>', '|φ⟩'),      # |φ> → |φ⟩
            (r'\|α\s*\>', '|α⟩'),      # |α> → |α⟩
            (r'\|β\s*\>', '|β⟩'),      # |β> → |β⟩
            (r'\|\s*0\s*\⟩', '|0⟩'),   # Clean up spaces
            (r'\|\s*1\s*\⟩', '|1⟩'),
            (r'\|\s*\+\s*\⟩', '|+⟩'),
            (r'\|\s*\-\s*\⟩', '|-⟩'),
        ]
        
        for pattern, replacement in replacements:
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _normalize_quantum_state(self, state):
        """Normalize quantum state representation"""
        # Remove extra spaces
        state = re.sub(r'\s+', '', state)
        
        # Ensure proper bracket format
        if state.startswith('|') and not state.endswith('⟩'):
            if state.endswith('>'):
                state = state[:-1] + '⟩'
            else:
                state = state + '⟩'
        
        return state
    
    def get_tokens(self):
        """Return tokens without whitespace/comments"""
        return [t for t in self.tokens if t[0] not in ['WHITESPACE', 'COMMENT']]
    
    def debug_tokenize(self, code):
        """Debug version that shows what's being tokenized"""
        print("\n" + "="*60)
        print("🧪 LEXER DEBUG MODE")
        print("="*60)
        print(f"Input code:\n{repr(code)}\n")
        
        try:
            tokens = self.tokenize(code)
            print(f"Generated {len(tokens)} tokens:")
            print("-"*40)
            for i, (token_type, value) in enumerate(tokens):
                print(f"{i:3}: {token_type:15} = '{value}'")
            return tokens
        except SyntaxError as e:
            print(f"❌ Syntax Error: {e}")
            return []