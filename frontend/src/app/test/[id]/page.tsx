'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
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
  AlertTriangle,
  Clock,
  Send,
  Loader2,
  BookOpen,
  Sparkles,
  Eye,
  EyeOff,
  Strikethrough,
  RotateCcw,
  Check,
  X,
  Eraser,
  Shield,
} from 'lucide-react';

export default function TestRunnerPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialStudyMode = searchParams.get('studyMode') !== 'false';

  const [questions, setQuestions] = useState<SanitizedQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [visitedQuestions, setVisitedQuestions] = useState<Record<string, boolean>>({});
  const [markedForReview, setMarkedForReview] = useState<Record<string, boolean>>({});
  const [struckOptions, setStruckOptions] = useState<Record<string, Record<string, boolean>>>({});
  const [startedAt, setStartedAt] = useState<string>(new Date().toISOString());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [studyMode, setStudyMode] = useState(initialStudyMode);
  const [evaluations, setEvaluations] = useState<Record<string, EvaluationResult>>({});
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [questionTimes, setQuestionTimes] = useState<Record<string, number>>({});
  const [currentStartTime, setCurrentStartTime] = useState<number>(Date.now());
  const [confidences, setConfidences] = useState<Record<string, string>>({});
  const [paletteFilter, setPaletteFilter] = useState<'all' | 'answered' | 'unanswered' | 'marked'>('all');

  useEffect(() => {
    async function loadTestSession() {
      try {
        const session = await apiRequest<TestSession>(`/tests/${params.id}`);
        if (session && session.questions && session.questions.length > 0) {
          setQuestions(session.questions);
          setStartedAt(session.started_at);
          setVisitedQuestions({ [session.questions[0].id]: true });
        } else {
          setError('This test session contains no questions. Please start a new test.');
        }
      } catch (err: any) {
        console.error('Failed to load test session:', err);
        setError(err.message || 'Failed to load test session. Please try again.');
      } finally {
        setLoading(false);
        setCurrentStartTime(Date.now());
      }
    }
    loadTestSession();
  }, [params.id]);

  const currentQ = questions[currentIndex];
  const isLast = currentIndex === questions.length - 1;
  const currentEval = currentQ ? evaluations[currentQ.id] : null;

  // Track visited questions
  useEffect(() => {
    if (currentQ) {
      setVisitedQuestions((prev) => ({ ...prev, [currentQ.id]: true }));
    }
  }, [currentQ]);

  // Handle option selection
  const handleSelectOption = async (key: string) => {
    if (!currentQ) return;
    
    // In study mode, if already evaluated for this question, prevent changes
    if (studyMode && currentEval) return;

    setAnswers((prev) => ({ ...prev, [currentQ.id]: key }));

    // In Study Mode (Marrow/PrepLadder QBank style), immediately submit and reveal explanation
    if (studyMode) {
      setSubmitting(true);
      try {
        const spent = Math.max(1, Math.round((Date.now() - currentStartTime) / 1000));
        const evalRes = await apiRequest<EvaluationResult>(`/tests/${params.id}/answers`, {
          method: 'POST',
          body: JSON.stringify({
            question_id: currentQ.id,
            selected_option_key: key,
            confidence: confidences[currentQ.id] || 'DEFINITELY_KNOW',
            time_spent_seconds: spent,
          }),
        });
        setEvaluations((prev) => ({ ...prev, [currentQ.id]: evalRes }));
      } catch (err: any) {
        console.error('Error evaluating answer:', err);
      } finally {
        setSubmitting(false);
      }
    }
  };

  // Clear current response (important for NEET PG negative marking defense)
  const handleClearResponse = () => {
    if (!currentQ || (studyMode && currentEval)) return;
    setAnswers((prev) => {
      const next = { ...prev };
      delete next[currentQ.id];
      return next;
    });
  };

  // Toggle option strikethrough (elimination tool)
  const handleToggleStrike = (e: React.MouseEvent, optKey: string) => {
    e.stopPropagation();
    if (!currentQ) return;
    setStruckOptions((prev) => {
      const qStrikes = { ...(prev[currentQ.id] || {}) };
      qStrikes[optKey] = !qStrikes[optKey];
      return { ...prev, [currentQ.id]: qStrikes };
    });
  };

  const handleToggleMark = () => {
    if (!currentQ) return;
    setMarkedForReview((prev) => ({ ...prev, [currentQ.id]: !prev[currentQ.id] }));
  };

  const handleNext = () => {
    const spent = Math.max(1, Math.round((Date.now() - currentStartTime) / 1000));
    if (currentQ) {
      setQuestionTimes((prev) => ({ ...prev, [currentQ.id]: (prev[currentQ.id] || 0) + spent }));
    }

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
      setCurrentStartTime(Date.now());
    } else {
      setShowSubmitModal(true);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1);
      setCurrentStartTime(Date.now());
    }
  };

  const handleJumpToQuestion = (index: number) => {
    const spent = Math.max(1, Math.round((Date.now() - currentStartTime) / 1000));
    if (currentQ) {
      setQuestionTimes((prev) => ({ ...prev, [currentQ.id]: (prev[currentQ.id] || 0) + spent }));
    }
    setCurrentIndex(index);
    setCurrentStartTime(Date.now());
  };

  const handleFinalSubmit = async () => {
    setSubmitting(true);
    try {
      // In Exam Mode, submit all answers that haven't been submitted yet
      for (const q of questions) {
        const selected = answers[q.id];
        if (selected && !evaluations[q.id]) {
          try {
            await apiRequest(`/tests/${params.id}/answers`, {
              method: 'POST',
              body: JSON.stringify({
                question_id: q.id,
                selected_option_key: selected,
                confidence: confidences[q.id] || 'DEFINITELY_KNOW',
                time_spent_seconds: questionTimes[q.id] || 15,
              }),
            });
          } catch {
            // continue
          }
        }
      }

      // Complete the test session
      try {
        await apiRequest(`/tests/${params.id}/complete`, { method: 'POST' });
      } catch {
        // may already be completed
      }

      router.push(`/test/${params.id}/result`);
    } catch (err: any) {
      alert(err.message || 'Failed to submit test.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return <TestRunnerSkeleton />;
  }

  if (error || questions.length === 0) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-16 text-center space-y-4">
        <AlertCircle className="h-12 w-12 text-rose-500 mx-auto" />
        <h2 className="text-lg font-bold text-slate-900">Test Could Not Be Loaded</h2>
        <p className="text-sm text-slate-600">{error || 'No questions found for this test session.'}</p>
        <button
          onClick={() => router.push('/practice')}
          className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-bold text-white hover:bg-brand-700"
        >
          Start a New Test
        </button>
      </div>
    );
  }

  const answeredCount = Object.keys(answers).length;
  const markedCount = Object.values(markedForReview).filter(Boolean).length;
  const isSelected = (key: string) => answers[currentQ.id] === key;
  const isMarked = Boolean(markedForReview[currentQ.id]);
  const currentStruck = struckOptions[currentQ.id] || {};



  return (
    <div className="mx-auto max-w-4xl px-4 py-6 space-y-6">
      {/* Top Test Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-brand-600">
              {currentQ.subject_name || 'NEET-PG Practice'} &bull; {currentQ.topic_name || 'Clinical Concept'}
            </span>
          </div>
          <h1 className="text-lg font-black text-slate-900 mt-0.5">
            Question {currentIndex + 1} of {questions.length}
          </h1>
        </div>

        <div className="flex items-center gap-2.5">
          {/* Study Mode / Exam Mode Toggle */}
          <button
            type="button"
            onClick={() => {
              setStudyMode(!studyMode);
            }}
            className={`flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-bold border transition-all shadow-sm ${
              studyMode
                ? 'border-purple-300 bg-purple-50 text-purple-800'
                : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
            }`}
          >
            <BookOpen className="h-3.5 w-3.5 text-purple-600" />
            <span>{studyMode ? 'Study Mode (Instant Key)' : 'Exam Mode (Timed)'}</span>
          </button>

          <TimerBadge
            startedAt={startedAt}
            durationMinutes={Math.max(15, Math.ceil((questions.length || 10) * 1.5))}
          />

          <button
            type="button"
            onClick={() => setShowSubmitModal(true)}
            className="flex items-center gap-1.5 rounded-xl bg-emerald-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-emerald-700 shadow-sm transition-colors"
          >
            <Send className="h-3.5 w-3.5" />
            Submit
          </button>
        </div>
      </div>

      {/* Progress & Live Stats Bar */}
      <div className="rounded-xl border border-slate-200 bg-slate-50/80 px-4 py-2.5 text-xs text-slate-600 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 font-bold text-emerald-800">
            <span className="h-2 w-2 rounded-full bg-emerald-500" /> Answered: {answeredCount}/{questions.length}
          </span>
          <span className="flex items-center gap-1.5 font-bold text-purple-800">
            <span className="h-2 w-2 rounded-full bg-purple-500" /> Marked: {markedCount}
          </span>
          <span className="flex items-center gap-1.5 text-slate-500">
            <span className="h-2 w-2 rounded-full bg-slate-300" /> Remaining: {questions.length - answeredCount}
          </span>
        </div>
        <div className="text-[11px] font-semibold text-slate-500">
          NEET-PG Standard Marking: <strong className="text-slate-800">+4 / -1 / 0</strong>
        </div>
      </div>

      {/* Main Question Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-start justify-between gap-4">
          <p className="text-sm sm:text-base font-semibold text-slate-900 leading-relaxed">
            {currentQ.question_text}
          </p>
        </div>

        {/* Options Grid (Marrow / PrepLadder Interactive Style) */}
        <div className="space-y-3 pt-1">
          {currentQ.options.map((opt) => {
            const selected = isSelected(opt.option_key);
            const isStruck = Boolean(currentStruck[opt.option_key]);
            
            let cardStyle = 'border-slate-200 bg-white hover:border-slate-300 text-slate-800';
            let badgeStyle = 'bg-slate-100 text-slate-700';
            let isCorrectKey = currentEval && opt.option_key === currentEval.correct_option_key;

            if (studyMode && currentEval) {
              if (isCorrectKey) {
                cardStyle = 'border-emerald-500 bg-emerald-50 text-emerald-950 font-semibold ring-2 ring-emerald-500/30';
                badgeStyle = 'bg-emerald-600 text-white';
              } else if (selected && !currentEval.is_correct) {
                cardStyle = 'border-rose-500 bg-rose-50 text-rose-950 font-semibold ring-2 ring-rose-500/30';
                badgeStyle = 'bg-rose-600 text-white';
              } else {
                cardStyle = 'border-slate-100 bg-slate-50/40 text-slate-400 opacity-60';
                badgeStyle = 'bg-slate-100 text-slate-400';
              }
            } else if (selected) {
              cardStyle = 'border-brand-600 bg-brand-50 text-brand-950 font-bold ring-2 ring-brand-500/20';
              badgeStyle = 'bg-brand-600 text-white';
            } else if (isStruck) {
              cardStyle = 'border-slate-100 bg-slate-50 text-slate-300 line-through opacity-40';
              badgeStyle = 'bg-slate-100 text-slate-300 line-through';
            }

            return (
              <div
                key={opt.option_key}
                onClick={() => handleSelectOption(opt.option_key)}
                className={`group relative w-full flex items-center justify-between rounded-xl border p-4 text-left text-xs sm:text-sm transition-all cursor-pointer ${cardStyle}`}
              >
                <div className="flex items-start gap-3.5 flex-1 pr-4">
                  <span
                    className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-lg text-xs font-bold transition-colors ${badgeStyle}`}
                  >
                    {opt.option_key}
                  </span>
                  <span className={`mt-0.5 leading-relaxed ${isStruck ? 'line-through text-slate-400' : ''}`}>
                    {opt.option_text}
                  </span>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {/* Option Strike-through Elimination Tool */}
                  {(!studyMode || !currentEval) && (
                    <button
                      type="button"
                      title={isStruck ? 'Unstrike option' : 'Strike out / Eliminate option'}
                      onClick={(e) => handleToggleStrike(e, opt.option_key)}
                      className={`p-1 rounded hover:bg-slate-200/80 transition-colors ${
                        isStruck ? 'text-rose-500 font-bold' : 'text-slate-300 hover:text-slate-600 opacity-0 group-hover:opacity-100'
                      }`}
                    >
                      <Strikethrough className="h-3.5 w-3.5" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Confidence Calibration Selector */}
        {(!studyMode || !currentEval) && (
          <div className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-slate-200 bg-slate-50/70 p-3 text-xs">
            <span className="font-bold text-slate-700 flex items-center gap-1.5">
              <Shield className="h-4 w-4 text-brand-600" />
              Confidence Self-Calibration:
            </span>
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setConfidences((prev) => ({ ...prev, [currentQ.id]: 'DEFINITELY_KNOW' }))}
                className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                  (confidences[currentQ.id] || 'DEFINITELY_KNOW') === 'DEFINITELY_KNOW'
                    ? 'bg-emerald-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                High Confidence
              </button>
              <button
                type="button"
                onClick={() => setConfidences((prev) => ({ ...prev, [currentQ.id]: 'GUESSED' }))}
                className={`rounded-lg px-3 py-1 text-xs font-bold transition-all ${
                  confidences[currentQ.id] === 'GUESSED'
                    ? 'bg-amber-500 text-white shadow-xs'
                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                Guess / 50:50
              </button>
            </div>
          </div>
        )}

        {/* Study Mode Instant Explanation View */}
        {studyMode && currentEval && (
          <div className="pt-4 border-t border-slate-100">
            <ExplanationCard question={currentQ} result={currentEval} />
          </div>
        )}

        {/* Controls Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-5">
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="flex items-center gap-1.5 rounded-xl border border-slate-300 px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-30 transition-colors shadow-sm"
            >
              <ArrowLeft className="h-3.5 w-3.5" /> Previous
            </button>

            <button
              type="button"
              onClick={handleToggleMark}
              className={`flex items-center gap-1.5 rounded-xl px-4 py-2.5 text-xs font-bold border transition-colors shadow-sm ${
                isMarked
                  ? 'border-purple-300 bg-purple-50 text-purple-700'
                  : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
              }`}
            >
              <Bookmark className="h-3.5 w-3.5" />
              {isMarked ? 'Marked for Review' : 'Mark for Review'}
            </button>

            {Boolean(answers[currentQ.id]) && (!studyMode || !currentEval) && (
              <button
                type="button"
                onClick={handleClearResponse}
                className="flex items-center gap-1.5 rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-2.5 text-xs font-bold text-rose-700 hover:bg-rose-100 transition-colors shadow-sm"
              >
                <Eraser className="h-3.5 w-3.5" /> Clear Selection
              </button>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleNext}
              className="flex items-center gap-1.5 rounded-xl bg-brand-600 px-6 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow-sm transition-colors"
            >
              {isLast ? 'Review & Submit' : 'Next Question'}
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* NBE-Standard Interactive Question Palette */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
                NBE Question Status Palette
              </h3>
              <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-600">
                NEET-PG 2024 Pattern
              </span>
            </div>
            <span className="text-[11px] text-slate-500">Click any question number to navigate</span>
          </div>

          {/* Palette Filter Pills */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs">
            <button
              type="button"
              onClick={() => setPaletteFilter('all')}
              className={`rounded-lg px-2.5 py-1 text-[11px] font-bold transition-all ${
                paletteFilter === 'all'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All ({questions.length})
            </button>
            <button
              type="button"
              onClick={() => setPaletteFilter('answered')}
              className={`rounded-lg px-2.5 py-1 text-[11px] font-bold transition-all ${
                paletteFilter === 'answered'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
              }`}
            >
              Answered ({answeredCount})
            </button>
            <button
              type="button"
              onClick={() => setPaletteFilter('unanswered')}
              className={`rounded-lg px-2.5 py-1 text-[11px] font-bold transition-all ${
                paletteFilter === 'unanswered'
                  ? 'bg-rose-600 text-white'
                  : 'bg-rose-50 text-rose-700 hover:bg-rose-100'
              }`}
            >
              Unanswered ({questions.length - answeredCount})
            </button>
            <button
              type="button"
              onClick={() => setPaletteFilter('marked')}
              className={`rounded-lg px-2.5 py-1 text-[11px] font-bold transition-all ${
                paletteFilter === 'marked'
                  ? 'bg-purple-600 text-white'
                  : 'bg-purple-50 text-purple-700 hover:bg-purple-100'
              }`}
            >
              Marked ({markedCount})
            </button>
          </div>
        </div>

        {/* NBE Section Tabs (for tests with 20+ questions) */}
        {questions.length >= 20 && (
          <div className="flex flex-wrap items-center gap-2 border-b border-slate-100 pb-3">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mr-1">
              Sections:
            </span>
            {Array.from({ length: Math.ceil(questions.length / (questions.length >= 40 ? 25 : 10)) }).map((_, sIdx) => {
              const secSize = questions.length >= 40 ? 25 : 10;
              const startQ = sIdx * secSize + 1;
              const endQ = Math.min((sIdx + 1) * secSize, questions.length);
              const isCurrentSec = currentIndex >= (startQ - 1) && currentIndex < endQ;
              const secLetter = String.fromCharCode(65 + sIdx);

              return (
                <button
                  key={sIdx}
                  type="button"
                  onClick={() => handleJumpToQuestion(startQ - 1)}
                  className={`rounded-lg px-3 py-1 text-xs font-bold transition-all flex items-center gap-1.5 ${
                    isCurrentSec
                      ? 'bg-brand-50 border-2 border-brand-500 text-brand-900 shadow-xs'
                      : 'bg-slate-50 border border-slate-200 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <span>Section {secLetter}</span>
                  <span className="text-[10px] text-slate-400 font-normal">
                    (Q{startQ}-{endQ})
                  </span>
                </button>
              );
            })}
          </div>
        )}

        {/* Palette Legend */}
        <div className="flex flex-wrap items-center gap-3 text-[10px] font-semibold text-slate-600">
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-emerald-500 inline-block" /> Answered
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-rose-500 inline-block" /> Not Answered
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-purple-500 inline-block" /> Marked for Review
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-slate-200 inline-block" /> Not Visited
          </span>
        </div>

        <div className="grid grid-cols-5 sm:grid-cols-10 gap-2">
          {questions.map((q, idx) => {
            const isAns = Boolean(answers[q.id]);
            const isMrk = Boolean(markedForReview[q.id]);
            const isVis = Boolean(visitedQuestions[q.id]);
            const isCur = idx === currentIndex;

            let matchesFilter = true;
            if (paletteFilter === 'answered') matchesFilter = isAns;
            else if (paletteFilter === 'unanswered') matchesFilter = !isAns;
            else if (paletteFilter === 'marked') matchesFilter = isMrk;

            let numStyle = 'bg-slate-100 text-slate-500 border-slate-200 hover:bg-slate-200';
            if (isCur) {
              numStyle = 'ring-2 ring-brand-500 bg-brand-600 text-white font-black border-brand-600';
            } else if (isMrk && isAns) {
              numStyle = 'bg-purple-100 text-purple-900 font-black border-purple-400 relative';
            } else if (isMrk) {
              numStyle = 'bg-purple-100 text-purple-800 font-bold border-purple-300';
            } else if (isAns) {
              numStyle = 'bg-emerald-100 text-emerald-800 font-bold border-emerald-300';
            } else if (isVis) {
              numStyle = 'bg-rose-50 text-rose-700 font-bold border-rose-200';
            }

            return (
              <button
                key={q.id}
                type="button"
                onClick={() => handleJumpToQuestion(idx)}
                className={`flex h-9 w-full items-center justify-center rounded-lg border text-xs transition-all ${numStyle} ${
                  !matchesFilter ? 'opacity-25 grayscale' : ''
                }`}
              >
                {idx + 1}
                {isMrk && isAns && (
                  <span className="absolute top-1 right-1 h-1.5 w-1.5 rounded-full bg-emerald-600" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Submit Confirmation Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm animate-in fade-in">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl space-y-5">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
                <Send className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Submit Test Session</h3>
                <p className="text-xs text-slate-500">Review your test progress before final submission.</p>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-600">Total Questions:</span>
                <span className="font-bold text-slate-900">{questions.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-emerald-700 font-semibold">Answered:</span>
                <span className="font-bold text-emerald-700">{answeredCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-700 font-semibold">Marked for Review:</span>
                <span className="font-bold text-purple-700">{markedCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Unanswered:</span>
                <span className="font-bold text-slate-500">{questions.length - answeredCount}</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowSubmitModal(false)}
                className="rounded-xl border border-slate-300 px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50"
              >
                Continue Test
              </button>
              <button
                type="button"
                disabled={submitting}
                onClick={handleFinalSubmit}
                className="flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-emerald-700 shadow-sm disabled:opacity-50"
              >
                {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
