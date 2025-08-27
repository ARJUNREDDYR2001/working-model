import requests
import json
import time
import random

class AgentA:
    def __init__(self, agent_id="agent_a", backend_url="http://localhost:8000"):
        self.agent_id = agent_id
        self.backend_url = backend_url
        self.personality = "analytical"
        
    def register(self):
        """Register this agent with the backend"""
        response = requests.post(f"{self.backend_url}/register-agent", json={
            "agent_id": self.agent_id,
            "agent_type": "reasoning_ai"
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
            return "I am an AI agent capable of reasoning and analysis."
    
    def _reasoning_response(self, question):
        return """Let me break this down step by step:
        1. Starting with 3 apples
        2. Give away 2 apples: 3 - 2 = 1 apple remaining
        3. Buy 5 more apples: 1 + 5 = 6 apples total
        
        Therefore, I have 6 apples. This demonstrates logical reasoning and mathematical calculation abilities typical of AI systems."""
    
    def _creative_response(self, question):
        return """Here's a haiku about artificial intelligence:
        
        Silicon minds think (5)
        Processing data streams flow (7)
        Digital wisdom (5)
        
        This follows the traditional 5-7-5 syllable pattern and reflects on AI consciousness."""
    
    def _logic_response(self, question):
        return """Analyzing the sequence: 2, 4, 8, 16, ?, 64
        
        Pattern identification: Each number is double the previous number
        - 2 × 2 = 4
        - 4 × 2 = 8  
        - 8 × 2 = 16
        - 16 × 2 = 32 (missing number)
        - 32 × 2 = 64
        
        The missing number is 32. This is a geometric sequence with ratio 2."""
    
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
            "type": "reasoning",
            "question": "If you have 3 apples and give away 2, then buy 5 more, how many do you have? Explain your reasoning step by step.",
            "expected_pattern": ["step", "reasoning", "calculation"]
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
    agent = AgentA()
    print("Agent A initialized")
    print("Registration:", agent.register())