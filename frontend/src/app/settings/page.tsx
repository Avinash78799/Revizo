'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import {
  Settings as SettingsIcon,
  User,
  Bell,
  Lock,
  Download,
  Trash2,
  CheckCircle2,
  Shield,
  Loader2,
} from 'lucide-react';

export default function SettingsPage() {
  const { user } = useAuth();
  const [dailyGoal, setDailyGoal] = useState(user?.daily_question_goal || 10);
  const [targetYear, setTargetYear] = useState(user?.target_exam_year || 2026);
  const [revisionReminders, setRevisionReminders] = useState(true);
  const [weeklyDigest, setWeeklyDigest] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleExportData = () => {
    const dataStr = JSON.stringify(
      {
        user: {
          id: user?.id,
          email: user?.email,
          full_name: user?.full_name,
          target_exam_year: user?.target_exam_year,
        },
        exportDate: new Date().toISOString(),
        note: 'Revizo Student Data Export',
      },
      null,
      2
    );
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `revizo-study-records-${user?.id || 'student'}.json`;
    a.click();
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Settings & Preferences</h1>
        <p className="text-xs sm:text-sm text-slate-600">
          Manage your NEET-PG exam target, learning goals, notifications, and data privacy
        </p>
      </div>

      {saved && (
        <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-xs font-bold text-emerald-900 animate-in fade-in">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>Your preferences have been saved successfully.</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Learning Goals */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <User className="h-4 w-4 text-brand-600" />
            Exam Target & Learning Goals
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Target NEET-PG Year</label>
              <select
                value={targetYear}
                onChange={(e) => setTargetYear(Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none bg-white"
              >
                <option value={2026}>NEET-PG 2026</option>
                <option value={2027}>NEET-PG 2027</option>
                <option value={2028}>NEET-PG 2028</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Daily Question Practice Goal</label>
              <select
                value={dailyGoal}
                onChange={(e) => setDailyGoal(Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none bg-white"
              >
                <option value={5}>5 Questions / day (Sprint)</option>
                <option value={10}>10 Questions / day (Standard)</option>
                <option value={20}>20 Questions / day (Intensive)</option>
                <option value={30}>30 Questions / day (Grand Revision)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Notifications & Reminders */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Bell className="h-4 w-4 text-brand-600" />
            Revision Notifications & Reminders
          </h2>

          <div className="space-y-3">
            <label className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 cursor-pointer">
              <div>
                <p className="text-xs font-bold text-slate-800">Spaced Revision Reminders</p>
                <p className="text-[11px] text-slate-500">Notify when high-yield concepts reach their review interval.</p>
              </div>
              <input
                type="checkbox"
                checked={revisionReminders}
                onChange={(e) => setRevisionReminders(e.target.checked)}
                className="h-4 w-4 rounded text-brand-600 focus:ring-brand-500"
              />
            </label>

            <label className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 cursor-pointer">
              <div>
                <p className="text-xs font-bold text-slate-800">Weekly Performance Digest</p>
                <p className="text-[11px] text-slate-500">Summary of accuracy, danger zone reduction, and concept mastery.</p>
              </div>
              <input
                type="checkbox"
                checked={weeklyDigest}
                onChange={(e) => setWeeklyDigest(e.target.checked)}
                className="h-4 w-4 rounded text-brand-600 focus:ring-brand-500"
              />
            </label>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            className="rounded-xl bg-brand-600 px-6 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow transition-colors"
          >
            Save Preferences
          </button>
        </div>
      </form>

      {/* Privacy & Data Management */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Shield className="h-4 w-4 text-slate-600" />
          Privacy & Data Management
        </h2>

        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
          <div>
            <p className="text-xs font-bold text-slate-900">Export Practice & Mistake Records</p>
            <p className="text-[11px] text-slate-500">
              Download your complete test logs, mistake journal, and confidence history as a JSON file.
            </p>
          </div>
          <button
            onClick={handleExportData}
            className="flex items-center gap-1.5 rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-sm"
          >
            <Download className="h-3.5 w-3.5" />
            Export Data
          </button>
        </div>
      </div>
    </div>
  );
}
