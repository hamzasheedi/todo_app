'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from '@/components/AuthWrapper';
import { authClient, getJWTToken } from '@/lib/auth-client';
import { apiClient } from '@/lib/api-client';
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
    const fetchBackendUserId = async () => {
      if (user) {
        try {
          // Add a small delay to ensure session is properly established after login/signup
          await new Promise(resolve => setTimeout(resolve, 150));

          // Use the apiClient which has proper token extraction
          const response = await apiClient.get('/auth/me');

          setBackendUserId(response.id); // Use the backend UUID
          setLoading(false);
        } catch (err) {
          console.error('Error fetching user info:', err);
          // Don't redirect to login, just set loading to false
          setLoading(false);
        }
      } else {
        // If there's no user, just set loading to false
        setLoading(false);
      }
    };

    fetchBackendUserId();
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