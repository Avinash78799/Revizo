'use client';

import React from 'react';
import Link from 'next/link';
import { Flag, ShieldCheck, AlertOctagon, CheckCircle2 } from 'lucide-react';

export default function ContentReportingPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-8">
      <div className="space-y-2 border-b border-slate-200 pb-4">
        <div className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-bold text-brand-800">
          <ShieldCheck className="h-4 w-4 text-brand-600" />
          Medical Governance & Quality Assurance
        </div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Content Reporting & Quarantine Policy</h1>
        <p className="text-xs text-slate-500">How Revizo maintains 100% verified and safe medical practice questions</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">How to Report a Question</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          While taking any test or reviewing your mistake journal, click the <strong>&ldquo;Report Question&rdquo;</strong> flag button on the bottom-right of the card. You can submit reports across 8 standardized categories:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Wrong Answer Key / Key Disputed
          </div>
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Inaccurate or Misleading Explanation
          </div>
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Ambiguous Stem / Overlapping Options
          </div>
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Outdated Clinical Guideline
          </div>
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Questionable Source Citation
          </div>
          <div className="rounded-lg bg-slate-50 p-3 border border-slate-200 font-semibold text-slate-800">
            &bull; Typographical / Grammar Error
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-rose-200 bg-rose-50/50 p-6 space-y-3">
        <div className="flex items-center gap-2 text-sm font-bold text-rose-900">
          <AlertOctagon className="h-5 w-5 text-rose-600 shrink-0" />
          Immediate Automated Safety Quarantine Circuit
        </div>
        <p className="text-xs text-rose-950 leading-relaxed font-medium">
          When any student submits a report marked with <strong>Critical Safety Severity</strong>, our automated circuit breaker immediately quarantines that question across the entire platform. Quarantined questions cannot be served in any new tests until independently adjudicated by two senior medical reviewers.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-3">
        <h2 className="text-base font-bold text-slate-900">Historical Test Attempt Preservation</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          When a question is quarantined, edited, or remediated, <strong>all previous test scores and mistake records remain intact</strong>. Remediated items receive a new version tag and audit record to ensure historical test accuracy is never retroactively distorted.
        </p>
      </div>
    </div>
  );
}
