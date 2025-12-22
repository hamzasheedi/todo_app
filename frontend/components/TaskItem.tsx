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
      const response = await apiClient.put(`/api/${backendUserId}/tasks/${task.id}`, {
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
        await apiClient.delete(`/api/${backendUserId}/tasks/${task.id}`);
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
      const response = await apiClient.patch(`/api/${backendUserId}/tasks/${task.id}/complete`, {
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
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {isEditing ? (
        <form onSubmit={handleUpdate} className="space-y-3">
          {error && (
            <div className="rounded-md bg-red-50 p-2">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}
          <div>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              maxLength={200}
              required
            />
          </div>
          <div>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              className="w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              maxLength={1000}
            />
          </div>
          <div className="flex items-center space-x-4">
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value as 'complete' | 'incomplete')}
              className="border border-gray-300 rounded px-2 py-1 text-sm"
            >
              <option value="incomplete">Incomplete</option>
              <option value="complete">Complete</option>
            </select>
            <button
              type="submit"
              disabled={loading}
              className="text-sm bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700 disabled:opacity-50"
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
              className="text-sm text-gray-600 px-3 py-1 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div>
          <div className="flex justify-between items-start">
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                checked={status === 'complete'}
                onChange={toggleStatus}
                className="mt-1 h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500"
              />
              <div className="flex-1 min-w-0">
                <h3 className={`text-lg font-medium ${status === 'complete' ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {title}
                </h3>
                {description && (
                  <p className={`mt-1 text-sm ${status === 'complete' ? 'text-gray-400' : 'text-gray-600'}`}>
                    {description}
                  </p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  Created: {new Date(task.created_date).toLocaleString()}
                  {task.updated_date !== task.created_date && (
                    <span>, Updated: {new Date(task.updated_date).toLocaleString()}</span>
                  )}
                </p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsEditing(true)}
                className="text-sm text-indigo-600 hover:text-indigo-900"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="text-sm text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}