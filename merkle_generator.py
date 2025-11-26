import hashlib
import json
from datetime import datetime

class SentinelMerkleEngine:
    def __init__(self):
        self.leaves = []

    def hash_data(self, data_string):
        """Standard SHA256 hashing for leaf nodes."""
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    def add_telemetry_log(self, log_entry):
        """Ingests a raw log (dict) and hashes it."""
        # Canonicalize the JSON to ensure consistent hashing
        log_string = json.dumps(log_entry, sort_keys=True)
        leaf_hash = self.hash_data(log_string)
        self.leaves.append(leaf_hash)
        return leaf_hash

    def build_merkle_root(self):
        """Recursively builds the Merkle Root from leaves."""
        if not self.leaves:
            return None
        
        current_level = self.leaves
        
        while len(current_level) > 1:
            next_level = []
            # Process pairs
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # Duplicate last element if odd number of leaves
                right = current_level[i+1] if i+1 < len(current_level) else left
                
                # Combine and hash
                combined = left + right
                next_level.append(self.hash_data(combined))
            current_level = next_level
            
        return current_level[0]

# --- Simulation for Demo ---
if __name__ == "__main__":
    engine = SentinelMerkleEngine()
    
    # Simulate critical infrastructure data
    logs = [
        {"asset_id": "TRANSFORMER-MIA-001", "temp": 85.4, "status": "OK", "timestamp": "2025-01-22T10:00:00Z"},
        {"asset_id": "TRANSFORMER-MIA-002", "temp": 102.1, "status": "WARN", "timestamp": "2025-01-22T10:00:05Z"},
        {"asset_id": "GRID-SWITCH-09", "load": "94%", "status": "OK", "timestamp": "2025-01-22T10:00:10Z"}
    ]

    print("--- Sentinel Grid Engine Starting ---")
    for log in logs:
        h = engine.add_telemetry_log(log)
        print(f"Ingested Log: {log['asset_id']} -> Hash: {h[:10]}...")

    root = engine.build_merkle_root()
    print("\n--- Batch Complete ---")
    print(f"Generated Merkle Root: 0x{root}")
    print("Ready for commitment to Avalanche PCC Contract.")
