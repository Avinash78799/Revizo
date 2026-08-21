'use client';

import React from 'react';
import { ShieldAlert } from 'lucide-react';

interface IntegrityWarningModalProps {
  isOpen: boolean;
  onDismiss: () => void;
  eventCount: number;
}

export function IntegrityWarningModal({ isOpen, onDismiss, eventCount }: IntegrityWarningModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-xl space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 text-amber-600">
            <ShieldAlert className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Test Integrity Notice</h3>
            <p className="text-xs text-slate-500">Notice #{eventCount}</p>
          </div>
        </div>

        <p className="text-sm text-slate-600 leading-relaxed">
          Leaving or switching away from the active test window has been recorded. To ensure authentic test conditions and accurate memory diagnostic tracking, please keep this window focused during practice.
        </p>

        <div className="flex justify-end pt-2">
          <button
            onClick={onDismiss}
            className="rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800 transition-colors"
          >
            I Understand — Continue Practice
          </button>
        </div>
      </div>
    </div>
  );
}
