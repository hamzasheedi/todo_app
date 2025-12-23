'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/AuthWrapper';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const { login, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login(email, password);
      // Navigate to tasks page after successful login
      router.push('/tasks');
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'Invalid email or password. Please try again.');
      console.error('Login error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Branding Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-[#F5F7FA] flex items-center justify-center">
            <span className="text-[#00F5FF] mr-2">✓</span>
            TaskFlow
          </h1>
          <p className="text-[#AAB0C0] mt-2">Organize your work. Stay focused.</p>
          <div className="w-16 h-0.5 bg-gradient-to-r from-[#00F5FF] to-[#B026FF] mx-auto mt-4 opacity-50"></div>
        </div>

        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold text-[#F5F7FA] mb-2">Welcome back</h2>
          <p className="text-[#AAB0C0]">Let's get things done.</p>
        </div>

        <div className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-2xl border border-gray-700 p-8 shadow-2xl shadow-[rgba(0,245,255,0.05)]">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md bg-red-500/20 p-3 border border-red-500/30">
                <div className="text-sm text-red-300">{error}</div>
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="email-address" className="block text-sm font-medium text-[#AAB0C0] mb-2">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-3 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
                  placeholder="Enter your email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-[#AAB0C0] mb-2">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-[#0B0F1A] border border-gray-600 rounded-lg px-3 py-3 text-[#F5F7FA] focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:border-[#00F5FF]"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="text-sm">
                <Link href="/signup" className="text-[#00F5FF] hover:text-[#00F5FF]/80 hover:underline">
                  Don't have an account? Sign up
                </Link>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-[#0B0F1A] bg-[#00F5FF] hover:bg-[#00F5FF]/90 focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:ring-offset-2 disabled:opacity-50"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}