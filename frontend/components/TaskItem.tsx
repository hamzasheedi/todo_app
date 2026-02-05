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
            ? 'bg-text-positive border-text-positive text-text-positive'
            : 'bg-bg-surface border-text-secondary text-brand-primary'
        }`}
      />
      <div className="flex-1 min-w-0">
        {isEditing ? (
          <form onSubmit={handleUpdate} className="space-y-3">
            {error && (
              <div className="rounded-md bg-status-error/20 p-2 border border-status-error/30">
                <div className="text-xs text-status-error">{error}</div>
              </div>
            )}
            <div>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-bg-primary border border-gray-600 rounded-lg px-3 py-2 text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary"
                maxLength={200}
                required
              />
            </div>
            <div>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={2}
                className="w-full bg-bg-primary border border-gray-600 rounded-lg px-3 py-2 text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary"
                maxLength={1000}
              />
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as 'complete' | 'incomplete')}
                className="bg-bg-primary border border-gray-600 rounded-lg px-2 py-1 text-sm text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary"
              >
                <option value="incomplete">Active</option>
                <option value="complete">Completed</option>
              </select>
              <button
                type="submit"
                disabled={loading}
                className="text-sm bg-brand-primary text-bg-primary px-3 py-1 rounded-lg hover:bg-brand-primary/90 disabled:opacity-50 font-medium transition-all duration-200"
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
                className="text-sm text-text-secondary px-3 py-1 rounded-lg border border-gray-600 hover:text-text-primary hover:border-brand-primary transition-all duration-200"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div>
            <h3 className={`font-medium ${status === 'complete' ? 'line-through text-text-secondary' : 'text-text-primary'}`}>
              {title}
            </h3>
            {description && (
              <p className={`mt-1 text-sm ${status === 'complete' ? 'text-text-disabled' : 'text-text-secondary'}`}>
                {description}
              </p>
            )}
            <p className="mt-2 text-xs text-text-disabled">
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
            className="text-sm text-brand-primary hover:text-brand-secondary hover:underline transition-colors duration-200"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="text-sm text-brand-secondary hover:text-brand-secondary/80 hover:underline transition-colors duration-200"
          >
            Delete
          </button>
        </div>
      )}
    </div>
  );
}