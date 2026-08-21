'use client';

import React from 'react';
import Link from 'next/link';
import { ShieldCheck, BookOpen, HeartPulse, Sparkles, CheckCircle2, ArrowRight } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-12">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-bold text-brand-800">
          <ShieldCheck className="h-4 w-4 text-brand-600" />
          Editorial Independence & Medical Governance
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">About Revizo</h1>
        <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Revizo is an independent medical revision platform designed to help NEET-PG aspirants practice, diagnose weaknesses, and master high-yield clinical concepts.
        </p>
      </div>

      {/* Mission & Core Loop */}
      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
        <h2 className="text-xl font-bold text-slate-900">Our Core Philosophy</h2>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          Most medical question banks focus on raw quantity: solving thousands of questions with surface-level rationales. Revizo is built on the principle that <strong>retention is won through mistake analysis and spaced retesting</strong>.
        </p>

        <div className="rounded-xl border border-brand-100 bg-brand-50/50 p-4 text-xs font-semibold text-brand-900 space-y-2">
          <p className="font-bold text-brand-800 flex items-center gap-1.5">
            <Sparkles className="h-4 w-4 text-brand-600" />
            The 5-Step Revizo Retention Engine:
          </p>
          <p className="font-mono text-xs">
            Practice &rarr; Diagnose Distractors &rarr; Spaced Schedule &rarr; 5-Min Retest &rarr; Clinical Recall
          </p>
        </div>
      </div>

      {/* Medical Governance Principles */}
      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
        <h2 className="text-xl font-bold text-slate-900">Medical Governance & Content Integrity</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="rounded-xl border border-slate-200 p-4 space-y-2">
            <div className="flex items-center gap-2 font-bold text-xs text-slate-900">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Two-Doctor Peer Review
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Every practice item undergoes structured medical review with verified references from authoritative textbooks (Harrison, Bailey & Love, Robbins, etc.).
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 p-4 space-y-2">
            <div className="flex items-center gap-2 font-bold text-xs text-slate-900">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Immediate Safety Quarantine
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              When a student flags a critical clinical safety concern, our automated circuit breaker immediately quarantines the question pending Medical Board adjudication.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 p-4 space-y-2">
            <div className="flex items-center gap-2 font-bold text-xs text-slate-900">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Zero Synthetic PYQ Claims
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              We never fabricate unofficial past-year questions. The PYQ module remains strictly locked (`VERIFIED_PYQ = 0`) until authentic official papers pass independent provenance audits.
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 p-4 space-y-2">
            <div className="flex items-center gap-2 font-bold text-xs text-slate-900">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Authoritative Server Scoring
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Standard +4 / -1 NEET-PG marking with server-authoritative timers and calibrated confidence tracking to isolate dangerous guessing habits.
            </p>
          </div>
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="rounded-2xl border border-slate-300 bg-slate-900 p-6 text-white space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-rose-400 flex items-center gap-1.5">
          <HeartPulse className="h-4 w-4" />
          Official Status & Disclaimer
        </h3>
        <p className="text-xs text-slate-300 leading-relaxed">
          Revizo is an independent educational platform. Revizo is <strong>not affiliated with, endorsed by, or certified by the National Board of Examinations in Medical Sciences (NBEMS) or the National Medical Commission (NMC)</strong>. Question materials are for educational practice and test revision only.
        </p>
      </div>

      {/* CTA */}
      <div className="text-center pt-4">
        <Link
          href="/register"
          className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-8 py-3 text-xs font-bold text-white shadow hover:bg-brand-700 transition-colors"
        >
          Start Practicing Free &rarr;
        </Link>
      </div>
    </div>
  );
}
