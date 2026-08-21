'use client';

import React, { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';

interface TimerBadgeProps {
  startedAt?: string;
  durationMinutes?: number;
  onExpire?: () => void;
}

export function TimerBadge({ startedAt, durationMinutes = 15 }: TimerBadgeProps) {
  const totalSeconds = Math.max(1, durationMinutes) * 60;
  const [secondsRemaining, setSecondsRemaining] = useState<number>(totalSeconds);

  useEffect(() => {
    // Reset timer to full duration for this test run
    setSecondsRemaining(totalSeconds);

    const interval = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [durationMinutes, totalSeconds]);

  const mins = Math.floor(secondsRemaining / 60);
  const secs = secondsRemaining % 60;
  const isTimeUp = secondsRemaining === 0;
  const isUrgent = secondsRemaining > 0 && secondsRemaining < 60;

  return (
    <div
      className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold font-mono tracking-tight transition-colors ${
        isTimeUp
          ? 'bg-rose-100 text-rose-800 ring-1 ring-rose-300'
          : isUrgent
          ? 'bg-amber-100 text-amber-800 animate-pulse'
          : 'bg-slate-100 text-slate-700'
      }`}
    >
      <Clock className={`h-3.5 w-3.5 ${isTimeUp ? 'text-rose-600' : isUrgent ? 'text-amber-600' : 'text-slate-500'}`} />
      <span>
        {isTimeUp ? '00:00 (Time Up)' : `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`}
      </span>
    </div>
  );
}
