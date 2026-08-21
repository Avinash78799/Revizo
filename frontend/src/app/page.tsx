'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth-context';
import { Activity, ShieldCheck, Repeat, AlertOctagon, ArrowRight } from 'lucide-react';

export default function HomePage() {
  const { user } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="max-w-3xl space-y-6">
        <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-700 shadow-sm">
          <ShieldCheck className="h-4 w-4 text-emerald-600" />
          Medically Verified + High-Yield Spaced Revision
        </div>

        <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">
          Serious NEET-PG Practice. <br />
          <span className="text-brand-600">Zero Fluff. Zero Gimmicks.</span>
        </h1>

        <p className="text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Study &rarr; Practice &rarr; Diagnose &rarr; Correct &rarr; Remember &rarr; Retest &rarr; Improve. Built specifically for medical aspirants who value question accuracy and high-yield retention over sheer question volume.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-3 pt-4">
          {user ? (
            <Link
              href="/dashboard"
              className="flex items-center gap-2 rounded-lg bg-slate-900 px-6 py-3 text-sm font-bold text-white shadow hover:bg-slate-800 transition-colors"
            >
              Go to Dashboard
              <ArrowRight className="h-4 w-4" />
            </Link>
          ) : (
            <>
              <Link
                href="/register"
                className="flex items-center gap-2 rounded-lg bg-brand-600 px-6 py-3 text-sm font-bold text-white shadow hover:bg-brand-700 transition-colors"
              >
                Start Practicing Free
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/login"
                className="rounded-lg border border-slate-300 bg-white px-6 py-3 text-sm font-bold text-slate-700 hover:bg-slate-50 transition-colors"
              >
                Doctor Sign In
              </Link>
            </>
          )}
        </div>

        {/* Value Pillars */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-12 text-left">
          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-2">
            <Activity className="h-5 w-5 text-brand-600" />
            <h3 className="text-sm font-bold text-slate-900">Structured Explanations</h3>
            <p className="text-xs text-slate-600">
              Why the correct answer is right, why your specific distractor was wrong, and the high-yield takeaway pearl.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-2">
            <AlertOctagon className="h-5 w-5 text-rose-600" />
            <h3 className="text-sm font-bold text-slate-900">Danger Zone Isolation</h3>
            <p className="text-xs text-slate-600">
              Isolates questions answered incorrectly despite 100% confidence to fix clinical misconceptions immediately.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-2">
            <Repeat className="h-5 w-5 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">Spaced Repetition</h3>
            <p className="text-xs text-slate-600">
              Adaptive concept-level review schedules ensuring you retain high-yield facts all the way to exam day.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
