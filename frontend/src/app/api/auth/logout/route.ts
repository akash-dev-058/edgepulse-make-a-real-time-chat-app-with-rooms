import { NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

const SECRET = process.env.NEXTAUTH_SECRET!;

export async function POST(request: Request) {
  const token = await getToken({ req: request, secret: SECRET });
  const response = NextResponse.json({ message: 'Logged out successfully' });

  if (token?.accessToken) {
    response.cookies.delete('next-auth.session-token');
  }

  return response;
}
