'use client';

import { AuthProvider } from '@/components/AuthWrapper';
import BottomNavigation from '@/components/BottomNavigation';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

export default function MainLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  // Don't show bottom nav on auth pages
  const showBottomNav = !pathname.startsWith('/login') && !pathname.startsWith('/signup');

  return (
    <AuthProvider>
      {children}
      {showBottomNav && <BottomNavigation />}
    </AuthProvider>
  );
}