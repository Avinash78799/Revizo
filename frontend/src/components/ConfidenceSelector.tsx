'use client';

import React from 'react';
import { CheckCircle2, HelpCircle, AlertCircle } from 'lucide-react';

interface ConfidenceSelectorProps {
  value: string;
  onChange: (val: string) => void;
  disabled?: boolean;
}

export function ConfidenceSelector({ value, onChange, disabled }: ConfidenceSelectorProps) {
  const options = [
    {
      id: 'DEFINITELY_KNOW',
      label: 'Definitely Know',
      desc: 'High confidence — triggers Danger Zone if wrong',
      icon: CheckCircle2,
      activeColor: 'border-emerald-600 bg-emerald-50 text-emerald-900',
    },
    {
      id: 'SOMEWHAT_CONFIDENT',
      label: 'Somewhat Confident',
      desc: 'Moderate confidence',
      icon: HelpCircle,
      activeColor: 'border-brand-600 bg-brand-50 text-brand-900',
    },
    {
      id: 'GUESSING',
      label: 'Educated Guess',
      desc: 'Unsure / elimination guess',
      icon: AlertCircle,
      activeColor: 'border-amber-600 bg-amber-50 text-amber-900',
    },
  ];

  return (
    <div className="space-y-1.5">
      <label className="text-xs font-semibold text-slate-700">
        Confidence Level <span className="font-normal text-slate-500">(Used for adaptive spaced repetition & Danger Zone)</span>
      </label>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
        {options.map((opt) => {
          const Icon = opt.icon;
          const isSelected = value === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              disabled={disabled}
              onClick={() => onChange(opt.id)}
              className={`flex items-start gap-2.5 rounded-lg border p-2.5 text-left transition-all ${
                isSelected
                  ? `${opt.activeColor} ring-1 ring-offset-0`
                  : 'border-slate-200 bg-white hover:border-slate-300 text-slate-700'
              } ${disabled ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <Icon className={`mt-0.5 h-4 w-4 shrink-0 ${isSelected ? 'text-current' : 'text-slate-400'}`} />
              <div>
                <div className="text-xs font-bold leading-tight">{opt.label}</div>
                <div className="text-[10px] text-slate-500 mt-0.5 leading-tight">{opt.desc}</div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
