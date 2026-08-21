import type { Metadata, Viewport } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth-context';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import MobileNav from '@/components/MobileNav';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  themeColor: '#0284c7',
};

export const metadata: Metadata = {
  title: 'Revizo — Turn Every Mistake Into Mastery | Intelligent Medical Revision',
  description:
    'Medically reviewed NEET-PG practice, adaptive spaced revision, mistake intelligence, and evidence-backed explanations.',
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="flex min-h-full flex-col bg-slate-50 text-slate-900 antialiased font-sans">
        <AuthProvider>
          <Navbar />
          <main className="flex-1 pb-16 md:pb-8">{children}</main>
          <MobileNav />
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
