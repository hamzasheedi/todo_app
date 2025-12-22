'use client';

import { useAuth } from '@/components/AuthWrapper';
import { useUser } from '@/contexts/UserContext';
import { useRouter } from 'next/navigation';

export default function UserNavigation() {
  const { user, logout } = useAuth();
  const { backendUserId } = useUser();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Don't render anything if user or backendUserId isn't available yet
  if (!user || !backendUserId) {
    return null;
  }

  return (
    <div className="flex items-center space-x-4">
      <span className="text-sm">Welcome, {user.email}</span>
      <button
        onClick={handleLogout}
        className="text-sm bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
      >
        Logout
      </button>
    </div>
  );
}