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
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user } = useAuth();

  // Determine if user is authenticated
  const isAuthenticated = !!(user && user.id);

  // Fetch conversation history if conversationId exists
  useEffect(() => {
    if (conversationId && isAuthenticated) {
      fetchConversationHistory(conversationId);
    }
  }, [conversationId, isAuthenticated]);

  const fetchConversationHistory = async (id: string) => {
    try {
      const response = await apiClient.get(`/api/v1/conversations/${id}`);
      const data = response.data;

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
      // Start with empty messages if there's an error
      setMessages([]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
      // Call the backend API - use the v1 API endpoint
      const response = await apiClient.post('/api/v1/chat/', {
        message: input,
        conversation_id: conversationId || undefined
      });

      const { response: botResponse, conversation_id: newConversationId } = response.data;

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
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md border">
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[calc(100vh-250px)]">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Welcome to AI Todo Assistant!</h3>
            <p className="text-gray-500 max-w-md">
              I can help you manage your tasks with natural language. Try saying things like:
            </p>
            <ul className="mt-3 text-left text-gray-500 list-disc list-inside space-y-1 max-w-md">
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
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[80%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Example: "Add a task to buy groceries", "Show me my tasks", "Complete task X"
        </p>
      </form>
    </div>
  );
}