'use client';

import { useAuth } from '@/components/AuthWrapper';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If user is not authenticated and not loading, redirect to login
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  // If not authenticated, don't render the dashboard content
  if (!user) {
    return null;
  }

  return (
    <div>
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">Todo App</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm">Welcome, {user.email}</span>
            <button
              onClick={handleLogout}
              className="text-sm bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main>
        {children}
      </main>
    </div>
  );
}