import React, { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';
import { generateSessionId } from '../utils';

const WS_URL = import.meta.env.DEV
  ? `ws://localhost:8000/ws`
  : `ws://${window.location.host}/ws`;

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => generateSessionId());
  const [messages, setMessages] = useState([]);
  const [activeToolCalls, setActiveToolCalls] = useState(new Map());
  const [activeLlmThinking, setActiveLlmThinking] = useState(new Map());
  const [isConnected, setIsConnected] = useState(false);
  const [isAgentReady, setIsAgentReady] = useState(false);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);

  // Refs mirror state for use inside WebSocket callbacks (avoids stale closures)
  const isWaitingRef = useRef(false);
  const isAgentReadyRef = useRef(false);
  const sessionIdRef = useRef(sessionId);
  const socketRef = useRef(null);

  const setWaiting = useCallback((val) => {
    isWaitingRef.current = val;
    setIsWaitingForResponse(val);
  }, []);

  const setAgentReady = useCallback((val) => {
    isAgentReadyRef.current = val;
    setIsAgentReady(val);
  }, []);

  const connect = useCallback((sid) => {
    const wsUrl = `${WS_URL}/${sid}`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;
    let agentReadyFallback;

    socket.onopen = () => {
      setIsConnected(true);
      agentReadyFallback = setTimeout(() => setAgentReady(true), 10000);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'response') {
        setWaiting(false);
        setActiveToolCalls(new Map());
        setActiveLlmThinking(new Map());
        setMessages(msgs => msgs.map(m =>
          (m.type === 'llm_thinking' && m.status === 'started') ? { ...m, status: 'completed' } : m
        ));
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setMessages(prev => [...prev, {
          id: Date.now() + Math.random(), type: 'message', text: data.text, role: 'assistant', time,
        }]);
      } else if (data.type === 'tool_call') {
        const argsSummary = data.args_summary || '';
        const toolName = data.tool_name;
        if (data.status === 'started') {
          const id = Date.now() + Math.random();
          setMessages(prev => [...prev, {
            id, type: 'tool_call', toolName, argsSummary,
            status: 'started', durationMs: null, resultPreview: null,
          }]);
          setActiveToolCalls(prev => { const n = new Map(prev); n.set(toolName, id); return n; });
        } else {
          setActiveToolCalls(prev => {
            const id = prev.get(toolName);
            if (id) {
              setMessages(msgs => msgs.map(m => m.id === id
                ? { ...m, status: data.status, durationMs: data.duration_ms, resultPreview: data.result_preview }
                : m));
              const n = new Map(prev); n.delete(toolName); return n;
            }
            return prev;
          });
        }
      } else if (data.type === 'llm_thinking') {
        const iteration = data.iteration || 1;
        if (data.status === 'started') {
          const id = Date.now() + Math.random();
          setMessages(prev => [...prev, {
            id, type: 'llm_thinking', iteration, status: 'started', startMs: Date.now(), durationMs: null,
          }]);
          setActiveLlmThinking(prev => { const n = new Map(prev); n.set(iteration, id); return n; });
        } else {
          setActiveLlmThinking(prev => {
            const id = prev.get(iteration);
            if (id) {
              setMessages(msgs => msgs.map(m => m.id === id
                ? { ...m, status: 'completed', durationMs: data.duration_ms }
                : m));
              const n = new Map(prev); n.delete(iteration); return n;
            }
            return prev;
          });
        }
      } else if (data.type === 'task_notification') {
        const label = data.task_name ? `[Scheduled: ${data.task_name}] ` : '[Scheduled Task] ';
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setMessages(prev => [...prev, {
          id: Date.now() + Math.random(), type: 'message', text: label + data.text, role: 'assistant', time,
        }]);
      } else if (data.type === 'agent_ready') {
        clearTimeout(agentReadyFallback);
        setAgentReady(true);
      }
    };

    socket.onclose = () => {
      clearTimeout(agentReadyFallback);
      setIsConnected(false);
      setAgentReady(false);
      setActiveLlmThinking(new Map());
      // Auto-reconnect with current session ID
      setTimeout(() => {
        if (socketRef.current === socket) {
          connect(sessionIdRef.current);
        }
      }, 3000);
    };
  }, [setMessages, setActiveToolCalls, setActiveLlmThinking, setWaiting, setAgentReady]);

  useEffect(() => { sessionIdRef.current = sessionId; }, [sessionId]);

  // Connect once on app mount — stays alive across page navigation
  useEffect(() => {
    connect(sessionId);
    return () => {
      if (socketRef.current) {
        socketRef.current.onclose = null;
        socketRef.current.close();
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Reads refs — never stale, no deps needed
  const sendMessage = useCallback((text) => {
    if (!text || !socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return false;
    if (!isAgentReadyRef.current || isWaitingRef.current) return false;
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages(prev => [...prev, {
      id: Date.now() + Math.random(), type: 'message', text, role: 'user', time,
    }]);
    socketRef.current.send(JSON.stringify({ type: 'message', text }));
    setWaiting(true);
    return true;
  }, [setMessages, setWaiting]);

  const clearSession = useCallback(() => {
    const sid = generateSessionId();
    sessionIdRef.current = sid;
    setSessionId(sid);
    setMessages([]);
    setActiveToolCalls(new Map());
    setActiveLlmThinking(new Map());
    setWaiting(false);
    setAgentReady(false);
    if (socketRef.current) {
      socketRef.current.onclose = null;
      socketRef.current.close();
    }
    connect(sid);
  }, [connect, setWaiting, setAgentReady]);

  return (
    <ChatContext.Provider value={{
      sessionId,
      messages,
      activeToolCalls,
      activeLlmThinking,
      isConnected,
      isAgentReady,
      isWaitingForResponse,
      sendMessage,
      clearSession,
    }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error('useChatContext must be used inside ChatProvider');
  return ctx;
}
