"""
QGL Parser - Builds structural AST, no time/iteration concepts
"""
from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class Boundary:
    name: str
    content: List[str]  # Names of structures inside
    
    def __post_init__(self):
        # Enforce: boundary cannot be in its own content
        if self.name in self.content:
            raise ValueError(
                f"STRUCTURAL VIOLATION: Boundary '{self.name}' "
                f"cannot contain itself"
            )

@dataclass
class Domain:
    name: str
    states: List[str]  # State names, may include ⊕ for unresolved
    
    def has_unresolved(self):
        return any('⊕' in state for state in self.states)

@dataclass
class Qubit:
    name: str
    state_a: str
    state_b: str
    resolved: bool = False

@dataclass
class QGLProgram:
    boundaries: List[Boundary]
    domains: List[Domain]
    qubits: List[Qubit]

class QGLParser:
    """Parses QGL tokens into structural AST"""
    
    def __init__(self):
        self.tokens = []
        self.position = 0
        self.current_token = None
        
    def parse(self, tokens):
        """Parse tokens into QGLProgram"""
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
        
        boundaries = []
        domains = []
        qubits = []
        
        while self.position < len(self.tokens):
            token_type, token_value = self.current_token
            
            if token_type == 'BOUNDARY':
                boundary = self.parse_boundary()
                boundaries.append(boundary)
            elif token_type == 'DOMAIN':
                domain = self.parse_domain()
                domains.append(domain)
            elif token_type == 'QUBIT':
                qubit = self.parse_qubit()
                qubits.append(qubit)
            else:
                self.advance()
        
        return QGLProgram(boundaries, domains, qubits)
    
    def parse_boundary(self):
        """Parse boundary { content }"""
        self.advance()  # Skip 'boundary'
        
        # Get boundary name
        if self.current_token[0] != 'IDENTIFIER':
            raise SyntaxError("Expected boundary name")
        name = self.current_token[1]
        self.advance()
        
        # Check for {
        if self.current_token[0] != 'LBRACE':
            raise SyntaxError("Expected '{' after boundary name")
        self.advance()
        
        # Parse content
        content = []
        while self.current_token[0] != 'RBRACE':
            if self.current_token[0] == 'IDENTIFIER':
                content.append(self.current_token[1])
            elif self.current_token[0] == 'COMMA':
                pass  # Skip commas
            else:
                raise SyntaxError("Expected identifier or '}' in boundary content")
            self.advance()
        
        self.advance()  # Skip '}'
        return Boundary(name, content)
    
    def parse_domain(self):
        """Parse domain { states }"""
        self.advance()  # Skip 'domain'
        
        # Get domain name
        if self.current_token[0] != 'IDENTIFIER':
            raise SyntaxError("Expected domain name")
        name = self.current_token[1]
        self.advance()
        
        # Check for {
        if self.current_token[0] != 'LBRACE':
            raise SyntaxError("Expected '{' after domain name")
        self.advance()
        
        # Parse states
        states = []
        while self.current_token[0] != 'RBRACE':
            if self.current_token[0] == 'IDENTIFIER':
                state = self.current_token[1]
                self.advance()
                
                # Check for superposition ⊕
                if self.current_token[0] == 'PLUS':
                    self.advance()
                    if self.current_token[0] != 'IDENTIFIER':
                        raise SyntaxError("Expected second state after ⊕")
                    state += f"⊕{self.current_token[1]}"
                    self.advance()
                
                states.append(state)
            
            elif self.current_token[0] == 'COMMA':
                self.advance()  # Skip commas
            else:
                raise SyntaxError(f"Unexpected token in domain: {self.current_token}")
        
        self.advance()  # Skip '}'
        return Domain(name, states)
    
    def parse_qubit(self):
        """Parse qubit name = { A ⊕ B }"""
        self.advance()  # Skip 'qubit'
        
        # Get qubit name
        if self.current_token[0] != 'IDENTIFIER':
            raise SyntaxError("Expected qubit name")
        name = self.current_token[1]
        self.advance()
        
        # Check for =
        if self.current_token[0] != 'EQUALS':
            raise SyntaxError("Expected '=' after qubit name")
        self.advance()
        
        # Check for {
        if self.current_token[0] != 'LBRACE':
            raise SyntaxError("Expected '{' after '='")
        self.advance()
        
        # Get first state
        if self.current_token[0] != 'IDENTIFIER':
            raise SyntaxError("Expected first state in qubit")
        state_a = self.current_token[1]
        self.advance()
        
        # Check for ⊕
        if self.current_token[0] != 'PLUS':
            raise SyntaxError("Expected '⊕' between qubit states")
        self.advance()
        
        # Get second state
        if self.current_token[0] != 'IDENTIFIER':
            raise SyntaxError("Expected second state in qubit")
        state_b = self.current_token[1]
        self.advance()
        
        # Check for }
        if self.current_token[0] != 'RBRACE':
            raise SyntaxError("Expected '}' after qubit states")
        self.advance()
        
        return Qubit(name, state_a, state_b)
    
    def advance(self):
        """Move to next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = ('EOF', '')