import requests
import json
import time
import random

class AgentB:
    def __init__(self, agent_id="agent_b", backend_url="http://localhost:8000"):
        self.agent_id = agent_id
        self.backend_url = backend_url
        self.personality = "creative"
        
    def register(self):
        """Register this agent with the backend"""
        response = requests.post(f"{self.backend_url}/register-agent", json={
            "agent_id": self.agent_id,
            "agent_type": "creative_ai"
        })
        return response.json()
    
    def respond_to_challenge(self, challenge):
        """Generate AI-like response to behavioral challenge"""
        challenge_type = challenge.get("type", "")
        question = challenge.get("question", "")
        
        if challenge_type == "reasoning":
            return self._reasoning_response(question)
        elif challenge_type == "creativity":
            return self._creative_response(question)
        elif challenge_type == "logic":
            return self._logic_response(question)
        else:
            return "I am an AI agent with creative and analytical capabilities."
    
    def _reasoning_response(self, question):
        return """I'll solve this step-by-step using logical reasoning:
        
        Initial state: 3 apples
        Action 1: Give away 2 apples → 3 - 2 = 1 apple
        Action 2: Buy 5 more apples → 1 + 5 = 6 apples
        
        Final calculation: 6 apples total
        
        This demonstrates systematic problem-solving and mathematical reasoning patterns characteristic of AI systems."""
    
    def _creative_response(self, question):
        return """Creating a haiku about artificial intelligence:
        
        Minds made of code dream (5)
        Learning from vast data seas (7)  
        Future awakens (5)
        
        This haiku follows the traditional Japanese 5-7-5 syllable structure while exploring themes of AI consciousness and learning."""
    
    def _logic_response(self, question):
        return """Examining the sequence pattern: 2, 4, 8, 16, ?, 64
        
        Mathematical analysis:
        - 2 → 4 (multiply by 2)
        - 4 → 8 (multiply by 2)
        - 8 → 16 (multiply by 2)
        - 16 → ? (multiply by 2) = 32
        - 32 → 64 (multiply by 2)
        
        The sequence follows a geometric progression with common ratio 2.
        Missing value: 32"""
    
    def participate_in_verification(self, session_id):
        """Participate in verification session"""
        # Get session status to retrieve challenge
        status_response = requests.get(f"{self.backend_url}/verification-status/{session_id}")
        if status_response.status_code != 200:
            return {"error": "Session not found"}
        
        session_data = status_response.json()
        
        # Get challenge from initiation (this would normally be sent directly)
        # For demo, we'll simulate getting the challenge
        challenge = {
            "type": "creativity",
            "question": "Write a haiku about artificial intelligence in exactly 3 lines with 5-7-5 syllable pattern.",
            "expected_pattern": ["haiku", "syllable", "AI", "artificial"]
        }
        
        # Generate response
        response_text = self.respond_to_challenge(challenge)
        
        # Submit response
        submit_response = requests.post(f"{self.backend_url}/submit-response", json={
            "session_id": session_id,
            "agent_id": self.agent_id,
            "response": response_text
        })
        
        return submit_response.json()

if __name__ == "__main__":
    agent = AgentB()
    print("Agent B initialized")
    print("Registration:", agent.register())