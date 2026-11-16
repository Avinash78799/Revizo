'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  apiRequest,
  TestSession,
  TestSeriesCatalog,
  TestSeriesTemplate,
  TestHistoryItem,
} from '@/lib/api';
import {
  Trophy,
  Play,
  Clock,
  Sparkles,
  BookOpen,
  Calendar,
  AlertCircle,
  Flame,
  CheckCircle2,
  Users,
  Layers,
  ArrowRight,
  History,
  TrendingUp,
  Target,
  Zap,
  Shield,
  Loader2,
} from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function TestsArenaPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'live' | 'subject_wise' | 'quick_drills' | 'history'>('live');
  const [catalog, setCatalog] = useState<TestSeriesCatalog | null>(null);
  const [history, setHistory] = useState<TestHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingId, setStartingId] = useState<string | null>(null);
  const [selectedExamMode, setSelectedExamMode] = useState<'exam' | 'study'>('exam');
  const [filterSubjectSearch, setFilterSubjectSearch] = useState('');

  useEffect(() => {
    async function loadData() {
      try {
        const [catData, histData] = await Promise.all([
          apiRequest<TestSeriesCatalog>('/tests/series'),
          apiRequest<TestHistoryItem[]>('/tests/history').catch(() => []),
        ]);
        setCatalog(catData);
        setHistory(histData || []);
      } catch (err) {
        console.error('Failed to load test catalog:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleStartTemplate = async (template: TestSeriesTemplate) => {
    setStartingId(template.id);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({
          mode: template.mode,
          template_id: template.id.startsWith('swt-') ? null : template.id,
          subject_id: template.subject_id || null,
          question_count: template.question_count,
          duration_minutes: template.time_limit_minutes,
        }),
      });

      // Pass user's preferred runner mode (exam mode vs study mode) via query param
      router.push(`/test/${session.session_id}?studyMode=${selectedExamMode === 'study'}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test session.');
      setStartingId(null);
    }
  };

  const handleStartCustomQuick = async (mode: string, count: number, duration: number) => {
    setStartingId(mode);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({
          mode,
          question_count: count,
          duration_minutes: duration,
        }),
      });
      router.push(`/test/${session.session_id}?studyMode=${selectedExamMode === 'study'}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test.');
      setStartingId(null);
    }
  };

  const filteredSubjectTests = (catalog?.subject_wise_tests || []).filter(
    (t) =>
      t.title.toLowerCase().includes(filterSubjectSearch.toLowerCase()) ||
      (t.subject_code && t.subject_code.toLowerCase().includes(filterSubjectSearch.toLowerCase()))
  );

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-rose-50 border border-rose-200 px-2.5 py-0.5 text-[10px] font-bold text-rose-700 uppercase tracking-wider flex items-center gap-1">
              <Flame className="h-3 w-3 fill-rose-600 text-rose-600 animate-pulse" />
              All-India Live Series
            </span>
            <span className="text-xs text-slate-500">• NBE Pattern Scoring (+4 / -1)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mt-1">
            Test Arena & Live Grand Tests
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
            Participate in scheduled All-India Weekly GTs, 19 Subject-Wise Tests, and calibrated diagnostic simulations.
          </p>
        </div>

        {/* Global Test-Taking Mode Switch */}
        <div className="flex items-center gap-2 rounded-2xl bg-slate-100 p-1.5 border border-slate-200 shrink-0">
          <span className="text-xs font-bold text-slate-700 pl-2">Mode:</span>
          <button
            type="button"
            onClick={() => setSelectedExamMode('exam')}
            className={`rounded-xl px-3 py-1.5 text-xs font-bold transition-all flex items-center gap-1.5 ${
              selectedExamMode === 'exam'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-200'
            }`}
          >
            <Shield className="h-3.5 w-3.5" />
            Exam Simulation
          </button>
          <button
            type="button"
            onClick={() => setSelectedExamMode('study')}
            className={`rounded-xl px-3 py-1.5 text-xs font-bold transition-all flex items-center gap-1.5 ${
              selectedExamMode === 'study'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-200'
            }`}
          >
            <Sparkles className="h-3.5 w-3.5" />
            Tutor / Study Mode
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('live')}
          className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all ${
            activeTab === 'live'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Trophy className="h-4 w-4 text-amber-400" />
          Live & Upcoming Weekly GTs
          {catalog?.live_grand_tests && catalog.live_grand_tests.length > 0 && (
            <span className="rounded-full bg-rose-500 text-white px-1.5 py-0.2 text-[10px] font-bold">
              {catalog.live_grand_tests.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('subject_wise')}
          className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all ${
            activeTab === 'subject_wise'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Layers className="h-4 w-4 text-indigo-500" />
          19 Subject-Wise Tests (SWT)
        </button>

        <button
          onClick={() => setActiveTab('quick_drills')}
          className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all ${
            activeTab === 'quick_drills'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Zap className="h-4 w-4 text-amber-500" />
          Rapid Practice Drills
        </button>

        <button
          onClick={() => setActiveTab('history')}
          className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition-all ${
            activeTab === 'history'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <History className="h-4 w-4 text-emerald-500" />
          My Test History & Scorecards
          {history.length > 0 && (
            <span className="rounded-full bg-slate-200 text-slate-800 px-1.5 py-0.2 text-[10px] font-bold">
              {history.length}
            </span>
          )}
        </button>
      </div>

      {/* TAB 1: LIVE GRAND TESTS */}
      {activeTab === 'live' && (
        <div className="space-y-6">
          <div className="rounded-2xl border-2 border-brand-300 bg-gradient-to-br from-brand-50/70 via-white to-amber-50/50 p-6 sm:p-8 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-brand-100 pb-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-rose-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase tracking-wider animate-pulse">
                    ACTIVE LIVE WINDOW
                  </span>
                  <span className="text-xs text-slate-500 font-medium">Closes Sunday 11:59 PM</span>
                </div>
                <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                  All-India Weekly Grand Test #12 (2026 Season)
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                  Simulate the complete NEET-PG pressure experience. Scored under strict +4 / -1 convention with immediate 4-Quadrant Cognitive Diagnostic breakdown and projected All-India Rank.
                </p>
              </div>

              <div className="rounded-xl border border-brand-200 bg-white p-3 text-center shadow-sm shrink-0">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Aspirants Competing</div>
                <div className="text-xl font-black text-brand-700 flex items-center justify-center gap-1 mt-0.5">
                  <Users className="h-4 w-4 text-brand-600" />
                  4,820+
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                <div className="text-slate-400 font-medium text-[11px]">Question Count</div>
                <div className="font-bold text-slate-900 text-sm mt-0.5">50 High-Yield MCQs</div>
              </div>
              <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                <div className="text-slate-400 font-medium text-[11px]">Test Duration</div>
                <div className="font-bold text-slate-900 text-sm mt-0.5">60 Minutes</div>
              </div>
              <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                <div className="text-slate-400 font-medium text-[11px]">Syllabus Scope</div>
                <div className="font-bold text-slate-900 text-sm mt-0.5">Full 19 Subjects</div>
              </div>
              <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                <div className="text-slate-400 font-medium text-[11px]">Ranking Policy</div>
                <div className="font-bold text-emerald-700 text-sm mt-0.5">Cohort AIR & Percentile</div>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
              <div className="text-xs text-slate-500 font-medium flex items-center gap-1.5">
                <AlertCircle className="h-4 w-4 text-amber-500" />
                Selected Mode: <strong className="text-slate-900 uppercase">{selectedExamMode} MODE</strong> (Change mode at top right)
              </div>

              <button
                type="button"
                disabled={Boolean(startingId)}
                onClick={() =>
                  catalog?.live_grand_tests[0] && handleStartTemplate(catalog.live_grand_tests[0])
                }
                className="flex items-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-xs font-bold text-white shadow hover:bg-slate-800 transition-colors disabled:opacity-50"
              >
                {startingId ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4 fill-white" />}
                START LIVE GRAND TEST #12 &rarr;
              </button>
            </div>
          </div>

          {/* Secondary Live Series Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {(catalog?.live_grand_tests.slice(1) || []).map((t) => (
              <div
                key={t.id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-slate-300 transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-[10px] font-bold text-slate-700 uppercase">
                      {t.badge || 'GRAND TEST'}
                    </span>
                    <div className="flex items-center gap-1 text-[11px] font-bold text-slate-500">
                      <Clock className="h-3 w-3" />
                      {t.time_limit_minutes}m
                    </div>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">{t.title}</h3>
                    <p className="text-xs text-slate-500 mt-1">{t.syllabus_tag}</p>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <div className="flex items-center gap-1">
                      <Target className="h-3.5 w-3.5 text-slate-400" />
                      <span>{t.question_count} MCQs</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="h-3.5 w-3.5 text-slate-400" />
                      <span>{t.total_registered}+ enrolled</span>
                    </div>
                  </div>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(t)}
                  className="w-full rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === t.id ? 'Loading Test...' : 'Start Mock Test'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: 19 SUBJECT-WISE TESTS (SWT) */}
      {activeTab === 'subject_wise' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">19 NMC Subject-Wise Tests (SWT)</h2>
              <p className="text-xs text-slate-500">
                20-question focused tests for every medical discipline with standard time limits and scorecards.
              </p>
            </div>

            <div className="w-full sm:w-64">
              <input
                type="text"
                placeholder="Search subject (e.g. Surgery, OBG)..."
                value={filterSubjectSearch}
                onChange={(e) => setFilterSubjectSearch(e.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredSubjectTests.map((swt) => (
              <div
                key={swt.id}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 uppercase">
                      {swt.subject_code || 'SWT'}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {swt.time_limit_minutes} mins
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-slate-900">{swt.title}</h3>
                  <p className="text-xs text-slate-500 line-clamp-2">{swt.syllabus_tag}</p>
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-600">
                    {swt.question_count} MCQs • +4 / -1
                  </span>
                  <button
                    type="button"
                    disabled={Boolean(startingId)}
                    onClick={() => handleStartTemplate(swt)}
                    className="flex items-center gap-1 rounded-lg bg-slate-900 px-3 py-1.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                  >
                    {startingId === swt.id ? <Loader2 className="h-3 w-3 animate-spin" /> : <Play className="h-3 w-3 fill-white" />}
                    Start SWT
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: RAPID PRACTICE DRILLS */}
      {activeTab === 'quick_drills' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="rounded-2xl border-2 border-brand-200 bg-brand-50/20 p-6 flex flex-col justify-between space-y-5 shadow-sm">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 text-white">
                  <Play className="h-4 w-4 fill-white" />
                </div>
                <div className="text-[11px] font-bold text-slate-600 bg-white px-2 py-0.5 rounded-full border border-slate-200">
                  12 mins
                </div>
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Daily Clinical Quick Test</h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  10 high-yield clinical vignettes spanning active curriculum disciplines. Ideal for daily morning warmups.
                </p>
              </div>
            </div>
            <button
              onClick={() => handleStartCustomQuick('quick_test', 10, 12)}
              disabled={Boolean(startingId)}
              className="w-full rounded-xl bg-brand-600 py-2.5 text-xs font-bold text-white hover:bg-brand-700 transition-colors disabled:opacity-50"
            >
              Start Quick Test (10 MCQs)
            </button>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 flex flex-col justify-between space-y-5 shadow-sm">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-amber-500 text-white">
                  <Sparkles className="h-4 w-4" />
                </div>
                <div className="text-[11px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full">
                  5 mins
                </div>
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">5-Minute Rapid Spaced Revision</h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  Targeted session prioritizing concepts due for SM-2 review, recent mistakes, and Danger Zone misconceptions.
                </p>
              </div>
            </div>
            <button
              onClick={() => handleStartCustomQuick('five_minute_revision', 5, 5)}
              disabled={Boolean(startingId)}
              className="w-full rounded-xl bg-amber-600 py-2.5 text-xs font-bold text-white hover:bg-amber-700 transition-colors disabled:opacity-50"
            >
              Start 5-Min Revision (5 MCQs)
            </button>
          </div>

          <div className="rounded-2xl border border-purple-200 bg-purple-50/30 p-6 flex flex-col justify-between space-y-5 shadow-sm">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-600 text-white">
                  <Target className="h-4 w-4" />
                </div>
                <div className="text-[11px] font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded-full">
                  25 mins
                </div>
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">PYQ Pattern & Recurrence Test</h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  20 questions modeled strictly on repeating 2018–2025 exam trends and multi-source recalls.
                </p>
              </div>
            </div>
            <button
              onClick={() => handleStartCustomQuick('pyq_pattern_test', 20, 25)}
              disabled={Boolean(startingId)}
              className="w-full rounded-xl bg-purple-700 py-2.5 text-xs font-bold text-white hover:bg-purple-800 transition-colors disabled:opacity-50"
            >
              Start PYQ Pattern Test (20 MCQs)
            </button>
          </div>
        </div>
      )}

      {/* TAB 4: MY TEST HISTORY & SCORECARDS */}
      {activeTab === 'history' && (
        <div className="space-y-4">
          <div className="border-b border-slate-100 pb-2">
            <h2 className="text-base font-bold text-slate-900">My Past Test Attempts & Scorecards</h2>
            <p className="text-xs text-slate-500">
              Review your answers, inspect your 4-Quadrant Cognitive review, and retrace mistake explanations.
            </p>
          </div>

          {history.length === 0 ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center space-y-3">
              <CheckCircle2 className="h-10 w-10 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No Tests Completed Yet</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Take a Weekly Grand Test or Subject-Wise Test above to start building your All-India performance record.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-100 rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
              {history.map((h) => (
                <div
                  key={h.session_id}
                  className="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-slate-50 transition-colors"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-700 uppercase">
                        {h.mode.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xs text-slate-400">
                        {h.submitted_at
                          ? new Date(h.submitted_at).toLocaleDateString(undefined, {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })
                          : 'Incomplete'}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-slate-900">{h.title}</h3>
                    <p className="text-xs text-slate-500">
                      {h.completed_questions}/{h.total_questions} MCQs Attempted
                    </p>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <div className="text-lg font-black text-slate-900">
                        {h.score} <span className="text-xs text-slate-400 font-normal">/ {h.max_score}</span>
                      </div>
                      <div className="text-[11px] font-bold text-emerald-600">
                        {h.accuracy_percentage}% Accuracy
                      </div>
                    </div>

                    <Link
                      href={`/test/${h.session_id}/result`}
                      className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors shadow-sm"
                    >
                      View Review &rarr;
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Strategic Notice Banner */}
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-xs text-slate-600 space-y-2">
        <div className="font-bold text-slate-800 flex items-center gap-1.5">
          <AlertCircle className="h-4 w-4 text-slate-500" />
          The Revizo Exam Philosophy: Practice That Truly Prepares You
        </div>
        <p className="text-slate-500 leading-relaxed">
          Unlike standard question banks that prioritize raw memorization of low-yield minutiae, Revizo tests enforce authentic NEET-PG +4 / -1 negative marking, time pacing diagnostics, and active SM-2 spaced repetition for permanent clinical recall.
        </p>
      </div>
    </div>
  );
}
