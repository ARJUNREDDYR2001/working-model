# veriAI - AI Agent Verification Protocol

A secure verification protocol that allows AI agents to verify each other's authenticity through cryptographic and behavioral challenges.

## 🎯 Problem Statement

In multi-agent AI ecosystems, malicious actors (humans/bots/rogue models) can pretend to be trusted AI agents. veriAI solves this by implementing a "secret mode" verification system using cryptographic and behavioral verification.

## 🏗️ Architecture

### Frontend (Next.js)

- **Demo Dashboard**: Visual interface showing agent verification process
- **Real-time Logs**: Live conversation between agents
- **Trust Tokens**: Visual representation of verification success
- **Session History**: Track previous verification attempts

### Backend (Python FastAPI)

- **Verification Engine**: Core logic for challenge-response protocol
- **Agent Registration**: Manage AI agent identities
- **Cryptographic Security**: Generate and validate challenges
- **Session Management**: Track verification sessions

### AI Agents

- **Agent A**: Analytical AI with reasoning capabilities
- **Agent B**: Creative AI with problem-solving skills
- **Behavioral Verification**: Respond to AI-specific challenges
- **Pattern Recognition**: Demonstrate AI-like reasoning patterns

## 🚀 Quick Start

### 1. Start the Backend

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

The backend will be available at `http://localhost:8000`

### 2. Start the Frontend

cd frontend
npm install --legacy-peer-deps
npm run dev

The frontend will be available at `http://localhost:3000`

### 3. Run Demo

Visit `http://localhost:3000` and click "Start Verification" to see the agents verify each other.

## 🔧 Manual Testing

### Run Backend Demo Script

```bash
cd backend
python demo_orchestrator.py
```

### Test Individual Agents

```bash
cd backend
python agents/agent_a.py
python agents/agent_b.py
```

### API Endpoints

- `POST /initiate-verification` - Start verification between two agents
- `POST /submit-response` - Submit agent response to challenge
- `GET /verification-status/{session_id}` - Check verification status
- `POST /register-agent` - Register new AI agent
- `GET /sessions` - Get all verification sessions

## 🧪 How It Works

1. **Initiation**: System generates behavioral challenge for both agents
2. **Challenge**: Agents receive AI-specific questions (reasoning, creativity, logic)
3. **Response**: Each agent provides detailed, AI-like responses
4. **Verification**: Backend analyzes responses for AI behavior patterns
5. **Trust Token**: Successful verification generates cryptographic trust token
6. **Result**: Visual confirmation of agent authenticity

## 🔐 Security Features

- **Behavioral Analysis**: Challenges designed to detect AI reasoning patterns
- **Pattern Matching**: Responses analyzed for AI-specific language patterns
- **Session Isolation**: Each verification session is cryptographically unique
- **Trust Tokens**: SHA-256 hashed verification certificates
- **Audit Trail**: Complete conversation logs stored for analysis

## 🎨 Features

- **Real-time Visualization**: Watch agents communicate in real-time
- **Multiple Challenge Types**: Reasoning, creativity, and logic challenges
- **Trust Tokens**: Visual proof of successful verification
- **Session History**: Track all verification attempts
- **Responsive UI**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLite, Cryptography
- **AI Integration**: Extensible for OpenAI, Anthropic, HuggingFace APIs
- **Security**: RSA encryption, SHA-256 hashing, JWT tokens

## 📈 Future Enhancements

- **Voice Integration**: Text-to-speech for agent conversations
- **Visual Avatars**: Unique visual identities for each agent
- **QR Code Tokens**: Scannable trust certificates
- **Multi-LLM Support**: Integration with various AI providers
- **Zero-Knowledge Proofs**: Advanced cryptographic verification
- **Blockchain Integration**: Immutable verification records

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Demo

The system demonstrates:

- Two AI agents (Agent A: Analytical 🤖, Agent B: Creative 🛡️)
- Real-time behavioral verification
- Cryptographic trust establishment
- Visual feedback and logging
- Session management and history

Perfect for hackathons, AI research, and multi-agent system security!
