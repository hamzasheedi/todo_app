'use client';

import { useState } from 'react';
import { useAuth } from './AuthWrapper';
import { apiClient } from '@/lib/api-client';

// Define the Task type based on the backend schema
type Task = {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: 'complete' | 'incomplete';
  created_date: string;
  updated_date: string;
};

type TaskFormProps = {
  onTaskCreated: (task: Task) => void;
  backendUserId?: string; // Backend user ID to use in API calls
};

export default function TaskForm({ onTaskCreated, backendUserId }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (!backendUserId) {
      setError('You must be logged in to create a task');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post(`/${backendUserId}/tasks`, {
        title,
        description: description || null,
        status: 'incomplete'
      });

      onTaskCreated(response);
      setTitle('');
      setDescription('');
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-[#F5F7FA] mb-4 flex items-center">
        <span className="w-2 h-2 bg-[#00F5FF] rounded-full mr-2"></span>
        Add New Task
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-md bg-red-500/20 p-3 border border-red-500/30">
            <div className="text-sm text-red-300">{error}</div>
          </div>
        )}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-[#AAB0C0] mb-2">
            Task Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-2 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
            placeholder="What needs to be done?"
            maxLength={200}
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-[#AAB0C0] mb-2">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-2 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
            placeholder="Add details (optional)"
            maxLength={1000}
          />
        </div>
        <div>
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-[#0B0F1A] bg-[#00F5FF] hover:bg-[#00F5FF]/90 focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Add Task'}
          </button>
        </div>
      </form>
    </div>
  );
}