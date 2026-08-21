'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { 
  BookOpen, 
  Activity, 
  AlertTriangle, 
  History, 
  Repeat, 
  Shield, 
  LogOut, 
  User as UserIcon 
} from 'lucide-react';

export function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  if (!user && (pathname === '/login' || pathname === '/register' || pathname === '/')) {
    return null;
  }

  const navLinks = [
    { href: '/dashboard', label: 'Dashboard', icon: Activity },
    { href: '/subjects', label: 'Curriculum', icon: BookOpen },
    { href: '/tests', label: 'Practice Tests', icon: Activity },
    { href: '/danger-zone', label: 'Danger Zone', icon: AlertTriangle, highlight: true },
    { href: '/mistakes', label: 'Mistake Bank', icon: History },
    { href: '/revision', label: 'Spaced Revision', icon: Repeat },
  ];

  const isStaff = user?.role === 'admin' || user?.role === 'medical_reviewer';

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-2.5 sm:px-6">
        <div className="flex items-center gap-8">
          <Link href="/dashboard" className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded bg-slate-900 text-sm font-bold text-white">
              +
            </div>
            <span className="text-base font-bold tracking-tight text-slate-900">
              NEET-PG <span className="text-brand-600">PRO</span>
            </span>
          </Link>

          {user && (
            <nav className="hidden md:flex items-center gap-1">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-semibold transition-colors ${
                      isActive
                        ? 'bg-slate-100 text-slate-900'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    } ${link.highlight ? 'text-rose-600 font-bold hover:text-rose-700' : ''}`}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {link.label}
                  </Link>
                );
              })}
              {isStaff && (
                <Link
                  href="/admin/questions"
                  className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-semibold transition-colors ${
                    pathname.startsWith('/admin')
                      ? 'bg-amber-100 text-amber-900'
                      : 'text-amber-700 hover:bg-amber-50'
                  }`}
                >
                  <Shield className="h-3.5 w-3.5" />
                  Review Queue
                </Link>
              )}
            </nav>
          )}
        </div>

        {user && (
          <div className="flex items-center gap-3">
            <Link
              href="/profile"
              className="flex items-center gap-2 rounded-md border border-slate-200 px-2.5 py-1 text-xs text-slate-700 hover:bg-slate-50"
            >
              <UserIcon className="h-3.5 w-3.5 text-slate-500" />
              <span className="max-w-[120px] truncate font-medium">
                {user.full_name || user.email.split('@')[0]}
              </span>
              {user.role !== 'student' && (
                <span className="rounded bg-amber-100 px-1 py-0.5 text-[10px] font-bold text-amber-800 uppercase">
                  {user.role}
                </span>
              )}
            </Link>
            <button
              onClick={logout}
              title="Logout"
              className="flex h-7 w-7 items-center justify-center rounded-md text-slate-500 hover:bg-slate-100 hover:text-slate-800"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
