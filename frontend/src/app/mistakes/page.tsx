'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, MistakeItem, TestSession } from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';
import { History, Play, CheckCircle2, AlertOctagon, Lightbulb, Download, Sparkles, ArrowRight, Loader2 } from 'lucide-react';

export default function MistakeBankPage() {
  const [mistakes, setMistakes] = useState<MistakeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingTest, setStartingTest] = useState(false);
  const [practicingQuestionId, setPracticingQuestionId] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function loadMistakes() {
      try {
        const data = await apiRequest<MistakeItem[]>('/student/mistakes');
        setMistakes(data);
      } catch (err) {
        console.error('Failed to load mistakes:', err);
      } finally {
        setLoading(false);
      }
    }
    loadMistakes();
  }, []);

  const handlePracticeMistakes = async () => {
    setStartingTest(true);
    try {
      const session = await apiRequest<TestSession>('/tests/start', {
        method: 'POST',
        body: JSON.stringify({ mode: 'mistake_retest', question_count: 10 }),
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start practice');
      setStartingTest(false);
    }
  };

  const handlePracticeSimilar = async (questionId: string) => {
    setPracticingQuestionId(questionId);
    try {
      const session = await apiRequest<{ session_id: string }>(`/student/questions/${questionId}/similar`, {
        method: 'POST',
      });
      router.push(`/test/${session.session_id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to start similar concept practice');
      setPracticingQuestionId(null);
    }
  };

  const handleExportMarkdown = () => {
    if (mistakes.length === 0) return;
    let md = `# Revizo Mistake Intelligence & High-Yield Pearls\n`;
    md += `Exported: ${new Date().toLocaleDateString()} | Total Unresolved Mistakes: ${mistakes.length}\n\n---\n\n`;

    mistakes.forEach((m, idx) => {
      md += `### ${idx + 1}. Concept: ${m.concept_name}\n`;
      md += `**Question**: ${m.question_text}\n\n`;
      md += `**Explanation**: ${m.correct_explanation}\n\n`;
      if (m.remember_takeaway) {
        md += `> 💡 **Takeaway Pearl**: ${m.remember_takeaway}\n\n`;
      }
      md += `---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Revizo_Mistake_Bank_${new Date().toISOString().slice(0, 10)}.md`;
    link.click();
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <History className="h-6 w-6 text-slate-700" />
            Mistake Bank
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Personalized intelligence on your past recall errors and time-traps.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {mistakes.length > 0 && (
            <button
              type="button"
              onClick={handleExportMarkdown}
              className="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
            >
              <Download className="h-3.5 w-3.5 text-slate-500" />
              Export Revision Sheet
            </button>
          )}

          {mistakes.length > 0 && (
            <button
              onClick={handlePracticeMistakes}
              disabled={startingTest}
              className="flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800 shadow-sm transition-colors disabled:opacity-50"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              {startingTest ? 'Generating Test...' : 'Retest All Mistakes'}
            </button>
          )}
        </div>
      </div>

      {mistakes.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-200 p-12 text-center space-y-3">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Zero Unresolved Mistakes</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            You currently have no active mistake records. Keep practicing high-yield questions!
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {mistakes.map((m) => (
            <div
              key={m.attempt_id}
              className={`rounded-2xl border p-6 space-y-4 bg-white shadow-sm transition-all ${
                m.is_danger_zone ? 'border-rose-300 ring-1 ring-rose-200' : 'border-slate-200'
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900">{m.concept_name}</span>
                  <span className="text-[10px] text-slate-400">&bull; Your Pick: Option {m.selected_option_key || '—'}</span>
                </div>

                <div className="flex items-center gap-2">
                  {m.time_trap_tag && (
                    <span
                      className={`rounded-md px-2 py-0.5 text-[10px] font-bold ${
                        m.time_trap_type === 'overthinking'
                          ? 'bg-purple-100 text-purple-800'
                          : m.time_trap_type === 'quick_gap'
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {m.time_trap_tag}
                    </span>
                  )}
                  {m.is_danger_zone && (
                    <span className="flex items-center gap-1 rounded-md bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                      <AlertOctagon className="h-3 w-3" />
                      Danger Zone
                    </span>
                  )}
                </div>
              </div>

              <p className="text-xs sm:text-sm text-slate-900 leading-relaxed font-semibold">
                {m.question_text}
              </p>

              <div className="rounded-xl bg-emerald-50/60 border border-emerald-100 p-4 text-xs text-emerald-950 space-y-1">
                <span className="font-bold text-emerald-900">Correct Explanation:</span>
                <p className="leading-relaxed font-medium">{m.correct_explanation}</p>
              </div>

              {m.remember_takeaway && (
                <div className="rounded-xl border border-amber-200 bg-amber-50/70 p-3 text-xs text-amber-950 flex items-start gap-2.5">
                  <Lightbulb className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-amber-900">Takeaway Pearl:</span> {m.remember_takeaway}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-end pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => handlePracticeSimilar(m.question_id)}
                  disabled={practicingQuestionId === m.question_id}
                  className="flex items-center gap-1.5 rounded-lg bg-slate-900 px-3.5 py-1.5 text-xs font-bold text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
                >
                  {practicingQuestionId === m.question_id ? (
                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  ) : (
                    <Sparkles className="h-3.5 w-3.5 text-amber-400" />
                  )}
                  Practice Similar MCQ
                  <ArrowRight className="h-3 w-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
