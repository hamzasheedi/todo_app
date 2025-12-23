'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { useUser } from '@/contexts/UserContext';
import { useRouter } from 'next/navigation';

export default function UserNavigation() {
  const { user, logout } = useAuth();
  const { backendUserId } = useUser();
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
      router.refresh();
      setIsOpen(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Don't render anything if user or backendUserId isn't available yet
  if (!user || !backendUserId) {
    return null;
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-[#AAB0C0] hover:text-[#F5F7FA] transition-colors duration-200"
        aria-label="User menu"
      >
        <div className="w-8 h-8 rounded-full bg-[#1a1f33] border border-gray-600 flex items-center justify-center">
          <span className="text-sm font-medium">
            {user.firstName?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase() || 'U'}
          </span>
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-[#0B0F1A] border border-gray-700 rounded-lg shadow-lg z-50 py-2">
          <div className="px-4 py-2 border-b border-gray-700">
            <p className="text-xs text-[#AAB0C0] truncate">📧 {user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-[#AAB0C0] hover:bg-[#1a1f33] hover:text-[#F5F7FA] transition-colors duration-200 flex items-center"
          >
            <span className="mr-2">🚪</span>
            Logout
          </button>
        </div>
      )}
    </div>
  );
}