import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import { LoginForm } from '@/components/Auth/LoginForm';

export default async function LoginPage() {
  const session = await getServerSession(authOptions);
  if (session) {
    redirect('/rooms');
  }

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight">Sign in to RealTimeChatApp</h1>
          <p className="mt-2 text-sm text-brand-muted-foreground">
            Enter your credentials to join the conversation
          </p>
        </div>
        <LoginForm />
      </div>
    </div>
  );
}
