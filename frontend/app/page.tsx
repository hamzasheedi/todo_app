'use client';

import { useAuth } from '@/components/AuthWrapper';
import { useUser } from '@/contexts/UserContext';
import { apiClient } from '@/lib/api-client';
import { useState, useEffect } from 'react';

interface Task {
  id: string;
  title: string;
  description: string | null;
  status: 'complete' | 'incomplete';
  created_date: string;
  updated_date: string;
}

export default function Home() {
  const { user } = useAuth();
  const { backendUserId, loading: userContextLoading } = useUser();
  const [taskCount, setTaskCount] = useState<number>(0);
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [statsLoading, setStatsLoading] = useState<boolean>(true);

  // Fetch user stats if authenticated
  useEffect(() => {
    if (user && backendUserId) {
      fetchUserStats();
    }
  }, [user, backendUserId]);

  const fetchUserStats = async () => {
    try {
      setStatsLoading(true);
      const response = await apiClient.get(`/${backendUserId}/tasks`);
      const tasks: Task[] = response;

      setTaskCount(tasks.length);
      setRecentTasks(tasks.slice(0, 3)); // Get 3 most recent tasks
    } catch (error) {
      console.error('Error fetching user stats:', error);
    } finally {
      setStatsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0B0F1A] via-[#0E1424] to-[#090C16] text-text-primary overflow-hidden">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/3 w-64 h-64 bg-emerald-500/5 rounded-full blur-2xl animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Hero Section */}
        <section className="flex-grow flex items-center py-12">
          <div className="container mx-auto px-6 max-w-6xl">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              {/* Left Content */}
              <div className="space-y-8">
                {/* Badge */}
                <div className="inline-flex items-center px-4 py-2 bg-cyan-900/30 border border-cyan-500/30 rounded-full text-cyan-400 text-sm font-medium backdrop-blur-sm">
                  <span className="mr-2">⚡</span> AI-Powered Productivity
                </div>

                {/* Headline */}
                <h1 className="text-5xl md:text-6xl lg:text-7xl font-black leading-none text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 tracking-tight">
                  TaskFlow AI
                </h1>

                {/* Tagline */}
                <div className="space-y-4">
                  <p className="text-2xl md:text-3xl font-bold text-text-primary animate-fade-in">
                    Organize your tasks.
                  </p>
                  <p className="text-2xl md:text-3xl font-bold text-text-primary animate-fade-in delay-200">
                    Stay focused.
                  </p>
                  <p className="text-2xl md:text-3xl font-bold text-text-primary animate-fade-in delay-300 relative">
                    Get things done.
                    <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-cyan-400 to-purple-400 opacity-70"></span>
                  </p>
                </div>

                {/* Description */}
                <p className="text-lg text-text-secondary max-w-lg">
                  A modern productivity app with AI-powered task management. Organize, prioritize, and complete tasks with intelligent assistance.
                </p>

                {/* CTA Buttons */}
                <div className="flex flex-wrap gap-4 pt-4">
                  <a
                    href="/signup"
                    className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-xl font-bold text-lg transition-all duration-300 hover:from-cyan-400 hover:to-purple-400 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-500/30 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 inline-flex items-center"
                  >
                    Get Started
                    <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  </a>
                  <a
                    href="/login"
                    className="px-8 py-4 bg-bg-surface/50 border border-gray-600 text-text-primary rounded-xl font-bold text-lg backdrop-blur-sm hover:bg-cyan-500/10 hover:border-cyan-500/50 transition-all duration-300 hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 inline-flex items-center"
                  >
                    Sign In
                  </a>
                </div>
              </div>

              {/* Right Abstract Glow Element - Demo Task Showcase */}
              <div className="flex justify-center items-center">
                <div className="relative w-80 h-80 md:w-96 md:h-96">
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-full blur-2xl animate-pulse"></div>
                  <div className="absolute inset-4 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-full backdrop-blur-sm border border-cyan-500/20 flex items-center justify-center">
                    <div className="w-full max-w-xs p-6">
                      {/* Demo Task Card */}
                      <div className="bg-bg-card/80 backdrop-blur-sm rounded-xl border border-gray-600 p-4 mb-3 animate-float" style={{ "--rotation": "2deg" } as React.CSSProperties}>
                        <div className="flex items-center">
                          <div className="w-5 h-5 rounded-full border border-cyan-400 mr-3 flex-shrink-0 flex items-center justify-center">
                            <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
                          </div>
                          <p className="text-text-primary text-sm">Add a new task</p>
                        </div>
                      </div>

                      <div className="bg-bg-card/80 backdrop-blur-sm rounded-xl border border-gray-600 p-4 mb-3 animate-float delay-100" style={{ "--rotation": "-3deg" } as React.CSSProperties}>
                        <div className="flex items-center">
                          <div className="w-5 h-5 rounded-full border border-gray-400 mr-3 flex-shrink-0 flex items-center justify-center">
                            <div className="w-2 h-2 bg-transparent rounded-full"></div>
                          </div>
                          <p className="text-text-primary text-sm">Plan meeting agenda</p>
                        </div>
                      </div>

                      <div className="bg-gradient-to-br from-cyan-500/20 to-purple-500/20 backdrop-blur-sm rounded-xl border border-cyan-400/50 p-4 animate-float-glow" style={{ "--rotation": "1deg" } as React.CSSProperties}>
                        <div className="flex items-center">
                          <div className="w-5 h-5 rounded-full border border-cyan-400 mr-3 flex-shrink-0 flex items-center justify-center">
                            <svg className="w-3 h-3 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
                            </svg>
                          </div>
                          <p className="text-text-primary text-sm">Complete project proposal</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Feature Highlights */}
        <section className="py-16">
          <div className="container mx-auto px-6 max-w-6xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Card 1 */}
              <div className="group bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-cyan-500/50 hover:-translate-y-2 hover:shadow-xl hover:shadow-cyan-500/10">
                <div className="text-4xl mb-4 group-hover:text-cyan-400 transition-colors">🤖</div>
                <h3 className="text-xl font-bold text-text-primary mb-2">AI-Powered Tasks</h3>
                <p className="text-text-secondary">Intelligent task management with natural language processing</p>
              </div>

              {/* Card 2 */}
              <div className="group bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-purple-500/50 hover:-translate-y-2 hover:shadow-xl hover:shadow-purple-500/10">
                <div className="text-4xl mb-4 group-hover:text-purple-400 transition-colors">✦</div>
                <h3 className="text-xl font-bold text-text-primary mb-2">Smart Prioritization</h3>
                <p className="text-text-secondary">Focus on what matters most with AI-driven priorities</p>
              </div>

              {/* Card 3 */}
              <div className="group bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-emerald-500/50 hover:-translate-y-2 hover:shadow-xl hover:shadow-emerald-500/10">
                <div className="text-4xl mb-4 group-hover:text-emerald-400 transition-colors">📊</div>
                <h3 className="text-xl font-bold text-text-primary mb-2">Progress Tracking</h3>
                <p className="text-text-secondary">Visualize your productivity and celebrate achievements</p>
              </div>
            </div>
          </div>
        </section>

        {/* Dashboard for All Users (with demo data for non-logged-in users) */}
        <section className="py-12 border-t border-gray-800/50">
          <div className="container mx-auto px-6 max-w-6xl">
            {/* Welcome Strip - Only for logged-in users */}
            {user && (
              <div className="bg-gradient-to-r from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 mb-12">
                <div className="flex items-center">
                  <div className="bg-cyan-500/10 p-3 rounded-xl border border-cyan-500/20 mr-4">
                    <span className="text-cyan-400 text-2xl">👋</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-text-primary">
                      Welcome back, {user.firstName || user.email?.split('@')[0]}
                    </h2>
                    <p className="text-text-secondary">Here's what's happening with your tasks today.</p>
                  </div>
                </div>
              </div>
            )}

            {/* Stats Grid - Show demo data for non-logged-in users */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-blue-500/30">
                <div className="text-4xl font-bold text-blue-400 mb-2">{user ? taskCount : 12}</div>
                <h3 className="text-lg font-semibold text-text-primary mb-1">Total Tasks</h3>
                <p className="text-text-secondary text-sm">All your tasks in one place</p>
              </div>

              <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-green-500/30">
                <div className="text-4xl font-bold text-green-400 mb-2">
                  {user ? recentTasks.filter(t => t.status === 'complete').length : 1}
                </div>
                <h3 className="text-lg font-semibold text-text-primary mb-1">Completed</h3>
                <p className="text-text-secondary text-sm">Tasks you've finished</p>
              </div>

              <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 transition-all duration-300 hover:border-orange-500/30">
                <div className="text-4xl font-bold text-orange-400 mb-2">
                  {user ? taskCount - recentTasks.filter(t => t.status === 'complete').length : 11}
                </div>
                <h3 className="text-lg font-semibold text-text-primary mb-1">Pending</h3>
                <p className="text-text-secondary text-sm">Tasks waiting to be done</p>
              </div>
            </div>

            {/* Recent Tasks - Show demo data for non-logged-in users */}
            <div className="mb-12">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-text-primary">Recent Tasks</h3>
                <a
                  href="/tasks"
                  className="text-cyan-400 hover:text-cyan-300 transition-colors duration-200 flex items-center group"
                >
                  View all
                  <svg xmlns="http://www.w3.org/2000/svg" className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </a>
              </div>

              {user ? (
                // Actual tasks for logged-in users
                statsLoading ? (
                  <div className="text-center py-12">
                    <div className="inline-flex space-x-2">
                      <div className="w-3 h-3 bg-cyan-500 rounded-full animate-bounce"></div>
                      <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce delay-100"></div>
                      <div className="w-3 h-3 bg-emerald-500 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                ) : recentTasks.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {recentTasks.map((task) => (
                      <div
                        key={task.id}
                        className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-xl border border-gray-700 p-4 transition-all duration-300 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/10"
                      >
                        <div className="flex justify-between items-start">
                          <h4 className={`font-medium ${task.status === 'complete' ? 'text-text-positive line-through' : 'text-text-primary'}`}>
                            {task.title}
                          </h4>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            task.status === 'complete'
                              ? 'bg-text-positive/10 text-text-positive'
                              : 'bg-cyan-500/10 text-cyan-400'
                          }`}>
                            {task.status}
                          </span>
                        </div>
                        {task.description && (
                          <p className="text-text-secondary text-sm mt-2 line-clamp-2">{task.description}</p>
                        )}
                        <p className="text-xs text-text-secondary/70 mt-3">
                          {new Date(task.created_date).toLocaleDateString()}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-xl border border-gray-700 p-8 text-center">
                    <p className="text-text-secondary">No tasks yet. Start by adding your first task!</p>
                  </div>
                )
              ) : (
                // Demo tasks for non-logged-in users
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-xl border border-gray-700 p-4 transition-all duration-300 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/10">
                    <div className="flex justify-between items-start">
                      <h4 className="font-medium text-text-primary">Buy groceries</h4>
                      <span className="text-xs px-2 py-1 rounded-full bg-cyan-500/10 text-cyan-400">
                        incomplete
                      </span>
                    </div>
                    <p className="text-xs text-text-secondary/70 mt-3">2/1/2026</p>
                  </div>

                  <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-xl border border-gray-700 p-4 transition-all duration-300 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/10">
                    <div className="flex justify-between items-start">
                      <h4 className="font-medium text-text-primary">Buy milk</h4>
                      <span className="text-xs px-2 py-1 rounded-full bg-text-positive/10 text-text-positive">
                        complete
                      </span>
                    </div>
                    <p className="text-xs text-text-secondary/70 mt-3">Buy milk from the store</p>
                    <p className="text-xs text-text-secondary/70 mt-1">2/1/2026</p>
                  </div>

                  <div className="bg-gradient-to-br from-bg-card/60 to-bg-surface/40 backdrop-blur-sm rounded-xl border border-gray-700 p-4 transition-all duration-300 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/10">
                    <div className="flex justify-between items-start">
                      <h4 className="font-medium text-text-primary">Drink water</h4>
                      <span className="text-xs px-2 py-1 rounded-full bg-text-positive/10 text-text-positive">
                        complete
                      </span>
                    </div>
                    <p className="text-xs text-text-secondary/70 mt-3">2/1/2026</p>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="mb-16">
              <h3 className="text-2xl font-bold text-text-primary mb-6 text-center">Quick Actions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
                <a
                  href="/tasks"
                  className="group bg-gradient-to-br from-bg-card/40 to-bg-surface/30 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 text-center transition-all duration-300 hover:border-cyan-500/50 hover:-translate-y-1 hover:shadow-xl hover:shadow-cyan-500/10"
                >
                  <div className="text-4xl mb-3 group-hover:text-cyan-400 transition-colors">📋</div>
                  <h4 className="text-lg font-bold text-text-primary mb-2">Manage Tasks</h4>
                  <p className="text-text-secondary text-sm">Organize and prioritize your work</p>
                  <div className="mt-4 flex items-center justify-center text-cyan-400 group-hover:translate-x-1 transition-transform">
                    <span className="text-sm">Get started</span>
                    <svg xmlns="http://www.w3.org/2000/svg" className="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </a>
                <a
                  href="/chat"
                  className="group bg-gradient-to-br from-bg-card/40 to-bg-surface/30 backdrop-blur-sm rounded-2xl border border-gray-700 p-6 text-center transition-all duration-300 hover:border-purple-500/50 hover:-translate-y-1 hover:shadow-xl hover:shadow-purple-500/10"
                >
                  <div className="text-4xl mb-3 group-hover:text-purple-400 transition-colors">🤖</div>
                  <h4 className="text-lg font-bold text-text-primary mb-2">AI Assistant</h4>
                  <p className="text-text-secondary text-sm">Get help with your tasks</p>
                  <div className="mt-4 flex items-center justify-center text-purple-400 group-hover:translate-x-1 transition-transform">
                    <span className="text-sm">Try now</span>
                    <svg xmlns="http://www.w3.org/2000/svg" className="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}