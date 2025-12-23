'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient } from '../lib/auth-client';

interface AuthContextType {
  user: any;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const result = await authClient.getSession();
      if (result?.data?.user) {
        setUser(result.data.user);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    } finally {
      setLoading(false);
    }
  };

  const syncUserWithBackend = async (betterAuthUser: any) => {
    try {
      // Check if betterAuthUser has the required properties
      if (!betterAuthUser || !betterAuthUser.id || !betterAuthUser.email) {
        console.error('Better Auth user object is invalid:', betterAuthUser);
        return null;
      }

      console.log('Syncing user with backend:', {
        better_auth_id: betterAuthUser.id,
        email: betterAuthUser.email
      });

      // Sync the Better Auth user with our backend
      const syncResponse = await fetch('http://localhost:8000/api/auth/sync-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          better_auth_id: betterAuthUser.id, // Better Auth user ID
          email: betterAuthUser.email
        })
      });

      if (!syncResponse.ok) {
        const errorText = await syncResponse.text();
        console.error('Failed to sync user with backend:', errorText);
        return null;
      }

      const syncData = await syncResponse.json();
      console.log('User sync response:', syncData);

      // Store the backend token for API calls
      if (syncData.backend_token) {
        // Store the backend token in localStorage or sessionStorage
        localStorage.setItem('backend_token', syncData.backend_token);
        console.log('Backend token stored for API calls');
      }

      return syncData;
    } catch (error) {
      console.error('Error syncing user with backend:', error);
      return null;
    }
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Sign in the user
      const response = await authClient.signIn.email({ email, password });
      if (response?.error) {
        throw new Error(response.error.message || 'Invalid email or password');
      }

      // Wait for session to be established
      await new Promise(resolve => setTimeout(resolve, 100));

      let sessionResult = await authClient.getSession();

      // Retry getting session if not immediately available
      if (!sessionResult?.data?.user) {
        for (let i = 0; i < 5; i++) {
          await new Promise(resolve => setTimeout(resolve, 200));
          sessionResult = await authClient.getSession();
          if (sessionResult?.data?.user) {
            break;
          }
        }
      }

      if (!sessionResult?.data?.user) {
        throw new Error('Login failed - session not found');
      }

      // Sync user with backend after successful login
      await syncUserWithBackend(sessionResult.data.user);

      setUser(sessionResult.data.user);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signup = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Sign up the user
      const response = await authClient.signUp.email({ email, password });
      if (response?.error) {
        throw new Error(response.error.message || 'Signup failed');
      }

      // Explicitly sign in after signup to establish session
      const loginResponse = await authClient.signIn.email({ email, password });
      if (loginResponse?.error) {
        throw new Error(loginResponse.error.message || 'Login after signup failed');
      }

      // Wait for session to be established
      await new Promise(resolve => setTimeout(resolve, 100));

      let sessionResult = await authClient.getSession();

      // Retry getting session if not immediately available
      if (!sessionResult?.data?.user) {
        for (let i = 0; i < 5; i++) {
          await new Promise(resolve => setTimeout(resolve, 200));
          sessionResult = await authClient.getSession();
          if (sessionResult?.data?.user) {
            break;
          }
        }
      }

      if (!sessionResult?.data?.user) {
        throw new Error('Signup succeeded but session not found');
      }

      // Sync user with backend after successful signup
      await syncUserWithBackend(sessionResult.data.user);

      setUser(sessionResult.data.user);
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authClient.signOut();
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    login,
    signup,
    logout,
    loading
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