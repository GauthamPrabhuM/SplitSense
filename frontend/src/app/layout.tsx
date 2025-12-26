import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import '../styles/globals.css';
import { cn } from '../lib/utils';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  title: 'SplitSense - Splitwise Analytics Dashboard',
  description: 'Comprehensive analytics and insights for your Splitwise data. Track spending, analyze balances, and understand your shared expenses.',
  keywords: ['splitwise', 'analytics', 'expenses', 'tracking', 'dashboard'],
  authors: [{ name: 'SplitSense Team' }],
  openGraph: {
    title: 'SplitSense - Splitwise Analytics Dashboard',
    description: 'Comprehensive analytics and insights for your Splitwise data.',
    type: 'website',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0b' },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          'min-h-screen bg-background font-sans antialiased',
          inter.variable
        )}
      >
        {children}
      </body>
    </html>
  );
}
