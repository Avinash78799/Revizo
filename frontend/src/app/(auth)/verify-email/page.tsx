'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Mail, CheckCircle2, ArrowRight } from 'lucide-react';

export default function VerifyEmailPage() {
  const [resent, setResent] = useState(false);

  const handleResend = () => {
    setResent(true);
    setTimeout(() => setResent(false), 4000);
  };

  return (
    <div className="flex min-h-[80vh] items-center justify-center px-4 py-12">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm space-y-6 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600 mx-auto">
          <Mail className="h-6 w-6" />
        </div>

        <div className="space-y-1">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Check Your Email</h2>
          <p className="text-xs text-slate-500 leading-relaxed">
            We have sent a verification link to your registered email address. Please click the link to activate all practice modules.
          </p>
        </div>

        {resent && (
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-2 text-xs font-semibold text-emerald-800">
            A fresh verification email has been dispatched.
          </div>
        )}

        <div className="space-y-3 pt-2">
          <button
            onClick={handleResend}
            className="w-full rounded-lg border border-slate-300 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 transition-colors"
          >
            Resend Verification Email
          </button>

          <Link
            href="/dashboard"
            className="flex items-center justify-center gap-1.5 w-full rounded-lg bg-brand-600 py-2.5 text-xs font-bold text-white hover:bg-brand-700 transition-colors shadow"
          >
            Continue to Dashboard <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
