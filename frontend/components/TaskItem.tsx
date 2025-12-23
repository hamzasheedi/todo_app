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

type TaskItemProps = {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;
  backendUserId?: string; // Backend user ID to use in API calls
};

export default function TaskItem({ task, onTaskUpdated, onTaskDeleted, backendUserId }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [status, setStatus] = useState<'complete' | 'incomplete'>(task.status as 'complete' | 'incomplete');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!backendUserId) return;

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.put(`/${backendUserId}/tasks/${task.id}`, {
        title,
        description: description || null,
        status
      });

      onTaskUpdated(response);
      setIsEditing(false);
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!backendUserId) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await apiClient.delete(`/${backendUserId}/tasks/${task.id}`);
        onTaskDeleted(task.id);
      } catch (err) {
        console.error('Error deleting task:', err);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const toggleStatus = async () => {
    if (!backendUserId) return;

    try {
      const newStatus = status === 'complete' ? 'incomplete' : 'complete';
      const response = await apiClient.patch(`/${backendUserId}/tasks/${task.id}/complete`, {
        status: newStatus
      });

      setStatus(newStatus);
      onTaskUpdated({ ...task, status: newStatus });
    } catch (err) {
      console.error('Error updating task status:', err);
      alert('Failed to update task status. Please try again.');
    }
  };

  return (
    <div className={`flex items-start space-x-3 group ${status === 'complete' ? 'opacity-70' : ''}`}>
      <input
        type="checkbox"
        checked={status === 'complete'}
        onChange={toggleStatus}
        className={`mt-1 h-5 w-5 rounded focus:ring-0 cursor-pointer ${
          status === 'complete'
            ? 'bg-[#39FF14] border-[#39FF14] text-[#39FF14]'
            : 'bg-[#1a1f33] border-[#AAB0C0] text-[#00F5FF]'
        }`}
      />
      <div className="flex-1 min-w-0">
        {isEditing ? (
          <form onSubmit={handleUpdate} className="space-y-3">
            {error && (
              <div className="rounded-md bg-red-500/20 p-2 border border-red-500/30">
                <div className="text-xs text-red-300">{error}</div>
              </div>
            )}
            <div>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-2 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
                maxLength={200}
                required
              />
            </div>
            <div>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={2}
                className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-2 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
                maxLength={1000}
              />
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as 'complete' | 'incomplete')}
                className="bg-[#0B0F1A] border border-gray-600 rounded-lg px-2 py-1 text-sm text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
              >
                <option value="incomplete">Active</option>
                <option value="complete">Completed</option>
              </select>
              <button
                type="submit"
                disabled={loading}
                className="text-sm bg-[#00F5FF] text-[#0B0F1A] px-3 py-1 rounded-lg hover:bg-[#00F5FF]/90 disabled:opacity-50 font-medium"
              >
                {loading ? 'Saving...' : 'Save'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsEditing(false);
                  setTitle(task.title);
                  setDescription(task.description || '');
                  setStatus(task.status as 'complete' | 'incomplete');
                  setError('');
                }}
                className="text-sm text-[#AAB0C0] px-3 py-1 rounded-lg border border-gray-600 hover:text-[#F5F7FA] hover:border-[#00F5FF]"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div>
            <h3 className={`font-medium ${status === 'complete' ? 'line-through text-[#AAB0C0]' : 'text-[#F5F7FA]'}`}>
              {title}
            </h3>
            {description && (
              <p className={`mt-1 text-sm ${status === 'complete' ? 'text-[#5a6170]' : 'text-[#AAB0C0]'}`}>
                {description}
              </p>
            )}
            <p className="mt-2 text-xs text-[#5a6170]">
              Created: {new Date(task.created_date).toLocaleDateString()}
              {task.updated_date !== task.created_date && (
                <span>, Updated: {new Date(task.updated_date).toLocaleDateString()}</span>
              )}
            </p>
          </div>
        )}
      </div>
      {!isEditing && (
        <div className="flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => setIsEditing(true)}
            className="text-sm text-[#00F5FF] hover:text-[#00F5FF]/80 hover:underline"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="text-sm text-[#B026FF] hover:text-[#B026FF]/80 hover:underline"
          >
            Delete
          </button>
        </div>
      )}
    </div>
  );
}