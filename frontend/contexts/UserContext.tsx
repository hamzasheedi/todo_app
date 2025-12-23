'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { authClient, getJWTToken } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

interface UserContextType {
  backendUserId: string | null;
  loading: boolean;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const { user, loading: authLoading } = useAuth();
  const [backendUserId, setBackendUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const getAuthHeaders = (): Record<string, string> => {
      // Use the backend token stored after sync
      const token = localStorage.getItem('backend_token');
      console.log('UserContext - Backend token being sent:', token ? 'Exists' : 'Missing');

      return {
        'Authorization': `Bearer ${token || ''}`,
        'Content-Type': 'application/json',
      };
    };

    const fetchBackendUserId = async () => {
      if (user) {
        try {
          // Add a small delay to ensure session is properly established after login/signup
          await new Promise(resolve => setTimeout(resolve, 150));

          // Use the apiClient which has proper token extraction
          const response = await fetch('http://localhost:8000/api/auth/me', {
            method: 'GET',
            headers: getAuthHeaders(),
          });

          if (response.ok) {
            const userData = await response.json();
            setBackendUserId(userData.id); // Use the backend UUID
            setLoading(false);
          } else {
            console.error('Failed to get user info from backend');
            // Redirect to login if backend authentication fails
            router.push('/login');
          }
        } catch (err) {
          console.error('Error fetching user info:', err);
          // Redirect to login if there's an error
          router.push('/login');
        }
      } else if (!authLoading) {
        // If there's no user and auth isn't loading, redirect to login
        router.push('/login');
      }
    };

    if (user) {
      fetchBackendUserId();
    } else if (!authLoading) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  return (
    <UserContext.Provider value={{ backendUserId, loading }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}