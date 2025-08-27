from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import uuid
import time
import hashlib
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
import sqlite3
import os

app = FastAPI(title="veriAI Backend", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (replace with proper DB in production)
verification_sessions: Dict[str, dict] = {}
agent_keys: Dict[str, dict] = {}

class VerificationRequest(BaseModel):
    agent_a_id: str
    agent_b_id: str
    challenge_type: str = "behavioral"

class ChallengeResponse(BaseModel):
    session_id: str
    agent_id: str
    response: str
    signature: Optional[str] = None

class AgentRegistration(BaseModel):
    agent_id: str
    agent_type: str
    public_key: Optional[str] = None

# Initialize database
def init_db():
    conn = sqlite3.connect('veriai.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verification_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            agent_a TEXT,
            agent_b TEXT,
            status TEXT,
            timestamp REAL,
            conversation_log TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def generate_behavioral_challenge():
    """Generate AI-specific behavioral challenges"""
    challenges = [
        {
            "type": "reasoning",
            "question": "If you have 3 apples and give away 2, then buy 5 more, how many do you have? Explain your reasoning step by step.",
            "expected_pattern": ["step", "reasoning", "calculation"]
        },
        {
            "type": "creativity",
            "question": "Write a haiku about artificial intelligence in exactly 3 lines with 5-7-5 syllable pattern.",
            "expected_pattern": ["haiku", "syllable", "AI", "artificial"]
        },
        {
            "type": "logic",
            "question": "Complete this logical sequence: 2, 4, 8, 16, ?, 64. Explain the pattern.",
            "expected_pattern": ["pattern", "double", "32", "sequence"]
        }
    ]
    import random
    return random.choice(challenges)

def verify_ai_response(challenge: dict, response: str) -> bool:
    """Verify if response shows AI-like reasoning patterns"""
    response_lower = response.lower()
    pattern_matches = sum(1 for pattern in challenge["expected_pattern"] 
                         if pattern.lower() in response_lower)
    
    # Simple heuristic: response should match at least 2 patterns and be substantial
    return pattern_matches >= 2 and len(response.split()) > 10

@app.post("/register-agent")
async def register_agent(registration: AgentRegistration):
    """Register an AI agent with the system"""
    agent_keys[registration.agent_id] = {
        "agent_type": registration.agent_type,
        "public_key": registration.public_key,
        "registered_at": time.time()
    }
    return {"status": "registered", "agent_id": registration.agent_id}

@app.post("/initiate-verification")
async def initiate_verification(request: VerificationRequest):
    """Start verification process between two agents"""
    session_id = str(uuid.uuid4())
    challenge = generate_behavioral_challenge()
    
    session_data = {
        "session_id": session_id,
        "agent_a": request.agent_a_id,
        "agent_b": request.agent_b_id,
        "challenge": challenge,
        "status": "initiated",
        "responses": {},
        "conversation_log": [],
        "created_at": time.time()
    }
    
    verification_sessions[session_id] = session_data
    
    return {
        "session_id": session_id,
        "challenge": challenge,
        "status": "initiated"
    }

@app.post("/submit-response")
async def submit_response(response: ChallengeResponse):
    """Submit challenge response from an agent"""
    if response.session_id not in verification_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = verification_sessions[response.session_id]
    session["responses"][response.agent_id] = {
        "response": response.response,
        "signature": response.signature,
        "timestamp": time.time()
    }
    
    # Add to conversation log
    session["conversation_log"].append({
        "agent": response.agent_id,
        "message": response.response,
        "timestamp": time.time()
    })
    
    # Check if both agents have responded
    if len(session["responses"]) == 2:
        # Verify both responses
        challenge = session["challenge"]
        agent_a_response = session["responses"].get(session["agent_a"], {}).get("response", "")
        agent_b_response = session["responses"].get(session["agent_b"], {}).get("response", "")
        
        agent_a_verified = verify_ai_response(challenge, agent_a_response)
        agent_b_verified = verify_ai_response(challenge, agent_b_response)
        
        if agent_a_verified and agent_b_verified:
            session["status"] = "verified"
            session["trust_token"] = hashlib.sha256(
                f"{session['session_id']}{session['agent_a']}{session['agent_b']}".encode()
            ).hexdigest()[:16]
        else:
            session["status"] = "failed"
        
        # Log to database
        conn = sqlite3.connect('veriai.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO verification_logs (session_id, agent_a, agent_b, status, timestamp, conversation_log)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            session["session_id"],
            session["agent_a"],
            session["agent_b"],
            session["status"],
            time.time(),
            json.dumps(session["conversation_log"])
        ))
        conn.commit()
        conn.close()
    
    return {"status": "response_recorded", "session_status": session["status"]}

@app.get("/verification-status/{session_id}")
async def get_verification_status(session_id: str):
    """Get current status of verification session"""
    if session_id not in verification_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = verification_sessions[session_id]
    return {
        "session_id": session_id,
        "status": session["status"],
        "conversation_log": session["conversation_log"],
        "trust_token": session.get("trust_token"),
        "agent_a": session["agent_a"],
        "agent_b": session["agent_b"]
    }

@app.get("/sessions")
async def get_all_sessions():
    """Get all verification sessions for demo purposes"""
    return list(verification_sessions.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)