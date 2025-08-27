"use client";

import { useState, useEffect } from "react";
import {
  Shield,
  Bot,
  CheckCircle,
  XCircle,
  Play,
  MessageSquare,
  Key,
} from "lucide-react";

interface ConversationLog {
  agent: string;
  message: string;
  timestamp: number;
}

interface VerificationSession {
  session_id: string;
  status: string;
  conversation_log: ConversationLog[];
  trust_token?: string;
  agent_a: string;
  agent_b: string;
}

export default function Home() {
  const [isVerifying, setIsVerifying] = useState(false);
  const [currentSession, setCurrentSession] =
    useState<VerificationSession | null>(null);
  const [sessions, setSessions] = useState<VerificationSession[]>([]);
  const [logs, setLogs] = useState<string[]>([]);

  const API_BASE = "http://localhost:8000";

  const addLog = (message: string) => {
    setLogs((prev) => [
      ...prev,
      `${new Date().toLocaleTimeString()}: ${message}`,
    ]);
  };

  const startVerification = async () => {
    setIsVerifying(true);
    addLog("Initiating verification between Agent A and Agent B...");

    try {
      // Start verification
      const response = await fetch(`${API_BASE}/initiate-verification`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_a_id: "agent_a",
          agent_b_id: "agent_b",
          challenge_type: "behavioral",
        }),
      });

      const data = await response.json();
      addLog(`Verification session created: ${data.session_id}`);
      addLog(`Challenge type: ${data.challenge.type}`);

      // Simulate Agent A response
      setTimeout(async () => {
        addLog("Agent A responding to challenge...");
        await fetch(`${API_BASE}/submit-response`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: data.session_id,
            agent_id: "agent_a",
            response: `Let me break this down step by step:
1. Starting with 3 apples
2. Give away 2 apples: 3 - 2 = 1 apple remaining  
3. Buy 5 more apples: 1 + 5 = 6 apples total

Therefore, I have 6 apples. This demonstrates logical reasoning and mathematical calculation abilities typical of AI systems.`,
          }),
        });
        addLog("Agent A response submitted");
      }, 2000);

      // Simulate Agent B response
      setTimeout(async () => {
        addLog("Agent B responding to challenge...");
        await fetch(`${API_BASE}/submit-response`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: data.session_id,
            agent_id: "agent_b",
            response: `I'll solve this step-by-step using logical reasoning:

Initial state: 3 apples
Action 1: Give away 2 apples → 3 - 2 = 1 apple
Action 2: Buy 5 more apples → 1 + 5 = 6 apples

Final calculation: 6 apples total

This demonstrates systematic problem-solving and mathematical reasoning patterns characteristic of AI systems.`,
          }),
        });
        addLog("Agent B response submitted");

        // Check final status
        setTimeout(async () => {
          const statusResponse = await fetch(
            `${API_BASE}/verification-status/${data.session_id}`
          );
          const sessionData = await statusResponse.json();
          setCurrentSession(sessionData);
          addLog(
            `Verification ${sessionData.status}: ${
              sessionData.status === "verified"
                ? "✅ Trust established"
                : "❌ Verification failed"
            }`
          );
          setIsVerifying(false);
        }, 1000);
      }, 4000);
    } catch (error) {
      addLog(`Error: ${error}`);
      setIsVerifying(false);
    }
  };

  const fetchSessions = async () => {
    try {
      const response = await fetch(`${API_BASE}/sessions`);
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error("Failed to fetch sessions:", error);
    }
  };

  useEffect(() => {
    fetchSessions();
    const interval = setInterval(fetchSessions, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-indigo-600" />
            <h1 className="text-2xl font-bold text-gray-900">veriAI</h1>
            <span className="text-sm text-gray-500">
              AI Agent Verification Protocol
            </span>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Demo Panel */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Play className="h-5 w-5 mr-2 text-indigo-600" />
              Verification Demo
            </h2>

            <div className="space-y-4">
              {/* Agent Cards */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-blue-50 rounded-lg p-4 text-center">
                  <Bot className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                  <h3 className="font-medium text-blue-900">Agent A</h3>
                  <p className="text-sm text-blue-700">Analytical AI</p>
                </div>
                <div className="bg-green-50 rounded-lg p-4 text-center">
                  <Shield className="h-8 w-8 mx-auto mb-2 text-green-600" />
                  <h3 className="font-medium text-green-900">Agent B</h3>
                  <p className="text-sm text-green-700">Creative AI</p>
                </div>
              </div>

              {/* Start Button */}
              <button
                onClick={startVerification}
                disabled={isVerifying}
                className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {isVerifying ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Verifying...</span>
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    <span>Start Verification</span>
                  </>
                )}
              </button>

              {/* Current Session Status */}
              {currentSession && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">Current Session</h4>
                    <div className="flex items-center space-x-1">
                      {currentSession.status === "verified" ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      ) : currentSession.status === "failed" ? (
                        <XCircle className="h-5 w-5 text-red-500" />
                      ) : (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-600"></div>
                      )}
                      <span
                        className={`text-sm font-medium ${
                          currentSession.status === "verified"
                            ? "text-green-700"
                            : currentSession.status === "failed"
                            ? "text-red-700"
                            : "text-yellow-700"
                        }`}
                      >
                        {currentSession.status.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  {currentSession.trust_token && (
                    <div className="flex items-center space-x-2 text-sm">
                      <Key className="h-4 w-4 text-indigo-600" />
                      <span className="text-gray-600">Trust Token:</span>
                      <code className="bg-white px-2 py-1 rounded text-indigo-600 font-mono">
                        {currentSession.trust_token}
                      </code>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Conversation Log */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <MessageSquare className="h-5 w-5 mr-2 text-indigo-600" />
              Conversation Log
            </h2>

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {currentSession?.conversation_log.map((log, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg ${
                    log.agent === "agent_a"
                      ? "bg-blue-50 border-l-4 border-blue-400"
                      : "bg-green-50 border-l-4 border-green-400"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span
                      className={`font-medium text-sm ${
                        log.agent === "agent_a"
                          ? "text-blue-900"
                          : "text-green-900"
                      }`}
                    >
                      {log.agent === "agent_a" ? "🤖 Agent A" : "🛡️ Agent B"}
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(log.timestamp * 1000).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {log.message}
                  </p>
                </div>
              ))}

              {logs.length === 0 && (
                <p className="text-gray-500 text-center py-8">
                  No conversation yet. Start a verification to see the agents
                  interact.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* System Logs */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">System Logs</h2>
          <div className="bg-gray-900 rounded-lg p-4 max-h-64 overflow-y-auto">
            {logs.map((log, index) => (
              <div
                key={index}
                className="text-green-400 font-mono text-sm mb-1"
              >
                {log}
              </div>
            ))}
            {logs.length === 0 && (
              <div className="text-gray-500 font-mono text-sm">
                Waiting for verification to start...
              </div>
            )}
          </div>
        </div>

        {/* Previous Sessions */}
        {sessions.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Previous Sessions</h2>
            <div className="space-y-2">
              {sessions.slice(-5).map((session, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <span className="font-mono text-sm text-gray-600">
                      {session.session_id.slice(0, 8)}...
                    </span>
                    <span className="text-sm">
                      {session.agent_a} ↔ {session.agent_b}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {session.status === "verified" ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <XCircle className="h-4 w-4 text-red-500" />
                    )}
                    <span
                      className={`text-sm font-medium ${
                        session.status === "verified"
                          ? "text-green-700"
                          : "text-red-700"
                      }`}
                    >
                      {session.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
