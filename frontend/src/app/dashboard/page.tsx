'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { apiRequest, DashboardData, TestSession } from '@/lib/api';
import { DashboardSkeleton } from '@/components/Skeleton';
import { 
  Play, 
  Repeat, 
  AlertTriangle, 
  History, 
  TrendingUp, 
  CheckCircle2, 
  ArrowRight,
  Sparkles,
  BookOpen
} from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [startingTest, setStartingTest] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const dashboardData = await apiRequest<DashboardData>('/student/dashboard');
        setData(dashboardData);
      } catch (err) {
        console.error('Failed to load dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  const handleStartQuickTest = async () => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({ mode: 'quick_test', question_count: 5 }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test');
      setStartingTest(false);
    }
  };

  const handleStartFiveMinRevision = async () => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/revision/five-minute-session', {
        method: 'POST',
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start revision');
      setStartingTest(false);
    }
  };

  if (loading || !data) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Welcome back, {user?.full_name || 'Dr. Aspirant'}
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Targeting NEET-PG {user?.target_exam_year || 2026} • Daily Goal: {user?.daily_question_goal || 10} Questions
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleStartFiveMinRevision}
            disabled={startingTest}
            className="flex items-center gap-1.5 rounded-lg border border-amber-300 bg-amber-50 px-3.5 py-2 text-xs font-bold text-amber-900 hover:bg-amber-100 transition-colors"
          >
            <Sparkles className="h-4 w-4 text-amber-600" />
            5-Min Rapid Revision
          </button>

          <button
            onClick={handleStartQuickTest}
            disabled={startingTest}
            className="flex items-center gap-1.5 rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-slate-800 transition-colors"
          >
            <Play className="h-4 w-4 fill-white" />
            Start Daily Practice
          </button>
        </div>
      </div>

      {/* Top Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Daily Target</div>
          <div className="mt-1 text-2xl font-extrabold text-slate-900">
            {data.todays_practice_count} <span className="text-xs font-normal text-slate-400">Questions</span>
          </div>
          <div className="mt-1 text-[11px] text-slate-500">~{data.todays_practice_est_minutes} min practice time</div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Revisions Due</div>
          <div className="mt-1 text-2xl font-extrabold text-amber-600">
            {data.due_revisions.length} <span className="text-xs font-normal text-slate-400">Concepts</span>
          </div>
          <Link href="/revision" className="mt-1 inline-flex items-center gap-1 text-[11px] font-semibold text-amber-700 hover:underline">
            Review due items &rarr;
          </Link>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Danger Zone</div>
          <div className="mt-1 text-2xl font-extrabold text-rose-600">
            {data.danger_zone_count} <span className="text-xs font-normal text-slate-400">Misconceptions</span>
          </div>
          <Link href="/danger-zone" className="mt-1 inline-flex items-center gap-1 text-[11px] font-semibold text-rose-700 hover:underline">
            Inspect & correct &rarr;
          </Link>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="text-xs font-medium text-slate-500">Accuracy & Practice</div>
          <div className="mt-1 text-2xl font-extrabold text-slate-900">
            {data.total_questions_attempted > 0 ? `${data.overall_accuracy_percentage}%` : '—'}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            {data.total_questions_attempted} attempts ({data.total_mistakes_count} mistakes)
          </div>
        </div>
      </div>

      {/* Main Content Sections: Due Revisions & Weak Areas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Due Concepts Spaced Repetition */}
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Repeat className="h-4 w-4 text-amber-600" />
              <h2 className="text-sm font-bold text-slate-900">Due for Spaced Review</h2>
            </div>
            <Link href="/revision" className="text-xs font-semibold text-brand-600 hover:underline">
              View all
            </Link>
          </div>

          {data.due_revisions.length === 0 ? (
            <div className="rounded-lg bg-slate-50 p-6 text-center text-xs text-slate-500">
              <CheckCircle2 className="h-6 w-6 text-emerald-500 mx-auto mb-1.5" />
              You are caught up on all scheduled concept revisions!
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {data.due_revisions.slice(0, 4).map((item) => (
                <div key={item.concept_id} className="py-2.5 flex items-center justify-between gap-3">
                  <div>
                    <div className="text-xs font-bold text-slate-800">{item.concept_name}</div>
                    <div className="text-[10px] text-slate-500">{item.subject_name} &bull; {item.topic_name}</div>
                  </div>
                  <span className="shrink-0 rounded bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                    Due Today
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Weak Concepts Matrix */}
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-rose-600" />
              <h2 className="text-sm font-bold text-slate-900">High-Yield Priority Topics (&lt;70%)</h2>
            </div>
            <Link href="/subjects" className="text-xs font-semibold text-brand-600 hover:underline">
              Browse syllabus
            </Link>
          </div>

          {data.weak_areas.length === 0 ? (
            <div className="rounded-lg bg-slate-50 p-6 text-center text-xs text-slate-500">
              <CheckCircle2 className="h-6 w-6 text-emerald-500 mx-auto mb-1.5" />
              No critical weak areas identified yet. Keep practicing across subjects.
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {data.weak_areas.slice(0, 4).map((area) => (
                <div key={area.topic_id} className="py-2.5 flex items-center justify-between gap-3">
                  <div>
                    <div className="text-xs font-bold text-slate-800">{area.topic_name}</div>
                    <div className="text-[10px] text-slate-500">{area.subject_name} &bull; {area.total_attempts} attempts</div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-bold text-rose-600">{area.mastery_percentage}%</span>
                    <div className="text-[10px] text-slate-400">Mastery</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Quick Launch Practice Modes */}
      <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
        <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-slate-700" />
          Select Practice Mode
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <Link
            href="/tests"
            className="rounded-lg border border-slate-200 p-4 hover:border-brand-500 hover:bg-brand-50/20 transition-all group"
          >
            <div className="text-xs font-bold text-slate-900 group-hover:text-brand-600 flex items-center justify-between">
              Quick Test Sprint
              <ArrowRight className="h-3.5 w-3.5" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">5 Questions &bull; 10 Minutes &bull; Mixed High-Yield</p>
          </Link>

          <Link
            href="/subjects"
            className="rounded-lg border border-slate-200 p-4 hover:border-brand-500 hover:bg-brand-50/20 transition-all group"
          >
            <div className="text-xs font-bold text-slate-900 group-hover:text-brand-600 flex items-center justify-between">
              Topic-Wise Practice
              <ArrowRight className="h-3.5 w-3.5" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Target specific high-yield pharmacology or pathology concepts</p>
          </Link>

          <Link
            href="/mistakes"
            className="rounded-lg border border-slate-200 p-4 hover:border-brand-500 hover:bg-brand-50/20 transition-all group"
          >
            <div className="text-xs font-bold text-slate-900 group-hover:text-brand-600 flex items-center justify-between">
              Mistake Bank Re-Test
              <ArrowRight className="h-3.5 w-3.5" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Review and re-test past errors to turn weaknesses into strength</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
