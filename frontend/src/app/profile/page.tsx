'use client';

import React from 'react';
import { useAuth } from '@/lib/auth-context';
import { User, Mail, Calendar, Shield, Award } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900">Aspirant Profile</h1>
        <p className="text-xs text-slate-500 mt-1">Your registered doctor credentials and study preferences.</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
        <div className="flex items-center gap-4 border-b border-slate-100 pb-5">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-slate-900 text-white font-bold text-lg">
            {user.full_name ? user.full_name[0].toUpperCase() : 'Dr'}
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">{user.full_name || 'Dr. Aspirant'}</h2>
            <div className="text-xs text-slate-500">{user.email}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 space-y-1">
            <div className="flex items-center gap-1.5 text-slate-500 font-semibold">
              <Shield className="h-4 w-4 text-slate-400" />
              Account Role
            </div>
            <div className="text-sm font-bold text-slate-900 capitalize">{user.role}</div>
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 space-y-1">
            <div className="flex items-center gap-1.5 text-slate-500 font-semibold">
              <Calendar className="h-4 w-4 text-slate-400" />
              Target Exam Year
            </div>
            <div className="text-sm font-bold text-slate-900">NEET-PG {user.target_exam_year || 2026}</div>
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 space-y-1">
            <div className="flex items-center gap-1.5 text-slate-500 font-semibold">
              <Award className="h-4 w-4 text-slate-400" />
              Daily Practice Target
            </div>
            <div className="text-sm font-bold text-slate-900">{user.daily_question_goal} Questions / Day</div>
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 space-y-1">
            <div className="flex items-center gap-1.5 text-slate-500 font-semibold">
              <User className="h-4 w-4 text-slate-400" />
              Access Level
            </div>
            <div className="text-sm font-bold text-emerald-700">Full Free Practice Access</div>
          </div>
        </div>
      </div>
    </div>
  );
}
