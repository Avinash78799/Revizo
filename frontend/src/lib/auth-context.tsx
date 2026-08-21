'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { UserProfile, apiRequest } from './api';

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  login: (token: string, profile: UserProfile) => void;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const refreshProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      const profile = await apiRequest<UserProfile>('/auth/me');
      setUser(profile);
    } catch {
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshProfile();
  }, []);

  const login = (token: string, profile: UserProfile) => {
    localStorage.setItem('token', token);
    setUser(profile);
    router.push('/dashboard');
  };

  const logout = async () => {
    try {
      await apiRequest('/auth/logout', { method: 'POST' });
    } catch {
      // Ignore network errors on logout
    }
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  // Route protection
  useEffect(() => {
    if (loading) return;
    const publicRoutes = ['/login', '/register', '/'];
    const isPublic = publicRoutes.includes(pathname);

    if (!user && !isPublic) {
      router.push('/login');
    } else if (user && (pathname === '/login' || pathname === '/register')) {
      router.push('/dashboard');
    } else if (user && pathname.startsWith('/admin') && user.role !== 'admin' && user.role !== 'medical_reviewer') {
      router.push('/dashboard');
    }
  }, [user, loading, pathname, router]);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
