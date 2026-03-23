import React, { createContext, useContext, useState, useCallback } from 'react';
import { generateSessionId } from '../utils';

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => generateSessionId());
  const [messages, setMessages] = useState([]);
  const [activeToolCalls, setActiveToolCalls] = useState(new Map());
  const [activeLlmThinking, setActiveLlmThinking] = useState(new Map());

  // Returns the new session ID so Chat.jsx can reconnect to it
  const clearSession = useCallback(() => {
    const sid = generateSessionId();
    setSessionId(sid);
    setMessages([]);
    setActiveToolCalls(new Map());
    setActiveLlmThinking(new Map());
    return sid;
  }, []);

  return (
    <ChatContext.Provider value={{
      sessionId,
      messages,
      setMessages,
      activeToolCalls,
      setActiveToolCalls,
      activeLlmThinking,
      setActiveLlmThinking,
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
