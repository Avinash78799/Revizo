'use client';

import React, { useState } from 'react';
import { apiRequest } from '@/lib/api';
import { Flag, AlertTriangle, ShieldCheck, CheckCircle2, Loader2, X } from 'lucide-react';

interface ReportQuestionModalProps {
  questionId: string;
  isOpen: boolean;
  onClose: () => void;
}

export default function ReportQuestionModal({ questionId, isOpen, onClose }: ReportQuestionModalProps) {
  const [category, setCategory] = useState('WRONG_ANSWER_KEY');
  const [severity, setSeverity] = useState<'normal' | 'important' | 'critical'>('normal');
  const [description, setDescription] = useState('');
  const [sourceReference, setSourceReference] = useState('');
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const categories = [
    { value: 'WRONG_ANSWER_KEY', label: 'Wrong Answer Key / Correct Option Disputed' },
    { value: 'INCORRECT_EXPLANATION', label: 'Inaccurate or Misleading Explanation' },
    { value: 'AMBIGUOUS', label: 'Ambiguous Question Stem or Overlapping Options' },
    { value: 'OUTDATED', label: 'Outdated Clinical Guideline / Obsolete Pharmacology' },
    { value: 'SOURCE_CONCERN', label: 'Questionable Textbook Source or Missing Citation' },
    { value: 'POOR_WORDING', label: 'Grammar / Typographical Error' },
    { value: 'TECHNICAL_PROBLEM', label: 'Formatting, Rendering, or Image Display Issue' },
    { value: 'OTHER', label: 'Other Clinical Concern' },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) {
      setError('Please provide a brief description of the issue.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await apiRequest('/governance/report', {
        method: 'POST',
        body: JSON.stringify({
          question_id: questionId,
          report_type: category,
          severity,
          comment: `${description}${sourceReference ? ` | Reference: ${sourceReference}` : ''}`,
        }),
      });

      if (severity === 'critical') {
        setSuccessMessage(
          'Critical safety report logged. This question has been immediately queued for safety quarantine and medical board adjudication.'
        );
      } else {
        setSuccessMessage('Thank you for reporting. Your report has been submitted to the Medical Review Queue.');
      }

      setTimeout(() => {
        onClose();
        setSuccessMessage(null);
        setDescription('');
        setSourceReference('');
      }, 2500);
    } catch (err: any) {
      setError(err.message || 'Failed to submit report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-50 text-rose-600">
              <Flag className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Report Question for Medical Review</h3>
              <p className="text-[11px] text-slate-500">Continuous medical governance & peer review</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-600">
            <X className="h-4 w-4" />
          </button>
        </div>

        {successMessage ? (
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-center space-y-2">
            <CheckCircle2 className="mx-auto h-8 w-8 text-emerald-600" />
            <p className="text-xs font-bold text-emerald-900">{successMessage}</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-lg border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
                {error}
              </div>
            )}

            {/* Category Select */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Issue Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-medium text-slate-800 focus:border-brand-500 focus:outline-none"
              >
                {categories.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Severity Picker */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Report Severity</label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => setSeverity('normal')}
                  className={`rounded-lg border p-2 text-xs font-semibold transition-all ${
                    severity === 'normal'
                      ? 'border-brand-500 bg-brand-50 text-brand-700'
                      : 'border-slate-200 bg-slate-50 text-slate-600'
                  }`}
                >
                  Normal
                </button>
                <button
                  type="button"
                  onClick={() => setSeverity('important')}
                  className={`rounded-lg border p-2 text-xs font-semibold transition-all ${
                    severity === 'important'
                      ? 'border-amber-500 bg-amber-50 text-amber-700'
                      : 'border-slate-200 bg-slate-50 text-slate-600'
                  }`}
                >
                  Important
                </button>
                <button
                  type="button"
                  onClick={() => setSeverity('critical')}
                  className={`rounded-lg border p-2 text-xs font-semibold transition-all ${
                    severity === 'critical'
                      ? 'border-rose-500 bg-rose-50 text-rose-700'
                      : 'border-slate-200 bg-slate-50 text-slate-600'
                  }`}
                >
                  Critical Safety
                </button>
              </div>
              {severity === 'critical' && (
                <p className="text-[10px] text-rose-600 font-medium pt-1 flex items-center gap-1">
                  <AlertTriangle className="h-3 w-3 shrink-0" />
                  Critical reports trigger immediate safety quarantine of this question for all students.
                </p>
              )}
            </div>

            {/* Description */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Detailed Clinical Feedback</label>
              <textarea
                required
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Explain why the question or answer key is disputed..."
                className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none"
              />
            </div>

            {/* Source Reference (Optional) */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">
                Textbook / Guideline Reference <span className="text-slate-400 font-normal">(Optional)</span>
              </label>
              <input
                type="text"
                value={sourceReference}
                onChange={(e) => setSourceReference(e.target.value)}
                placeholder="e.g., Harrison 21st Ed, Chapter 245, Page 1890"
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-xs text-slate-800 focus:border-brand-500 focus:outline-none"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-1.5 rounded-lg bg-rose-600 px-4 py-2 text-xs font-bold text-white hover:bg-rose-700 disabled:opacity-50"
              >
                {loading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Flag className="h-3.5 w-3.5" />}
                Submit Report
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
