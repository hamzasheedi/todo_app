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
    // Check if user is already logged in on component mount
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const session = await authClient.getSession();
      if (session) {
        setUser(session.user);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Use authClient to login
      const response = await authClient.signIn.email({
        email,
        password,
        callbackURL: "/dashboard"  // Redirect after login
      });
      if (response) {
        setUser(response.user);
      }
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
      // Use authClient to register
      const response = await authClient.signUp.email({
        email,
        password,
        callbackURL: "/dashboard"  // Redirect after signup
      });
      if (response) {
        setUser(response.user);
      }
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