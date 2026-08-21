'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiRequest, SubjectTree } from '@/lib/api';
import { BookOpen, ChevronRight, Layers, Award } from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSubjects() {
      try {
        const data = await apiRequest<SubjectTree[]>('/taxonomy/subjects');
        setSubjects(data);
      } catch (err) {
        console.error('Failed to load subjects:', err);
      } finally {
        setLoading(false);
      }
    }
    loadSubjects();
  }, []);

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900">NEET-PG Curriculum Syllabus</h1>
        <p className="text-xs text-slate-500 mt-1">
          Explore structured chapters, high-yield topics, and clinical concepts.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {subjects.map((subject) => {
          const totalChapters = subject.chapters?.length || 0;
          const totalConcepts = subject.chapters?.reduce(
            (acc, chap) => acc + (chap.topics?.reduce((tAcc, top) => tAcc + (top.concepts?.length || 0), 0) || 0),
            0
          ) || 0;

          return (
            <Link
              key={subject.id}
              href={`/subjects/${subject.id}`}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-brand-500 hover:shadow transition-all group"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 uppercase">
                    {subject.code}
                  </span>
                  <h2 className="text-base font-bold text-slate-900 group-hover:text-brand-600">
                    {subject.name}
                  </h2>
                  <p className="text-xs text-slate-500">{subject.description || 'Medical curriculum discipline'}</p>
                </div>
                <ChevronRight className="h-5 w-5 text-slate-400 group-hover:text-brand-600 group-hover:translate-x-0.5 transition-all" />
              </div>

              <div className="mt-4 flex items-center gap-4 pt-3 border-t border-slate-100 text-xs text-slate-500">
                <div className="flex items-center gap-1.5">
                  <Layers className="h-3.5 w-3.5 text-slate-400" />
                  <span>{totalChapters} Chapters</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Award className="h-3.5 w-3.5 text-slate-400" />
                  <span>{totalConcepts} High-Yield Concepts</span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
