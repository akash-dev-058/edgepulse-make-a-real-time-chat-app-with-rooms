import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';
import { Toaster } from '@/components/ui/Toaster';
import { SkipNav } from '@/components/layout/SkipNav';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: {
    default: 'RealTimeChatApp - Connect in Real-Time',
    template: '%s | RealTimeChatApp',
  },
  description: 'A real-time multi-room chat application with user authentication, moderation tools, and message history',
  keywords: ['chat', 'real-time', 'rooms', 'community', 'messaging'],
  authors: [{ name: 'RealTimeChatApp Team' }],
  creator: 'RealTimeChatApp',
  publisher: 'RealTimeChatApp',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: 'RealTimeChatApp - Connect in Real-Time',
    description: 'A real-time multi-room chat application with user authentication, moderation tools, and message history',
    url: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3000',
    siteName: 'RealTimeChatApp',
    images: [
      {
        url: 'https://images.pexels.com/photos/33688258/pexels-photo-33688258.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
        width: 1200,
        height: 630,
        alt: 'RealTimeChatApp - Connect in Real-Time',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'RealTimeChatApp - Connect in Real-Time',
    description: 'A real-time multi-room chat application with user authentication, moderation tools, and message history',
    images: ['https://images.pexels.com/photos/33688258/pexels-photo-33688258.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'],
    creator: '@realtimechatapp',
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#3b82f6" />
        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </head>
      <body className={`${inter.variable} font-sans antialiased bg-brand-light text-brand-dark`}>
        <SkipNav />
        <Providers>
          <div className="min-h-screen flex flex-col">
            {children}
          </div>
        </Providers>
        <Toaster />
      </body>
    </html>
  );
}
