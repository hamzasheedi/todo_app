'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { apiClient } from '@/lib/api-client';

interface ChatKitWrapperProps {
  conversationId: string | null;
  onConversationChange: (id: string) => void;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

export function ChatKitWrapper({ conversationId, onConversationChange }: ChatKitWrapperProps) {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConversationLoading, setIsConversationLoading] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user } = useAuth();

  // Determine if user is authenticated
  const isAuthenticated = !!(user && user.id);

  // Fetch conversation history if conversationId exists
  useEffect(() => {
    if (conversationId && isAuthenticated) {
      // Only fetch if we don't already have messages
      if (messages.length === 0) {
        fetchConversationHistory(conversationId).finally(() => {
          setIsConversationLoading(false);
        });
      } else {
        setIsConversationLoading(false);
      }
    } else {
      // If no conversation exists, still set loading to false
      setIsConversationLoading(false);
    }
  }, [conversationId, isAuthenticated, messages.length]);

  const fetchConversationHistory = async (id: string) => {
    try {
      const response = await apiClient.get(`/api/v1/conversations/${id}`);
      // The response is already parsed by apiClient.handleResponse
      const data = response;

      // Transform the conversation data to match our Message interface
      const chatMessages: Message[] = data.messages.map((msg: any) => ({
        id: msg.id,
        content: msg.content,
        role: msg.role,
        timestamp: msg.timestamp
      }));

      setMessages(chatMessages);
    } catch (error) {
      console.error('Error fetching conversation history:', error);
      // If it's a 404 error (conversation not found), start with empty messages
      // Otherwise, log the error but still start with empty messages
      setMessages([]);
    }
  };

  // Scroll to bottom once when component mounts to show input field
  useEffect(() => {
    // Wait for the component to render before scrolling
    const timer = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'auto' });
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  // Removed auto-scrolling to bottom on new messages - users can scroll manually

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call the backend API - use the correct API endpoint
      const response = await apiClient.post('/api/v1/chat/', {
        message: input,
        conversation_id: conversationId || undefined
      });

      // Handle the response based on its actual structure
      // The response should have the structure defined in ChatResponse
      const responseData = response; // apiClient.handleResponse already parses JSON

      // Extract the required fields from the response
      const botResponse = responseData.response;
      const newConversationId = responseData.conversation_id;

      // Update conversation ID if it's new
      if (newConversationId && !conversationId) {
        onConversationChange(newConversationId);
      }

      // Add bot response to the chat
      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        content: botResponse,
        role: 'assistant',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-bg-card bg-opacity-60 backdrop-blur-sm rounded-2xl border border-gray-700">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {isConversationLoading ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-text-secondary py-12">
            <div className="flex space-x-2 mb-4">
              <div className="w-3 h-3 bg-cyan-500 rounded-full animate-bounce"></div>
              <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce delay-100"></div>
              <div className="w-3 h-3 bg-emerald-500 rounded-full animate-bounce delay-200"></div>
            </div>
            <p>Loading your conversation...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-text-secondary">
            <h3 className="text-lg font-medium text-text-primary mb-2">Welcome to AI Todo Assistant!</h3>
            <p className="text-text-secondary max-w-md">
              I can help you manage your tasks with natural language. Try saying things like:
            </p>
            <ul className="mt-3 text-left text-text-secondary list-disc list-inside space-y-1 max-w-md">
              <li>"Add a task to buy groceries"</li>
              <li>"Show me my tasks"</li>
              <li>"Complete the project report task"</li>
              <li>"Update my shopping task"</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-brand-primary text-bg-primary'
                    : 'bg-bg-surface text-text-primary'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-bg-primary' : 'text-text-secondary'}`}>
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-bg-surface text-text-primary rounded-lg px-4 py-2 max-w-[80%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4 mt-auto">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 bg-bg-primary border border-gray-600 rounded-lg px-4 py-2 text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-opacity-50"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-brand-gradient text-white rounded-lg px-4 py-2 hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-opacity-50 disabled:opacity-50 transition-all duration-200"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-text-secondary mt-2">
          Example: "Add a task to buy groceries", "Show me my tasks", "Complete task X"
        </p>
      </form>
    </div>
  );
}