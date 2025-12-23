'use client';

import { useAuth } from '@/components/AuthWrapper';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const BottomNavigation = () => {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [isVisible, setIsVisible] = useState(true);

  // Handle navigation and visibility
  const handleNavigation = (path: string) => {
    if (pathname === path) return; // Don't navigate if already on the same page
    router.push(path);
  };

  // Hide navigation on auth pages
  useEffect(() => {
    const shouldHide = pathname.startsWith('/login') || pathname.startsWith('/signup');
    setIsVisible(!shouldHide);
  }, [pathname]);

  // Don't show if loading or should be hidden
  if (loading || !isVisible) {
    return null;
  }

  return (
    <nav className="fixed bottom-4 left-4 right-4 max-w-md mx-auto z-50">
      <div className="flex justify-around items-center relative">
        {/* Home Button */}
        <button
          onClick={() => handleNavigation('/')}
          className={`flex flex-col items-center px-4 py-3 rounded-xl transition-all duration-300 relative z-10 ${
            pathname === '/'
              ? 'text-[#00F5FF] scale-110'
              : 'text-[#AAB0C0] hover:text-[#F5F7FA]'
          }`}
          aria-label="Home"
        >
          <span className="text-lg mb-1">🏠</span>
          <span className="text-xs">Home</span>
        </button>

        {/* Conditional buttons based on auth status */}
        {user ? (
          <>
            {/* Tasks Button - Primary for logged in users */}
            <button
              onClick={() => handleNavigation('/tasks')}
              className={`flex flex-col items-center px-4 py-3 rounded-xl transition-all duration-300 relative z-10 ${
                pathname === '/tasks'
                  ? 'text-[#00F5FF] scale-110'
                  : 'text-[#AAB0C0] hover:text-[#F5F7FA] hover:text-[#00F5FF]'
              }`}
              aria-label="Tasks"
            >
              <span className="text-lg mb-1">📋</span>
              <span className="text-xs">Tasks</span>
            </button>

            {/* Logout Button */}
            <button
              onClick={async () => {
                try {
                  await logout();
                  router.push('/'); // Redirect to home after logout
                } catch (error) {
                  console.error('Logout error:', error);
                }
              }}
              className="flex flex-col items-center px-4 py-3 rounded-xl transition-all duration-300 text-[#AAB0C0] hover:text-[#F5F7FA] hover:text-[#B026FF] relative z-10"
              aria-label="Logout"
            >
              <span className="text-lg mb-1">🚪</span>
              <span className="text-xs">Logout</span>
            </button>
          </>
        ) : (
          <>
            {/* Login Button - Primary for logged out users */}
            <button
              onClick={() => handleNavigation('/login')}
              className={`flex flex-col items-center px-4 py-3 rounded-xl transition-all duration-300 relative z-10 ${
                pathname === '/login'
                  ? 'text-[#00F5FF] scale-110'
                  : 'text-[#AAB0C0] hover:text-[#F5F7FA] hover:text-[#00F5FF]'
              }`}
              aria-label="Login"
            >
              <span className="text-lg mb-1">🔐</span>
              <span className="text-xs">Login</span>
            </button>

            {/* Sign Up Button */}
            <button
              onClick={() => handleNavigation('/signup')}
              className={`flex flex-col items-center px-4 py-3 rounded-xl transition-all duration-300 relative z-10 ${
                pathname === '/signup'
                  ? 'text-[#B026FF] scale-110'
                  : 'text-[#AAB0C0] hover:text-[#F5F7FA] hover:text-[#B026FF]'
              }`}
              aria-label="Sign Up"
            >
              <span className="text-lg mb-1">✍️</span>
              <span className="text-xs">Sign Up</span>
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default BottomNavigation;