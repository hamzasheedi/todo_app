'use client';

import { useAuth } from '@/components/AuthWrapper';
import { UserProvider } from '@/contexts/UserContext';
import UserNavigation from '@/components/UserNavigation';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading } = useAuth();
  const router = useRouter();

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

  return (
    <UserProvider>
      <div className="min-h-screen bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16] text-white">
        <header className="border-b border-gray-700 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold text-[#F5F7FA] flex items-center">
                <span className="text-[#00F5FF] mr-2">✓</span>
                TaskFlow
              </h1>
              <p className="text-sm text-[#AAB0C0] hidden md:block">Organize. Focus. Execute.</p>
              <div className="w-2 h-0.5 bg-gradient-to-r from-[#00F5FF] to-[#B026FF] opacity-50 ml-2 hidden md:block"></div>
            </div>
            <div className="flex items-center space-x-4">
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