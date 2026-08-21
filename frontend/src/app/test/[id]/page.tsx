'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest, SanitizedQuestion, EvaluationResult, TestSession } from '@/lib/api';
import { ConfidenceSelector } from '@/components/ConfidenceSelector';
import { ExplanationCard } from '@/components/ExplanationCard';
import { TimerBadge } from '@/components/TimerBadge';
import { IntegrityWarningModal } from '@/components/IntegrityWarningModal';
import { TestRunnerSkeleton } from '@/components/Skeleton';
import { ArrowRight, Flag, RefreshCw, AlertCircle, CheckCircle } from 'lucide-react';

export default function TestRunnerPage({ params }: { params: { id: string } }) {
  const [questions, setQuestions] = useState<SanitizedQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<string>('SOMEWHAT_CONFIDENT');
  const [startedAt, setStartedAt] = useState<string>(new Date().toISOString());
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [questionStartTime, setQuestionStartTime] = useState<number>(Date.now());
  const [showIntegrityModal, setShowIntegrityModal] = useState(false);
  const [integrityCount, setIntegrityCount] = useState(0);
  const [reporting, setReporting] = useState(false);
  const [reportReason, setReportReason] = useState('INCORRECT');
  const [reportText, setReportText] = useState('');
  const [reportSuccess, setReportSuccess] = useState(false);

  const router = useRouter();

  // Load questions or check active session
  useEffect(() => {
    async function loadTestQuestions() {
      try {
        const available = await apiRequest<SanitizedQuestion[]>('/questions/available');
        if (available && available.length > 0) {
          setQuestions(available.slice(0, 5));
        }
      } catch (err) {
        console.error('Failed to load questions:', err);
      } finally {
        setLoading(false);
        setQuestionStartTime(Date.now());
      }
    }
    loadTestQuestions();
  }, [params.id]);

  // Test Integrity Listener (Focus Loss / Tab Switch Detection)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        logIntegrityEvent('TAB_HIDDEN');
      }
    };

    const handleBlur = () => {
      logIntegrityEvent('WINDOW_BLURRED');
    };

    window.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('blur', handleBlur);

    return () => {
      window.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('blur', handleBlur);
    };
  }, [params.id]);

  const logIntegrityEvent = async (type: string) => {
    try {
      setIntegrityCount((c) => c + 1);
      setShowIntegrityModal(true);
      await apiRequest(`/tests/${params.id}/integrity-events`, {
        method: 'POST',
        body: JSON.stringify({
          session_id: params.id,
          event_type: type,
          metadata: { timestamp: new Date().toISOString() },
        }),
      });
    } catch {
      // Non-blocking integrity logging
    }
  };

  const handleOptionSelect = (key: string) => {
    if (evaluation) return; // Answer locked
    setSelectedOption(key);
  };

  const handleSubmitAnswer = async () => {
    if (!selectedOption || submitting) return;

    const currentQ = questions[currentIndex];
    const timeSpent = Math.max(1, Math.round((Date.now() - questionStartTime) / 1000));
    setSubmitting(true);

    try {
      const evalRes = await apiRequest<EvaluationResult>(`/tests/${params.id}/answers`, {
        method: 'POST',
        body: JSON.stringify({
          question_id: currentQ.id,
          selected_option_key: selectedOption,
          confidence: confidence,
          time_spent_seconds: timeSpent,
        }),
      });
      setEvaluation(evalRes);
    } catch (err: any) {
      alert(err.message || 'Submission error. Please check your connection.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
      setSelectedOption(null);
      setConfidence('SOMEWHAT_CONFIDENT');
      setEvaluation(null);
      setQuestionStartTime(Date.now());
    } else {
      router.push(`/test/${params.id}/result`);
    }
  };

  const handleRetestConcept = async () => {
    if (!evaluation) return;
    try {
      const altQ = await apiRequest<SanitizedQuestion>('/tests/retest-concept', {
        method: 'POST',
        body: JSON.stringify({
          concept_id: evaluation.concept_id,
          exclude_question_id: questions[currentIndex].id,
        }),
      });
      // Replace current question with alternative question
      const updated = [...questions];
      updated[currentIndex] = altQ;
      setQuestions(updated);
      setSelectedOption(null);
      setConfidence('SOMEWHAT_CONFIDENT');
      setEvaluation(null);
      setQuestionStartTime(Date.now());
    } catch (err: any) {
      alert(err.message || 'No alternative question found for this concept.');
    }
  };

  const handleSendReport = async () => {
    const currentQ = questions[currentIndex];
    try {
      await apiRequest(`/questions/${currentQ.id}/report`, {
        method: 'POST',
        body: JSON.stringify({
          reason: reportReason,
          description: reportText,
          is_serious_medical_error: reportReason === 'INCORRECT',
        }),
      });
      setReportSuccess(true);
      setTimeout(() => {
        setReporting(false);
        setReportSuccess(false);
        setReportText('');
      }, 1500);
    } catch (err: any) {
      alert(err.message || 'Report failed.');
    }
  };

  if (loading || questions.length === 0) {
    return <TestRunnerSkeleton />;
  }

  const currentQuestion = questions[currentIndex];
  const isLastQuestion = currentIndex === questions.length - 1;

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 space-y-6">
      {/* Integrity Modal */}
      <IntegrityWarningModal
        isOpen={showIntegrityModal}
        eventCount={integrityCount}
        onDismiss={() => setShowIntegrityModal(false)}
      />

      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
            {currentQuestion.subject_name || 'Medical Sciences'} &bull; {currentQuestion.topic_name || 'Clinical Practice'}
          </span>
          <div className="text-sm font-bold text-slate-900 mt-0.5">
            Question {currentIndex + 1} of {questions.length}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <TimerBadge
            startedAt={startedAt}
            durationMinutes={10}
            onExpire={() => alert('Test duration has completed.')}
          />
        </div>
      </div>

      {/* Question Stem */}
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
        <p className="text-sm sm:text-base font-medium text-slate-900 leading-relaxed">
          {currentQuestion.question_text}
        </p>

        {/* Option Choices */}
        <div className="space-y-2.5 pt-2">
          {currentQuestion.options.map((opt) => {
            const isSelected = selectedOption === opt.option_key;
            let optStyle = 'border-slate-200 bg-white hover:border-slate-300 text-slate-800';

            if (evaluation) {
              if (opt.option_key === evaluation.correct_option_key) {
                optStyle = 'border-emerald-500 bg-emerald-50 text-emerald-950 font-semibold ring-1 ring-emerald-400';
              } else if (isSelected && !evaluation.is_correct) {
                optStyle = 'border-rose-500 bg-rose-50 text-rose-950 font-semibold ring-1 ring-rose-400';
              } else {
                optStyle = 'border-slate-200 bg-slate-50/50 opacity-60 text-slate-500';
              }
            } else if (isSelected) {
              optStyle = 'border-brand-600 bg-brand-50 text-brand-950 font-semibold ring-1 ring-brand-500';
            }

            return (
              <button
                key={opt.option_key}
                type="button"
                disabled={Boolean(evaluation)}
                onClick={() => handleOptionSelect(opt.option_key)}
                className={`w-full flex items-start gap-3 rounded-xl border p-3.5 text-left text-xs sm:text-sm transition-all ${optStyle}`}
              >
                <span
                  className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                    isSelected
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 text-slate-700'
                  }`}
                >
                  {opt.option_key}
                </span>
                <span className="mt-0.5 leading-snug">{opt.option_text}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Pre-submission: Confidence Selection & Submit */}
      {!evaluation ? (
        <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <ConfidenceSelector
            value={confidence}
            onChange={setConfidence}
            disabled={submitting}
          />

          <div className="flex justify-end pt-2">
            <button
              onClick={handleSubmitAnswer}
              disabled={!selectedOption || submitting}
              className="flex items-center gap-2 rounded-lg bg-slate-900 px-6 py-2.5 text-xs font-bold text-white shadow hover:bg-slate-800 disabled:opacity-40 transition-colors"
            >
              {submitting ? 'Evaluating Answer...' : 'Submit Answer'}
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      ) : (
        /* Post-submission: Structured Explanation Anatomy */
        <div className="space-y-4">
          <ExplanationCard
            result={evaluation}
            onRetest={handleRetestConcept}
            onReport={() => setReporting(true)}
          />

          <div className="flex justify-end pt-2">
            <button
              onClick={handleNextQuestion}
              className="flex items-center gap-2 rounded-lg bg-slate-900 px-6 py-3 text-xs font-bold text-white shadow hover:bg-slate-800 transition-colors"
            >
              {isLastQuestion ? 'Finish Test & View Analysis' : 'Next Question'}
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Question Reporting Modal */}
      {reporting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                <Flag className="h-4 w-4 text-rose-600" />
                Report Medical Question
              </h3>
              <button onClick={() => setReporting(false)} className="text-xs text-slate-400 hover:text-slate-600">
                Cancel
              </button>
            </div>

            {reportSuccess ? (
              <div className="flex items-center gap-2 rounded-lg bg-emerald-50 p-4 text-xs font-bold text-emerald-800">
                <CheckCircle className="h-4 w-4 text-emerald-600" />
                Thanks. This question has been flagged for medical review.
              </div>
            ) : (
              <div className="space-y-3">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">Reason for report</label>
                  <select
                    value={reportReason}
                    onChange={(e) => setReportReason(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 p-2 text-xs focus:border-brand-500 focus:outline-none bg-white"
                  >
                    <option value="INCORRECT">Incorrect Answer / Medical Fact Error (Auto-Quarantine)</option>
                    <option value="AMBIGUOUS">Ambiguous / Multiple Best Answers</option>
                    <option value="TYPO">Typo / Grammatical Issue</option>
                    <option value="OUTDATED">Outdated Clinical Guideline</option>
                    <option value="OUT_OF_SYLLABUS">Out of NEET-PG Syllabus</option>
                    <option value="POOR_EXPLANATION">Poor Explanation</option>
                    <option value="OTHER">Other Issue</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">Description / Textbook Reference (Optional)</label>
                  <textarea
                    rows={3}
                    value={reportText}
                    onChange={(e) => setReportText(e.target.value)}
                    placeholder="Provide details or standard textbook page reference..."
                    className="w-full rounded-lg border border-slate-300 p-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    onClick={() => setReporting(false)}
                    className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50"
                  >
                    Close
                  </button>
                  <button
                    onClick={handleSendReport}
                    className="rounded-lg bg-rose-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-rose-700"
                  >
                    Submit Report
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
