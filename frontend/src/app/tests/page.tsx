'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, TestSession } from '@/lib/api';
import { Play, Sparkles, BookOpen, Clock, AlertCircle } from 'lucide-react';

export default function TestsLauncherPage() {
  const [loadingMode, setLoadingMode] = useState<string | null>(null);
  const router = useRouter();

  const handleStart = async (mode: string, count: number) => {
    setLoadingMode(mode);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({ mode, question_count: count }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start practice test');
      setLoadingMode(null);
    }
  };

  const testModes = [
    {
      id: 'quick_test',
      title: 'Daily Quick Test',
      count: 5,
      duration: '10 mins',
      desc: 'Rapid 5-question sprint covering high-yield verified clinical vignettes.',
      icon: Play,
      buttonText: 'Start Quick Test (5 MCQs)',
      highlight: true,
    },
    {
      id: 'five_minute_revision',
      title: '5-Minute Rapid Revision',
      count: 5,
      duration: '5 mins',
      desc: 'Targeted session prioritizing concepts due for review, recent mistakes, and Danger Zone items.',
      icon: Sparkles,
      buttonText: 'Start 5-Min Revision (5 MCQs)',
      highlight: false,
    },
    {
      id: 'topic_test',
      title: 'Deep Topic Practice Sprint',
      count: 10,
      duration: '15 mins',
      desc: 'Focused 10-question practice across active curriculum topics.',
      icon: BookOpen,
      buttonText: 'Start Topic Sprint (10 MCQs)',
      highlight: false,
    },
  ];

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900">Practice & Mock Tests</h1>
        <p className="text-xs text-slate-500 mt-1">
          Server-authoritative testing with structured explanations and instant diagnostic feedback.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {testModes.map((mode) => {
          const Icon = mode.icon;
          const isLoading = loadingMode === mode.id;

          return (
            <div
              key={mode.id}
              className={`rounded-2xl border p-6 flex flex-col justify-between space-y-5 transition-all ${
                mode.highlight
                  ? 'border-brand-300 bg-brand-50/20 shadow-md ring-1 ring-brand-200'
                  : 'border-slate-200 bg-white shadow-sm hover:border-slate-300'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 text-white">
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="flex items-center gap-1 text-[11px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full">
                    <Clock className="h-3 w-3" />
                    {mode.duration}
                  </div>
                </div>

                <div>
                  <h2 className="text-base font-bold text-slate-900">{mode.title}</h2>
                  <p className="text-xs text-slate-600 mt-1 leading-relaxed">{mode.desc}</p>
                </div>
              </div>

              <button
                onClick={() => handleStart(mode.id, mode.count)}
                disabled={Boolean(loadingMode)}
                className={`w-full rounded-lg py-2.5 text-xs font-bold transition-colors ${
                  mode.highlight
                    ? 'bg-brand-600 text-white hover:bg-brand-700'
                    : 'bg-slate-900 text-white hover:bg-slate-800'
                } disabled:opacity-50`}
              >
                {isLoading ? 'Preparing Test...' : mode.buttonText}
              </button>
            </div>
          );
        })}
      </div>

      <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs text-slate-600 space-y-1.5">
        <div className="font-bold text-slate-800 flex items-center gap-1.5">
          <AlertCircle className="h-4 w-4 text-slate-500" />
          Test-Taking Guidelines
        </div>
        <ul className="list-disc list-inside space-y-0.5 text-slate-500 pl-1">
          <li>Options and explanations are verified server-side; answers lock upon submission.</li>
          <li>Marking your confidence level calibrates your spaced repetition intervals and flags Danger Zone misconceptions.</li>
          <li>You can immediately review why your chosen option was correct or incorrect before proceeding.</li>
        </ul>
      </div>
    </div>
  );
}
