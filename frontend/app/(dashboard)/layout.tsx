'use client';

import { useAuth } from '@/components/AuthWrapper';
import { UserProvider } from '@/contexts/UserContext';
import UserNavigation from '@/components/UserNavigation';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  // If not authenticated and auth isn't loading, redirect to login
  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16]">
        <p className="text-gray-400">Loading...</p>
      </div>
    );
  }

  // If not authenticated, don't render the layout
  if (!user) {
    return null;
  }

  // Determine active navigation item
  const isActiveRoute = (route: string) => pathname === route;

  return (
    <UserProvider>
      <div className="min-h-screen bg-gradient-to-b from-bg-primary via-bg-secondary to-bg-tertiary text-text-primary">
        <header className="border-b border-gray-700 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold text-text-primary flex items-center">
                <span className="text-brand-primary mr-2">✓</span>
                TaskFlow AI
              </h1>
              <p className="text-sm text-text-secondary hidden md:block">Organize. Focus. Execute.</p>
              <div className="w-2 h-0.5 bg-brand-gradient opacity-50 ml-2 hidden md:block"></div>
            </div>
            <div className="flex items-center space-x-4">
              <nav className="hidden md:flex space-x-4">
                <a
                  href="/tasks"
                  className={`text-text-secondary hover:text-text-primary transition-colors duration-200 px-3 py-1 rounded-lg hover:bg-bg-surface relative ${
                    isActiveRoute('/tasks') ? 'text-brand-primary border border-brand-primary bg-brand-primary/10' : ''
                  }`}
                >
                  Tasks
                  {isActiveRoute('/tasks') && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-primary rounded-full"></div>
                  )}
                </a>
                <a
                  href="/chat"
                  className={`text-text-secondary hover:text-text-primary transition-colors duration-200 px-3 py-1 rounded-lg hover:bg-bg-surface flex items-center relative ${
                    isActiveRoute('/chat') ? 'text-brand-primary border border-brand-primary bg-brand-primary/10' : ''
                  }`}
                >
                  <span className="mr-1">🤖</span> AI Chat
                  {isActiveRoute('/chat') && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-primary rounded-full"></div>
                  )}
                </a>
              </nav>
              <UserNavigation />
            </div>
          </div>
        </header>
        <main>
          {children}
        </main>
      </div>
    </UserProvider>
  );
}