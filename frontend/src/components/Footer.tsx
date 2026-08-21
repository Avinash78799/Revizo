'use client';

import React from 'react';
import Link from 'next/link';
import { ShieldCheck, BookOpen, HeartPulse } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-slate-900 text-slate-400 text-sm mt-auto pb-16 md:pb-0">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-slate-800">
          {/* Brand Column */}
          <div className="space-y-4 md:col-span-1">
            <Link href="/" className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-white font-black text-lg">
                R
              </div>
              <span className="text-xl font-bold tracking-tight text-white">REVIZO</span>
            </Link>
            <p className="text-xs text-slate-400 font-medium leading-relaxed">
              Intelligent Medical Revision. <br />
              <span className="text-slate-300 font-semibold">Turn every mistake into mastery.</span>
            </p>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-700 bg-slate-800/80 px-2.5 py-1 text-[11px] font-medium text-emerald-400">
              <ShieldCheck className="h-3.5 w-3.5" />
              Medically Reviewed Practice
            </div>
          </div>

          {/* Practice & Learning */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Practice & Revise</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/practice" className="hover:text-white transition-colors">Daily Short Test</Link>
              </li>
              <li>
                <Link href="/revision" className="hover:text-white transition-colors">Spaced Repetition</Link>
              </li>
              <li>
                <Link href="/mistakes" className="hover:text-white transition-colors">Mistake Journal</Link>
              </li>
              <li>
                <Link href="/danger-zone" className="hover:text-white transition-colors">Danger Zone (Overconfidence)</Link>
              </li>
              <li>
                <Link href="/subjects" className="hover:text-white transition-colors">19 Medical Disciplines</Link>
              </li>
              <li>
                <Link href="/analytics" className="hover:text-white transition-colors">Performance Analytics</Link>
              </li>
            </ul>
          </div>

          {/* About & Medical Governance */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Medical Governance</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/about" className="hover:text-white transition-colors">About Revizo</Link>
              </li>
              <li>
                <Link href="/help" className="hover:text-white transition-colors">How Scoring Works (+4 / -1)</Link>
              </li>
              <li>
                <Link href="/content-reporting" className="hover:text-white transition-colors">Report a Question</Link>
              </li>
              <li>
                <Link href="/medical-disclaimer" className="hover:text-white transition-colors">Evidence & Provenance Rules</Link>
              </li>
              <li>
                <span className="text-slate-500 cursor-not-allowed">PYQ Module (Locked - 0 Verified)</span>
              </li>
            </ul>
          </div>

          {/* Legal & Trust */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Trust & Legal</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/medical-disclaimer" className="hover:text-white transition-colors">Medical Disclaimer</Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
              </li>
              <li>
                <Link href="/help" className="hover:text-white transition-colors">Help Center & Support</Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Mandatory Educational & Medical Disclaimer */}
        <div className="pt-6 space-y-3">
          <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4 text-[11px] text-slate-400 leading-relaxed">
            <p className="font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
              <HeartPulse className="h-3.5 w-3.5 text-rose-400 shrink-0" />
              IMPORTANT MEDICAL & EDUCATIONAL PRACTICE DISCLAIMER:
            </p>
            <p>
              Revizo is an independent educational practice and adaptive revision platform designed for medical students preparing for postgraduate examinations. Revizo is <strong>not affiliated with, endorsed by, or certified by the National Board of Examinations in Medical Sciences (NBEMS) or the National Medical Commission (NMC)</strong>. Question content represents medically reviewed practice material and does not constitute guaranteed examination questions or real-world clinical treatment advice.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
            <p>&copy; 2026 Revizo. All rights reserved.</p>
            <p className="text-[11px]">Practice smarter. Revise better. Master more.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
