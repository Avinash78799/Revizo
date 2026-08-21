'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiRequest, SubjectTree, TestSession } from '@/lib/api';
import {
  Sparkles,
  Layers,
  Clock,
  Shield,
  AlertCircle,
  CheckCircle2,
  Lock,
  ArrowRight,
  Loader2,
  TrendingUp,
  BookOpen,
  Award,
} from 'lucide-react';

interface PatternSummary {
  status: string;
  governance_notice: {
    verified_pyq_count: number;
    disclaimer: string;
    sources_analyzed: string;
  };
  total_historical_patterns: number;
  years_analyzed: number[];
  clinical_vignette_percentage: number;
  subject_distribution: Record<string, number>;
  most_repeated_concepts: Array<{
    id: string;
    internal_id: string;
    concept_name: string;
    subject_name: string;
    exam_year: number;
    frequency_score: number;
    category: string;
    takeaway_pearl: string;
  }>;
}

export default function PyqPatternsPage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [summary, setSummary] = useState<PatternSummary | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<string>('all');
  const [questionCount, setQuestionCount] = useState<number>(20);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [subjData, sumData] = await Promise.all([
          apiRequest<SubjectTree[]>('/taxonomy/tree'),
          apiRequest<PatternSummary>('/historical-patterns/summary'),
        ]);
        setSubjects(subjData || []);
        setSummary(sumData);
      } catch (err) {
        console.error('Failed to load patterns:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleStartPatternTest = async () => {
    setError(null);
    setStarting(true);
    try {
      const payload: any = {
        mode: 'pyq_pattern_test',
        question_count: questionCount,
      };
      if (selectedSubject !== 'all') {
        payload.subject_id = selectedSubject;
      }

      const res = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      router.push(`/test/${res.session_id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create PYQ Pattern test. Please try again.');
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-16 text-center text-xs text-slate-500">
        <Loader2 className="mx-auto h-6 w-6 animate-spin text-brand-600 mb-2" />
        Loading historical pattern blueprints...
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-purple-200 bg-purple-50 px-3 py-1 text-xs font-bold text-purple-800 mb-2">
            <Sparkles className="h-3.5 w-3.5 text-purple-600" />
            PYQ Patterns & Recall Intelligence
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            NEET-PG Pattern-Based Practice
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-1">
            Original clinical test series modeled on multi-source candidate recalls and historical exam trends (2018–2025)
          </p>
        </div>

        <Link
          href="/analytics/historical-trends"
          className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-sm"
        >
          <TrendingUp className="h-4 w-4 text-brand-600" />
          View Historical Trend Analytics &rarr;
        </Link>
      </div>

      {/* Governance Banner */}
      <div className="rounded-2xl border border-purple-200 bg-purple-50/70 p-5 space-y-3">
        <div className="flex items-start gap-3">
          <Shield className="h-5 w-5 text-purple-700 shrink-0 mt-0.5" />
          <div className="space-y-1 text-xs">
            <p className="font-bold text-purple-950">Strict Medical Provenance & Non-Fabrication Policy</p>
            <p className="text-purple-800 leading-relaxed">
              These are <strong>original Revizo practice questions</strong> engineered to mirror frequently tested clinical concepts, drug regimens, and diagnostic criteria. They are <strong>NOT</strong> official past papers.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-2 border-t border-purple-200/60 text-[11px]">
          <div className="flex items-center gap-1.5 text-purple-900 font-medium">
            <span className="h-2 w-2 rounded-full bg-purple-600" />
            <strong>Pattern-Based Practice:</strong> Trend-derived MCQs
          </div>
          <div className="flex items-center gap-1.5 text-purple-900 font-medium">
            <span className="h-2 w-2 rounded-full bg-blue-600" />
            <strong>Corroborated Recall:</strong> Verified across &ge;2 sources
          </div>
          <div className="flex items-center gap-1.5 text-purple-900 font-medium">
            <Lock className="h-3 w-3 text-purple-600" />
            <strong>Verified Official PYQs:</strong> Strictly 0 (Locked)
          </div>
        </div>
      </div>

      {/* Test Configurator */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Layers className="h-4 w-4 text-brand-600" />
          Configure PYQ Pattern Test
        </h2>

        {error && (
          <div className="flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Subject Scope */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700">Subject Coverage</label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full rounded-xl border border-slate-300 p-3 text-xs font-semibold text-slate-800 focus:border-brand-500 focus:outline-none bg-white"
            >
              <option value="all">Grand NEET-PG Pattern Mix (All 19 Subjects)</option>
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </select>
            <p className="text-[11px] text-slate-500">
              {selectedSubject === 'all'
                ? 'Balanced clinical blueprint: 45% Clinical, 35% Para-clinical, 20% Pre-clinical.'
                : 'High-yield questions strictly focused on this subject’s historical patterns.'}
            </p>
          </div>

          {/* Test Size */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700">Number of Questions</label>
            <div className="grid grid-cols-5 gap-2">
              {[10, 15, 20, 30, 50].map((count) => (
                <button
                  key={count}
                  type="button"
                  onClick={() => setQuestionCount(count)}
                  className={`rounded-xl py-2.5 text-xs font-bold transition-all ${
                    questionCount === count
                      ? 'bg-brand-600 text-white shadow-sm ring-2 ring-brand-500 ring-offset-1'
                      : 'border border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {count} Qs
                  {count === 20 && (
                    <span className="block text-[9px] font-normal opacity-90">Standard</span>
                  )}
                  {count === 50 && (
                    <span className="block text-[9px] font-normal opacity-90">Grand</span>
                  )}
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-500">
              Scoring: <strong>+4 / -1 / 0</strong> &bull; Estimated Time: <strong>{questionCount * 1.2} Mins</strong>
            </p>
          </div>
        </div>

        {/* Start Button */}
        <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
          <div className="text-xs text-slate-500 hidden sm:block">
            Server-authoritative timed test session with instant 4-part explanations.
          </div>
          <button
            type="button"
            onClick={handleStartPatternTest}
            disabled={starting}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-8 py-3 text-sm font-bold text-white hover:bg-slate-800 disabled:opacity-50 transition-colors shadow-sm"
          >
            {starting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Generating Pattern Test...
              </>
            ) : (
              <>
                Start {questionCount}-Question Pattern Test <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* High-Yield Historical Patterns Preview */}
      {summary && summary.most_repeated_concepts.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900">
              High-Frequency Concept Highlights (Recent NEET-PG Recalls)
            </h3>
            <span className="text-xs font-semibold text-slate-500">
              {summary.most_repeated_concepts.length} Key Concepts Tested &ge;3 Times
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summary.most_repeated_concepts.slice(0, 6).map((c) => (
              <div
                key={c.id}
                className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm hover:border-brand-300 transition-colors space-y-2.5"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="inline-block rounded-md bg-purple-100 text-purple-900 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider">
                      {c.subject_name}
                    </span>
                    <h4 className="text-xs font-bold text-slate-900 mt-1">{c.concept_name}</h4>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                      Tested {c.frequency_score}x
                    </span>
                    <p className="text-[10px] text-slate-400 mt-0.5">NEET-PG {c.exam_year}</p>
                  </div>
                </div>

                <p className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded-xl border border-slate-100 leading-relaxed">
                  💡 <strong>High-Yield Pearl:</strong> {c.takeaway_pearl}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
