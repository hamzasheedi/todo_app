import { useState, useEffect, useContext, createContext, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';

interface User {
  id: string;
  email: string;
  created_date: string;
  updated_date: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is already authenticated on initial load
    const checkAuthStatus = async () => {
      try {
        // Try to get user info from API to verify token
        const tokens = getAuthTokens();
        if (tokens?.accessToken) {
          // Verify token and get user info
          const response = await apiClient.get('/auth/me');
          setUser(response.user);
        }
      } catch (error) {
        // Token is invalid or expired, clear tokens
        clearAuthTokens();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/signin', { email, password });

      // Store tokens
      setAuthTokens(response.accessToken, response.refreshToken);

      // Set user
      setUser(response.user);

      // Redirect to dashboard
      router.push('/tasks');
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/signup', { email, password });

      // Store tokens
      setAuthTokens(response.accessToken, response.refreshToken);

      // Set user
      setUser(response.user);

      // Redirect to dashboard
      router.push('/tasks');
    } catch (error) {
      throw new Error('Registration failed');
    }
  };

  const signOut = async () => {
    try {
      await apiClient.post('/auth/signout', {});
    } catch (error) {
      // Continue with sign out even if API call fails
      console.error('Sign out API call failed:', error);
    } finally {
      clearAuthTokens();
      setUser(null);
      router.push('/login');
    }
  };

  const isAuthenticated = () => {
    return user !== null;
  };

  const value = {
    user,
    loading,
    signIn,
    signUp,
    signOut,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Helper functions for token management
function setAuthTokens(accessToken: string, refreshToken: string) {
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
}

function getAuthTokens() {
  const accessToken = localStorage.getItem('accessToken');
  const refreshToken = localStorage.getItem('refreshToken');

  if (accessToken && refreshToken) {
    return { accessToken, refreshToken };
  }
  return null;
}

function clearAuthTokens() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
}