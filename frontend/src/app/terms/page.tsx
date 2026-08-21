'use client';

import React from 'react';

export default function TermsPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-8">
      <div className="space-y-2 border-b border-slate-200 pb-4">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Terms of Service</h1>
        <p className="text-xs text-slate-500">Effective Date: January 1, 2026 &bull; Revizo Educational Systems</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">1. Educational License</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Revizo grants you a personal, non-exclusive, non-transferable license to access practice questions and learning analytics for your personal NEET-PG preparation. Automated scraping, unauthorized redistribution, or commercial reproduction of question content is strictly prohibited.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">2. Test Integrity & Platform Behavior</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Students agree to take practice tests fairly. Attempts to exploit client-side scripts, bypass server timers, or tamper with question payloads will result in automated session termination.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">3. Limitation of Liability</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Revizo does not warrant that questions will match actual examination papers. Performance on Revizo tests does not guarantee specific rank or scores on the official NEET-PG exam.
        </p>
      </div>
    </div>
  );
}
