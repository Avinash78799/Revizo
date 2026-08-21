'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiRequest, SubjectTree, TestSession } from '@/lib/api';
import { ChevronLeft, Play, Bookmark, Layers, Sparkles } from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function SubjectDetailPage({ params }: { params: { id: string } }) {
  const [subject, setSubject] = useState<SubjectTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [questionCount, setQuestionCount] = useState<number>(10);
  const [startingTest, setStartingTest] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function loadSubject() {
      try {
        const data = await apiRequest<SubjectTree>(`/taxonomy/subjects/${params.id}/tree`);
        setSubject(data);
      } catch (err) {
        console.error('Failed to load subject tree:', err);
      } finally {
        setLoading(false);
      }
    }
    loadSubject();
  }, [params.id]);

  const handleStartTopicTest = async (topicId: string) => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({
          mode: 'topic_test',
          topic_id: topicId,
          question_count: questionCount,
        }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start topic test');
      setStartingTest(false);
    }
  };

  if (loading || !subject) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
      <Link href="/subjects" className="inline-flex items-center gap-1 text-xs font-semibold text-slate-500 hover:text-slate-900">
        <ChevronLeft className="h-4 w-4" />
        Back to All Subjects
      </Link>

      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 uppercase">
              {subject.code}
            </span>
            <h1 className="text-2xl font-bold text-slate-900">{subject.name}</h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">{subject.description}</p>
        </div>

        {/* Question Count Selector */}
        <div className="flex items-center gap-2 rounded-xl bg-slate-100 p-1.5 border border-slate-200">
          <span className="text-xs font-bold text-slate-700 pl-2">Questions:</span>
          {[5, 10, 20, 30].map((num) => (
            <button
              key={num}
              type="button"
              onClick={() => setQuestionCount(num)}
              className={`rounded-lg px-2.5 py-1 text-xs font-bold transition-all ${
                questionCount === num
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-200'
              }`}
            >
              {num}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-6">
        {subject.chapters?.map((chap, idx) => (
          <div key={chap.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
              <Layers className="h-4 w-4 text-brand-600" />
              <h2 className="text-sm font-bold text-slate-900">
                Chapter {idx + 1}: {chap.name}
              </h2>
            </div>

            <div className="space-y-4 pl-2">
              {chap.topics?.map((topic) => (
                <div key={topic.id} className="rounded-lg border border-slate-100 bg-slate-50/50 p-4 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="text-xs font-bold text-slate-800">{topic.name}</h3>
                    <button
                      onClick={() => handleStartTopicTest(topic.id)}
                      disabled={startingTest}
                      className="flex items-center gap-1.5 rounded-md bg-slate-900 px-3 py-1.5 text-[11px] font-bold text-white hover:bg-slate-800 transition-colors"
                    >
                      <Play className="h-3 w-3 fill-white" />
                      Practice Topic
                    </button>
                  </div>

                  {topic.concepts && topic.concepts.length > 0 && (
                    <div className="space-y-2 pt-2 border-t border-slate-200/60">
                      <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        High-Yield Concepts
                      </div>
                      <div className="grid grid-cols-1 gap-2">
                        {topic.concepts.map((con) => (
                          <div key={con.id} className="rounded bg-white p-2.5 border border-slate-200/80 text-xs space-y-1">
                            <div className="font-semibold text-slate-900 flex items-center justify-between">
                              <span>{con.name}</span>
                              <span className="rounded bg-emerald-50 px-1.5 py-0.5 text-[10px] font-bold text-emerald-700">
                                Score: {Math.round(con.exam_relevance_score * 100)}%
                              </span>
                            </div>
                            {con.clinical_pearl && (
                              <p className="text-[11px] text-slate-600 leading-snug">
                                <span className="font-medium text-amber-700">Pearl:</span> {con.clinical_pearl}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
