'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, SubjectTree, TestSession } from '@/lib/api';
import {
  BookOpen,
  Sparkles,
  Repeat,
  AlertOctagon,
  Clock,
  ChevronRight,
  Lock,
  Layers,
  Flame,
  ShieldCheck,
  Loader2,
  Calendar,
} from 'lucide-react';

export default function PracticePage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'all' | 'daily' | 'subject' | 'remediation'>('all');
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('');

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const data = await apiRequest<SubjectTree[]>('/taxonomy/tree');
      setSubjects(data);
      if (data.length > 0) setSelectedSubjectId(data[0].id);
    } catch {
      // Fallback
    }
  };

  const startTest = async (mode: string, subjectId?: string, questionCount: number = 10) => {
    setLoading(true);
    try {
      const session = await apiRequest<TestSession>('/tests/generate', {
        method: 'POST',
        body: JSON.stringify({
          mode,
          subject_id: subjectId || null,
          total_questions: questionCount,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test session.');
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Choose Your Practice</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Medically reviewed question bank with standard +4 / -1 NEET-PG scoring
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-800">
          <ShieldCheck className="h-4 w-4 text-emerald-600" />
          891 Verified Practice Questions
        </div>
      </div>

      {/* Practice Mode Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* 1. Daily Short Test */}
        <div className="rounded-2xl border border-brand-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-brand-400 hover:shadow-md transition-all">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-50 text-brand-700 font-bold">
                ⚡
              </div>
              <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-[10px] font-bold text-brand-700">
                Recommended Daily
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900">Daily Short Test</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              10 high-yield clinical questions sampled across high-frequency exam topics to maintain daily test readiness.
            </p>
            <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
              <span className="flex items-center gap-1">
                <BookOpen className="h-3 w-3" /> 10 Questions
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" /> ~12 Mins
              </span>
              <span className="font-semibold text-emerald-600">+4 / -1</span>
            </div>
          </div>
          <button
            onClick={() => startTest('daily_short_test', undefined, 10)}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-brand-600 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'START DAILY TEST'}
          </button>
        </div>

        {/* 2. Mistake Retest */}
        <div className="rounded-2xl border border-rose-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-rose-400 hover:shadow-md transition-all">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-rose-50 text-rose-700 font-bold">
                🎯
              </div>
              <span className="rounded-full bg-rose-50 px-2.5 py-0.5 text-[10px] font-bold text-rose-700">
                Mistake Intelligence
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900">Mistake Retest</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Targeted session re-testing your previously missed questions and weak concepts until mastered.
            </p>
            <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
              <span className="flex items-center gap-1">
                <BookOpen className="h-3 w-3" /> 10 Questions
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" /> ~10 Mins
              </span>
            </div>
          </div>
          <button
            onClick={() => startTest('mistake_retest', undefined, 10)}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-rose-600 py-2.5 text-xs font-bold text-white hover:bg-rose-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'RETEST MISTAKES'}
          </button>
        </div>

        {/* 3. Danger Zone Retest */}
        <div className="rounded-2xl border border-amber-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-amber-400 hover:shadow-md transition-all">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-700 font-bold">
                🚨
              </div>
              <span className="rounded-full bg-amber-50 px-2.5 py-0.5 text-[10px] font-bold text-amber-800">
                Confidence Calibration
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900">Danger Zone Test</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Dedicated re-test of high-confidence mistakes to eliminate costly misconceptions and negative marking.
            </p>
            <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
              <span className="flex items-center gap-1">
                <BookOpen className="h-3 w-3" /> 10 Questions
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" /> ~12 Mins
              </span>
            </div>
          </div>
          <button
            onClick={() => startTest('danger_zone_test', undefined, 10)}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-amber-600 py-2.5 text-xs font-bold text-white hover:bg-amber-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'START DANGER ZONE TEST'}
          </button>
        </div>

        {/* 4. Subject-Wise Test */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-slate-300 transition-all">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-slate-700 font-bold">
                📚
              </div>
              <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-[10px] font-bold text-slate-700">
                19 Subjects
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900">Subject Practice Test</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Drill deep into a specific medical discipline with customized clinical question sets.
            </p>
            <select
              value={selectedSubjectId}
              onChange={(e) => setSelectedSubjectId(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-2 text-xs font-medium text-slate-800 bg-white focus:border-brand-500 focus:outline-none"
            >
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={() => startTest('subject_test', selectedSubjectId, 15)}
            disabled={loading || !selectedSubjectId}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'START SUBJECT TEST (15 Qs)'}
          </button>
        </div>

        {/* 5. Full Grand Mock Test */}
        <div className="rounded-2xl border border-indigo-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-indigo-300 transition-all">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-50 text-indigo-700 font-bold">
                🏆
              </div>
              <span className="rounded-full bg-indigo-50 px-2.5 py-0.5 text-[10px] font-bold text-indigo-700">
                Exam Simulation
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900">Weekly Grand Test</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Multi-subject clinical simulation with strict timed conditions, question navigator, and calibration analytics.
            </p>
            <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
              <span className="flex items-center gap-1">
                <BookOpen className="h-3 w-3" /> 25 Questions
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" /> ~30 Mins
              </span>
            </div>
          </div>
          <button
            onClick={() => startTest('grand_test', undefined, 25)}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-indigo-600 py-2.5 text-xs font-bold text-white hover:bg-indigo-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'START GRAND TEST'}
          </button>
        </div>

        {/* 6. Past-Year Questions (PYQ) — Strictly LOCKED */}
        <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-6 space-y-4 flex flex-col justify-between opacity-80">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-200 text-slate-600">
                <Lock className="h-4 w-4" />
              </div>
              <span className="rounded-full bg-slate-200 px-2.5 py-0.5 text-[10px] font-bold text-slate-700">
                0 Verified (Locked)
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-800">Past-Year Questions (PYQ)</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Verified PYQ practice is not currently available. Revizo strictly prohibits synthetic recall claims until authentic official master papers pass provenance verification.
            </p>
          </div>
          <button
            disabled
            className="w-full flex items-center justify-center gap-1.5 rounded-xl border border-slate-300 bg-slate-200 py-2.5 text-xs font-bold text-slate-500 cursor-not-allowed"
          >
            <Lock className="h-3.5 w-3.5" /> MODULE CURRENTLY LOCKED
          </button>
        </div>
      </div>
    </div>
  );
}
