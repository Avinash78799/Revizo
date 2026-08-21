'use client';

import React, { useEffect, useState, useRef } from 'react';
import { Clock } from 'lucide-react';

interface TimerBadgeProps {
  startedAt?: string;
  durationMinutes?: number;
  onExpire?: () => void;
}

/**
 * Safely parses an ISO date string as UTC timestamp.
 * Handles missing 'Z' suffix from naive database timestamps.
 */
function parseUtcTimestamp(dateStr?: string): number {
  if (!dateStr) return Date.now();
  let str = dateStr.trim();
  // If string has no timezone offset (no Z, no +xx:xx, no -xx:xx at end), append Z
  if (!str.endsWith('Z') && !str.includes('+') && !/-\d{2}:\d{2}$/.test(str)) {
    str += 'Z';
  }
  const ts = new Date(str).getTime();
  return isNaN(ts) ? Date.now() : ts;
}

export function TimerBadge({ startedAt, durationMinutes = 15, onExpire }: TimerBadgeProps) {
  const [secondsRemaining, setSecondsRemaining] = useState<number>(() => durationMinutes * 60);
  const onExpireRef = useRef(onExpire);
  const hasExpiredRef = useRef(false);

  useEffect(() => {
    onExpireRef.current = onExpire;
  }, [onExpire]);

  useEffect(() => {
    const startTime = parseUtcTimestamp(startedAt);
    const totalDurationSeconds = Math.max(1, durationMinutes) * 60;
    const expiryTime = startTime + totalDurationSeconds * 1000;

    // Calculate initial diff
    const initialDiff = Math.floor((expiryTime - Date.now()) / 1000);
    
    // If startedAt is corrupted or in the distant past (e.g. from an old orphaned session),
    // default to fresh duration from when user opened page rather than instant auto-fail.
    const effectiveDiff = initialDiff > 0 ? initialDiff : totalDurationSeconds;
    setSecondsRemaining(effectiveDiff);

    const interval = setInterval(() => {
      const now = Date.now();
      const diff = Math.floor((expiryTime - now) / 1000);
      const clamped = Math.max(0, diff);
      setSecondsRemaining(clamped);

      if (clamped <= 0) {
        clearInterval(interval);
        if (!hasExpiredRef.current) {
          hasExpiredRef.current = true;
          if (onExpireRef.current) {
            onExpireRef.current();
          }
        }
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [startedAt, durationMinutes]);

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
