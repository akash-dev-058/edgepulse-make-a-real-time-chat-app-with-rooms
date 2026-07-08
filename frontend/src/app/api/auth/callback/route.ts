import { NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

const SECRET = process.env.NEXTAUTH_SECRET!;

const JWT_SECRET = process.env.JWT_SECRET!;

export async function GET(request: Request) {
  const token = await getToken({ req: request, secret: SECRET });
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  const response = NextResponse.redirect(new URL('/rooms', request.url));
  response.cookies.set('next-auth.session-token', token.accessToken || '', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7,
    path: '/',
  });

  return response;
}
