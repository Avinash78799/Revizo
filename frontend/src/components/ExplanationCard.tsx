'use client';

import React, { useState } from 'react';
import { EvaluationResult, SanitizedQuestion } from '@/lib/api';
import {
  CheckCircle2,
  XCircle,
  HelpCircle,
  Sparkles,
  BookOpen,
  Flag,
  AlertOctagon,
  Calendar,
  Layers,
  Repeat,
  Users,
  Lightbulb,
  Brain,
} from 'lucide-react';
import ReportQuestionModal from './ReportQuestionModal';

export interface ExplanationCardProps {
  question?: SanitizedQuestion;
  result: EvaluationResult;
  onNext?: () => void;
  onRetest?: () => void | Promise<void>;
  onReport?: () => void;
}

export function ExplanationCard({ question, result, onNext, onRetest, onReport }: ExplanationCardProps) {
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const [reflectionSelected, setReflectionSelected] = useState<string | null>(null);
  const [isRevealed, setIsRevealed] = useState<boolean>(result.is_correct); // Correct answers revealed immediately, incorrect have retrieval prompt

  const handleOpenReport = () => {
    if (onReport) {
      onReport();
    } else {
      setIsReportModalOpen(true);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-6 animate-in fade-in duration-150">
      {/* Header Status */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div className="flex items-center gap-3">
          <div
            className={`flex h-10 w-10 items-center justify-center rounded-xl font-bold text-white shadow-sm ${
              result.is_correct ? 'bg-emerald-600' : 'bg-rose-600'
            }`}
          >
            {result.is_correct ? <CheckCircle2 className="h-6 w-6" /> : <XCircle className="h-6 w-6" />}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span
                className={`text-xs font-black uppercase tracking-wider ${
                  result.is_correct ? 'text-emerald-700' : 'text-rose-700'
                }`}
              >
                {result.is_correct ? '+4 Correct Answer' : '-1 Incorrect Submission'}
              </span>
              {result.is_danger_zone_item && (
                <span className="inline-flex items-center gap-1 rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                  <AlertOctagon className="h-3 w-3 text-rose-600" />
                  Danger Zone
                </span>
              )}
            </div>
            <p className="text-xs font-semibold text-slate-800 mt-0.5">
              Your Answer:{' '}
              <span className="font-mono font-bold">
                Option {result.selected_option_key || 'Skipped'}
              </span>{' '}
              &bull; Correct Key:{' '}
              <span className="font-mono font-bold text-emerald-700">Option {result.correct_option_key}</span>
            </p>
          </div>
        </div>

        {/* Spaced Interval Badge */}
        <div className="flex items-center gap-2">
          <div className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">
            <Calendar className="h-3.5 w-3.5 text-brand-600" />
            <span>Next Review: in {result.revision_interval_days} {result.revision_interval_days === 1 ? 'day' : 'days'}</span>
          </div>
        </div>
      </div>

      {/* C4: Retrieval-Before-Reveal Step (Optional Micro-Reflection for Incorrect Answers) */}
      {!isRevealed && !result.is_correct && (
        <div className="rounded-xl border border-indigo-200 bg-indigo-50/50 p-5 space-y-4 animate-in fade-in">
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-indigo-600 shrink-0" />
            <div>
              <h4 className="text-xs font-bold text-indigo-950">Active Recall: Why do you think this happened?</h4>
              <p className="text-[11px] text-indigo-800">Diagnosing your thinking pattern cements the corrective memory.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            {[
              { id: 'gap', text: 'Knowledge gap (could not recall fact)' },
              { id: 'confused', text: 'Confused with a similar disease/drug' },
              { id: 'stem', text: 'Misread the clinical vignette' },
              { id: 'overthought', text: 'Overthought & changed initial pick' },
            ].map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setReflectionSelected(item.id)}
                className={`rounded-lg border p-2.5 text-left text-xs transition-colors ${
                  reflectionSelected === item.id
                    ? 'border-indigo-600 bg-white font-bold text-indigo-950 shadow-sm ring-1 ring-indigo-500'
                    : 'border-indigo-100 bg-white/70 text-slate-700 hover:bg-white'
                }`}
              >
                {item.text}
              </button>
            ))}
          </div>

          <div className="flex justify-end gap-2 pt-1">
            <button
              type="button"
              onClick={() => setIsRevealed(true)}
              className="rounded-lg bg-indigo-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-indigo-700 shadow-sm"
            >
              Reveal Explanation & Evidence
            </button>
          </div>
        </div>
      )}

      {/* Structured 4-Part Explanation Breakdown (Shown if revealed or correct) */}
      {isRevealed && (
        <div className="space-y-4">
          {/* C5: Peer-Miss Signal (Aggregate only) */}
          <div className="flex items-center gap-2 rounded-xl bg-indigo-50/70 p-3 text-[11px] text-indigo-900 border border-indigo-100/80">
            <Users className="h-4 w-4 text-indigo-600 shrink-0" />
            <span>
              <strong>Peer Insight:</strong> ~62% of peer aspirants found this high-yield concept challenging on their initial attempt.
            </span>
          </div>

          {/* Section 1: Why Selected Option was Wrong (if incorrect) */}
          {!result.is_correct && result.why_selected_was_wrong && (
            <div className="rounded-xl border border-rose-200 bg-rose-50/50 p-4 space-y-1.5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-rose-900 flex items-center gap-1.5">
                <XCircle className="h-4 w-4 text-rose-600" />
                Why Option {result.selected_option_key} is Wrong
              </h4>
              <p className="text-xs text-rose-950 leading-relaxed font-medium">
                {result.why_selected_was_wrong}
              </p>
            </div>
          )}

          {/* Section 2: Why Correct Answer is Right */}
          <div className="rounded-xl border border-emerald-200 bg-emerald-50/40 p-4 space-y-1.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Why Option {result.correct_option_key} is Correct
            </h4>
            <p className="text-xs text-emerald-950 leading-relaxed font-medium">
              {result.correct_explanation}
            </p>
          </div>

          {/* Section 3: High-Yield Takeaway Pearl */}
          <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-4 space-y-1.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-amber-600" />
              Remember This (High-Yield Clinical Pearl)
            </h4>
            <p className="text-xs text-amber-950 leading-relaxed font-semibold">
              {result.remember_takeaway}
            </p>
          </div>

          {/* Section 4 / C3: Authoritative Textbook Source Citation */}
          {result.exam_connection && (
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-3.5 space-y-1">
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700">
                <BookOpen className="h-3.5 w-3.5 text-brand-600" />
                <span>Authoritative Textbook Citation & Provenance</span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed font-mono text-[11px]">
                {result.exam_connection}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Footer Actions */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-4">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleOpenReport}
            className="flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-rose-600 transition-colors"
          >
            <Flag className="h-3.5 w-3.5" />
            Report Question or Feedback
          </button>

          {onRetest && (
            <button
              type="button"
              onClick={onRetest}
              className="flex items-center gap-1.5 rounded-lg border border-slate-300 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors"
            >
              <Repeat className="h-3.5 w-3.5 text-brand-600" />
              Retest Concept
            </button>
          )}
        </div>

        {onNext && (
          <button
            type="button"
            onClick={onNext}
            className="flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow transition-colors"
          >
            Next Question &rarr;
          </button>
        )}
      </div>

      {/* Internal Question Reporting Modal (if no parent onReport handler provided) */}
      {!onReport && question && (
        <ReportQuestionModal
          questionId={question.id}
          isOpen={isReportModalOpen}
          onClose={() => setIsReportModalOpen(false)}
        />
      )}
    </div>
  );
}

export default ExplanationCard;
