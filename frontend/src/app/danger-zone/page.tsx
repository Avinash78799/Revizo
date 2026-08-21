'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiRequest, DangerZoneItem, TestSession } from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';
import { AlertOctagon, ShieldCheck, Play, Lightbulb, BookOpen } from 'lucide-react';

export default function DangerZonePage() {
  const [items, setItems] = useState<DangerZoneItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingTest, setStartingTest] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function loadDangerZone() {
      try {
        const data = await apiRequest<DangerZoneItem[]>('/student/danger-zone');
        setItems(data);
      } catch (err) {
        console.error('Failed to load danger zone:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDangerZone();
  }, []);

  const handleStartTargetedTest = async (topicId?: string) => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({
          mode: 'quick_test',
          question_count: 5,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test');
      setStartingTest(false);
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
          <div className="flex items-center gap-2">
            <span className="rounded bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800 uppercase">
              High-Yield Priority
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2 mt-1">
            <AlertOctagon className="h-6 w-6 text-rose-600" />
            Danger Zone Misconceptions
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Concepts where you answered incorrectly with 100% confidence. Addressing these clears false certainties.
          </p>
        </div>

        {items.length > 0 && (
          <button
            onClick={() => handleStartTargetedTest()}
            disabled={startingTest}
            className="flex items-center gap-1.5 rounded-lg bg-rose-600 px-4 py-2 text-xs font-bold text-white hover:bg-rose-700 transition-colors"
          >
            <Play className="h-3.5 w-3.5 fill-white" />
            Retest Danger Concepts
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center space-y-3">
          <ShieldCheck className="h-10 w-10 text-emerald-500 mx-auto" />
          <h2 className="text-base font-bold text-slate-800">No Critical Misconceptions Detected</h2>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            You currently have no high-confidence mistakes. When you answer a question wrong while stating you "Definitely Know" it, the concept is quarantined here for rapid correction.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div
              key={item.concept_id}
              className="rounded-xl border border-rose-200 bg-white p-5 shadow-sm space-y-3"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-rose-100 pb-2.5">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-rose-700">
                    {item.subject_name} &bull; {item.topic_name}
                  </span>
                  <h2 className="text-sm font-bold text-slate-900 mt-0.5">{item.concept_name}</h2>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${
                      item.trigger_type === 'repeated_mistake'
                        ? 'bg-amber-100 text-amber-800'
                        : item.trigger_type === 'overthinking_trap'
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}
                  >
                    {item.trigger_reason || `${item.high_confidence_wrong_count} High-Confidence Error(s)`}
                  </span>
                </div>
              </div>

              {item.clinical_pearl && (
                <div className="rounded-lg border border-amber-200 bg-amber-50/80 p-3 text-xs text-amber-950 flex items-start gap-2">
                  <Lightbulb className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-amber-900">Clinical Correction Pearl:</span>{' '}
                    {item.clinical_pearl}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between pt-1 text-xs">
                <span className="text-slate-400">
                  Last misdiagnosed: {new Date(item.last_practiced_at).toLocaleDateString()}
                </span>

                <button
                  onClick={() => handleStartTargetedTest()}
                  className="flex items-center gap-1 font-bold text-rose-600 hover:text-rose-700"
                >
                  <Play className="h-3 w-3 fill-current" />
                  Retest This Concept
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
