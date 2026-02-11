markdown
# QGL Admissibility Engine

**Structural Validation Engine - Not a Simulator, Not an Optimizer**

## Purpose
Answer ONE question: *"Is this structure admissible without violating boundary, inversion, or non-locality constraints?"*

## Core Design Rule (Non-Negotiable)
**No boundary may be a member of the system it bounds.**  
Everything enforces this structurally, not procedurally. No exceptions.

## Architecture
Language Layer (QGL) → Describes structure
Admissibility Engine → Validates possibility
Witness Interfaces → Expose results (never mechanics)

text

## What QGL Is NOT
- ❌ NOT a simulator
- ❌ NOT an optimizer  
- ❌ NOT a quantum computer
- ❌ NOT a physics engine
- ❌ NOT a numerical solver

## Key Features
1. **Grammar-enforced validity** - Invalid structures cannot be expressed
2. **No time/iteration concepts** - Structural only
3. **Atomic inversion only** - One dynamic operation
4. **Non-local validation** - Global constraints checked simultaneously
5. **Hardware independence** - Same result everywhere

## Quick Start

```bash
# Run tests
python -m pytest tests/structural_tests.py
python -m pytest tests/invariance_tests.py

# Run demos
python demos/run_demos.py

# Start daemon
python runtime/daemon.py