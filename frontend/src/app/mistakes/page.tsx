'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, MistakeItem, TestSession } from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';
import { History, Play, CheckCircle2, AlertOctagon, Lightbulb } from 'lucide-react';

export default function MistakeBankPage() {
  const [mistakes, setMistakes] = useState<MistakeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingTest, setStartingTest] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function loadMistakes() {
      try {
        const data = await apiRequest<MistakeItem[]>('/student/mistakes');
        setMistakes(data);
      } catch (err) {
        console.error('Failed to load mistakes:', err);
      } finally {
        setLoading(false);
      }
    }
    loadMistakes();
  }, []);

  const handlePracticeMistakes = async () => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({ mode: 'quick_test', question_count: 5 }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start practice');
      setStartingTest(false);
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <History className="h-6 w-6 text-slate-700" />
            Mistake Bank
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Active recall review of questions answered incorrectly during practice.
          </p>
        </div>

        {mistakes.length > 0 && (
          <button
            onClick={handlePracticeMistakes}
            disabled={startingTest}
            className="flex items-center gap-1.5 rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800 transition-colors"
          >
            <Play className="h-3.5 w-3.5 fill-white" />
            Practice Mistakes ({mistakes.length})
          </button>
        )}
      </div>

      {mistakes.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center space-y-3">
          <CheckCircle2 className="h-10 w-10 text-emerald-500 mx-auto" />
          <h2 className="text-base font-bold text-slate-800">Your Mistake Bank is Empty</h2>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Keep practicing high-yield tests. Any questions you miss will automatically appear here for active recall and re-testing.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {mistakes.map((m) => (
            <div
              key={m.attempt_id}
              className={`rounded-xl border p-5 space-y-3 bg-white ${
                m.is_danger_zone ? 'border-rose-300 ring-1 ring-rose-200' : 'border-slate-200'
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-800">{m.concept_name}</span>
                  <span className="text-[10px] text-slate-400">&bull; Selected Option {m.selected_option_key || '—'}</span>
                </div>

                <div className="flex items-center gap-2">
                  {m.is_danger_zone && (
                    <span className="flex items-center gap-1 rounded bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                      <AlertOctagon className="h-3 w-3" />
                      Danger Zone
                    </span>
                  )}
                  <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] text-slate-600 font-medium">
                    Confidence: {m.confidence}
                  </span>
                </div>
              </div>

              <p className="text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                {m.question_text}
              </p>

              <div className="rounded-lg bg-emerald-50/70 p-3 text-xs text-emerald-950 space-y-1">
                <span className="font-bold text-emerald-800">Correct Explanation:</span>
                <p className="leading-relaxed">{m.correct_explanation}</p>
              </div>

              {m.remember_takeaway && (
                <div className="rounded-lg border border-amber-200 bg-amber-50/70 p-2.5 text-xs text-amber-950 flex items-start gap-2">
                  <Lightbulb className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-amber-900">Takeaway Pearl:</span> {m.remember_takeaway}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
