'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { HelpCircle, ChevronDown, ChevronUp, Mail, Send, CheckCircle2, ShieldCheck, Flag } from 'lucide-react';

export default function HelpPage() {
  const [openFaq, setOpenFaq] = useState<number | null>(0);
  const [supportCategory, setSupportCategory] = useState('question_inquiry');
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const faqs = [
    {
      q: 'How does Revizo scoring work?',
      a: 'Revizo follows standard NEET-PG scoring rules: +4 marks for each correct response, -1 mark for an incorrect response, and 0 marks for unattempted questions. Your accuracy, net score, and negative marks lost are calculated authoritatively upon submission.',
    },
    {
      q: 'What is the "Danger Zone"?',
      a: 'The Danger Zone isolates questions that you answered INCORRECTLY even though you selected "Definitely Know (100% Confidence)". In NEET-PG, overconfidence errors are the #1 cause of lost ranks. Revizo flags these clinical misconceptions so you can remediate them before the real exam.',
    },
    {
      q: 'How does Adaptive Spaced Revision work?',
      a: 'When you attempt or miss a concept, Revizo calculates an optimal retention interval (1 day, 3 days, 7 days, 14 days, 30 days). Concepts due for review automatically appear on your Dashboard and in the 5-Minute Spaced Revision queue.',
    },
    {
      q: 'Why is the Past-Year Questions (PYQ) module currently locked?',
      a: 'Revizo enforces strict medical provenance: we never display unverified or fabricated "memory recall" questions under the banner of official exams. The PYQ module remains disabled until official master papers with authentic answer keys pass independent cryptographic verification.',
    },
    {
      q: 'How do I report an issue with a question or explanation?',
      a: 'During or after any test, click "Report Question". You can flag disputed answer keys, ambiguous stems, or outdated guidelines. Critical safety reports trigger immediate automated quarantine for medical board review.',
    },
  ];

  const handleSupportSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setSubject('');
      setMessage('');
    }, 3000);
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 space-y-12">
      <div className="text-center space-y-2">
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Help Center & FAQ</h1>
        <p className="text-sm text-slate-600">Everything you need to know about practicing and revising with Revizo</p>
      </div>

      {/* FAQs */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm space-y-4">
        <h2 className="text-lg font-bold text-slate-900 mb-4">Frequently Asked Questions</h2>
        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div key={i} className="rounded-xl border border-slate-200 overflow-hidden">
              <button
                onClick={() => setOpenFaq(openFaq === i ? null : i)}
                className="w-full flex items-center justify-between p-4 text-left font-bold text-xs sm:text-sm text-slate-800 hover:bg-slate-50 transition-colors"
              >
                <span>{faq.q}</span>
                {openFaq === i ? <ChevronUp className="h-4 w-4 text-brand-600" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
              </button>
              {openFaq === i && (
                <div className="p-4 pt-0 text-xs sm:text-sm text-slate-600 leading-relaxed border-t border-slate-100 bg-slate-50/50">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Support Contact Form */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm space-y-6">
        <div className="space-y-1">
          <h2 className="text-lg font-bold text-slate-900">Contact Support & Clinical Governance</h2>
          <p className="text-xs text-slate-500">Need help with your account or have feedback for our medical reviewers?</p>
        </div>

        {submitted ? (
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-6 text-center space-y-2">
            <CheckCircle2 className="mx-auto h-8 w-8 text-emerald-600" />
            <p className="text-sm font-bold text-emerald-900">Support Ticket Submitted</p>
            <p className="text-xs text-emerald-700">Our medical education team will respond to your registered email shortly.</p>
          </div>
        ) : (
          <form onSubmit={handleSupportSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Category</label>
                <select
                  value={supportCategory}
                  onChange={(e) => setSupportCategory(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none bg-white"
                >
                  <option value="question_inquiry">Question / Content Inquiry</option>
                  <option value="technical_support">Technical Support</option>
                  <option value="account_billing">Account & Login</option>
                  <option value="medical_board">Medical Board Feedback</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Subject</label>
                <input
                  type="text"
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="Brief summary of your inquiry..."
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Message</label>
              <textarea
                required
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Provide details so we can assist you quickly..."
                className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-brand-500 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              className="flex items-center gap-2 rounded-lg bg-brand-600 px-6 py-2.5 text-xs font-bold text-white hover:bg-brand-700 shadow transition-colors"
            >
              <Send className="h-3.5 w-3.5" />
              Submit Ticket
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
