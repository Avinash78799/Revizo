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
  Sparkles,
  BookOpen,
  HelpCircle,
  Flag,
  RotateCcw,
} from 'lucide-react';
import ReportQuestionModal from '@/components/ReportQuestionModal';

export default function TestResultPage({ params }: { params: { id: string } }) {
  const [result, setResult] = useState<TestResultData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'incorrect' | 'correct'>('all');
  const [reportingQuestionId, setReportingQuestionId] = useState<string | null>(null);

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

  const filteredQuestions = question_breakdowns.filter((q) => {
    if (filter === 'incorrect') return !q.is_correct;
    if (filter === 'correct') return q.is_correct;
    return true;
  });

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-[10px] font-bold text-brand-700 uppercase tracking-wider">
              {result.mode.replace(/_/g, ' ')}
            </span>
            <span className="text-xs text-slate-400">&bull; Test Completed</span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 mt-1">Test Result & Detailed Review</h1>
        </div>

        <div className="flex items-center gap-2.5">
          <Link
            href="/practice"
            className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition-colors"
          >
            Practice Another Topic
          </Link>
          <Link
            href="/dashboard"
            className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800 shadow transition-colors"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>

      {/* Encouraging Contextual Banner */}
      <div className="rounded-2xl border border-brand-100 bg-brand-50/60 p-5 space-y-1.5">
        <p className="text-xs font-bold text-brand-900 flex items-center gap-1.5">
          <Sparkles className="h-4 w-4 text-brand-600" />
          Turn Today&apos;s Mistakes Into Permanent Retention
        </p>
        <p className="text-xs text-brand-950 leading-relaxed font-medium">
          Remember: Every mistake you make in practice is a point saved on exam day! Review the 4-part explanations below, read the clinical pearls, and let Revizo schedule them for spaced retesting.
        </p>
      </div>

      {/* Primary Score Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Net Score</div>
          <div className="text-3xl font-black text-slate-900">
            {scoring.score} <span className="text-xs font-normal text-slate-400">/ {scoring.max_possible_score}</span>
          </div>
          <div className="text-[11px] text-slate-500 font-medium">+4 for correct, -1 for wrong</div>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-sm space-y-1">
          <div className="text-xs font-bold text-emerald-700 uppercase tracking-wider">Accuracy</div>
          <div className="text-3xl font-black text-emerald-600">{scoring.accuracy_percentage}%</div>
          <div className="text-[11px] text-slate-500 font-medium">
            {scoring.correct_count} of {scoring.attempted_count} attempted
          </div>
        </div>

        <div className="rounded-2xl border border-rose-200 bg-white p-5 shadow-sm space-y-1">
          <div className="text-xs font-bold text-rose-700 uppercase tracking-wider">Negative Marks</div>
          <div className="text-3xl font-black text-rose-600">-{scoring.incorrect_count}</div>
          <div className="text-[11px] text-slate-500 font-medium">{scoring.incorrect_count} incorrect answers</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Time Spent</div>
          <div className="text-3xl font-black text-slate-900">
            {Math.round(scoring.total_time_seconds / 60)}m
          </div>
          <div className="text-[11px] text-slate-500 font-medium">
            ~{scoring.avg_time_per_question_seconds}s per question
          </div>
        </div>
      </div>

      {/* Action Banner */}
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-slate-800">Filter Explanations:</span>
          <div className="flex gap-1.5">
            <button
              onClick={() => setFilter('all')}
              className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                filter === 'all'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All ({question_breakdowns.length})
            </button>
            <button
              onClick={() => setFilter('incorrect')}
              className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                filter === 'incorrect'
                  ? 'bg-rose-600 text-white'
                  : 'bg-rose-50 text-rose-700 hover:bg-rose-100'
              }`}
            >
              Missed Questions ({scoring.incorrect_count})
            </button>
            <button
              onClick={() => setFilter('correct')}
              className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                filter === 'correct'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
              }`}
            >
              Correct ({scoring.correct_count})
            </button>
          </div>
        </div>

        <Link
          href="/revision"
          className="flex items-center gap-1.5 rounded-lg bg-amber-500 px-4 py-1.5 text-xs font-bold text-white hover:bg-amber-600 shadow-sm transition-colors"
        >
          <Repeat className="h-3.5 w-3.5" />
          View Spaced Revision Queue
        </Link>
      </div>

      {/* Question Review Cards */}
      <div className="space-y-6">
        <h2 className="text-base font-bold text-slate-900">
          Question-by-Question Explanations & Pearls
        </h2>

        {filteredQuestions.map((q, idx) => (
          <div
            key={q.question_id}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4"
          >
            {/* Top Question Row */}
            <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2.5">
                <div
                  className={`flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold text-white ${
                    q.is_correct ? 'bg-emerald-600' : 'bg-rose-600'
                  }`}
                >
                  {idx + 1}
                </div>
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                    {q.concept_name || 'Medical Concept'}
                  </span>
                  <p className="text-xs font-bold text-slate-800">
                    {q.is_correct ? (
                      <span className="text-emerald-700 font-bold">+4 Correct Response</span>
                    ) : (
                      <span className="text-rose-700 font-bold">-1 Incorrect Response</span>
                    )}
                  </p>
                </div>
              </div>

              <div className="text-right text-xs">
                <span className="text-slate-500 font-medium">Your Pick: </span>
                <strong className={q.is_correct ? 'text-emerald-700' : 'text-rose-700'}>
                  Option {q.selected_option_key || 'Skipped'}
                </strong>
                <span className="text-slate-400 mx-1.5">&bull;</span>
                <span className="text-slate-500 font-medium">Correct Key: </span>
                <strong className="text-emerald-700 font-bold">Option {q.correct_option_key}</strong>
              </div>
            </div>

            {/* Question Text */}
            <p className="text-xs sm:text-sm font-semibold text-slate-900 leading-relaxed">
              {q.question_text}
            </p>

            {/* Structured Explanation Breakdown */}
            <div className="space-y-3 pt-2">
              {/* Section 1: Why Correct Key is Right */}
              <div className="rounded-xl border border-emerald-200 bg-emerald-50/40 p-4 space-y-1">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                  Why Option {q.correct_option_key} is Correct
                </h4>
                <p className="text-xs text-emerald-950 leading-relaxed font-medium">
                  {q.correct_explanation}
                </p>
              </div>

              {/* Section 2: High-Yield Takeaway Pearl */}
              {q.remember_takeaway && (
                <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-4 space-y-1">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center gap-1.5">
                    <Sparkles className="h-3.5 w-3.5 text-amber-600" />
                    Remember This (High-Yield Clinical Pearl)
                  </h4>
                  <p className="text-xs text-amber-950 leading-relaxed font-semibold">
                    {q.remember_takeaway}
                  </p>
                </div>
              )}
            </div>

            {/* Footer action */}
            <div className="flex justify-end pt-2 border-t border-slate-100">
              <button
                onClick={() => setReportingQuestionId(q.question_id)}
                className="flex items-center gap-1 text-[11px] font-bold text-slate-400 hover:text-rose-600 transition-colors"
              >
                <Flag className="h-3 w-3" />
                Report this question
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Question Report Modal */}
      {reportingQuestionId && (
        <ReportQuestionModal
          questionId={reportingQuestionId}
          isOpen={Boolean(reportingQuestionId)}
          onClose={() => setReportingQuestionId(null)}
        />
      )}
    </div>
  );
}
