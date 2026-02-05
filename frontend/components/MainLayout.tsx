'use client';

import { AuthProvider } from '@/components/AuthWrapper';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { UserProvider } from '@/contexts/UserContext';
import BottomNavigation from '@/components/BottomNavigation';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

export default function MainLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  // Don't show bottom nav on auth pages
  const showBottomNav = !pathname.startsWith('/login') && !pathname.startsWith('/signup');

  return (
    <ThemeProvider>
      <AuthProvider>
        <UserProvider>
          {children}
          {showBottomNav && <BottomNavigation />}
        </UserProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}