'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { apiRequest, AuthResponse } from '@/lib/api';
import { Lock, Mail, User, Calendar, AlertCircle, Loader2, Eye, EyeOff, Sparkles, ArrowRight } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [targetYear, setTargetYear] = useState(2026);
  const [rememberedEmail, setRememberedEmail] = useState<string | null>(null);
  const [accountExists, setAccountExists] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  useEffect(() => {
    const saved = localStorage.getItem('revizo_last_email');
    if (saved) {
      setRememberedEmail(saved);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setAccountExists(false);
    setLoading(true);

    const cleanEmail = email.trim().toLowerCase();

    try {
      const data = await apiRequest<AuthResponse>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          email: cleanEmail,
          password,
          full_name: fullName.trim(),
          target_exam_year: Number(targetYear),
        }),
      });

      localStorage.setItem('revizo_last_email', cleanEmail);

      login(data.access_token, {
        id: data.user_id,
        email: data.email,
        role: data.role,
        full_name: data.full_name,
        target_exam_year: Number(targetYear),
        daily_question_goal: 10,
      });
    } catch (err: any) {
      const msg = err.message || '';
      if (msg.toLowerCase().includes('already exists') || msg.toLowerCase().includes('conflict')) {
        setAccountExists(true);
        setError(`An account for ${cleanEmail} already exists.`);
      } else {
        setError(msg || 'Registration failed. Please check your connection and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[85vh] items-center justify-center px-4 py-12">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
        <div className="text-center space-y-1">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Create Free Aspirant Account</h2>
          <p className="text-xs text-slate-500">Free, trustworthy medical practice & spaced revision</p>
        </div>

        {/* Existing Remembered Account Hint */}
        {rememberedEmail && !accountExists && (
          <div className="flex items-center justify-between rounded-xl border border-brand-200 bg-brand-50/80 p-3 text-xs text-brand-900">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-brand-600 shrink-0" />
              <span>
                Existing account: <strong>{rememberedEmail}</strong>
              </span>
            </div>
            <Link
              href={`/login?email=${encodeURIComponent(rememberedEmail)}`}
              className="font-bold text-brand-700 hover:text-brand-800 flex items-center gap-0.5"
            >
              Sign In <ArrowRight className="h-3 w-3" />
            </Link>
          </div>
        )}

        {/* Account Conflict Alert */}
        {accountExists && (
          <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-xs text-amber-900 space-y-2.5 animate-in fade-in">
            <div className="flex items-start gap-2">
              <AlertCircle className="h-4 w-4 shrink-0 text-amber-600 mt-0.5" />
              <div>
                <p className="font-bold text-amber-950">Account Already Exists</p>
                <p className="text-amber-800 mt-0.5">
                  An account is already registered for <strong>{email}</strong>. Would you like to sign in instead?
                </p>
              </div>
            </div>
            <div className="pt-1">
              <Link
                href={`/login?email=${encodeURIComponent(email)}`}
                className="inline-flex w-full items-center justify-center gap-1.5 rounded-lg bg-amber-700 px-4 py-2 font-bold text-white hover:bg-amber-800 shadow-sm"
              >
                Sign In with {email} &rarr;
              </Link>
            </div>
          </div>
        )}

        {error && !accountExists && (
          <div className="flex items-center gap-2 rounded-lg border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-700">Full Name</label>
            <div className="relative">
              <User className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Dr. Rajesh Kumar"
                className="w-full rounded-lg border border-slate-300 py-2.5 pl-9 pr-3 text-sm focus:border-brand-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-700">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type="email"
                inputMode="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="doctor@hospital.org"
                className="w-full rounded-lg border border-slate-300 py-2.5 pl-9 pr-3 text-sm focus:border-brand-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold text-slate-700">Password (Min 8 chars)</label>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-[11px] font-medium text-slate-500 hover:text-slate-800 flex items-center gap-1"
              >
                {showPassword ? (
                  <>
                    <EyeOff className="h-3 w-3" /> Hide
                  </>
                ) : (
                  <>
                    <Eye className="h-3 w-3" /> Show
                  </>
                )}
              </button>
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type={showPassword ? 'text' : 'password'}
                autoComplete="new-password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full rounded-lg border border-slate-300 py-2.5 pl-9 pr-10 text-sm focus:border-brand-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-700">Target NEET-PG Year</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <select
                value={targetYear}
                onChange={(e) => setTargetYear(Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 py-2.5 pl-9 pr-3 text-sm focus:border-brand-500 focus:outline-none bg-white"
              >
                <option value={2026}>NEET-PG 2026</option>
                <option value={2027}>NEET-PG 2027</option>
                <option value={2028}>NEET-PG 2028</option>
                <option value={2029}>NEET-PG 2029</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full min-h-[44px] flex items-center justify-center gap-2 rounded-xl bg-brand-600 py-3 text-sm font-bold text-white hover:bg-brand-700 disabled:opacity-50 transition-colors shadow-sm"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Create Account'}
          </button>
        </form>

        <div className="text-center text-xs text-slate-500">
          Already have an account?{' '}
          <Link href="/login" className="font-bold text-brand-600 hover:text-brand-700">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
