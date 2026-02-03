'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { apiClient } from '@/lib/api-client';
import { ChatKitWrapper } from '@/components/ChatInterface/ChatKitWrapper';

export default function ChatPage() {
  const { user, loading } = useAuth();
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Initialize with an existing conversation or create a new one
  useEffect(() => {
    if (user && user.id) {  // User is authenticated if user object exists with an ID
      // You could fetch the user's most recent conversation here
      // For now, we'll start with a new conversation ID
      setConversationId(null);
    }
  }, [user]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!user || !user.id) {  // User is not authenticated if no user or no user ID
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Please log in to access the chat</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm py-4 px-6">
        <h1 className="text-xl font-semibold text-gray-800">AI Todo Assistant</h1>
        <p className="text-sm text-gray-600">Manage your tasks with natural language</p>
      </header>

      <main className="flex-1 overflow-hidden p-4">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          <ChatKitWrapper
            conversationId={conversationId}
            onConversationChange={setConversationId}
          />
        </div>
      </main>
    </div>
  );
}