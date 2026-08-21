'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Search, X, BookOpen, Layers, Sparkles, ArrowRight } from 'lucide-react';
import { apiRequest, SubjectTree } from '@/lib/api';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SearchModal({ isOpen, onClose }: SearchModalProps) {
  const [query, setQuery] = useState('');
  const [subjects, setSubjects] = useState<SubjectTree[]>([]);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      loadTaxonomy();
    }
  }, [isOpen]);

  const loadTaxonomy = async () => {
    try {
      setLoading(true);
      const data = await apiRequest<SubjectTree[]>('/taxonomy/tree');
      setSubjects(data);
    } catch {
      // Fallback
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  // Filtered concepts and topics
  const matchingConcepts: { conceptName: string; topicName: string; subjectName: string; subjectId: string }[] = [];
  const matchingSubjects: SubjectTree[] = [];

  const cleanQuery = query.trim().toLowerCase();

  if (cleanQuery.length > 1) {
    subjects.forEach((subj) => {
      if (subj.name.toLowerCase().includes(cleanQuery) || subj.code.toLowerCase().includes(cleanQuery)) {
        matchingSubjects.push(subj);
      }
      subj.chapters?.forEach((chap) => {
        chap.topics?.forEach((top) => {
          if (top.name.toLowerCase().includes(cleanQuery)) {
            matchingConcepts.push({
              conceptName: top.name,
              topicName: chap.name,
              subjectName: subj.name,
              subjectId: subj.id,
            });
          }
          top.concepts?.forEach((con) => {
            if (con.name.toLowerCase().includes(cleanQuery)) {
              matchingConcepts.push({
                conceptName: con.name,
                topicName: top.name,
                subjectName: subj.name,
                subjectId: subj.id,
              });
            }
          });
        });
      });
    });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center bg-slate-950/60 backdrop-blur-sm p-4 pt-20">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-200 bg-white shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Search Input Bar */}
        <div className="relative flex items-center border-b border-slate-200 px-4 py-3">
          <Search className="h-5 w-5 text-slate-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search medical subjects, topics, high-yield concepts..."
            className="w-full bg-transparent px-3 py-1 text-sm font-medium text-slate-900 placeholder:text-slate-400 focus:outline-none"
          />
          {query && (
            <button onClick={() => setQuery('')} className="p-1 text-slate-400 hover:text-slate-600">
              <X className="h-4 w-4" />
            </button>
          )}
          <button
            onClick={onClose}
            className="ml-2 rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-200"
          >
            ESC
          </button>
        </div>

        {/* Search Results Area */}
        <div className="max-h-96 overflow-y-auto p-4 space-y-4">
          {cleanQuery.length <= 1 ? (
            <div className="py-6 text-center text-xs text-slate-500 space-y-2">
              <p className="font-semibold text-slate-700">Quick Navigation</p>
              <p>Type at least 2 characters to search across all 19 medical disciplines and high-yield concepts.</p>
              <div className="flex flex-wrap justify-center gap-2 pt-2">
                <Link
                  href="/practice"
                  onClick={onClose}
                  className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-brand-50 hover:text-brand-700"
                >
                  ⚡ Daily Short Test
                </Link>
                <Link
                  href="/revision"
                  onClick={onClose}
                  className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-brand-50 hover:text-brand-700"
                >
                  🔁 5-Min Spaced Revision
                </Link>
                <Link
                  href="/danger-zone"
                  onClick={onClose}
                  className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-rose-50 hover:text-rose-700"
                >
                  🚨 Danger Zone Mistakes
                </Link>
              </div>
            </div>
          ) : matchingConcepts.length === 0 && matchingSubjects.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-500">
              No matching medical concepts found for &ldquo;{query}&rdquo;.
            </div>
          ) : (
            <div className="space-y-4">
              {/* Matching Subjects */}
              {matchingSubjects.length > 0 && (
                <div className="space-y-2">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Subjects</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {matchingSubjects.map((s) => (
                      <Link
                        key={s.id}
                        href={`/subjects/${s.id}`}
                        onClick={onClose}
                        className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-3 hover:border-brand-300 hover:bg-brand-50/50 transition-colors"
                      >
                        <div className="flex items-center gap-2">
                          <BookOpen className="h-4 w-4 text-brand-600" />
                          <span className="text-xs font-bold text-slate-900">{s.name}</span>
                        </div>
                        <span className="text-[10px] font-bold text-slate-500">{s.code}</span>
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Matching Concepts & Topics */}
              {matchingConcepts.length > 0 && (
                <div className="space-y-2">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">High-Yield Concepts</p>
                  <div className="space-y-1.5">
                    {matchingConcepts.slice(0, 10).map((c, i) => (
                      <Link
                        key={i}
                        href={`/subjects/${c.subjectId}`}
                        onClick={onClose}
                        className="flex items-center justify-between rounded-lg border border-slate-100 bg-white p-2.5 text-xs hover:border-brand-200 hover:bg-slate-50 transition-colors"
                      >
                        <div className="space-y-0.5">
                          <div className="font-bold text-slate-800 flex items-center gap-1.5">
                            <Sparkles className="h-3.5 w-3.5 text-amber-500" />
                            {c.conceptName}
                          </div>
                          <div className="text-[11px] text-slate-500">
                            {c.subjectName} &bull; {c.topicName}
                          </div>
                        </div>
                        <ArrowRight className="h-4 w-4 text-slate-400" />
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
