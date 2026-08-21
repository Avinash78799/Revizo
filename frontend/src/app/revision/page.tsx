'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, DueRevisionItem, TestSession } from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';
import { Repeat, Sparkles, CheckCircle2, Calendar, Check, ArrowRight } from 'lucide-react';

export default function SpacedRevisionPage() {
  const [dueItems, setDueItems] = useState<DueRevisionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingRevision, setStartingRevision] = useState(false);
  const router = useRouter();

  const loadRevisions = async () => {
    try {
      const data = await apiRequest<DueRevisionItem[]>('/revision/due');
      setDueItems(data);
    } catch (err) {
      console.error('Failed to load revisions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRevisions();
  }, []);

  const handleStart5MinSession = async () => {
    setStartingRevision(true);
    try {
      const session = await apiRequest<TestSession>('/revision/five-minute-session', {
        method: 'POST',
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start revision session');
      setStartingRevision(false);
    }
  };

  const handleCompleteItem = async (conceptId: string) => {
    try {
      await apiRequest('/revision/complete', {
        method: 'POST',
        body: JSON.stringify({ concept_id: conceptId }),
      });
      setDueItems((prev) => prev.filter((item) => item.concept_id !== conceptId));
    } catch (err: any) {
      alert(err.message || 'Failed to update revision status');
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <Repeat className="h-6 w-6 text-amber-600" />
            Spaced Revision Engine
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Adaptive SM-2 interval scheduling to guarantee long-term retention of high-yield facts.
          </p>
        </div>

        <button
          onClick={handleStart5MinSession}
          disabled={startingRevision || dueItems.length === 0}
          className="flex items-center gap-1.5 rounded-lg bg-amber-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-amber-700 disabled:opacity-50 transition-colors"
        >
          <Sparkles className="h-4 w-4" />
          {startingRevision ? 'Loading...' : 'Start 5-Min Rapid Revision'}
        </button>
      </div>

      {dueItems.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center space-y-3">
          <CheckCircle2 className="h-10 w-10 text-emerald-500 mx-auto" />
          <h2 className="text-base font-bold text-slate-800">You're All Caught Up</h2>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            No scheduled concept revisions due right now. Keep practicing questions to feed the adaptive spaced repetition scheduler.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="text-xs font-semibold text-slate-600">
            {dueItems.length} concept(s) ready for spaced review today:
          </div>

          <div className="divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
            {dueItems.map((item) => (
              <div
                key={item.concept_id}
                className="flex flex-wrap items-center justify-between gap-4 p-4 hover:bg-slate-50/60 transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 uppercase">
                      {item.subject_name}
                    </span>
                    <span className="text-xs text-slate-400">&bull; {item.topic_name}</span>
                  </div>
                  <h2 className="text-sm font-bold text-slate-900">{item.concept_name}</h2>
                  <div className="text-[11px] text-slate-500 flex items-center gap-1">
                    <Calendar className="h-3 w-3 text-slate-400" />
                    Interval: {item.revision_interval_days} day(s)
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleCompleteItem(item.concept_id)}
                    className="flex items-center gap-1 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:border-slate-300"
                  >
                    <Check className="h-3.5 w-3.5 text-emerald-600" />
                    Mark Reviewed
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
