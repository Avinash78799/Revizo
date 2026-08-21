'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiRequest, TestResultData } from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';
import { 
  Trophy, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  AlertTriangle, 
  Repeat, 
  ArrowRight, 
  Lightbulb, 
  ShieldAlert 
} from 'lucide-react';

export default function TestResultPage({ params }: { params: { id: string } }) {
  const [result, setResult] = useState<TestResultData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadResult() {
      try {
        const data = await apiRequest<TestResultData>(`/tests/${params.id}/result`);
        setResult(data);
      } catch (err) {
        console.error('Failed to load test result:', err);
      } finally {
        setLoading(false);
      }
    }
    loadResult();
  }, [params.id]);

  if (loading || !result) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
        </div>
        <Skeleton className="h-64" />
      </div>
    );
  }

  const { scoring, question_breakdowns } = result;
  const confStats = scoring.confidence_breakdown || {};

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 uppercase">
              {result.mode}
            </span>
            <span className="text-xs text-slate-400">&bull; Status: {result.status}</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Test Performance Diagnostics</h1>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/dashboard"
            className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50"
          >
            Dashboard
          </Link>
          <Link
            href="/revision"
            className="flex items-center gap-1.5 rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800"
          >
            <Repeat className="h-3.5 w-3.5" />
            Spaced Revisions
          </Link>
        </div>
      </div>

      {/* Primary Score Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">NEET-PG Score</div>
          <div className="mt-1 text-2xl font-extrabold text-slate-900">
            {scoring.score} <span className="text-xs font-normal text-slate-400">/ {scoring.max_possible_score}</span>
          </div>
          <div className="mt-1 text-[10px] text-slate-400">+4 for correct, -1 for wrong</div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Accuracy</div>
          <div className="mt-1 text-2xl font-extrabold text-emerald-600">
            {scoring.accuracy_percentage}%
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            {scoring.correct_count} correct, {scoring.incorrect_count} incorrect
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Danger Zone Items</div>
          <div className="mt-1 text-2xl font-extrabold text-rose-600">
            {scoring.danger_zone_count}
          </div>
          <div className="mt-1 text-[10px] text-rose-700 font-semibold">Wrong with 100% confidence</div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Total Practice Time</div>
          <div className="mt-1 text-2xl font-extrabold text-slate-900">
            {Math.floor(scoring.total_time_seconds / 60)}m {scoring.total_time_seconds % 60}s
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            ~{scoring.avg_time_per_question_seconds}s per question
          </div>
        </div>
      </div>

      {/* Confidence Analysis Breakdown */}
      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
        <h2 className="text-sm font-bold text-slate-900">Confidence Calibration Analysis</h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div className="rounded-lg border border-slate-100 bg-slate-50 p-3 space-y-1">
            <div className="font-bold text-emerald-800">Definitely Know</div>
            <div className="text-slate-600">
              Total: {confStats['DEFINITELY_KNOW']?.total || 0} &bull; Correct: {confStats['DEFINITELY_KNOW']?.correct || 0}
            </div>
            {confStats['DEFINITELY_KNOW']?.incorrect > 0 && (
              <div className="text-[11px] font-bold text-rose-600">
                {confStats['DEFINITELY_KNOW']?.incorrect} Danger Zone Misconception(s)
              </div>
            )}
          </div>

          <div className="rounded-lg border border-slate-100 bg-slate-50 p-3 space-y-1">
            <div className="font-bold text-brand-800">Somewhat Confident</div>
            <div className="text-slate-600">
              Total: {confStats['SOMEWHAT_CONFIDENT']?.total || 0} &bull; Correct: {confStats['SOMEWHAT_CONFIDENT']?.correct || 0}
            </div>
          </div>

          <div className="rounded-lg border border-slate-100 bg-slate-50 p-3 space-y-1">
            <div className="font-bold text-amber-800">Educated Guess</div>
            <div className="text-slate-600">
              Total: {confStats['GUESSING']?.total || 0} &bull; Correct: {confStats['GUESSING']?.correct || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Question-by-Question Full Review */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-slate-900">Question Review & Structured Explanations</h2>

        <div className="space-y-4">
          {question_breakdowns.map((q, idx) => (
            <div
              key={q.question_id}
              className={`rounded-xl border p-5 space-y-3 bg-white ${
                q.is_danger_zone_item
                  ? 'border-rose-300 ring-1 ring-rose-200'
                  : q.is_correct
                  ? 'border-emerald-200'
                  : 'border-slate-200'
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-500">Q{idx + 1}.</span>
                  <span className="text-xs font-bold text-slate-800">{q.concept_name}</span>
                </div>

                <div className="flex items-center gap-2">
                  {q.is_danger_zone_item && (
                    <span className="flex items-center gap-1 rounded bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                      <ShieldAlert className="h-3 w-3" />
                      Danger Zone
                    </span>
                  )}
                  {q.is_correct ? (
                    <span className="flex items-center gap-1 rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                      <CheckCircle2 className="h-3 w-3" />
                      Correct (+4)
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 rounded bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                      <XCircle className="h-3 w-3" />
                      Incorrect (-1)
                    </span>
                  )}
                </div>
              </div>

              <p className="text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                {q.question_text}
              </p>

              <div className="grid grid-cols-2 gap-2 text-xs pt-1">
                <div className="rounded bg-slate-50 p-2 text-slate-700">
                  <span className="font-semibold text-slate-500">Your Answer:</span> Option {q.selected_option_key || '—'}
                  <span className="text-[10px] text-slate-400 block mt-0.5">Confidence: {q.confidence}</span>
                </div>
                <div className="rounded bg-emerald-50 p-2 text-emerald-950 font-semibold">
                  <span className="font-semibold text-emerald-700">Correct Answer:</span> Option {q.correct_option_key}
                </div>
              </div>

              {/* Rationale */}
              <div className="rounded-lg bg-slate-50/80 p-3 text-xs text-slate-700 space-y-1">
                <div className="font-bold text-slate-900">Why Option {q.correct_option_key} is Correct:</div>
                <p className="leading-relaxed">{q.correct_explanation}</p>
              </div>

              {/* Takeaway */}
              {q.remember_takeaway && (
                <div className="rounded-lg border border-amber-200 bg-amber-50/60 p-2.5 text-xs text-amber-950 flex items-start gap-2">
                  <Lightbulb className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-amber-900">High-Yield Pearl:</span> {q.remember_takeaway}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
