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
  Stethoscope,
  Landmark,
  Image as ImageIcon,
  Compass,
  Search,
} from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

type ActiveTab =
  | 'neet_pg_pro'
  | 'medicine_prep'
  | 'inicet'
  | 'fmge_next'
  | 'image_based'
  | 'subject_wise'
  | 'quick_drills'
  | 'history';

export default function TestsArenaPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<ActiveTab>('neet_pg_pro');
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
          template_id: template.id,
          subject_id: template.subject_id || null,
          subject_ids: template.subject_ids || null,
          question_count: template.question_count,
          duration_minutes: template.time_limit_minutes,
          difficulty: template.difficulty || 'all',
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

  const proSeries = catalog?.neet_pg_pro_series && catalog.neet_pg_pro_series.length > 0
    ? catalog.neet_pg_pro_series
    : catalog?.live_grand_tests || [];

  const medicineSeries = catalog?.medicine_prep_series || [];
  const inicetSeries = catalog?.inicet_series || [];
  const fmgeNextSeries = catalog?.fmge_next_series || [];
  const imageBasedSeries = catalog?.image_based_series || [];
  const subjectTests = catalog?.subject_wise_tests || [];
  const quickDrills = catalog?.quick_drills || [];

  const filteredSubjectTests = subjectTests.filter(
    (t) =>
      t.title.toLowerCase().includes(filterSubjectSearch.toLowerCase()) ||
      (t.subject_code && t.subject_code.toLowerCase().includes(filterSubjectSearch.toLowerCase())) ||
      (t.subject_name && t.subject_name.toLowerCase().includes(filterSubjectSearch.toLowerCase()))
  );

  const getDifficultyColor = (diff?: string) => {
    switch (diff?.toLowerCase()) {
      case 'hard':
        return 'text-rose-700 bg-rose-50 border-rose-200';
      case 'moderate':
      case 'medium':
        return 'text-amber-700 bg-amber-50 border-amber-200';
      case 'easy':
        return 'text-emerald-700 bg-emerald-50 border-emerald-200';
      default:
        return 'text-slate-700 bg-slate-50 border-slate-200';
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-rose-50 border border-rose-200 px-2.5 py-0.5 text-[10px] font-bold text-rose-700 uppercase tracking-wider flex items-center gap-1">
              <Flame className="h-3 w-3 fill-rose-600 text-rose-600 animate-pulse" />
              All-India Test Arena
            </span>
            <span className="text-xs text-slate-500">• NBE Pattern Scoring (+4 / -1)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mt-1">
            Standard & Specialty Test Series
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
            Calibrated NBE 4-Section Grand Tests, Clinical Specialty Rounds, AIIMS Apex Vignettes, and 19 NMC Subject-Wise Tests.
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

      {/* Series Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('neet_pg_pro')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'neet_pg_pro'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Trophy className="h-4 w-4 text-amber-400" />
          NEET-PG Pro Series
          {proSeries.length > 0 && (
            <span className="rounded-full bg-rose-500 text-white px-1.5 py-0.2 text-[10px] font-bold">
              {proSeries.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('medicine_prep')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'medicine_prep'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Stethoscope className="h-4 w-4 text-rose-500" />
          NEET Medicine Prep
          {medicineSeries.length > 0 && (
            <span className="rounded-full bg-rose-100 text-rose-800 px-1.5 py-0.2 text-[10px] font-bold">
              {medicineSeries.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('inicet')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'inicet'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Landmark className="h-4 w-4 text-indigo-500" />
          INI-CET Apex Series
          {inicetSeries.length > 0 && (
            <span className="rounded-full bg-indigo-100 text-indigo-800 px-1.5 py-0.2 text-[10px] font-bold">
              {inicetSeries.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('fmge_next')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'fmge_next'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Compass className="h-4 w-4 text-teal-600" />
          FMGE / NExT Series
          {fmgeNextSeries.length > 0 && (
            <span className="rounded-full bg-teal-100 text-teal-800 px-1.5 py-0.2 text-[10px] font-bold">
              {fmgeNextSeries.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('image_based')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'image_based'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <ImageIcon className="h-4 w-4 text-amber-500" />
          Image-Based (IBQ)
          {imageBasedSeries.length > 0 && (
            <span className="rounded-full bg-amber-100 text-amber-800 px-1.5 py-0.2 text-[10px] font-bold">
              {imageBasedSeries.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('subject_wise')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'subject_wise'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Layers className="h-4 w-4 text-blue-500" />
          19 Subject-Wise (SWT)
        </button>

        <button
          onClick={() => setActiveTab('quick_drills')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'quick_drills'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Zap className="h-4 w-4 text-amber-500" />
          Rapid Drills
        </button>

        <button
          onClick={() => setActiveTab('history')}
          className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-bold transition-all ${
            activeTab === 'history'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <History className="h-4 w-4 text-emerald-500" />
          History & Scorecards
          {history.length > 0 && (
            <span className="rounded-full bg-slate-200 text-slate-800 px-1.5 py-0.2 text-[10px] font-bold">
              {history.length}
            </span>
          )}
        </button>
      </div>

      {loading && (
        <div className="py-12 text-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin text-brand-600 mx-auto" />
          <p className="text-sm font-semibold text-slate-600">Loading comprehensive test catalog...</p>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 1. NEET-PG PRO SERIES TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'neet_pg_pro' && (
        <div className="space-y-6">
          {/* Featured NBE Sectional Mock Banner */}
          {proSeries.length > 0 && (
            <div className="rounded-2xl border-2 border-brand-300 bg-gradient-to-br from-brand-50/70 via-white to-amber-50/50 p-6 sm:p-8 shadow-sm space-y-5">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-brand-100 pb-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-rose-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase tracking-wider animate-pulse">
                      {proSeries[0].badge || 'LIVE NOW'}
                    </span>
                    <span className="rounded-full bg-slate-900 px-2 py-0.5 text-[10px] font-bold text-white uppercase">
                      {proSeries[0].test_type || 'NBE 4-SECTION SIMULATION'}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">All-India Cohort Calibrated</span>
                  </div>
                  <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                    {proSeries[0].title}
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                    {proSeries[0].clinical_focus || 'Simulate the full 4-section NBE examination environment with realistic negative marking, timed section pacing, and post-test branch eligibility prediction.'}
                  </p>
                </div>

                <div className="rounded-xl border border-brand-200 bg-white p-3 text-center shadow-sm shrink-0">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Aspirants Registered</div>
                  <div className="text-xl font-black text-brand-700 flex items-center justify-center gap-1 mt-0.5">
                    <Users className="h-4 w-4 text-brand-600" />
                    {proSeries[0].total_registered}+
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                  <div className="text-slate-400 font-medium text-[11px]">Question Count</div>
                  <div className="font-bold text-slate-900 text-sm mt-0.5">{proSeries[0].question_count} High-Yield MCQs</div>
                </div>
                <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                  <div className="text-slate-400 font-medium text-[11px]">Test Duration</div>
                  <div className="font-bold text-slate-900 text-sm mt-0.5">{proSeries[0].time_limit_minutes} Minutes</div>
                </div>
                <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                  <div className="text-slate-400 font-medium text-[11px]">Syllabus Scope</div>
                  <div className="font-bold text-slate-900 text-sm mt-0.5">All 19 Subjects</div>
                </div>
                <div className="rounded-xl bg-white p-3 border border-slate-200 text-xs">
                  <div className="text-slate-400 font-medium text-[11px]">Post-Test Analysis</div>
                  <div className="font-bold text-emerald-700 text-sm mt-0.5">Branch Cutoffs & AIR</div>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div className="text-xs text-slate-500 font-medium flex items-center gap-1.5">
                  <AlertCircle className="h-4 w-4 text-amber-500" />
                  Mode: <strong className="text-slate-900 uppercase">{selectedExamMode} MODE</strong>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(proSeries[0])}
                  className="flex items-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-xs font-bold text-white shadow hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === proSeries[0].id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4 fill-white" />}
                  START NEET-PG PRO GT #1 &rarr;
                </button>
              </div>
            </div>
          )}

          {/* Additional NEET-PG Pro Series Tests */}
          <div>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3">
              Specialized Pro Series Mini-Mocks & Foundations
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {proSeries.slice(1).map((t) => (
                <div
                  key={t.id}
                  className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-2.5">
                    <div className="flex items-center justify-between gap-2">
                      <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-black text-slate-800 uppercase">
                        {t.badge || 'PRO MOCK'}
                      </span>
                      <div className="flex items-center gap-1 text-[11px] font-bold text-slate-500">
                        <Clock className="h-3 w-3" />
                        {t.time_limit_minutes}m
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-bold text-slate-900 leading-snug">{t.title}</h4>
                      <p className="text-xs text-brand-600 font-medium mt-0.5 line-clamp-1">{t.clinical_focus}</p>
                      <p className="text-xs text-slate-500 mt-1 line-clamp-2">{t.syllabus_tag}</p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2 pt-1">
                      <span className="rounded bg-slate-50 border border-slate-200 px-2 py-0.5 text-[10px] font-semibold text-slate-600">
                        {t.question_count} MCQs
                      </span>
                      <span className={`rounded border px-2 py-0.5 text-[10px] font-bold ${getDifficultyColor(t.difficulty)}`}>
                        {(t.difficulty || 'All').toUpperCase()}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        {t.total_registered}+ enrolled
                      </span>
                    </div>
                  </div>

                  <button
                    type="button"
                    disabled={Boolean(startingId)}
                    onClick={() => handleStartTemplate(t)}
                    className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                  >
                    {startingId === t.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5 fill-white" />}
                    Start Test
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 2. NEET MEDICINE PREP SERIES TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'medicine_prep' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-rose-200 bg-gradient-to-r from-rose-50 via-white to-orange-50 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-rose-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase">
                  Harrison 21st Edition Standards
                </span>
                <span className="text-xs text-rose-700 font-semibold">• High-Yield Internal Medicine</span>
              </div>
              <h2 className="text-xl font-black text-slate-900">
                NEET Medicine Clinical Rounds & Specialty Modules
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                Diagnostic decision-making vignettes focused on Cardiology, Neurology, Nephrology, Endocrinology, and Pulmonology/Infectious diseases.
              </p>
            </div>
            <div className="text-right shrink-0">
              <span className="text-xs font-bold text-slate-500">Coverage</span>
              <div className="text-lg font-black text-rose-700">5 Specialty Blocks</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {medicineSeries.map((t) => (
              <div
                key={t.id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-rose-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-rose-50 border border-rose-200 px-2.5 py-0.5 text-[10px] font-black text-rose-700 uppercase">
                      {t.badge || 'MEDICINE'}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {t.time_limit_minutes} mins
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">{t.title}</h3>
                    <div className="text-xs font-semibold text-rose-600 mt-1">{t.clinical_focus}</div>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2">{t.syllabus_tag}</p>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <span className="font-semibold">{t.question_count} MCQs</span>
                    <span>•</span>
                    <span className={`rounded border px-2 py-0.2 text-[10px] font-bold ${getDifficultyColor(t.difficulty)}`}>
                      {(t.difficulty || 'Moderate').toUpperCase()}
                    </span>
                    <span>•</span>
                    <span className="text-slate-400">{t.total_registered}+ enrolled</span>
                  </div>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(t)}
                  className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === t.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5 fill-white" />}
                  Start Clinical Round
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 3. INI-CET & AIIMS ELITE SERIES TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'inicet' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-indigo-200 bg-gradient-to-r from-indigo-50 via-white to-purple-50 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-indigo-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase">
                  AIIMS • PGI • JIPMER Pattern
                </span>
                <span className="text-xs text-indigo-700 font-semibold">• High-Cognitive Load Diagnostics</span>
              </div>
              <h2 className="text-xl font-black text-slate-900">
                INI-CET Apex Series: Clinical Vignettes & Molecular Medicine
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                Tackle two-step diagnostic decision trees, targeted oncology therapeutics, immunohistochemistry stains, and advanced investigative pathology.
              </p>
            </div>
            <div className="text-right shrink-0">
              <span className="text-xs font-bold text-slate-500">Tier</span>
              <div className="text-lg font-black text-indigo-700">Apex High-Difficulty</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {inicetSeries.map((t) => (
              <div
                key={t.id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-indigo-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-indigo-50 border border-indigo-200 px-2.5 py-0.5 text-[10px] font-black text-indigo-700 uppercase">
                      {t.badge || 'INI-CET'}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {t.time_limit_minutes} mins
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">{t.title}</h3>
                    <div className="text-xs font-semibold text-indigo-600 mt-1">{t.clinical_focus}</div>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2">{t.syllabus_tag}</p>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <span className="font-semibold">{t.question_count} MCQs</span>
                    <span>•</span>
                    <span className={`rounded border px-2 py-0.2 text-[10px] font-bold ${getDifficultyColor(t.difficulty)}`}>
                      {(t.difficulty || 'Hard').toUpperCase()}
                    </span>
                    <span>•</span>
                    <span className="text-slate-400">{t.total_registered}+ enrolled</span>
                  </div>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(t)}
                  className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === t.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5 fill-white" />}
                  Start INI-CET Mock
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 4. FMGE / NEXT SERIES TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'fmge_next' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-teal-200 bg-gradient-to-r from-teal-50 via-white to-emerald-50 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-teal-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase">
                  NMC Licensure Blueprint
                </span>
                <span className="text-xs text-teal-700 font-semibold">• Primary & Outpatient Care Focus</span>
              </div>
              <h2 className="text-xl font-black text-slate-900">
                FMGE & NExT Step-1 Clinical Decision Making Series
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                Realistic outpatient case presentations, emergency screening guidelines, first-line antibiotic regimens, and National Health Program schedules.
              </p>
            </div>
            <div className="text-right shrink-0">
              <span className="text-xs font-bold text-slate-500">Exam Blueprint</span>
              <div className="text-lg font-black text-teal-700">NExT Step-1</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {fmgeNextSeries.map((t) => (
              <div
                key={t.id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-teal-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-teal-50 border border-teal-200 px-2.5 py-0.5 text-[10px] font-black text-teal-700 uppercase">
                      {t.badge || 'FMGE / NEXT'}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {t.time_limit_minutes} mins
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">{t.title}</h3>
                    <div className="text-xs font-semibold text-teal-600 mt-1">{t.clinical_focus}</div>
                    <p className="text-xs text-slate-500 mt-1">{t.syllabus_tag}</p>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <span className="font-semibold">{t.question_count} MCQs</span>
                    <span>•</span>
                    <span className={`rounded border px-2 py-0.2 text-[10px] font-bold ${getDifficultyColor(t.difficulty)}`}>
                      {(t.difficulty || 'Moderate').toUpperCase()}
                    </span>
                    <span>•</span>
                    <span className="text-slate-400">{t.total_registered}+ enrolled</span>
                  </div>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(t)}
                  className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === t.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5 fill-white" />}
                  Start NExT Simulation
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 5. IMAGE-BASED QUESTION (IBQ) SERIES TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'image_based' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-amber-200 bg-gradient-to-r from-amber-50 via-white to-orange-50 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-amber-600 px-2.5 py-0.5 text-[10px] font-black text-white uppercase">
                  30%+ of NEET-PG Weightage
                </span>
                <span className="text-xs text-amber-700 font-semibold">• Visual Spotters & Signs</span>
              </div>
              <h2 className="text-xl font-black text-slate-900">
                High-Yield Image-Based Question (IBQ) Masterclass Series
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-2xl">
                Master classical radiological signs on X-Ray / CT / MRI, clinical dermatological lesions and exanthems, and rhythm strip ECG recognition.
              </p>
            </div>
            <div className="text-right shrink-0">
              <span className="text-xs font-bold text-slate-500">Visual Discipline</span>
              <div className="text-lg font-black text-amber-700">Radio + Derm + ECG</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {imageBasedSeries.map((t) => (
              <div
                key={t.id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-amber-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-amber-50 border border-amber-200 px-2.5 py-0.5 text-[10px] font-black text-amber-700 uppercase">
                      {t.badge || 'IBQ SPOTTER'}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {t.time_limit_minutes} mins
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">{t.title}</h3>
                    <div className="text-xs font-semibold text-amber-600 mt-1">{t.clinical_focus}</div>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2">{t.syllabus_tag}</p>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <span className="font-semibold">{t.question_count} MCQs</span>
                    <span>•</span>
                    <span className={`rounded border px-2 py-0.2 text-[10px] font-bold ${getDifficultyColor(t.difficulty)}`}>
                      {(t.difficulty || 'Moderate').toUpperCase()}
                    </span>
                    <span>•</span>
                    <span className="text-slate-400">{t.total_registered}+ enrolled</span>
                  </div>
                </div>

                <button
                  type="button"
                  disabled={Boolean(startingId)}
                  onClick={() => handleStartTemplate(t)}
                  className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {startingId === t.id ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5 fill-white" />}
                  Start IBQ Spotter
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 6. 19 SUBJECT-WISE TESTS (SWT) TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'subject_wise' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">19 NMC Subject-Wise Tests (SWT)</h2>
              <p className="text-xs text-slate-500">
                20-question focused mastery tests for every medical discipline with standard time limits and scorecards.
              </p>
            </div>

            <div className="w-full sm:w-72 relative">
              <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <input
                type="text"
                placeholder="Filter by subject or code (e.g. SURG, OBG)..."
                value={filterSubjectSearch}
                onChange={(e) => setFilterSubjectSearch(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 rounded-xl border border-slate-300 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-brand-500"
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

      {/* ==================================================================== */}
      {/* 7. RAPID PRACTICE DRILLS TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'quick_drills' && (
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
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-purple-600 text-white">
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

      {/* ==================================================================== */}
      {/* 8. MY TEST HISTORY & SCORECARDS TAB */}
      {/* ==================================================================== */}
      {!loading && activeTab === 'history' && (
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