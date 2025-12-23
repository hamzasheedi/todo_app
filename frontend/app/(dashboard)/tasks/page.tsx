'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { useUser } from '@/contexts/UserContext';
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
  const [filterOption, setFilterOption] = useState<string>('all'); // all, active, completed
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

  // Filter tasks based on filterOption
  const filteredTasks = tasks.filter(task => {
    if (filterOption === 'active') return task.status === 'incomplete';
    if (filterOption === 'completed') return task.status === 'complete';
    return true; // 'all' option
  });

  // Group tasks by status
  const activeTasks = filteredTasks.filter(task => task.status === 'incomplete');
  const completedTasks = filteredTasks.filter(task => task.status === 'complete');

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]); // Add new task to the top
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleFilterChange = (filter: string) => {
    setFilterOption(filter);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOption(e.target.value);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16] text-white pt-8 pb-24">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {contextLoading || !backendUserId ? (
          <div className="min-h-screen flex items-center justify-center">
            <p className="text-gray-400">Loading...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Page Header */}
            <div className="text-center">
              <h1 className="text-3xl font-bold text-[#F5F7FA] mb-2">Your Tasks</h1>
              <p className="text-[#AAB0C0] text-sm">Stay organized. One task at a time.</p>
              <div className="w-16 h-0.5 bg-gradient-to-r from-[#00F5FF] to-[#B026FF] mx-auto mt-4 opacity-50"></div>
            </div>

            {/* Filters & Controls */}
            <div className="flex flex-col lg:flex-row justify-between items-center gap-4">
              <div className="flex space-x-2">
                {['all', 'active', 'completed'].map((filter) => (
                  <button
                    key={filter}
                    onClick={() => handleFilterChange(filter)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      filterOption === filter
                        ? 'text-[#00F5FF] border border-[#00F5FF] bg-[#00F5FF]/10'
                        : 'text-[#AAB0C0] hover:text-[#F5F7FA] hover:bg-[#1a1f33]/50'
                    }`}
                  >
                    {filter.charAt(0).toUpperCase() + filter.slice(1)}
                  </button>
                ))}
              </div>

              <div className="flex items-center space-x-3">
                <span className="text-sm text-[#AAB0C0]">Sort by:</span>
                <select
                  value={sortOption}
                  onChange={handleSortChange}
                  className="bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-2 text-sm text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:ring-opacity-50"
                >
                  <option value="newest_first">Newest First</option>
                  <option value="oldest_first">Oldest First</option>
                  <option value="highest_priority">Highest Priority</option>
                  <option value="lowest_priority">Lowest Priority</option>
                </select>
              </div>
            </div>

            {/* Task Form */}
            <div className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 shadow-2xl shadow-[rgba(0,245,255,0.05)]">
              <TaskForm onTaskCreated={handleTaskCreated} backendUserId={backendUserId} />
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-md bg-red-500/20 p-4 border border-red-500/30">
                <div className="text-sm text-red-300">{error}</div>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="flex justify-center py-8">
                <p className="text-[#AAB0C0]">Loading tasks...</p>
              </div>
            )}

            {/* Task Groups */}
            {!loading && (
              <div className="space-y-8">
                {/* Active Tasks */}
                {activeTasks.length > 0 && (
                  <div>
                    <h2 className="text-lg font-semibold text-[#F5F7FA] mb-4 flex items-center">
                      <span className="w-2 h-2 bg-[#00F5FF] rounded-full mr-2"></span>
                      Active Tasks
                    </h2>
                    <div className="space-y-3">
                      {activeTasks.map((task) => (
                        <div
                          key={task.id}
                          className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-xl border border-gray-700 p-4 hover:border-[#00F5FF]/30 transition-all duration-200"
                        >
                          <TaskItem
                            task={task}
                            onTaskUpdated={handleTaskUpdated}
                            onTaskDeleted={handleTaskDeleted}
                            backendUserId={backendUserId}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Completed Tasks */}
                {completedTasks.length > 0 && (
                  <div>
                    <h2 className="text-lg font-semibold text-[#F5F7FA] mb-4 flex items-center">
                      <span className="w-2 h-2 bg-[#39FF14] rounded-full mr-2"></span>
                      Completed
                    </h2>
                    <div className="space-y-3">
                      {completedTasks.map((task) => (
                        <div
                          key={task.id}
                          className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-xl border border-gray-700 p-4 opacity-70 hover:border-[#39FF14]/30 transition-all duration-200"
                        >
                          <TaskItem
                            task={task}
                            onTaskUpdated={handleTaskUpdated}
                            onTaskDeleted={handleTaskDeleted}
                            backendUserId={backendUserId}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Empty State */}
                {filteredTasks.length === 0 && !loading && (
                  <div className="text-center py-12">
                    <p className="text-[#AAB0C0] text-lg">No tasks yet. Start with one small win.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}