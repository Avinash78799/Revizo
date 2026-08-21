'use client';

import React from 'react';
import { CheckCircle, XCircle, AlertOctagon, Lightbulb, BookmarkCheck, BookOpen } from 'lucide-react';
import { EvaluationResult } from '@/lib/api';

interface ExplanationCardProps {
  result: EvaluationResult;
  onRetest?: () => void;
  onReport?: () => void;
}

export function ExplanationCard({ result, onRetest, onReport }: ExplanationCardProps) {
  return (
    <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* 1. Status Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          {result.is_correct ? (
            <div className="flex items-center gap-1.5 text-emerald-700 font-bold text-sm">
              <CheckCircle className="h-5 w-5 text-emerald-600" />
              Correct Answer (Option {result.correct_option_key})
            </div>
          ) : (
            <div className="flex items-center gap-1.5 text-rose-700 font-bold text-sm">
              <XCircle className="h-5 w-5 text-rose-600" />
              Incorrect (You selected Option {result.selected_option_key})
            </div>
          )}
        </div>

        {result.is_danger_zone_item && (
          <div className="flex items-center gap-1 rounded bg-rose-100 px-2 py-0.5 text-xs font-bold text-rose-800">
            <AlertOctagon className="h-3.5 w-3.5" />
            Danger Zone Triggered
          </div>
        )}
      </div>

      {/* 2. Why Correct */}
      <div className="space-y-1">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
          <BookmarkCheck className="h-4 w-4 text-emerald-600" />
          Why Option {result.correct_option_key} is Correct
        </div>
        <p className="text-sm text-slate-800 leading-relaxed bg-emerald-50/50 p-3 rounded-lg border border-emerald-100">
          {result.correct_explanation}
        </p>
      </div>

      {/* 3. Why Selected Distractor Was Wrong (if incorrect) */}
      {!result.is_correct && result.why_selected_was_wrong && (
        <div className="space-y-1">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <XCircle className="h-4 w-4 text-rose-600" />
            Why Your Answer (Option {result.selected_option_key}) Was Wrong
          </div>
          <p className="text-sm text-slate-800 leading-relaxed bg-rose-50/50 p-3 rounded-lg border border-rose-100">
            {result.why_selected_was_wrong}
          </p>
        </div>
      )}

      {/* 4. High-Yield Clinical Pearl */}
      {result.remember_takeaway && (
        <div className="rounded-lg border border-amber-200 bg-amber-50/80 p-3.5 text-amber-950 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-amber-800 uppercase tracking-wider">
            <Lightbulb className="h-4 w-4 text-amber-600" />
            High-Yield Clinical Pearl (Remember)
          </div>
          <p className="text-xs font-medium leading-relaxed">
            {result.remember_takeaway}
          </p>
        </div>
      )}

      {/* 5. Exam Connection & Textbook Context */}
      {(result.exam_connection || result.detailed_explanation) && (
        <div className="space-y-2 pt-2 border-t border-slate-100 text-xs text-slate-600">
          {result.exam_connection && (
            <p><span className="font-semibold text-slate-800">Exam Connection:</span> {result.exam_connection}</p>
          )}
          {result.detailed_explanation && (
            <p className="text-slate-500 italic">{result.detailed_explanation}</p>
          )}
        </div>
      )}

      {/* 6. Action Footer: Retest & Report */}
      <div className="flex items-center justify-between pt-2 text-xs">
        <div className="text-slate-500">
          Next revision in: <span className="font-semibold text-slate-700">{result.revision_interval_days} day(s)</span>
        </div>
        <div className="flex items-center gap-3">
          {onReport && (
            <button
              onClick={onReport}
              className="text-slate-400 hover:text-slate-600 underline font-medium"
            >
              Report Question
            </button>
          )}
          {onRetest && (
            <button
              onClick={onRetest}
              className="flex items-center gap-1 rounded bg-slate-100 hover:bg-slate-200 px-2.5 py-1 font-semibold text-slate-700"
            >
              <BookOpen className="h-3.5 w-3.5" />
              Retest Concept
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
