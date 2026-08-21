'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, SanitizedQuestion, EvaluationResult, TestSession } from '@/lib/api';
import { ExplanationCard } from '@/components/ExplanationCard';
import { TimerBadge } from '@/components/TimerBadge';
import { TestRunnerSkeleton } from '@/components/Skeleton';
import {
  ArrowRight,
  ArrowLeft,
  Bookmark,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Clock,
  Layers,
  Send,
  Loader2,
  BookOpen,
} from 'lucide-react';

export default function TestRunnerPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [questions, setQuestions] = useState<SanitizedQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [markedForReview, setMarkedForReview] = useState<Record<string, boolean>>({});
  const [startedAt, setStartedAt] = useState<string>(new Date().toISOString());
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [studyMode, setStudyMode] = useState(false); // Default: Standard Exam Mode (review at end)
  const [instantEvaluation, setInstantEvaluation] = useState<EvaluationResult | null>(null);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [questionTimes, setQuestionTimes] = useState<Record<string, number>>({});
  const [currentStartTime, setCurrentStartTime] = useState<number>(Date.now());

  useEffect(() => {
    async function loadTestQuestions() {
      try {
        const available = await apiRequest<SanitizedQuestion[]>('/questions/available');
        if (available && available.length > 0) {
          setQuestions(available.slice(0, 10));
        }
      } catch (err) {
        console.error('Failed to load questions:', err);
      } finally {
        setLoading(false);
        setCurrentStartTime(Date.now());
      }
    }
    loadTestQuestions();
  }, [params.id]);

  const currentQ = questions[currentIndex];
  const isLast = currentIndex === questions.length - 1;

  const handleSelectOption = (key: string) => {
    if (studyMode && instantEvaluation) return; // locked in study mode until next
    setAnswers((prev) => ({ ...prev, [currentQ.id]: key }));
  };

  const handleToggleMark = () => {
    setMarkedForReview((prev) => ({ ...prev, [currentQ.id]: !prev[currentQ.id] }));
  };

  const handleNext = () => {
    // Record time spent
    const spent = Math.max(1, Math.round((Date.now() - currentStartTime) / 1000));
    setQuestionTimes((prev) => ({ ...prev, [currentQ.id]: (prev[currentQ.id] || 0) + spent }));

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
      setInstantEvaluation(null);
      setCurrentStartTime(Date.now());
    } else {
      setShowSubmitModal(true);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1);
      setInstantEvaluation(null);
      setCurrentStartTime(Date.now());
    }
  };

  // Check answer immediately if student enabled Study Mode
  const handleCheckImmediate = async () => {
    const selected = answers[currentQ.id];
    if (!selected || submitting) return;

    setSubmitting(true);
    try {
      const evalRes = await apiRequest<EvaluationResult>(`/tests/${params.id}/answers`, {
        method: 'POST',
        body: JSON.stringify({
          question_id: currentQ.id,
          selected_option_key: selected,
          confidence: 'SOMEWHAT_CONFIDENT',
          time_spent_seconds: 10,
        }),
      });
      setInstantEvaluation(evalRes);
    } catch (err: any) {
      alert(err.message || 'Error checking answer.');
    } finally {
      setSubmitting(false);
    }
  };

  // Final Test Submission
  const handleFinalSubmit = async () => {
    setSubmitting(true);
    try {
      // Submit all answered questions to backend
      for (const q of questions) {
        const selected = answers[q.id] || null;
        if (selected) {
          try {
            await apiRequest(`/tests/${params.id}/answers`, {
              method: 'POST',
              body: JSON.stringify({
                question_id: q.id,
                selected_option_key: selected,
                confidence: 'SOMEWHAT_CONFIDENT',
                time_spent_seconds: questionTimes[q.id] || 15,
              }),
            });
          } catch {
            // continue
          }
        }
      }

      router.push(`/test/${params.id}/result`);
    } catch (err: any) {
      alert(err.message || 'Failed to submit test.');
      setSubmitting(false);
    }
  };

  if (loading || questions.length === 0) {
    return <TestRunnerSkeleton />;
  }

  const answeredCount = Object.keys(answers).length;
  const isSelected = (key: string) => answers[currentQ.id] === key;
  const isMarked = Boolean(markedForReview[currentQ.id]);

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 space-y-6">
      {/* Top Test Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-brand-600">
              {currentQ.subject_name || 'Medical Practice'} &bull; {currentQ.topic_name || 'Clinical Topic'}
            </span>
          </div>
          <h1 className="text-lg font-black text-slate-900 mt-0.5">
            Question {currentIndex + 1} of {questions.length}
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {/* Study Mode Toggle */}
          <button
            type="button"
            onClick={() => setStudyMode(!studyMode)}
            className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-semibold border transition-all ${
              studyMode
                ? 'border-brand-500 bg-brand-50 text-brand-700'
                : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
            }`}
          >
            <BookOpen className="h-3.5 w-3.5 text-brand-600" />
            <span>{studyMode ? 'Study Mode (Instant Key)' : 'Exam Mode (Review at End)'}</span>
          </button>

          <TimerBadge
            startedAt={startedAt}
            durationMinutes={15}
            onExpire={() => setShowSubmitModal(true)}
          />

          <button
            onClick={() => setShowSubmitModal(true)}
            className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-emerald-700 shadow-sm transition-colors"
          >
            <Send className="h-3.5 w-3.5" />
            Submit Test
          </button>
        </div>
      </div>

      {/* Encouraging Realistic Marking Reminder */}
      <div className="rounded-xl border border-slate-200 bg-slate-50/70 px-4 py-2 text-[11px] text-slate-600 flex items-center justify-between">
        <span>
          💡 <strong>NEET-PG Practice (+4 / -1 / 0)</strong>: Mimics real exam marking. Take your time to test your recall without stress!
        </span>
        <span className="font-semibold text-slate-700">
          Answered: {answeredCount}/{questions.length}
        </span>
      </div>

      {/* Main Question Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm space-y-6">
        <p className="text-sm sm:text-base font-semibold text-slate-900 leading-relaxed">
          {currentQ.question_text}
        </p>

        {/* Options Grid */}
        <div className="space-y-3 pt-1">
          {currentQ.options.map((opt) => {
            const selected = isSelected(opt.option_key);
            let style = 'border-slate-200 bg-white hover:border-slate-300 text-slate-800';

            if (studyMode && instantEvaluation) {
              if (opt.option_key === instantEvaluation.correct_option_key) {
                style = 'border-emerald-500 bg-emerald-50 text-emerald-950 font-semibold ring-1 ring-emerald-500';
              } else if (selected && !instantEvaluation.is_correct) {
                style = 'border-rose-500 bg-rose-50 text-rose-950 font-semibold ring-1 ring-rose-500';
              } else {
                style = 'border-slate-200 bg-slate-50/50 opacity-60 text-slate-500';
              }
            } else if (selected) {
              style = 'border-brand-600 bg-brand-50 text-brand-950 font-bold ring-2 ring-brand-500/20';
            }

            return (
              <button
                key={opt.option_key}
                type="button"
                onClick={() => handleSelectOption(opt.option_key)}
                className={`w-full flex items-start gap-3.5 rounded-xl border p-4 text-left text-xs sm:text-sm transition-all ${style}`}
              >
                <span
                  className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-lg text-xs font-bold ${
                    selected ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-700'
                  }`}
                >
                  {opt.option_key}
                </span>
                <span className="mt-0.5 leading-relaxed">{opt.option_text}</span>
              </button>
            );
          })}
        </div>

        {/* Study Mode Instant Explanation View (if enabled) */}
        {studyMode && instantEvaluation && (
          <div className="pt-4">
            <ExplanationCard question={currentQ} result={instantEvaluation} />
          </div>
        )}

        {/* Controls Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-5">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="flex items-center gap-1.5 rounded-lg border border-slate-300 px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-30 transition-colors"
            >
              <ArrowLeft className="h-3.5 w-3.5" /> Previous
            </button>

            <button
              type="button"
              onClick={handleToggleMark}
              className={`flex items-center gap-1.5 rounded-lg px-3.5 py-2 text-xs font-bold border transition-colors ${
                isMarked
                  ? 'border-purple-300 bg-purple-50 text-purple-700'
                  : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
              }`}
            >
              <Bookmark className="h-3.5 w-3.5" />
              {isMarked ? 'Marked for Review' : 'Mark for Review'}
            </button>
          </div>

          <div className="flex items-center gap-2">
            {studyMode && !instantEvaluation && answers[currentQ.id] && (
              <button
                type="button"
                onClick={handleCheckImmediate}
                disabled={submitting}
                className="flex items-center gap-1.5 rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800"
              >
                {submitting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <CheckCircle2 className="h-3.5 w-3.5" />}
                Check Explanation
              </button>
            )}

            <button
              type="button"
              onClick={handleNext}
              className="flex items-center gap-1.5 rounded-lg bg-brand-600 px-5 py-2 text-xs font-bold text-white hover:bg-brand-700 shadow-sm transition-colors"
            >
              {isLast ? 'Review & Submit' : 'Next Question'}
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Question Palette Navigator */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
        <div className="flex items-center justify-between text-xs">
          <span className="font-bold text-slate-900">Question Palette</span>
          <div className="flex items-center gap-3 text-[11px] text-slate-500">
            <span className="flex items-center gap-1">
              <span className="h-2.5 w-2.5 rounded-full bg-brand-600 inline-block" /> Answered
            </span>
            <span className="flex items-center gap-1">
              <span className="h-2.5 w-2.5 rounded-full bg-purple-500 inline-block" /> Marked
            </span>
            <span className="flex items-center gap-1">
              <span className="h-2.5 w-2.5 rounded-full bg-slate-200 inline-block" /> Unanswered
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 pt-1">
          {questions.map((q, idx) => {
            const isAns = Boolean(answers[q.id]);
            const isMrk = Boolean(markedForReview[q.id]);
            const isCur = idx === currentIndex;

            let btnStyle = 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100';
            if (isAns) btnStyle = 'border-brand-500 bg-brand-600 text-white font-bold';
            if (isMrk) btnStyle = 'border-purple-500 bg-purple-100 text-purple-800 font-bold';
            if (isCur) btnStyle += ' ring-2 ring-slate-900 ring-offset-1';

            return (
              <button
                key={q.id}
                type="button"
                onClick={() => {
                  setCurrentIndex(idx);
                  setInstantEvaluation(null);
                  setCurrentStartTime(Date.now());
                }}
                className={`flex h-9 w-9 items-center justify-center rounded-xl border text-xs transition-all ${btnStyle}`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Submit Confirmation Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-slate-900">Submit Practice Test?</h3>
            <div className="rounded-xl bg-slate-50 p-4 text-xs space-y-1.5 text-slate-600">
              <p>
                &bull; Total Questions: <strong>{questions.length}</strong>
              </p>
              <p>
                &bull; Answered: <strong className="text-emerald-700">{answeredCount}</strong>
              </p>
              <p>
                &bull; Unanswered:{' '}
                <strong className="text-rose-700">{questions.length - answeredCount}</strong>
              </p>
              <p>
                &bull; Marked for Review:{' '}
                <strong className="text-purple-700">
                  {Object.values(markedForReview).filter(Boolean).length}
                </strong>
              </p>
            </div>

            <p className="text-xs text-slate-500">
              Upon submission, you will see your full score (+4 / -1) and can review all 4-part explanations and clinical pearls.
            </p>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setShowSubmitModal(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-50"
              >
                Continue Test
              </button>
              <button
                type="button"
                disabled={submitting}
                onClick={handleFinalSubmit}
                className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-5 py-2 text-xs font-bold text-white hover:bg-emerald-700 shadow"
              >
                {submitting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
                Confirm Submission
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
