'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiRequest } from '@/lib/api';
import {
  TrendingUp,
  BarChart3,
  Calendar,
  Layers,
  Shield,
  Search,
  Filter,
  Sparkles,
  BookOpen,
  CheckCircle2,
  Lock,
  ArrowLeft,
  Loader2,
} from 'lucide-react';

interface HistoricalPattern {
  id: string;
  internal_id: string;
  concept_name: string;
  subject_name: string;
  exam_year: number;
  frequency_score: number;
  category: string;
  provenance_classification: string;
  source_organization: string;
  corroboration_count: number;
  takeaway_pearl: string;
}

interface TrendSummary {
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
  category_breakdown: Record<string, number>;
  most_repeated_concepts: HistoricalPattern[];
}

export default function HistoricalTrendsPage() {
  const [data, setData] = useState<TrendSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function loadTrends() {
      try {
        const res = await apiRequest<TrendSummary>('/historical-patterns/summary');
        setData(res);
      } catch (err) {
        console.error('Failed to load historical trends:', err);
      } finally {
        setLoading(false);
      }
    }
    loadTrends();
  }, []);

  if (loading || !data) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-16 text-center text-xs text-slate-500">
        <Loader2 className="mx-auto h-6 w-6 animate-spin text-brand-600 mb-2" />
        Loading historical trend models and provenance records...
      </div>
    );
  }

  const filteredConcepts = data.most_repeated_concepts.filter((c) => {
    const matchesYear = selectedYear === 'all' || c.exam_year === Number(selectedYear);
    const matchesCategory = selectedCategory === 'all' || c.category === selectedCategory;
    const matchesSearch =
      searchQuery === '' ||
      c.concept_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.subject_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.takeaway_pearl.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesYear && matchesCategory && matchesSearch;
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500 mb-1">
            <Link href="/practice/pyq-patterns" className="hover:text-slate-800 flex items-center gap-1">
              <ArrowLeft className="h-3 w-3" /> Back to Pattern Practice
            </Link>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            Historical Trend & Recall Analytics
          </h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Multi-year blueprint analysis, recurring clinical pearls, and subject weightage (2018–2025)
          </p>
        </div>

        <Link
          href="/practice/pyq-patterns"
          className="rounded-xl bg-purple-700 px-5 py-2.5 text-xs font-bold text-white hover:bg-purple-800 shadow transition-colors"
        >
          Practice Pattern Test &rarr;
        </Link>
      </div>

      {/* Top Level Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Clinical Vignette Ratio</p>
          <p className="text-3xl font-black text-slate-900">{data.clinical_vignette_percentage}%</p>
          <p className="text-[11px] text-slate-500">Case-based scenarios dominating modern NEET-PG</p>
        </div>

        <div className="rounded-2xl border border-purple-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-purple-700 uppercase tracking-wider">Exam Years Analyzed</p>
          <p className="text-3xl font-black text-purple-900">{data.years_analyzed.length} Sessions</p>
          <p className="text-[11px] text-purple-800">
            {data.years_analyzed.join(', ')}
          </p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-emerald-700 uppercase tracking-wider">Corroborated Patterns</p>
          <p className="text-3xl font-black text-emerald-700">{data.total_historical_patterns}</p>
          <p className="text-[11px] text-slate-500">&ge;2 Independent source reviews</p>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-white p-5 shadow-sm space-y-1">
          <p className="text-xs font-bold text-amber-700 uppercase tracking-wider">Verified Official PYQ</p>
          <p className="text-3xl font-black text-amber-800">0 (Locked)</p>
          <p className="text-[11px] text-amber-900 font-semibold">Strict zero invariant</p>
        </div>
      </div>

      {/* Subject Distribution Matrix */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-brand-600" />
          Subject-Wise Historical High-Yield Density
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {Object.entries(data.subject_distribution).map(([subj, count]) => (
            <div key={subj} className="rounded-xl border border-slate-100 bg-slate-50 p-3 space-y-1">
              <div className="flex items-center justify-between text-xs font-bold text-slate-900">
                <span>{subj}</span>
                <span className="rounded bg-brand-100 text-brand-800 px-1.5 py-0.5 text-[10px]">
                  {count} patterns
                </span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-slate-200 overflow-hidden">
                <div
                  className="h-full bg-brand-600 rounded-full"
                  style={{ width: `${Math.min(100, count * 25)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Searchable Concept Table with Filters */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-purple-600" />
            Most Repeated Medical Concepts & Pearls
          </h2>

          <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
            {/* Search Input */}
            <div className="relative flex-1 sm:w-64">
              <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search concepts or pearls..."
                className="w-full rounded-lg border border-slate-300 py-1.5 pl-8 pr-3 text-xs focus:border-brand-500 focus:outline-none"
              />
            </div>

            {/* Year Filter */}
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="rounded-lg border border-slate-300 py-1.5 px-2.5 text-xs text-slate-700 bg-white focus:outline-none"
            >
              <option value="all">All Years</option>
              {data.years_analyzed.map((y) => (
                <option key={y} value={y}>
                  NEET-PG {y}
                </option>
              ))}
            </select>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="rounded-lg border border-slate-300 py-1.5 px-2.5 text-xs text-slate-700 bg-white focus:outline-none"
            >
              <option value="all">All Categories</option>
              <option value="CLINICAL_APPLICATION">Clinical Application</option>
              <option value="PHARMACOLOGY_REGIMEN">Pharmacology Regimen</option>
              <option value="DIAGNOSTIC_CRITERIA">Diagnostic Criteria</option>
              <option value="INVESTIGATION_OF_CHOICE">Investigation of Choice</option>
            </select>
          </div>
        </div>

        {/* Concept Cards */}
        <div className="space-y-3">
          {filteredConcepts.length === 0 ? (
            <p className="text-xs text-slate-500 py-8 text-center">
              No historical patterns match the selected search filters.
            </p>
          ) : (
            filteredConcepts.map((c) => (
              <div
                key={c.id}
                className="rounded-xl border border-slate-200 p-4 space-y-2 hover:bg-slate-50/60 transition-colors"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="rounded-md bg-purple-100 text-purple-900 px-2 py-0.5 text-[10px] font-bold">
                      {c.subject_name}
                    </span>
                    <span className="rounded-md bg-slate-100 text-slate-700 px-2 py-0.5 text-[10px] font-semibold">
                      {c.category.replace(/_/g, ' ')}
                    </span>
                    <h3 className="text-xs font-bold text-slate-900">{c.concept_name}</h3>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                      Repeated {c.frequency_score}x
                    </span>
                    <span className="text-[10px] text-slate-400 font-medium">NEET-PG {c.exam_year}</span>
                  </div>
                </div>

                <p className="text-xs text-slate-700 bg-amber-50/50 p-2.5 rounded-lg border border-amber-100 leading-relaxed">
                  💡 <strong>Takeaway Pearl:</strong> {c.takeaway_pearl}
                </p>

                <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1">
                  <span>Corroboration: {c.corroboration_count} Independent Reviews</span>
                  <span>Provenance ID: {c.internal_id}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
