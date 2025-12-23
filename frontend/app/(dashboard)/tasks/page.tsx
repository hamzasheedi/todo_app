'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { useUser } from '@/contexts/UserContext';
import { authClient } from '@/lib/auth-client';
import { apiClient } from '@/lib/api-client';
import TaskForm from '@/components/TaskForm';
import TaskItem from '@/components/TaskItem';
import { TaskRead } from '../../../backend/schemas/task'; // This would be an API response type

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

export default function TasksPage() {
  const { user } = useAuth(); // user is guaranteed to exist due to layout protection
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortOption, setSortOption] = useState<string>('newest_first');

  // Get backend user ID from the context
  const { backendUserId, loading: contextLoading } = useUser();

  const fetchTasks = async () => {
    if (!backendUserId) return;

    try {
      setLoading(true);
      // Use the backend user ID in the API call (apiClient automatically adds /api prefix)
      const response = await apiClient.get(`/${backendUserId}/tasks?sort=${sortOption}`);
      setTasks(response);
      setError(null);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks from the API
  useEffect(() => {
    if (backendUserId) {
      fetchTasks();
    }
  }, [backendUserId, sortOption]);

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]); // Add new task to the top
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOption(e.target.value);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {contextLoading || !backendUserId ? (
          <div className="min-h-screen flex items-center justify-center">
            <p>Loading...</p>
          </div>
        ) : (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">Sort by:</span>
                <select
                  value={sortOption}
                  onChange={handleSortChange}
                  className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="newest_first">Newest First</option>
                  <option value="oldest_first">Oldest First</option>
                  <option value="highest_priority">Highest Priority</option>
                  <option value="lowest_priority">Lowest Priority</option>
                </select>
              </div>
            </div>

            <TaskForm onTaskCreated={handleTaskCreated} backendUserId={backendUserId} />

            {error && (
              <div className="rounded-md bg-red-50 p-4 mb-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            {loading ? (
              <div className="flex justify-center py-8">
                <p>Loading tasks...</p>
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No tasks yet. Create your first task above!</p>
              </div>
            ) : (
              <div className="space-y-4 mt-6">
                {tasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onTaskUpdated={handleTaskUpdated}
                    onTaskDeleted={handleTaskDeleted}
                    backendUserId={backendUserId}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}