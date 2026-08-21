'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiRequest, DashboardData, SubjectTree } from '@/lib/api';
import {
  BarChart3,
  TrendingUp,
  Target,
  AlertOctagon,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Sparkles,
  BookOpen,
  Calendar,
  Layers,
} from 'lucide-react';

export default function AnalyticsPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [dashData, taxonomy] = await Promise.all([
          apiRequest<DashboardData>('/student/dashboard'),
          apiRequest<SubjectTree[]>('/taxonomy/tree'),
        ]);
        setData(dashData);
        setSubjects(taxonomy);
      } catch (err) {
        console.error('Failed to load analytics:', err);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  if (loading || !data) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-12 text-center text-xs text-slate-500">
        Loading performance analytics...
      </div>
    );
  }

  const correctAttempts = Math.max(0, data.total_questions_attempted - data.total_mistakes_count);
  const negativeMarksLost = data.total_mistakes_count * 1;
  const grossMarksGained = correctAttempts * 4;
  const netEstimatedScore = grossMarksGained - negativeMarksLost;

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Performance Analytics</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Clinical calibration, negative marking audit, and concept retention metrics
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-bold text-brand-800">
          <Target className="h-4 w-4 text-brand-600" />
          NEET-PG Scoring Model (+4 / -1)
        </div>
      </div>

      {/* Top Level Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Overall Accuracy</p>
          <p className="text-3xl font-black text-slate-900">
            {data.total_questions_attempted > 0 ? `${data.overall_accuracy_percentage}%` : '0%'}
          </p>
          <p className="text-[11px] text-slate-500">
            {correctAttempts} Correct &bull; {data.total_mistakes_count} Incorrect
          </p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-emerald-700 uppercase tracking-wider">Net Score Impact</p>
          <p className="text-3xl font-black text-emerald-600">
            {netEstimatedScore >= 0 ? `+${netEstimatedScore}` : netEstimatedScore}
          </p>
          <p className="text-[11px] text-slate-500">
            +{grossMarksGained} gross marks gained
          </p>
        </div>

        <div className="rounded-2xl border border-rose-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-rose-700 uppercase tracking-wider">Negative Marks Lost</p>
          <p className="text-3xl font-black text-rose-600">-{negativeMarksLost}</p>
          <p className="text-[11px] text-rose-800 font-semibold">
            {data.danger_zone_count} overconfidence mistakes
          </p>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-amber-800 uppercase tracking-wider">Spaced Revision Due</p>
          <p className="text-3xl font-black text-amber-600">{data.due_revisions.length}</p>
          <Link href="/revision" className="text-[11px] font-bold text-amber-700 hover:underline inline-block">
            Start 5-min review &rarr;
          </Link>
        </div>
      </div>

      {/* Confidence Calibration Analysis */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-brand-600" />
              Confidence Calibration Curve
            </h2>
            <p className="text-xs text-slate-500">
              Measuring alignment between your subjective confidence and objective medical correctness.
            </p>
          </div>
          <Link
            href="/danger-zone"
            className="rounded-lg bg-rose-50 px-3 py-1.5 text-xs font-bold text-rose-700 hover:bg-rose-100 transition-colors"
          >
            Review Danger Zone ({data.danger_zone_count})
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div className="rounded-xl border border-emerald-200 bg-emerald-50/40 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-900">Definitely Know (100%)</span>
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            </div>
            <p className="text-[11px] text-emerald-950 leading-relaxed font-medium">
              High confidence items that were answered correctly. These represent your rock-solid clinical core knowledge.
            </p>
          </div>

          <div className="rounded-xl border border-amber-200 bg-amber-50/40 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-900">Leaning Towards (50-70%)</span>
              <HelpCircle className="h-4 w-4 text-amber-600" />
            </div>
            <p className="text-[11px] text-amber-950 leading-relaxed font-medium">
              Educated eliminations. Reviewing why the distractors were eliminated transforms these into definite mastery.
            </p>
          </div>

          <div className="rounded-xl border border-rose-200 bg-rose-50/40 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-rose-900">Danger Zone (Overconfidence)</span>
              <AlertOctagon className="h-4 w-4 text-rose-600" />
            </div>
            <p className="text-[11px] text-rose-950 leading-relaxed font-medium">
              Questions marked 100% confident but answered incorrectly. These require immediate distractor analysis.
            </p>
          </div>
        </div>
      </div>

      {/* Weak Areas & Subject Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* High Priority Topics */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-rose-600" />
            Weakest Topics (&lt;70% Mastery)
          </h2>

          {data.weak_areas.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-500">
              <CheckCircle2 className="mx-auto h-6 w-6 text-emerald-500 mb-1" />
              No critical weak areas detected. Maintain consistent practice across all disciplines.
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {data.weak_areas.map((w) => (
                <div key={w.topic_id} className="py-3 flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-bold text-slate-900">{w.topic_name}</p>
                    <p className="text-[10px] text-slate-500">
                      {w.subject_name} &bull; {w.total_attempts} total attempts
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-black text-rose-600">{w.mastery_percentage}%</span>
                    <p className="text-[10px] text-slate-400 font-semibold">Mastery</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 19 Subject Coverage Status */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-brand-600" />
              19-Discipline Coverage
            </h2>
            <Link href="/subjects" className="text-xs font-bold text-brand-600 hover:underline">
              View syllabus &rarr;
            </Link>
          </div>

          <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
            {subjects.map((s) => (
              <div
                key={s.id}
                className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/50 p-2.5 text-xs font-medium text-slate-800"
              >
                <div className="flex items-center gap-2">
                  <span className="rounded-md bg-white border border-slate-200 px-1.5 py-0.5 text-[10px] font-bold text-slate-600">
                    {s.code}
                  </span>
                  <span>{s.name}</span>
                </div>
                <span className="text-[10px] font-bold text-slate-500">
                  {s.chapters?.reduce((acc, ch) => acc + (ch.topics?.length || 0), 0)} Topics
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
