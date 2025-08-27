#!/usr/bin/env python3
"""
Demo orchestrator for veriAI system
Simulates the full verification flow between two AI agents
"""

import requests
import time
import json
from agents.agent_a import AgentA
from agents.agent_b import AgentB

class VeriAIDemo:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.agent_a = AgentA(backend_url=backend_url)
        self.agent_b = AgentB(backend_url=backend_url)
    
    def run_demo(self):
        print("🚀 Starting veriAI Demo")
        print("=" * 50)
        
        # Step 1: Register agents
        print("\n1. Registering agents...")
        reg_a = self.agent_a.register()
        reg_b = self.agent_b.register()
        print(f"   Agent A: {reg_a}")
        print(f"   Agent B: {reg_b}")
        
        # Step 2: Initiate verification
        print("\n2. Initiating verification...")
        response = requests.post(f"{self.backend_url}/initiate-verification", json={
            "agent_a_id": "agent_a",
            "agent_b_id": "agent_b",
            "challenge_type": "behavioral"
        })
        
        if response.status_code != 200:
            print(f"   ❌ Failed to initiate: {response.text}")
            return
        
        session_data = response.json()
        session_id = session_data["session_id"]
        challenge = session_data["challenge"]
        
        print(f"   ✅ Session created: {session_id}")
        print(f"   📝 Challenge type: {challenge['type']}")
        print(f"   ❓ Question: {challenge['question']}")
        
        # Step 3: Agent A responds
        print("\n3. Agent A responding...")
        time.sleep(1)  # Simulate thinking time
        
        response_a = self.agent_a.respond_to_challenge(challenge)
        submit_a = requests.post(f"{self.backend_url}/submit-response", json={
            "session_id": session_id,
            "agent_id": "agent_a",
            "response": response_a
        })
        
        print(f"   🤖 Agent A response: {response_a[:100]}...")
        print(f"   📤 Submission status: {submit_a.json()}")
        
        # Step 4: Agent B responds
        print("\n4. Agent B responding...")
        time.sleep(1)  # Simulate thinking time
        
        response_b = self.agent_b.respond_to_challenge(challenge)
        submit_b = requests.post(f"{self.backend_url}/submit-response", json={
            "session_id": session_id,
            "agent_id": "agent_b",
            "response": response_b
        })
        
        print(f"   🛡️ Agent B response: {response_b[:100]}...")
        print(f"   📤 Submission status: {submit_b.json()}")
        
        # Step 5: Check verification result
        print("\n5. Checking verification result...")
        time.sleep(1)
        
        status_response = requests.get(f"{self.backend_url}/verification-status/{session_id}")
        final_status = status_response.json()
        
        print(f"   📊 Final status: {final_status['status']}")
        
        if final_status['status'] == 'verified':
            print(f"   ✅ VERIFICATION SUCCESSFUL!")
            print(f"   🔑 Trust token: {final_status.get('trust_token', 'N/A')}")
        else:
            print(f"   ❌ VERIFICATION FAILED!")
        
        # Step 6: Show conversation log
        print("\n6. Conversation log:")
        for i, log_entry in enumerate(final_status.get('conversation_log', []), 1):
            agent_emoji = "🤖" if log_entry['agent'] == 'agent_a' else "🛡️"
            print(f"   {agent_emoji} {log_entry['agent']}: {log_entry['message'][:80]}...")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed!")
        
        return final_status

if __name__ == "__main__":
    demo = VeriAIDemo()
    demo.run_demo()