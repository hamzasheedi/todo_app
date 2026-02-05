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

  // Don't render anything during initial loading to prevent hydration mismatch
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16]">
        <p className="text-gray-400">Loading...</p>
      </div>
    );
  }

  if (!user || !user.id) {  // User is not authenticated if no user or no user ID
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16]">
        <p className="text-gray-400">Please log in to access the chat</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-bg-primary via-bg-secondary to-bg-tertiary text-text-primary pt-8 pb-24 flex flex-col">
      <div className="w-full px-4 sm:px-6 lg:px-8 flex-1 flex flex-col">
        <div className="space-y-6 flex-1 flex flex-col max-w-4xl mx-auto w-full">
          {/* Page Header */}
          <div className="text-center">
            <h1 className="text-3xl font-bold text-text-primary mb-2">AI Todo Assistant</h1>
            <p className="text-text-secondary text-sm">Manage your tasks with natural language</p>
            <div className="w-16 h-0.5 bg-brand-gradient mx-auto mt-4 opacity-50"></div>
          </div>

          {/* Chat Interface - Full width container */}
          <div className="bg-bg-card bg-opacity-60 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 shadow-2xl shadow-[rgba(0,245,255,0.05)] flex-1 flex flex-col w-full">
            <ChatKitWrapper
              conversationId={conversationId}
              onConversationChange={setConversationId}
            />
          </div>
        </div>
      </div>
    </div>
  );
}