import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import { RegisterForm } from '@/components/Auth/RegisterForm';

export default async function RegisterPage() {
  const session = await getServerSession(authOptions);
  if (session) {
    redirect('/rooms');
  }

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight">Create your account</h1>
          <p className="mt-2 text-sm text-brand-muted-foreground">
            Join RealTimeChatApp and start chatting in real-time
          </p>
        </div>
        <RegisterForm />
      </div>
    </div>
  );
}
