'use client';

import React from 'react';
import { ShieldCheck, Lock } from 'lucide-react';

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-8">
      <div className="space-y-2 border-b border-slate-200 pb-4">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Privacy Policy</h1>
        <p className="text-xs text-slate-500">Effective Date: January 1, 2026 &bull; Revizo Learning Platform</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">1. Information We Collect</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          We collect your name, email address, password hash, exam target year, and practice data (test attempts, question responses, time spent, confidence ratings, and mistake history) solely to personalize your adaptive spaced revision schedule.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">2. How We Protect Your Data</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          All passwords are encrypted with bcrypt. We enforce strict database Row-Level Security (RLS) ensuring that your test results, mistake journal, and learning analytics are completely private to your account. We never sell or share your study data with third-party advertisers.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">3. Data Export & Account Deletion</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          You may request an export of your practice records or permanently delete your account at any time in your Settings tab.
        </p>
      </div>
    </div>
  );
}
