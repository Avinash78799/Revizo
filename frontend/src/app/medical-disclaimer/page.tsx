'use client';

import React from 'react';
import { HeartPulse, ShieldAlert, BookOpen, AlertTriangle } from 'lucide-react';

export default function MedicalDisclaimerPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-8">
      <div className="space-y-2 border-b border-slate-200 pb-4">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Medical & Educational Disclaimer</h1>
        <p className="text-xs text-slate-500">Effective Date: January 1, 2026 &bull; Revizo Editorial & Governance Board</p>
      </div>

      <div className="rounded-2xl border border-rose-200 bg-rose-50/50 p-6 space-y-3">
        <div className="flex items-center gap-2 text-sm font-bold text-rose-900">
          <HeartPulse className="h-5 w-5 text-rose-600 shrink-0" />
          NOT MEDICAL OR CLINICAL TREATMENT ADVICE
        </div>
        <p className="text-xs text-rose-950 leading-relaxed font-medium">
          The contents of Revizo (including practice questions, clinical rationales, takeaways, and memory pearls) are intended <strong>strictly for postgraduate medical examination preparation and educational revision</strong>. Nothing on Revizo constitutes real-world clinical decision support, patient diagnosis, or treatment guidance. Healthcare providers must always exercise independent clinical judgment and consult official institutional protocols for real patient care.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">1. Independent Educational Platform</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Revizo is an independent educational platform. Revizo is <strong>not affiliated with, endorsed by, certified by, or sponsored by the National Board of Examinations in Medical Sciences (NBEMS) or the National Medical Commission (NMC)</strong>. Mention of NEET-PG, INI-CET, or medical curriculum terms is solely for descriptive educational purposes.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">2. Past-Year Questions (PYQ) Policy</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Revizo maintains a strict zero-tolerance policy against fabricated or unauthenticated past-year question claims (`VERIFIED_PYQ = 0`). The PYQ practice module remains completely disabled until official master question papers and authoritative answer keys have been verified with cryptographic SHA-256 hashes.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">3. Continuous Medical Review & Quarantine</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Medicine evolves constantly. If a student, faculty member, or doctor identifies an updated clinical guideline or disputed answer key, they may flag the question via the built-in reporting mechanism. Critical safety reports trigger immediate automated quarantine of the question for review by our Medical Adjudication Board.
        </p>
      </div>
    </div>
  );
}
