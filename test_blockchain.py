# test_blockchain.py
print("="*60)
print("BLOCKCHAIN CONSENSUS PROTOCOL VALIDATION")
print("="*60)

# Will this blockchain design have consensus failure?
qgl_code = """
boundary Blockchain {
    nodes, blocks, transactions
}

domain Nodes {
    miner_1, miner_2, miner_3, miner_4, miner_5
}

// Consensus rule: Longest chain wins
boundary ConsensusRule {
    select_longest_chain
}

// Fork possibility
qubit chain_fork = { chain_A ⊕ chain_B }

// Critical constraint: Can't have double spend
constraint DoubleSpendPrevention {
    transaction_in_one_chain_only
}

// 51% attack possibility
domain AttackScenario {
    malicious_miners_control_51_percent
}
"""

print("\nValidating blockchain consensus protocol...")
try:
    tokens = lexer.tokenize(qgl_code)
    program = parser.parse(tokens)
    admissible, reason = engine.check_structure(program)
    
    if admissible:
        print("✅ Blockchain structure is valid")
        print("   Consensus rules are properly defined")
        
        # Check for potential attacks
        has_attack_scenario = any('Attack' in d.name for d in program.domains)
        if has_attack_scenario:
            print("   ⚠ Contains attack scenario definitions")
            print("   (This doesn't mean it's vulnerable, just that attacks are modeled)")
            
    else:
        print(f"❌ Consensus issues: {reason}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("Blockchain validation complete!")