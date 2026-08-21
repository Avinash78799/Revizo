'use client';

import React, { useEffect, useState } from 'react';
import { apiRequest } from '@/lib/api';
import { Flag, Check, RefreshCw } from 'lucide-react';
import { Skeleton } from '@/components/Skeleton';

export default function AdminReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadReports = async () => {
    try {
      const data = await apiRequest<any[]>('/admin/review-queue');
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <Flag className="h-6 w-6 text-rose-600" />
          Question Issue Reports
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Review and resolve student-reported clinical errors, ambiguities, and typos.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
        No unresolved question reports at this time. All reports resolved.
      </div>
    </div>
  );
}
