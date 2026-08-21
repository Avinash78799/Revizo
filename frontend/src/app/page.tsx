'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth-context';
import {
  ShieldCheck,
  Repeat,
  AlertOctagon,
  ArrowRight,
  Sparkles,
  BookOpen,
  Activity,
  CheckCircle2,
  Clock,
  Layers,
  HelpCircle,
  Stethoscope,
  HeartPulse,
} from 'lucide-react';

export default function HomePage() {
  const { user } = useAuth();

  const subjectsPreview = [
    'General Medicine',
    'General Surgery',
    'Obstetrics & Gynaecology',
    'Pediatrics',
    'Pharmacology',
    'Pathology',
    'Microbiology',
    'PSM / Community Medicine',
    'Ophthalmology',
    'ENT / Otorhinolaryngology',
    'Anatomy',
    'Physiology',
    'Biochemistry',
    'Forensic Medicine & Toxicology',
    'Dermatology',
    'Psychiatry',
    'Radiology',
    'Orthopaedics',
    'Anaesthesia',
  ];

  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="mx-auto max-w-5xl px-4 text-center space-y-8 pt-6 sm:pt-12">
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50/80 px-4 py-1.5 text-xs font-bold text-brand-800 shadow-sm">
          <ShieldCheck className="h-4 w-4 text-brand-600" />
          Medically Reviewed Practice & Adaptive Spaced Revision
        </div>

        <div className="space-y-4">
          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-slate-900 leading-tight">
            Turn Every Mistake <br className="hidden sm:inline" />
            <span className="text-brand-600">Into Mastery.</span>
          </h1>

          <p className="mx-auto max-w-2xl text-base sm:text-lg text-slate-600 font-medium leading-relaxed">
            Medically reviewed NEET-PG practice with adaptive spaced revision, intelligent mistake isolation, and evidence-backed explanations.
          </p>
        </div>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          {user ? (
            <Link
              href="/dashboard"
              className="flex items-center gap-2 rounded-xl bg-slate-900 px-7 py-3.5 text-sm font-bold text-white shadow-lg hover:bg-slate-800 transition-all hover:scale-105"
            >
              Go to Dashboard
              <ArrowRight className="h-4 w-4" />
            </Link>
          ) : (
            <>
              <Link
                href="/register"
                className="flex items-center gap-2 rounded-xl bg-brand-600 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-brand-600/20 hover:bg-brand-700 transition-all hover:scale-105"
              >
                START PRACTICING FREE
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/subjects"
                className="rounded-xl border border-slate-300 bg-white px-7 py-3.5 text-sm font-bold text-slate-700 hover:bg-slate-50 transition-colors"
              >
                EXPLORE SUBJECTS
              </Link>
            </>
          )}
        </div>

        {/* Live Proof Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8 border-t border-slate-100 max-w-4xl mx-auto">
          <div className="space-y-1">
            <p className="text-2xl font-black text-slate-900">891</p>
            <p className="text-xs font-semibold text-slate-500">Medically Reviewed Questions</p>
          </div>
          <div className="space-y-1">
            <p className="text-2xl font-black text-brand-600">19</p>
            <p className="text-xs font-semibold text-slate-500">Medical Disciplines</p>
          </div>
          <div className="space-y-1">
            <p className="text-2xl font-black text-emerald-600">+4 / -1</p>
            <p className="text-xs font-semibold text-slate-500">Authoritative Scoring</p>
          </div>
          <div className="space-y-1">
            <p className="text-2xl font-black text-indigo-600">100%</p>
            <p className="text-xs font-semibold text-slate-500">Continuous Governance</p>
          </div>
        </div>

        {/* Educational Disclaimer Banner */}
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3.5 text-xs text-slate-500 max-w-3xl mx-auto">
          ⚠️ <strong>Educational Practice Notice</strong>: Revizo is an independent medical practice platform and is not affiliated with or endorsed by NBE/NMC. Does not guarantee exam questions.
        </div>
      </section>

      {/* Core Learning Loop Diagram */}
      <section className="mx-auto max-w-6xl px-4 space-y-10">
        <div className="text-center space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-widest text-brand-600">The Revizo Method</h2>
          <p className="text-3xl font-black text-slate-900">How Revizo Builds Long-Term Retention</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 relative">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-700 font-bold text-sm">
              01
            </div>
            <h3 className="text-sm font-bold text-slate-900">Practice</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Take daily timed short tests and subject tests calibrated to NEET-PG clinical difficulty.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-700 font-bold text-sm">
              02
            </div>
            <h3 className="text-sm font-bold text-slate-900">Diagnose</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Understand why your selected option was wrong and discover why the correct answer is right.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-700 font-bold text-sm">
              03
            </div>
            <h3 className="text-sm font-bold text-slate-900">Spaced Revision</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Revizo automatically schedules missed concepts on Day 1, Day 3, Day 7, and Day 14.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-700 font-bold text-sm">
              04
            </div>
            <h3 className="text-sm font-bold text-slate-900">Retest</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Re-attempt missed concepts in short 5-minute sessions to reinforce neural pathways.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 font-bold text-sm">
              05
            </div>
            <h3 className="text-sm font-bold text-slate-900">Mastery</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Eliminate danger-zone overconfidence mistakes and achieve clinical recall on exam day.
            </p>
          </div>
        </div>
      </section>

      {/* Feature Showcase Grid */}
      <section className="mx-auto max-w-6xl px-4 space-y-10">
        <div className="text-center space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-widest text-brand-600">Built For High-Yield Results</h2>
          <p className="text-3xl font-black text-slate-900">Engineered Specifically For Serious Medical Aspirants</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-3 hover:border-brand-300 transition-colors">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
              <BookOpen className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Structured 4-Part Explanations</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              No lazy one-line rationales. Every explanation breaks down why the correct key is right, why your specific distractor was wrong, and gives you a high-yield takeaway pearl.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-3 hover:border-rose-300 transition-colors">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-600">
              <AlertOctagon className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Danger Zone Isolation</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              When you answer a question wrong despite 100% confidence, it is isolated into the Danger Zone to repair clinical misconceptions before they cost you negative marks.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-3 hover:border-emerald-300 transition-colors">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
              <Repeat className="h-5 w-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Adaptive Spaced Repetition</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Forget cramming. Revizo builds an individual daily revision queue that reminds you of high-yield facts right at the edge of the forgetting curve.
            </p>
          </div>
        </div>
      </section>

      {/* 19 Subject Coverage Section */}
      <section className="mx-auto max-w-6xl px-4 space-y-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 border-b border-slate-200 pb-4">
          <div className="space-y-1">
            <h2 className="text-xs font-bold uppercase tracking-widest text-brand-600">Curriculum Breadth</h2>
            <p className="text-2xl font-black text-slate-900">Complete 19-Subject Medical Coverage</p>
          </div>
          <Link
            href="/subjects"
            className="flex items-center gap-1 text-xs font-bold text-brand-600 hover:text-brand-700"
          >
            Explore all chapters and topics &rarr;
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {subjectsPreview.map((subj, i) => (
            <Link
              key={i}
              href="/subjects"
              className="rounded-xl border border-slate-200 bg-white p-3 text-xs font-bold text-slate-800 shadow-sm hover:border-brand-300 hover:bg-brand-50/40 transition-colors"
            >
              {subj}
            </Link>
          ))}
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="mx-auto max-w-4xl px-4 text-center">
        <div className="rounded-3xl bg-slate-900 p-8 sm:p-12 text-white space-y-6 shadow-2xl">
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
            Ready to Transform Your Practice?
          </h2>
          <p className="mx-auto max-w-xl text-sm text-slate-300 leading-relaxed font-medium">
            Join medical aspirants who practice smarter, understand their mistakes, and achieve clinical mastery.
          </p>
          <div className="pt-2">
            <Link
              href="/register"
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-8 py-3.5 text-sm font-bold text-white shadow-lg hover:bg-brand-700 transition-all hover:scale-105"
            >
              START PRACTICING FREE
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
