import React, { useState, useEffect, useRef } from 'react';
import { formatMessage } from '../utils';
import { useChatContext } from '../context/ChatContext';

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
  const {
    messages,
    isConnected,
    isAgentReady,
    isWaitingForResponse,
    sendMessage: ctxSendMessage,
    clearSession,
  } = useChatContext();

  const [inputValue, setInputValue] = useState('');

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isWaitingForResponse]);

  const sendMessage = () => {
    const text = inputValue.trim();
    if (!ctxSendMessage(text)) return;
    setInputValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const newSession = () => {
    clearSession();
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
      <header className="glass-header ambient-shadow flex justify-between items-center px-4 py-3 flex-shrink-0">
        <div className="flex items-center gap-2 text-xs text-secondary">
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-tertiary' : 'bg-surface-dim'}`}></span>
          <span>{isConnected ? (isAgentReady ? 'Agent ready' : 'Connecting...') : 'Disconnected'}</span>
        </div>
        <button
          onClick={newSession}
          title="New Session"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-secondary hover:bg-surface-container-high transition-colors duration-150"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
          </svg>
          New Session
        </button>
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
                } else if (item.type === 'system_error') {
                  return (
                    <div key={item.id} className="flex items-start gap-2.5 px-3.5 py-2.5 bg-red-50 border border-red-300 rounded text-[13px] text-red-800 animate-fade-in my-1 w-fit max-w-[80%]">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 shrink-0 mt-0.5 text-red-500">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                      </svg>
                      <span>{item.text}</span>
                    </div>
                  );
                } else if (item.type === 'system_info') {
                  return (
                    <div key={item.id} className="flex items-start gap-2.5 px-3.5 py-2.5 bg-green-50 border border-green-300 rounded text-[13px] text-green-800 animate-fade-in my-1 w-fit max-w-[80%]">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 shrink-0 mt-0.5 text-green-500">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span>{item.text}</span>
                    </div>
                  );
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

    </div>
  );
}
