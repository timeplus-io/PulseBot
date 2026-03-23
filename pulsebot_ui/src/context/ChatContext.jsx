import React, { createContext, useContext, useState, useEffect, useRef, useCallback } from 'react';
import { generateSessionId } from '../utils';

const WS_URL = import.meta.env.DEV
  ? `ws://localhost:8000/ws`
  : `ws://${window.location.host}/ws`;

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => generateSessionId());
  const [isConnected, setIsConnected] = useState(false);
  const [isAgentReady, setIsAgentReady] = useState(false);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const [messages, setMessages] = useState([]);
  const [activeToolCalls, setActiveToolCalls] = useState(new Map());
  const [activeLlmThinking, setActiveLlmThinking] = useState(new Map());
  const [toast, setToast] = useState({ visible: false, message: '', isError: false });

  const socketRef = useRef(null);
  // Keep a ref so reconnect closure always sees the current session ID
  const sessionIdRef = useRef(sessionId);

  const showToast = useCallback((message, isError = false) => {
    setToast({ visible: true, message, isError });
    setTimeout(() => setToast(prev => ({ ...prev, visible: false })), 3000);
  }, []);

  const addMessage = useCallback((text, role) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages(prev => [...prev, {
      id: Date.now() + Math.random(),
      type: 'message',
      text,
      role,
      time,
    }]);
  }, []);

  const removeToolCallIndicators = useCallback(() => {
    setActiveToolCalls(new Map());
    setActiveLlmThinking(new Map());
    setMessages(msgs => msgs.map(m =>
      (m.type === 'llm_thinking' && m.status === 'started') ? { ...m, status: 'completed' } : m
    ));
  }, []);

  const handleToolCall = useCallback((data) => {
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
  }, []);

  const handleLlmThinking = useCallback((data) => {
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
  }, []);

  const connect = useCallback((sid) => {
    // Close any existing socket without triggering the reconnect logic
    if (socketRef.current) {
      const old = socketRef.current;
      old.onclose = null;
      old.close();
    }

    const socket = new WebSocket(`${WS_URL}/${sid}`);
    socketRef.current = socket;
    let agentReadyFallback;

    socket.onopen = () => {
      setIsConnected(true);
      agentReadyFallback = setTimeout(() => setIsAgentReady(true), 10000);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'response') {
        setIsWaitingForResponse(false);
        removeToolCallIndicators();
        addMessage(data.text, 'assistant');
      } else if (data.type === 'tool_call') {
        handleToolCall(data);
      } else if (data.type === 'llm_thinking') {
        handleLlmThinking(data);
      } else if (data.type === 'task_notification') {
        const label = data.task_name ? `[Scheduled: ${data.task_name}] ` : '[Scheduled Task] ';
        addMessage(label + data.text, 'assistant');
      } else if (data.type === 'agent_ready') {
        clearTimeout(agentReadyFallback);
        setIsAgentReady(true);
      }
    };

    socket.onclose = () => {
      clearTimeout(agentReadyFallback);
      setIsConnected(false);
      setIsAgentReady(false);
      setActiveLlmThinking(new Map());
      // Reconnect with the same session ID (from ref, always current)
      setTimeout(() => {
        if (socketRef.current === socket) {
          connect(sessionIdRef.current);
        }
      }, 3000);
    };

    socket.onerror = () => {
      showToast('Connection error. Retrying...', true);
    };
  }, [addMessage, removeToolCallIndicators, handleToolCall, handleLlmThinking, showToast]);

  // Initial connection
  useEffect(() => {
    connect(sessionId);
    return () => {
      if (socketRef.current) {
        socketRef.current.onclose = null;
        socketRef.current.close();
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const sendMessage = useCallback((text) => {
    if (!text || !isConnected || !isAgentReady || isWaitingForResponse) return false;
    addMessage(text, 'user');
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'message', text }));
    }
    setIsWaitingForResponse(true);
    return true;
  }, [isConnected, isAgentReady, isWaitingForResponse, addMessage]);

  const newSession = useCallback(() => {
    const sid = generateSessionId();
    sessionIdRef.current = sid;
    setSessionId(sid);
    setMessages([]);
    setIsWaitingForResponse(false);
    setActiveToolCalls(new Map());
    setActiveLlmThinking(new Map());
    setIsAgentReady(false);
    connect(sid);
  }, [connect]);

  return (
    <ChatContext.Provider value={{
      sessionId,
      isConnected,
      isAgentReady,
      isWaitingForResponse,
      messages,
      activeToolCalls,
      activeLlmThinking,
      toast,
      sendMessage,
      newSession,
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
