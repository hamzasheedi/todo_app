'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useTheme } from '@/contexts/ThemeContext';
import { motion } from 'framer-motion';
import { useAuth } from '@/components/AuthWrapper';
import { useState } from 'react';

const BottomNavigation = () => {
  const pathname = usePathname();
  const { theme } = useTheme();
  const { logout, user } = useAuth();
  const router = useRouter();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  // Define navigation items
  const navItems = [
    { href: '/', label: 'Home', icon: '🏠' },
    { href: '/tasks', label: 'Tasks', icon: '📝' },
    { href: '/chat', label: 'AI Chat', icon: '🤖' },
  ];

  const handleLogout = async () => {
    try {
      setIsLoggingOut(true);
      await logout();
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout error:', error);
      setIsLoggingOut(false);
    }
  };

  // Only show bottom nav if user is authenticated
  if (!user) {
    return null;
  }

  return (
    <motion.nav
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', damping: 20 }}
      className="fixed bottom-0 left-0 right-0 bg-bg-secondary border-t border-gray-700 z-50 md:hidden"
    >
      <div className="flex justify-around items-center py-3">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-col items-center justify-center px-4 py-2 rounded-xl transition-all duration-300 relative ${
              pathname === item.href
                ? 'text-brand-primary bg-brand-primary/10'
                : 'text-text-secondary hover:text-text-primary'
            }`}
          >
            <motion.span
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              className="text-xl mb-1"
            >
              {item.icon}
            </motion.span>
            <span className="text-xs">{item.label}</span>
            {pathname === item.href && (
              <motion.div
                layoutId="activeTabIndicator"
                className="absolute bottom-0 w-8 h-0.5 bg-brand-primary rounded-full"
                initial={false}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            )}
          </Link>
        ))}

        {/* Logout button - styled differently to be less dominant */}
        <button
          onClick={handleLogout}
          disabled={isLoggingOut}
          className="flex flex-col items-center justify-center px-4 py-2 rounded-xl transition-all duration-300 text-text-disabled hover:text-text-negative disabled:opacity-50"
        >
          <motion.span
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="text-xl mb-1"
          >
            {isLoggingOut ? '⏳' : '🚪'}
          </motion.span>
          <span className="text-xs">Logout</span>
        </button>
      </div>
    </motion.nav>
  );
};

export default BottomNavigation;