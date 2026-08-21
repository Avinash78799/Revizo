'use client';

import React, { useEffect, useState } from 'react';
import { apiRequest, SubjectTree } from '@/lib/api';
import { BookOpen, Plus, Trash2, ChevronRight } from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function AdminTaxonomyPage() {
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [loading, setLoading] = useState(true);
  const [newSubjectName, setNewSubjectName] = useState('');
  const [newSubjectCode, setNewSubjectCode] = useState('');

  const loadTaxonomy = async () => {
    try {
      const data = await apiRequest<SubjectTree[]>('/taxonomy/subjects');
      setSubjects(data);
    } catch (err) {
      console.error('Failed to load taxonomy:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTaxonomy();
  }, []);

  const handleCreateSubject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubjectName || !newSubjectCode) return;
    try {
      await apiRequest('/taxonomy/subjects', {
        method: 'POST',
        body: JSON.stringify({ name: newSubjectName, code: newSubjectCode }),
      });
      setNewSubjectName('');
      setNewSubjectCode('');
      loadTaxonomy();
    } catch (err: any) {
      alert(err.message || 'Subject creation failed');
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-slate-700" />
          Curriculum Taxonomy Management
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage subjects, chapters, topics, and high-yield concepts.
        </p>
      </div>

      {/* Create Subject Form */}
      <form onSubmit={handleCreateSubject} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
        <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
          <Plus className="h-4 w-4 text-brand-600" />
          Add Medical Subject
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <input
            type="text"
            required
            placeholder="Subject Name (e.g. Pathology)"
            value={newSubjectName}
            onChange={(e) => setNewSubjectName(e.target.value)}
            className="rounded-lg border border-slate-300 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
          />
          <input
            type="text"
            required
            placeholder="Subject Code (e.g. PATH)"
            value={newSubjectCode}
            onChange={(e) => setNewSubjectCode(e.target.value.toUpperCase())}
            className="rounded-lg border border-slate-300 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none uppercase"
          />
          <button
            type="submit"
            className="rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800"
          >
            Create Subject
          </button>
        </div>
      </form>

      {/* Active Taxonomy Tree */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-slate-900">Active Curriculum Subjects</h2>
        <div className="divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
          {subjects.map((sub) => (
            <div key={sub.id} className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="rounded bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700">
                  {sub.code}
                </span>
                <div>
                  <div className="text-xs font-bold text-slate-900">{sub.name}</div>
                  <div className="text-[10px] text-slate-400">{sub.chapters?.length || 0} chapter(s)</div>
                </div>
              </div>
              <ChevronRight className="h-4 w-4 text-slate-400" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
