'use client';

import React, { useEffect, useState } from 'react';
import { apiRequest } from '@/lib/api';
import { Shield, Check, AlertOctagon, RefreshCw } from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function AdminReviewQueuePage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const loadQueue = async () => {
    try {
      const data = await apiRequest<any[]>('/admin/review-queue');
      setQuestions(data);
    } catch (err) {
      console.error('Failed to load review queue:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQueue();
  }, []);

  const handlePublish = async (id: string) => {
    setActionLoading(id);
    try {
      await apiRequest(`/admin/questions/${id}/publish`, {
        method: 'POST',
        body: JSON.stringify({ verdict: 'approved', is_high_yield: true }),
      });
      setQuestions((prev) => prev.filter((q) => q.id !== id));
    } catch (err: any) {
      alert(err.message || 'Publish failed');
    } finally {
      setActionLoading(null);
    }
  };

  const handleQuarantine = async (id: string) => {
    setActionLoading(id);
    try {
      await apiRequest(`/admin/questions/${id}/quarantine`, {
        method: 'POST',
        body: JSON.stringify({ reason: 'Medical Reviewer Quarantine' }),
      });
      setQuestions((prev) => prev.filter((q) => q.id !== id));
    } catch (err: any) {
      alert(err.message || 'Quarantine failed');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <Shield className="h-6 w-6 text-amber-600" />
            Medical Review Queue
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Doctor review pipeline for candidate questions before publication into the verified pool.
          </p>
        </div>

        <button
          onClick={() => { setLoading(true); loadQueue(); }}
          className="flex items-center gap-1 text-xs font-semibold text-slate-600 hover:text-slate-900"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Refresh
        </button>
      </div>

      {questions.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
          Review queue is currently empty. No candidate questions awaiting review.
        </div>
      ) : (
        <div className="space-y-4">
          {questions.map((q) => (
            <div key={q.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
                <span className="rounded bg-amber-50 px-2 py-0.5 text-[10px] font-bold text-amber-800 uppercase">
                  Status: {q.status}
                </span>
                <span className="text-xs text-slate-400">ID: {q.id.slice(0, 8)}...</span>
              </div>

              <p className="text-sm font-medium text-slate-900 leading-relaxed">{q.question_text}</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                {q.options?.map((opt: any) => (
                  <div
                    key={opt.option_key}
                    className={`rounded p-2 border ${
                      opt.is_correct
                        ? 'border-emerald-300 bg-emerald-50 text-emerald-950 font-semibold'
                        : 'border-slate-200 bg-slate-50 text-slate-700'
                    }`}
                  >
                    <span className="font-bold mr-1">{opt.option_key}.</span> {opt.option_text}
                  </div>
                ))}
              </div>

              <div className="rounded bg-slate-50 p-3 text-xs text-slate-700 space-y-1">
                <div className="font-bold text-slate-900">Correct Explanation:</div>
                <p>{q.correct_explanation}</p>
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
                <button
                  onClick={() => handleQuarantine(q.id)}
                  disabled={actionLoading === q.id}
                  className="flex items-center gap-1 rounded-lg border border-rose-200 bg-rose-50 px-3 py-1.5 text-xs font-bold text-rose-700 hover:bg-rose-100"
                >
                  <AlertOctagon className="h-3.5 w-3.5" />
                  Quarantine
                </button>
                <button
                  onClick={() => handlePublish(q.id)}
                  disabled={actionLoading === q.id}
                  className="flex items-center gap-1 rounded-lg bg-emerald-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-emerald-700"
                >
                  <Check className="h-3.5 w-3.5" />
                  Approve & Publish
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
