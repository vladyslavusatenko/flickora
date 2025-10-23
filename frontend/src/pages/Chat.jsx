import { useState, useEffect, useRef } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useLocation } from 'react-router-dom';
import { chatAPI } from '../api/chat';
import { Send, Download, Trash2, RotateCw } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import '../styles/pages/Chat.css';

const Chat = () => {
  const location = useLocation();
  const [chatMessage, setChatMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesContainerRef = useRef(null);

  const quickSuggestions = [
    "Recommend a thriller",
    "Explain Inception",
    "Best 2023 movies"
  ];

  const sendMessageMutation = useMutation({
    mutationFn: (message) => chatAPI.sendMessage(message, null),
    onSuccess: (response) => {
      const aiMessage = {
        role: 'assistant',
        content: response.data.message,
        sources: response.data.sources,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      };
      setMessages(prev => [...prev, aiMessage]);
    },
    onError: (error) => {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        isError: true,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  });

  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, sendMessageMutation.isPending]);

  useEffect(() => {
    if (location.state?.initialQuestion) {
      const userMessage = {
        role: 'user',
        content: location.state.initialQuestion,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      };
      setMessages([userMessage]);
      sendMessageMutation.mutate(location.state.initialQuestion);
    }
  }, [location.state]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (chatMessage.trim() && !sendMessageMutation.isPending) {
      const userMessage = {
        role: 'user',
        content: chatMessage.trim(),
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      };
      setMessages(prev => [...prev, userMessage]);
      sendMessageMutation.mutate(chatMessage.trim());
      setChatMessage('');
    }
  };

  const handleQuickSuggestion = (suggestion) => {
    if (!sendMessageMutation.isPending) {
      const userMessage = {
        role: 'user',
        content: suggestion,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
      };
      setMessages(prev => [...prev, userMessage]);
      sendMessageMutation.mutate(suggestion);
    }
  };

  const handleClearHistory = () => {
    setMessages([]);
  };

  const handleExportChat = () => {
    const chatText = messages.map(m => `[${m.timestamp}] ${m.role}: ${m.content}`).join('\n\n');
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-export-${new Date().toISOString()}.txt`;
    a.click();
  };

  return (
    <div className="chat-page-global">
      <div className="chat-global-container">
        <div className="chat-global-header">
          <div className="chat-global-header-left">
            <h1 className="chat-global-title">Global Movie Chat</h1>
            <p className="chat-global-subtitle">Ask anything about movies, get instant AI responses</p>
          </div>
          <div className="chat-global-header-right">
            <div className="ai-status">
              <span className="status-dot"></span>
              AI Assistant Online
            </div>
            <button className="header-btn" onClick={handleExportChat} disabled={messages.length === 0}>
              <Download size={18} />
              Export Chat
            </button>
            <button className="header-btn" onClick={handleClearHistory} disabled={messages.length === 0}>
              <Trash2 size={18} />
              Clear History
            </button>
          </div>
        </div>

        <div className="chat-global-messages" ref={messagesContainerRef}>
          {messages.length === 0 && (
            <div className="chat-global-welcome">
              <div className="welcome-avatar">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
                </svg>
              </div>
              <h2>Hi! I'm your movie AI assistant. Ask me anything!</h2>
            </div>
          )}

          {messages.map((msg, index) => (
            <div key={index} className={`chat-global-message ${msg.role}-message-global`}>
              {msg.role === 'assistant' && (
                <div className="message-avatar">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 14s1.5 2 4 2 4-2 4-2"/>
                    <line x1="9" y1="9" x2="9.01" y2="9" strokeWidth="2" strokeLinecap="round"/>
                    <line x1="15" y1="9" x2="15.01" y2="9" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </div>
              )}
              <div className="message-content-wrapper">
                <div className={`message-bubble ${msg.isError ? 'error-bubble' : ''}`}>
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
                <span className="message-timestamp">{msg.timestamp}</span>
              </div>
            </div>
          ))}

          {sendMessageMutation.isPending && (
            <div className="chat-global-message assistant-message-global">
              <div className="message-avatar">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 14s1.5 2 4 2 4-2 4-2"/>
                  <line x1="9" y1="9" x2="9.01" y2="9" strokeWidth="2" strokeLinecap="round"/>
                  <line x1="15" y1="9" x2="15.01" y2="9" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </div>
              <div className="message-content-wrapper">
                <div className="message-bubble">
                  <div className="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="chat-global-footer">
          <div className="quick-suggestions">
            {quickSuggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-btn"
                onClick={() => handleQuickSuggestion(suggestion)}
                disabled={sendMessageMutation.isPending}
              >
                {suggestion}
              </button>
            ))}
            <button className="suggestion-btn refresh-btn" disabled={sendMessageMutation.isPending}>
              <RotateCw size={16} />
            </button>
          </div>

          <form onSubmit={handleSendMessage} className="chat-global-input-form">
            <input
              type="text"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="Ask about movies..."
              className="chat-global-input"
            />
            <button
              type="submit"
              className="chat-global-send-btn"
              disabled={!chatMessage.trim() || sendMessageMutation.isPending}
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;