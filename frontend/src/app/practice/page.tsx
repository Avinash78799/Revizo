'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, SubjectTree, Chapter, Topic, TestSession } from '@/lib/api';
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
  Filter,
  Zap,
  Target,
  Sliders,
} from 'lucide-react';

export default function PracticePage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('');
  const [selectedChapterId, setSelectedChapterId] = useState<string>('');
  const [selectedTopicId, setSelectedTopicId] = useState<string>('');
  const [targetFocus, setTargetFocus] = useState<string>('all'); // 'all', 'high_yield', 'mistakes', 'danger_zone', 'due_revision'
  const [difficultyTier, setDifficultyTier] = useState<string>('all'); // 'all', 'core', 'hard'
  const [questionCount, setQuestionCount] = useState<number>(10);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTaxonomy();
  }, []);

  const loadTaxonomy = async () => {
    try {
      const data = await apiRequest<SubjectTree[]>('/taxonomy/tree');
      setSubjects(data);
      if (data.length > 0) {
        setSelectedSubjectId(data[0].id);
        if (data[0].chapters && data[0].chapters.length > 0) {
          setSelectedChapterId(data[0].chapters[0].id);
          if (data[0].chapters[0].topics && data[0].chapters[0].topics.length > 0) {
            setSelectedTopicId(data[0].chapters[0].topics[0].id);
          }
        }
      }
    } catch {
      // Fallback
    }
  };

  const currentSubject = subjects.find((s) => s.id === selectedSubjectId);
  const availableChapters = currentSubject?.chapters || [];
  const currentChapter = availableChapters.find((c) => c.id === selectedChapterId);
  const availableTopics = currentChapter?.topics || [];

  const handleSubjectChange = (subjId: string) => {
    setSelectedSubjectId(subjId);
    const subj = subjects.find((s) => s.id === subjId);
    if (subj?.chapters && subj.chapters.length > 0) {
      setSelectedChapterId(subj.chapters[0].id);
      if (subj.chapters[0].topics && subj.chapters[0].topics.length > 0) {
        setSelectedTopicId(subj.chapters[0].topics[0].id);
      } else {
        setSelectedTopicId('');
      }
    } else {
      setSelectedChapterId('');
      setSelectedTopicId('');
    }
  };

  const handleChapterChange = (chapId: string) => {
    setSelectedChapterId(chapId);
    const chap = availableChapters.find((c) => c.id === chapId);
    if (chap?.topics && chap.topics.length > 0) {
      setSelectedTopicId(chap.topics[0].id);
    } else {
      setSelectedTopicId('');
    }
  };

  const startTest = async (mode: string, subjectId?: string, count: number = 10) => {
    setLoading(true);
    try {
      let resolvedMode = mode;
      if (selectedTopicId) resolvedMode = 'topic_test';
      else if (selectedChapterId) resolvedMode = 'chapter_test';
      else if (selectedSubjectId) resolvedMode = 'subject_test';

      if (targetFocus === 'mistakes') resolvedMode = 'mistake_retest';
      else if (targetFocus === 'danger_zone') resolvedMode = 'danger_zone_retest';
      else if (targetFocus === 'due_revision') resolvedMode = 'five_minute_revision';

      const session = await apiRequest<TestSession>('/tests/generate', {
        method: 'POST',
        body: JSON.stringify({
          mode: resolvedMode,
          subject_id: selectedSubjectId || null,
          chapter_id: selectedChapterId || null,
          topic_id: selectedTopicId || null,
          question_count: count,
          total_questions: count,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start test session.');
      setLoading(false);
    }
  };

  const startRapidRevision = async (minutes: number, count: number) => {
    setLoading(true);
    try {
      const session = await apiRequest<TestSession>('/tests/generate', {
        method: 'POST',
        body: JSON.stringify({
          mode: 'five_minute_revision',
          total_questions: count,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start rapid revision.');
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Practice & Custom Test Builder</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Build custom MCQ sessions by subject, topic, difficulty, or target your active mistakes and due revisions.
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-800">
          <ShieldCheck className="h-4 w-4 text-emerald-600" />
          871 Medically Reviewed Questions
        </div>
      </div>

      {/* 🚀 Feature 10: Rapid Revision Sprints */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Zap className="h-4 w-4 text-amber-600" />
            Rapid Timed Revision Modes
          </h2>
          <span className="text-xs text-slate-500">Pulls High-Yield + Due Spaced Revisions</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { min: 10, q: 10, title: '10-Min Power Drill', desc: '10 Targeted MCQs' },
            { min: 15, q: 15, title: '15-Min Focused Block', desc: '15 High-Yield Concepts' },
            { min: 20, q: 20, title: '20-Min Clinical Sprint', desc: '20 Mixed Clinicals' },
            { min: 30, q: 30, title: '30-Min Mini Mock', desc: '30 Comprehensive Questions' },
          ].map((item) => (
            <button
              key={item.min}
              type="button"
              disabled={loading}
              onClick={() => startRapidRevision(item.min, item.q)}
              className="rounded-2xl border border-amber-200 bg-amber-50/50 p-4 text-left hover:bg-amber-100/70 hover:border-amber-400 transition-all shadow-sm flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between text-xs font-bold text-amber-900">
                  <span>{item.min} Minutes</span>
                  <Clock className="h-3.5 w-3.5 text-amber-600" />
                </div>
                <div className="mt-1 text-sm font-bold text-slate-900">{item.title}</div>
                <div className="text-[11px] text-slate-600 mt-0.5">{item.desc}</div>
              </div>
              <div className="mt-3 text-[11px] font-bold text-amber-800 flex items-center gap-1">
                Start Sprint &rarr;
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* 🎯 Feature 2: Advanced Custom Test Builder */}
      <div className="rounded-2xl border-2 border-brand-200 bg-white p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
              <Sliders className="h-4 w-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Advanced Custom Test Builder</h2>
              <p className="text-xs text-slate-500">Tailor question sources, discipline scope, and difficulty</p>
            </div>
          </div>
          <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-[10px] font-bold text-brand-700">
            Precision Practice
          </span>
        </div>

        {/* 1. Target Focus Filters */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-700">Focus Target:</label>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
            {[
              { id: 'all', label: 'All Questions', icon: Target },
              { id: 'high_yield', label: 'High-Yield Only', icon: Sparkles },
              { id: 'mistakes', label: 'Mistake Bank Only', icon: Repeat },
              { id: 'danger_zone', label: 'Danger Zone Only', icon: AlertOctagon },
              { id: 'due_revision', label: 'Due for Revision', icon: Calendar },
            ].map((tgt) => {
              const Icon = tgt.icon;
              return (
                <button
                  key={tgt.id}
                  type="button"
                  onClick={() => setTargetFocus(tgt.id)}
                  className={`flex items-center gap-1.5 rounded-xl border p-2.5 text-xs font-bold transition-all ${
                    targetFocus === tgt.id
                      ? 'border-brand-600 bg-brand-50 text-brand-900 shadow-sm'
                      : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <Icon className="h-3.5 w-3.5 text-brand-600 shrink-0" />
                  <span className="truncate">{tgt.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* 2. Taxonomy Selectors (Subject -> Chapter -> Topic) */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">1. Discipline / Subject (19 Available)</label>
            <select
              value={selectedSubjectId}
              onChange={(e) => handleSubjectChange(e.target.value)}
              className="w-full rounded-xl border border-slate-300 p-2.5 text-xs font-semibold text-slate-800 bg-white focus:border-brand-500 focus:outline-none"
            >
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">2. Chapter</label>
            <select
              value={selectedChapterId}
              onChange={(e) => handleChapterChange(e.target.value)}
              disabled={availableChapters.length === 0}
              className="w-full rounded-xl border border-slate-300 p-2.5 text-xs font-semibold text-slate-800 bg-white focus:border-brand-500 focus:outline-none disabled:opacity-50"
            >
              {availableChapters.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">3. Topic</label>
            <select
              value={selectedTopicId}
              onChange={(e) => setSelectedTopicId(e.target.value)}
              disabled={availableTopics.length === 0}
              className="w-full rounded-xl border border-slate-300 p-2.5 text-xs font-semibold text-slate-800 bg-white focus:border-brand-500 focus:outline-none disabled:opacity-50"
            >
              {availableTopics.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* 3. Question Count & Launcher */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-3 border-t border-slate-100">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-slate-700">Question Count:</span>
            <div className="flex gap-1.5">
              {[10, 15, 20, 25, 30].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setQuestionCount(num)}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                    questionCount === num
                      ? 'bg-slate-900 text-white shadow-sm'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {num} MCQs
                </button>
              ))}
            </div>
          </div>

          <button
            type="button"
            disabled={loading || !selectedSubjectId}
            onClick={() => startTest('subject_test', selectedSubjectId, questionCount)}
            className="flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <BookOpen className="h-4 w-4" />}
            LAUNCH TEST ({questionCount} MCQs) &rarr;
          </button>
        </div>
      </div>

      {/* 🔒 Official PYQ Integrity Notice */}
      <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-6 space-y-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-200 text-slate-600">
            <Lock className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">Official Past Year Papers (PYQ)</h3>
            <p className="text-[11px] text-slate-500">Temporarily Locked &bull; Zero Fabricated Memory Recalls</p>
          </div>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Revizo upholds strict medical accuracy standards. All 871 questions currently live are verified against standard medical textbooks (Harrison, Bailey & Love, Robbins, Park, etc.). We do not publish unverified memory recalls.
        </p>
      </div>
    </div>
  );
}
