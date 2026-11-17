'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiRequest, TestResultData, TestSession } from '@/lib/api';
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
  Zap,
  Target,
  Layers,
  TrendingUp,
  Brain,
  AlertOctagon,
  ChevronRight,
  Loader2,
  Award,
  Stethoscope,
  GraduationCap,
  Check,
} from 'lucide-react';
import ReportQuestionModal from '@/components/ReportQuestionModal';

export default function TestResultPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [result, setResult] = useState<TestResultData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'incorrect' | 'correct'>('all');
  const [reportingQuestionId, setReportingQuestionId] = useState<string | null>(null);
  const [remediating, setRemediating] = useState(false);

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

  const handleRemediateLeakyTopics = async () => {
    if (!result?.leaky_concepts || result.leaky_concepts.length === 0) return;
    setRemediating(true);
    try {
      // Launch a focused 10-question sprint targeting due concepts / mistakes
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({
          mode: 'mistake_retest',
          question_count: 10,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start remediation drill.');
      setRemediating(false);
    }
  };

  if (loading || !result) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
        </div>
        <Skeleton className="h-64" />
      </div>
    );
  }

  const scoring = result.scoring || {
    score: 0,
    max_possible_score: (result.question_breakdowns?.length || 0) * 4,
    accuracy_percentage: 0,
    calibration_percentage: 0,
    correct_count: 0,
    incorrect_count: 0,
    unanswered_count: 0,
    total_time_seconds: 0,
    avg_time_per_question_seconds: 0,
    attempted_count: result.question_breakdowns?.length || 0,
    danger_zone_count: 0,
    total_questions: result.question_breakdowns?.length || 0,
    confidence_breakdown: {},
  };

  const ranking = result.ranking;
  const quadrants = result.cognitive_quadrants || {
    genius_count: 0,
    slow_correct_count: 0,
    silly_mistake_count: 0,
    sinkhole_count: 0,
    moderate_mistake_count: 0,
    silly_marks_lost: 0,
  };
  const subjects = result.subject_breakdown || [];
  const leakyConcepts = result.leaky_concepts || [];
  const questionBreakdowns = result.question_breakdowns || [];

  const filteredQuestions = questionBreakdowns.filter((q) => {
    if (filter === 'incorrect') return !q.is_correct;
    if (filter === 'correct') return q.is_correct;
    return true;
  });

  const displayMode = (result.mode || 'Practice Test').replace(/_/g, ' ');

  const totalMaxScore = scoring.max_possible_score || (questionBreakdowns.length * 4) || 40;
  const rawScore = scoring.score || 0;
  const projectedScore800 = Math.max(0, Math.min(800, Math.round((rawScore / totalMaxScore) * 800)));

  const calculateAIR = (score800: number) => {
    if (score800 >= 720) return { air: Math.max(1, Math.round(1 + (800 - score800) * 1.2)), percentile: 99.9, label: 'Single/Double Digit Rank' };
    if (score800 >= 660) return { air: Math.round(100 + (720 - score800) * 8), percentile: 99.6, label: 'Top AIQ Elite' };
    if (score800 >= 620) return { air: Math.round(580 + (660 - score800) * 25), percentile: 99.0, label: 'Top Clinical Contender' };
    if (score800 >= 570) return { air: Math.round(1580 + (620 - score800) * 60), percentile: 97.2, label: 'High Demand Specialties' };
    if (score800 >= 520) return { air: Math.round(4580 + (570 - score800) * 110), percentile: 94.5, label: 'Core Clinical Specialties' };
    if (score800 >= 470) return { air: Math.round(10080 + (520 - score800) * 150), percentile: 90.0, label: 'Broad Specialties' };
    if (score800 >= 420) return { air: Math.round(17580 + (470 - score800) * 220), percentile: 82.5, label: 'Para-Clinical / DNB' };
    if (score800 >= 350) return { air: Math.round(28580 + (420 - score800) * 350), percentile: 72.0, label: 'State Quota Contender' };
    return { air: Math.min(185000, Math.round(53080 + (350 - score800) * 450)), percentile: Math.max(15, Math.round((score800 / 350) * 65)), label: 'Revision Required' };
  };

  const standing = calculateAIR(projectedScore800);
  const sillyMarks = quadrants.silly_marks_lost || 0;
  const potentialScore800 = Math.min(800, Math.round(((rawScore + sillyMarks) / totalMaxScore) * 800));
  const potentialStanding = calculateAIR(potentialScore800);
  const airJump = Math.max(0, standing.air - potentialStanding.air);

  const CLINICAL_BRANCHES = [
    { name: 'MD Radiodiagnosis', minScore: 635, targetAIR: 1500, category: 'Top Clinical' },
    { name: 'MD General Medicine', minScore: 610, targetAIR: 2800, category: 'Top Clinical' },
    { name: 'MD Dermatology (DVL)', minScore: 600, targetAIR: 3500, category: 'Top Clinical' },
    { name: 'MD Pediatrics', minScore: 570, targetAIR: 6000, category: 'High Demand' },
    { name: 'MS Orthopedics', minScore: 545, targetAIR: 8500, category: 'Surgical Specialty' },
    { name: 'MS Obstetrics & Gynecology', minScore: 535, targetAIR: 9500, category: 'Surgical Specialty' },
    { name: 'MS General Surgery', minScore: 520, targetAIR: 11000, category: 'Core Surgical' },
    { name: 'MD Anesthesiology', minScore: 480, targetAIR: 16500, category: 'Broad Specialty' },
    { name: 'MD Pathology', minScore: 430, targetAIR: 24000, category: 'Diagnostic Pillar' },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-8">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-[10px] font-bold text-brand-700 uppercase tracking-wider">
              {displayMode}
            </span>
            <span className="text-xs text-slate-400">• Test Completed</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 mt-1">
            Diagnostic Scorecard & Cognitive Review
          </h1>
        </div>

        <div className="flex items-center gap-2.5">
          <Link
            href="/tests"
            className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
          >
            Take Another Test
          </Link>
          <Link
            href="/dashboard"
            className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800 shadow transition-colors"
          >
            Dashboard
          </Link>
        </div>
      </div>

      {/* 🏆 ALL-INDIA RANKING & PERCENTILE BANNER */}
      {ranking && ranking.is_enabled && (
        <div className="rounded-2xl border-2 border-amber-300 bg-gradient-to-r from-amber-500/10 via-brand-50/20 to-emerald-500/10 p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-amber-200/60 pb-3">
            <div className="flex items-center gap-2.5">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500 text-white shadow-sm">
                <Trophy className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">All-India Benchmarking & Standing</h3>
                <p className="text-xs text-slate-500">{ranking.disclaimer}</p>
              </div>
            </div>

            <span className="rounded-full bg-emerald-100 text-emerald-800 px-3 py-1 text-xs font-bold">
              {ranking.percentile}th Percentile
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            <div className="rounded-xl bg-white p-3 border border-amber-200 shadow-xs">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Projected AIR</div>
              <div className="text-xl sm:text-2xl font-black text-slate-900 mt-0.5">
                #{ranking.projected_air.toLocaleString()}
              </div>
              <div className="text-[10px] text-slate-400">among 200k aspirants</div>
            </div>

            <div className="rounded-xl bg-white p-3 border border-amber-200 shadow-xs">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Your Net Score</div>
              <div className="text-xl sm:text-2xl font-black text-brand-700 mt-0.5">
                {scoring.score}
              </div>
              <div className="text-[10px] text-slate-400">out of {scoring.max_possible_score}</div>
            </div>

            <div className="rounded-xl bg-white p-3 border border-amber-200 shadow-xs">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Cohort Topper</div>
              <div className="text-xl sm:text-2xl font-black text-emerald-700 mt-0.5">
                {ranking.topper_score}
              </div>
              <div className="text-[10px] text-slate-400">top score achieved</div>
            </div>

            <div className="rounded-xl bg-white p-3 border border-amber-200 shadow-xs">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Average Score</div>
              <div className="text-xl sm:text-2xl font-black text-slate-600 mt-0.5">
                {ranking.average_score}
              </div>
              <div className="text-[10px] text-slate-400">cohort average</div>
            </div>
          </div>
        </div>
      )}

      {/* Primary Score Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 sm:gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Net Score</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {scoring.score} <span className="text-xs font-normal text-slate-400">/ {scoring.max_possible_score || (questionBreakdowns.length * 4)}</span>
          </div>
          <div className="text-[11px] text-slate-500 font-medium">+4 correct, -1 wrong</div>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-4 shadow-sm space-y-1">
          <div className="text-xs font-bold text-emerald-700 uppercase tracking-wider">Accuracy</div>
          <div className="text-2xl sm:text-3xl font-black text-emerald-600">{scoring.accuracy_percentage}%</div>
          <div className="text-[11px] text-slate-500 font-medium">
            {scoring.correct_count}/{scoring.attempted_count || questionBreakdowns.length} attempted
          </div>
        </div>

        <div className="rounded-2xl border border-brand-200 bg-white p-4 shadow-sm space-y-1">
          <div className="text-xs font-bold text-brand-700 uppercase tracking-wider">Calibration</div>
          <div className="text-2xl sm:text-3xl font-black text-brand-600">
            {scoring.calibration_percentage ?? scoring.accuracy_percentage}%
          </div>
          <div className="text-[11px] text-slate-500 font-medium">Confidence alignment</div>
        </div>

        <div className="rounded-2xl border border-rose-200 bg-white p-4 shadow-sm space-y-1">
          <div className="text-xs font-bold text-rose-700 uppercase tracking-wider">Negative Marks</div>
          <div className="text-2xl sm:text-3xl font-black text-rose-600">-{scoring.incorrect_count}</div>
          <div className="text-[11px] text-slate-500 font-medium">{scoring.incorrect_count} incorrect</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm space-y-1">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Time Spent</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {Math.round((scoring.total_time_seconds || 0) / 60)}m
          </div>
          <div className="text-[11px] text-slate-500 font-medium">
            ~{scoring.avg_time_per_question_seconds || 0}s / MCQ
          </div>
        </div>
      </div>

      {/* 🎯 NEET-PG STANDING & CLINICAL BRANCH CUTOFF PREDICTOR */}
      <div className="rounded-2xl border-2 border-brand-200 bg-white p-6 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-600 text-white shadow-sm">
              <Stethoscope className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-slate-900">
                  NEET-PG Branch Eligibility & All-India Standing Predictor
                </h2>
                <span className="rounded-full bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                  NBE 800-Mark Scale
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Calibrated against All-India 50% Quota (AIQ) Government Medical College closing ranks.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="text-right">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Projected Score</div>
              <div className="text-xl sm:text-2xl font-black text-brand-700">
                {projectedScore800} <span className="text-xs font-normal text-slate-400">/ 800</span>
              </div>
            </div>
            <div className="h-8 w-px bg-slate-200 mx-1" />
            <div className="text-right">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Projected AIR</div>
              <div className="text-xl sm:text-2xl font-black text-slate-900">
                #{standing.air.toLocaleString()}
              </div>
            </div>
          </div>
        </div>

        {/* Clinical Branch Eligibility Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {CLINICAL_BRANCHES.map((b) => {
            const isSafe = projectedScore800 >= b.minScore;
            const isBorderline = !isSafe && projectedScore800 >= (b.minScore - 35);
            const scoreGap = b.minScore - projectedScore800;

            let badgeBg = 'bg-slate-50 border-slate-200 text-slate-600';
            let statusPill = (
              <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-500">
                Gap: -{scoreGap} marks
              </span>
            );

            if (isSafe) {
              badgeBg = 'bg-emerald-50/60 border-emerald-200 text-emerald-950 ring-1 ring-emerald-500/20';
              statusPill = (
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-black text-emerald-800 flex items-center gap-1">
                  <Check className="h-3 w-3 text-emerald-600" /> Likely Seat (Safe)
                </span>
              );
            } else if (isBorderline) {
              badgeBg = 'bg-amber-50/60 border-amber-200 text-amber-950 ring-1 ring-amber-500/20';
              statusPill = (
                <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-900 flex items-center gap-1">
                  <TrendingUp className="h-3 w-3 text-amber-600" /> Competitive (-{scoreGap}m)
                </span>
              );
            }

            return (
              <div
                key={b.name}
                className={`rounded-xl border p-3.5 space-y-2 transition-all shadow-xs ${badgeBg}`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    {b.category}
                  </span>
                  {statusPill}
                </div>

                <div>
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">{b.name}</h4>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 mt-1">
                    <span>Cutoff Score: &ge;<strong>{b.minScore}</strong>/800</span>
                    <span>Target AIR &le;<strong>#{b.targetAIR.toLocaleString()}</strong></span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Mark Recovery Projection Callout */}
        {sillyMarks > 0 && (
          <div className="rounded-xl border border-amber-300 bg-amber-50/80 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs shadow-xs">
            <div className="space-y-0.5">
              <div className="font-bold text-amber-950 flex items-center gap-1.5">
                <Zap className="h-4 w-4 text-amber-600" />
                Silly Mistake Recovery: +{sillyMarks} Marks = Potential Score {potentialScore800}/800
              </div>
              <div className="text-amber-800 text-[11px]">
                Eliminating rushed answers (&lt;30s) propels your projected All India Rank from #{standing.air.toLocaleString()} to #{potentialStanding.air.toLocaleString()} &mdash; jumping <strong>+{airJump.toLocaleString()} ranks</strong>!
              </div>
            </div>
            <span className="rounded-lg bg-amber-600 text-white font-bold px-3.5 py-1.5 shrink-0 text-xs shadow-xs">
              +{airJump.toLocaleString()} Ranks Leap
            </span>
          </div>
        )}
      </div>

      {/* 🧠 4-QUADRANT COGNITIVE TIME-ACCURACY DIAGNOSTIC MATRIX */}
      <div className="rounded-2xl border-2 border-indigo-200 bg-white p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Brain className="h-5 w-5 text-indigo-600" />
              4-Quadrant Cognitive Diagnostic Matrix
            </h2>
            <p className="text-xs text-slate-500">
              Correlating response velocity with medical correctness to isolate high-yield score improvement opportunities.
            </p>
          </div>
          {quadrants.silly_marks_lost > 0 && (
            <span className="rounded-full bg-rose-100 text-rose-800 px-3 py-1 text-xs font-bold flex items-center gap-1">
              <Zap className="h-3.5 w-3.5 text-rose-600" />
              +{quadrants.silly_marks_lost} Marks Recoverable
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Quadrant 1: Concept Mastery */}
          <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-900 uppercase">Concept Mastery</span>
              <span className="rounded-full bg-emerald-200 text-emerald-900 px-2 py-0.5 text-xs font-bold">
                {quadrants.genius_count} MCQs
              </span>
            </div>
            <div className="text-[11px] text-emerald-950 font-medium leading-snug">
              <strong>Correct & Fast (&lt;45s):</strong> Solidified clinical instincts. These facts are deeply locked in long-term memory.
            </div>
          </div>

          {/* Quadrant 2: Overthinking / Inefficient */}
          <div className="rounded-xl border border-amber-200 bg-amber-50/50 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-900 uppercase">High Time Cost</span>
              <span className="rounded-full bg-amber-200 text-amber-900 px-2 py-0.5 text-xs font-bold">
                {quadrants.slow_correct_count} MCQs
              </span>
            </div>
            <div className="text-[11px] text-amber-950 font-medium leading-snug">
              <strong>Correct but Slow (&ge;45s):</strong> You knew the concept, but second-guessing burned valuable exam clock time.
            </div>
          </div>

          {/* Quadrant 3: Silly Mistake Zone */}
          <div className="rounded-xl border-2 border-rose-300 bg-rose-50/70 p-4 space-y-2 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-black text-rose-900 uppercase flex items-center gap-1">
                <AlertOctagon className="h-3.5 w-3.5 text-rose-600" /> Silly Mistakes
              </span>
              <span className="rounded-full bg-rose-600 text-white px-2 py-0.5 text-xs font-black">
                {quadrants.silly_mistake_count} MCQs
              </span>
            </div>
            <div className="text-[11px] text-rose-950 font-semibold leading-snug">
              <strong>Incorrect & Rushed (&lt;30s):</strong> Careless reading or hasty clicking. Fixing these delivers immediate +{quadrants.silly_marks_lost} marks!
            </div>
          </div>

          {/* Quadrant 4: Knowledge Sinkhole */}
          <div className="rounded-xl border border-slate-300 bg-slate-50 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-800 uppercase">Knowledge Sinkhole</span>
              <span className="rounded-full bg-slate-200 text-slate-800 px-2 py-0.5 text-xs font-bold">
                {quadrants.sinkhole_count} MCQs
              </span>
            </div>
            <div className="text-[11px] text-slate-700 font-medium leading-snug">
              <strong>Incorrect & Long (&ge;45s):</strong> True concept blindspots. You struggled through the vignette and still missed it.
            </div>
          </div>
        </div>
      </div>

      {/* 🚀 LEAKY BUCKET CONCEPT PRESCRIPTION */}
      {leakyConcepts.length > 0 && (
        <div className="rounded-2xl border-2 border-brand-200 bg-brand-50/40 p-6 space-y-4 shadow-sm">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div>
              <span className="rounded-full bg-brand-100 text-brand-800 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider">
                Targeted Remediation Prescription
              </span>
              <h3 className="text-base font-bold text-slate-900 mt-1">
                Top Concepts Costing You Marks in This Test
              </h3>
              <p className="text-xs text-slate-600">
                These specific high-yield concepts caused 70%+ of your score penalty today.
              </p>
            </div>

            <button
              type="button"
              disabled={remediating}
              onClick={handleRemediateLeakyTopics}
              className="flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow transition-colors disabled:opacity-50 shrink-0"
            >
              {remediating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              Remediate These Concepts (10 MCQs) &rarr;
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {leakyConcepts.map((con, idx) => (
              <div key={con.concept_id} className="rounded-xl border border-brand-200 bg-white p-4 space-y-1.5 shadow-xs">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-brand-700">#{idx + 1} {con.subject_name}</span>
                  <span className="rounded bg-rose-50 px-1.5 py-0.5 text-[10px] font-bold text-rose-700">
                    -{con.marks_lost} marks lost
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-900 leading-snug">{con.concept_name}</h4>
                <p className="text-[11px] text-slate-500">{con.mistakes_count} mistake(s) logged</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 📊 SUBJECT-WISE PERFORMANCE BREAKDOWN */}
      {subjects.length > 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">Subject-Wise Performance Breakdown</h2>
              <p className="text-xs text-slate-500">
                Sorted by net score impact to expose which medical disciplines require immediate revision.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-[11px] font-bold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Subject</th>
                  <th className="py-2.5 px-3 text-center">MCQs</th>
                  <th className="py-2.5 px-3 text-center">Correct</th>
                  <th className="py-2.5 px-3 text-center">Incorrect</th>
                  <th className="py-2.5 px-3 text-center">Accuracy</th>
                  <th className="py-2.5 px-3 text-center">Avg Time</th>
                  <th className="py-2.5 px-3 text-right">Net Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {subjects.map((s) => (
                  <tr key={s.subject_name} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-3 font-bold text-slate-900 flex items-center gap-2">
                      <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold text-slate-600">
                        {s.subject_code}
                      </span>
                      {s.subject_name}
                    </td>
                    <td className="py-3 px-3 text-center text-slate-700 font-semibold">{s.total_questions}</td>
                    <td className="py-3 px-3 text-center text-emerald-600 font-bold">+{s.correct_count}</td>
                    <td className="py-3 px-3 text-center text-rose-600 font-bold">-{s.incorrect_count}</td>
                    <td className="py-3 px-3 text-center font-bold text-slate-800">{s.accuracy_percentage}%</td>
                    <td className="py-3 px-3 text-center text-slate-500 font-medium">
                      ~{s.total_questions > 0 ? Math.round(s.time_spent_seconds / s.total_questions) : 0}s
                    </td>
                    <td className="py-3 px-3 text-right font-black text-slate-900">
                      <span className={s.score >= 0 ? 'text-emerald-700' : 'text-rose-700'}>
                        {s.score >= 0 ? `+${s.score}` : s.score}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Filter Action Row */}
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
              All ({questionBreakdowns.length})
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
          Question-by-Question Explanations & Clinical Pearls
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
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      {q.concept_name || 'Medical Concept'}
                    </span>
                    {q.is_broadened_pool && (
                      <span className="rounded-md bg-amber-50 border border-amber-200 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                        {q.scope_note || 'Related Subject Question'}
                      </span>
                    )}
                  </div>
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
            <div className="flex items-center justify-between pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={async () => {
                  try {
                    const session = await apiRequest<{ session_id: string }>(`/student/questions/${q.question_id}/similar`, {
                      method: 'POST',
                    });
                    window.location.href = `/test/${session.session_id}`;
                  } catch {
                    alert('Failed to launch similar practice question');
                  }
                }}
                className="flex items-center gap-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 px-3 py-1.5 text-xs font-bold text-slate-800 transition-colors"
              >
                <Sparkles className="h-3.5 w-3.5 text-brand-600" />
                Practice Similar MCQ
              </button>

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
