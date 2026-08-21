'use client';

import React, { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';

interface TimerBadgeProps {
  startedAt: string;
  durationMinutes?: number;
  onExpire?: () => void;
}

export function TimerBadge({ startedAt, durationMinutes = 10, onExpire }: TimerBadgeProps) {
  const [secondsRemaining, setSecondsRemaining] = useState<number>(durationMinutes * 60);

  useEffect(() => {
    const startTime = new Date(startedAt).getTime();
    const expiryTime = startTime + durationMinutes * 60 * 1000;

    const interval = setInterval(() => {
      const now = Date.now();
      const diff = Math.max(0, Math.floor((expiryTime - now) / 1000));
      setSecondsRemaining(diff);

      if (diff <= 0) {
        clearInterval(interval);
        if (onExpire) {
          onExpire();
        }
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [startedAt, durationMinutes, onExpire]);

  const mins = Math.floor(secondsRemaining / 60);
  const secs = secondsRemaining % 60;
  const isUrgent = secondsRemaining < 60;

  return (
    <div
      className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold font-mono tracking-tight transition-colors ${
        isUrgent
          ? 'bg-rose-100 text-rose-700 animate-pulse'
          : 'bg-slate-100 text-slate-700'
      }`}
    >
      <Clock className="h-3.5 w-3.5" />
      <span>
        {String(mins).padStart(2, '0')}:{String(secs).padStart(2, '0')}
      </span>
    </div>
  );
}
