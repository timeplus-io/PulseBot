import React, { useState, useEffect, useRef, useCallback } from 'react';
import { generateSessionId, formatMessage } from '../utils';

const WS_URL = import.meta.env.DEV
  ? `ws://localhost:8000/ws`
  : `ws://${window.location.host}/ws`;

const ThinkingIndicator = ({ think }) => {
  const [now, setNow] = useState(Date.now());
  const isStarted = think.status === 'started';

  useEffect(() => {
    if (!isStarted) return;
    const interval = setInterval(() => setNow(Date.now()), 100);
    return () => clearInterval(interval);
  }, [isStarted]);

  const elapsedS = isStarted
    ? ((now - think.startMs) / 1000).toFixed(1)
    : (think.durationMs ? (think.durationMs / 1000).toFixed(1) : ((Date.now() - think.startMs) / 1000).toFixed(1));

  return (
    <div className={`flex flex-col items-start p-2 px-3.5 border border-gray-200 rounded text-[13px] my-1 w-fit max-w-[80%] ${isStarted ? 'animate-shimmer' : 'bg-gray-50 opacity-75'}`}>
      <div className={`flex items-start gap-2.5 w-full ${isStarted ? 'text-gray-600' : 'text-gray-500'}`}>
        <svg className={`shrink-0 w-[18px] h-[18px] ${isStarted ? 'animate-spin cursor-wait' : ''}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.346.346a.5.5 0 01-.16.113l-.342.15a.5.5 0 01-.195.04H9.5a.5.5 0 01-.195-.04l-.342-.15a.5.5 0 01-.16-.113l-.346-.346z" />
        </svg>
        <div className="flex flex-col flex-1 font-medium font-sans">
          <span>Thinking</span>
        </div>
        <span className="text-xs whitespace-nowrap ml-auto text-gray-500">
          {isStarted ? `${elapsedS}s...` : `${elapsedS}s`}
        </span>
      </div>
    </div>
  );
};

export default function Chat() {
  const [isConnected, setIsConnected] = useState(false);
  const [isAgentReady, setIsAgentReady] = useState(false);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const [messages, setMessages] = useState([]);
  const [activeToolCalls, setActiveToolCalls] = useState(new Map());
  const [activeLlmThinking, setActiveLlmThinking] = useState(new Map());
  const [inputValue, setInputValue] = useState('');
  const [toast, setToast] = useState({ visible: false, message: '', isError: false });

  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const sessionIdRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, activeToolCalls, activeLlmThinking, isWaitingForResponse]);

  const showToast = useCallback((message, isError = false) => {
    setToast({ visible: true, message, isError });
    setTimeout(() => {
      setToast(prev => ({ ...prev, visible: false }));
    }, 3000);
  }, []);

  const connect = useCallback(() => {
    const sessionId = generateSessionId();
    sessionIdRef.current = sessionId;
    const wsUrl = `${WS_URL}/${sessionId}`;

    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      setIsConnected(true);
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
        setIsAgentReady(true);
      }
    };

    socket.onclose = () => {
      setIsConnected(false);
      setIsAgentReady(false);
      setActiveLlmThinking(new Map());
      setTimeout(connect, 3000);
    };

    socket.onerror = () => {
      showToast('Connection error. Retrying...', true);
    };
  }, [showToast]);

  useEffect(() => {
    connect();
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [connect]);

  const addMessage = (text, role) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages(prev => [...prev, {
      id: Date.now() + Math.random(),
      type: 'message',
      text,
      role,
      time,
    }]);
  };

  const handleToolCall = (data) => {
    const argsSummary = data.args_summary || '';
    const toolName = data.tool_name;

    if (data.status === 'started') {
      const id = Date.now() + Math.random();
      setMessages(prev => [...prev, {
        id, type: 'tool_call', toolName, argsSummary,
        status: 'started', durationMs: null, resultPreview: null,
      }]);
      setActiveToolCalls(prev => {
        const next = new Map(prev);
        next.set(toolName, id);
        return next;
      });
    } else {
      setActiveToolCalls(prev => {
        const id = prev.get(toolName);
        if (id) {
          setMessages(msgs => msgs.map(m => m.id === id ? {
            ...m, status: data.status, durationMs: data.duration_ms, resultPreview: data.result_preview,
          } : m));
          const next = new Map(prev);
          next.delete(toolName);
          return next;
        }
        return prev;
      });
    }
  };

  const handleLlmThinking = (data) => {
    const iteration = data.iteration || 1;
    if (data.status === 'started') {
      const id = Date.now() + Math.random();
      setMessages(prev => [...prev, {
        id, type: 'llm_thinking', iteration, status: 'started', startMs: Date.now(), durationMs: null,
      }]);
      setActiveLlmThinking(prev => {
        const next = new Map(prev);
        next.set(iteration, id);
        return next;
      });
    } else {
      setActiveLlmThinking(prev => {
        const id = prev.get(iteration);
        if (id) {
          setMessages(msgs => msgs.map(m => m.id === id ? {
            ...m, status: 'completed', durationMs: data.duration_ms,
          } : m));
          const next = new Map(prev);
          next.delete(iteration);
          return next;
        }
        return prev;
      });
    }
  };

  const removeToolCallIndicators = () => {
    setActiveToolCalls(new Map());
    setActiveLlmThinking(new Map());
    setMessages(msgs => msgs.map(m =>
      (m.type === 'llm_thinking' && m.status === 'started') ? { ...m, status: 'completed' } : m
    ));
  };

  const sendMessage = () => {
    const text = inputValue.trim();
    if (!text || !isConnected || !isAgentReady || isWaitingForResponse) return;

    addMessage(text, 'user');
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'message', text }));
    }
    setInputValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    setIsWaitingForResponse(true);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  const isSendDisabled = !inputValue.trim() || !isConnected || !isAgentReady || isWaitingForResponse;

  return (
    <div className="flex flex-col h-full bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">Chat</h1>
        <div className="ml-auto flex items-center gap-2 text-xs text-gray-600">
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-tertiary' : 'bg-surface-dim'}`}></span>
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-[900px] w-full mx-auto p-6 gap-4 overflow-hidden">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2 messages-scroll pb-4">
          {messages.length === 0 && !isWaitingForResponse ? (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-600 text-center p-10">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-8 h-8 text-gray-500">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h2 className="text-base font-semibold text-gray-900 mb-2">Start a conversation</h2>
              <p>Send a message to begin chatting with PulseBot</p>
            </div>
          ) : (
            <>
              {messages.map((item) => {
                if (item.type === 'message') {
                  return (
                    <div key={item.id} className={`flex gap-3 animate-fade-in ${item.role === 'user' ? 'flex-row-reverse' : ''}`}>
                      <div className={`w-8 h-8 rounded shrink-0 flex items-center justify-center text-xs font-semibold text-white ${item.role === 'assistant' ? 'bg-pink-500' : 'bg-gray-700'}`}>
                        {item.role === 'assistant' ? 'P' : 'U'}
                      </div>
                      <div className="w-fit max-w-[70%]">
                        <div
                          className={`border rounded px-4 py-3 break-words markdown-body ${item.role === 'user' ? 'bg-gray-800 text-white border-gray-800 markdown-user' : 'bg-white border-gray-200'} text-[14px]`}
                          dangerouslySetInnerHTML={{ __html: formatMessage(item.text) }}
                        />
                        <div className={`text-[11px] text-gray-500 mt-1 ${item.role === 'user' ? 'text-right' : ''}`}>
                          {item.time}
                        </div>
                      </div>
                    </div>
                  );
                } else if (item.type === 'tool_call') {
                  const isSuccess = item.status === 'success';
                  const isStarted = item.status === 'started';
                  const hasDetails = item.resultPreview && (item.resultPreview.length > 50 || item.resultPreview.includes('\n') || !isSuccess);

                  let wrapperClass = 'flex flex-col items-start p-2 px-3.5 bg-gray-100 border border-gray-200 rounded text-[13px] text-gray-700 animate-fade-in my-1 w-fit max-w-[80%]';
                  if (isStarted) wrapperClass = 'flex flex-col items-start p-2 px-3.5 border border-gray-200 rounded text-[13px] text-gray-700 animate-shimmer my-1 w-fit max-w-[80%]';
                  if (isSuccess) wrapperClass = 'flex flex-col items-start p-2 px-3.5 bg-[#E6FFFA] border border-[#38B2AC] text-[#234E52] animate-fade-in my-1 w-fit max-w-[80%] rounded';
                  if (!isStarted && !isSuccess) wrapperClass = 'flex flex-col items-start p-2 px-3.5 bg-[#FED7D7] border border-error-primary text-error-hover animate-fade-in my-1 w-fit max-w-[80%] rounded';

                  return (
                    <div key={item.id} className={wrapperClass}>
                      <div className="flex items-start gap-2.5 w-full">
                        <svg className={`shrink-0 w-[18px] h-[18px] ${isStarted ? 'animate-spin' : ''}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          {isStarted ? (
                            <>
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            </>
                          ) : isSuccess ? (
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                          ) : (
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                          )}
                        </svg>
                        <div className="flex flex-col flex-1">
                          <div>
                            <span className="font-mono font-medium">{item.toolName}</span>
                            {item.argsSummary && (
                              <span className={`font-mono text-xs ml-1 whitespace-pre-wrap ${isSuccess ? 'text-[#276749]' : 'text-gray-600'}`}>
                                {item.argsSummary}
                              </span>
                            )}
                          </div>
                        </div>
                        <span className={`text-xs whitespace-nowrap ml-auto ${isSuccess ? 'text-[#38B2AC]' : 'text-gray-500'}`}>
                          {isStarted ? 'running...' : isSuccess ? `${item.durationMs}ms` : 'failed'}
                        </span>
                      </div>
                      {hasDetails && (
                        <div className={`mt-2 pt-2 border-t border-dashed w-full font-mono text-[11px] p-2 rounded whitespace-pre-wrap overflow-x-auto max-h-[300px] overflow-y-auto ${!isSuccess ? 'border-[#FEB2B2] bg-white/50 text-[#9B2C2C]' : 'border-[#A0AEC0] bg-white/50 text-[#2D3748]'}`}>
                          {item.resultPreview}
                        </div>
                      )}
                    </div>
                  );
                } else if (item.type === 'llm_thinking') {
                  return <ThinkingIndicator key={item.id} think={item} />;
                }
                return null;
              })}
            </>
          )}

          {isWaitingForResponse && (
            <div className="flex items-center gap-3 py-2">
              <div className="w-8 h-8 rounded shrink-0 flex items-center justify-center text-xs font-semibold text-white bg-pink-500">P</div>
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full typing-dot"></span>
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full typing-dot"></span>
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full typing-dot"></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border border-gray-200 rounded p-[12px] flex gap-[12px] items-end focus-within:border-pink-primary focus-within:ring-[2px] focus-within:ring-pink-light transition-all">
          <textarea
            ref={textareaRef}
            className="flex-1 bg-transparent border-none outline-none font-sans text-[14px] leading-[1.5] resize-none min-h-[24px] max-h-[120px] placeholder:text-gray-500"
            placeholder={!isConnected ? 'Connecting...' : !isAgentReady ? 'Waiting for agent...' : 'Type a message...'}
            rows="1"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <button
            className="h-8 px-4 bg-pink-primary hover:bg-pink-hover text-white border-none rounded text-[14px] font-medium cursor-pointer transition-colors flex items-center gap-[6px] disabled:bg-gray-400 disabled:cursor-not-allowed shrink-0"
            disabled={isSendDisabled}
            onClick={sendMessage}
          >
            <span>Send</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>

      {/* Toast */}
      <div className={`fixed bottom-6 left-1/2 -translate-x-1/2 px-5 py-3 rounded text-sm text-white shadow-lg transition-all duration-300 z-50 ${toast.visible ? 'translate-y-0 opacity-100' : 'translate-y-[100px] opacity-0'} ${toast.isError ? 'bg-obs-error' : 'bg-on-surface'}`}>
        {toast.message}
      </div>
    </div>
  );
}
