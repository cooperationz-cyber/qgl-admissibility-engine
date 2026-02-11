# test_database_schema.py
from qgl.lexer import QGLLexer
from qgl.parser import QGLParser
from engine.admissibility import AdmissibilityEngine

print("="*60)
print("DATABASE SCHEMA VALIDATION")
print("="*60)

# Will this database schema have referential integrity issues?
qgl_code = """
boundary Database {
    users, posts, comments, likes
}

boundary users {
    id, name, email
}

boundary posts {
    id, user_id, content, created_at
}

boundary comments {
    id, post_id, user_id, content
}

boundary likes {
    id, post_id, user_id
}

// The constraint: Every foreign key must reference existing row
domain ForeignKeyConstraints {
    posts.user_id → users.id,
    comments.post_id → posts.id,
    comments.user_id → users.id,
    likes.post_id → posts.id,
    likes.user_id → users.id
}
"""

lexer = QGLLexer()
parser = QGLParser()
engine = AdmissibilityEngine()

print("\n1. Checking database schema structure...")
try:
    tokens = lexer.tokenize(qgl_code)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("✅ Database schema is structurally valid")
        print("   No circular references or orphaned tables")
    else:
        print(f"❌ Schema issues: {reason}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test a problematic schema
print("\n" + "="*60)
print("2. Testing problematic schema with circular reference...")

qgl_code_bad = """
boundary Database {
    A, B, C
}

boundary A {
    id, b_id
}

boundary B {
    id, c_id
}

boundary C {
    id, a_id  // Circular reference!
}
"""

try:
    tokens = lexer.tokenize(qgl_code_bad)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if not admissible:
        print("✅ CORRECT: Circular reference detected!")
        print(f"   Reason: {reason}")
        print("   A → B → C → A forms a loop")
    else:
        print("❌ UNEXPECTED: Should have caught circular reference")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Database validation complete!")