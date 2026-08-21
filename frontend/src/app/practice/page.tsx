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
} from 'lucide-react';

export default function PracticePage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('');
  const [selectedChapterId, setSelectedChapterId] = useState<string>('');
  const [selectedTopicId, setSelectedTopicId] = useState<string>('');
  const [topicQuestionCount, setTopicQuestionCount] = useState<number>(10);
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
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Practice by Subject & Topic</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Select what you are currently studying and test your recall with realistic +4 / -1 NEET-PG scoring
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-800">
          <ShieldCheck className="h-4 w-4 text-emerald-600" />
          891 Medically Reviewed Questions
        </div>
      </div>

      {/* 🎯 Interactive Subject & Topic Practice Selector */}
      <div className="rounded-2xl border-2 border-brand-200 bg-white p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
              <Filter className="h-4 w-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Custom Subject & Topic Test</h2>
              <p className="text-xs text-slate-500">Pick the exact subject, chapter, and topic from your study plan</p>
            </div>
          </div>
          <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-[10px] font-bold text-brand-700">
            Study-Alignd Practice
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* 1. Subject Select */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">1. Select Subject (19 Disciplines)</label>
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

          {/* 2. Chapter Select */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">2. Select Chapter</label>
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

          {/* 3. Topic Select */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">3. Select Specific Topic</label>
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

        {/* Question Count & Launcher */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-3 border-t border-slate-100">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-slate-700">Questions:</span>
            <div className="flex gap-1.5">
              {[5, 10, 15, 20].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setTopicQuestionCount(num)}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                    topicQuestionCount === num
                      ? 'bg-slate-900 text-white'
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
            onClick={() => startTest('subject_test', selectedSubjectId, topicQuestionCount)}
            className="flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow disabled:opacity-50 transition-colors"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <BookOpen className="h-4 w-4" />}
            START TOPIC TEST ({topicQuestionCount} MCQs) &rarr;
          </button>
        </div>
      </div>

      {/* Quick Practice Mode Cards */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-slate-900">Standard Practice Modes</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* 1. Daily Short Test */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-brand-400 transition-all">
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
                10 clinical MCQs sampled across high-frequency exam topics to build daily practice habits.
              </p>
              <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
                <span>10 MCQs</span>
                <span>&bull;</span>
                <span>~12 Mins</span>
                <span>&bull;</span>
                <span className="font-semibold text-emerald-600">+4 / -1</span>
              </div>
            </div>
            <button
              onClick={() => startTest('daily_short_test', undefined, 10)}
              disabled={loading}
              className="w-full rounded-xl bg-slate-900 py-2.5 text-xs font-bold text-white hover:bg-slate-800 shadow disabled:opacity-50 transition-colors"
            >
              START DAILY TEST
            </button>
          </div>

          {/* 2. Mistake Retest */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between hover:border-rose-300 transition-all">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-rose-50 text-rose-700 font-bold">
                  🎯
                </div>
                <span className="rounded-full bg-rose-50 px-2.5 py-0.5 text-[10px] font-bold text-rose-700">
                  Mistake Journal
                </span>
              </div>
              <h3 className="text-base font-bold text-slate-900">Mistake Retest</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Targeted practice re-testing your previously missed questions and weak concepts until mastered.
              </p>
              <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium pt-1">
                <span>10 MCQs</span>
                <span>&bull;</span>
                <span>~10 Mins</span>
              </div>
            </div>
            <button
              onClick={() => startTest('mistake_retest', undefined, 10)}
              disabled={loading}
              className="w-full rounded-xl bg-rose-600 py-2.5 text-xs font-bold text-white hover:bg-rose-700 shadow disabled:opacity-50 transition-colors"
            >
              RETEST MISTAKES
            </button>
          </div>

          {/* 3. Past-Year Questions (PYQ) — Honest Locked Notice */}
          <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-6 space-y-4 flex flex-col justify-between opacity-80">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-200 text-slate-600">
                  <Lock className="h-4 w-4" />
                </div>
                <span className="rounded-full bg-slate-200 px-2.5 py-0.5 text-[10px] font-bold text-slate-700">
                  Module Disabled
                </span>
              </div>
              <h3 className="text-base font-bold text-slate-800">Past-Year Questions (PYQ)</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Verified official PYQs are not currently available. Revizo strictly prohibits unverified memory-recall claims until official master papers are verified.
              </p>
            </div>
            <button
              disabled
              className="w-full flex items-center justify-center gap-1.5 rounded-xl border border-slate-300 bg-slate-200 py-2.5 text-xs font-bold text-slate-500 cursor-not-allowed"
            >
              <Lock className="h-3.5 w-3.5" /> PYQ MODULE LOCKED
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
