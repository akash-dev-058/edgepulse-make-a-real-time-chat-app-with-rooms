import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';
import { useToast } from '@/hooks/useToast';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setError,
  } = useForm<LoginFormData>({ resolver: zodResolver(loginSchema), mode: 'onChange' });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    try {
      const result = await signIn('credentials', {
        email: data.email,
        password: data.password,
        redirect: false,
        callbackUrl: '/rooms',
      });

      if (result?.error) {
        setError('root', { type: 'server', message: result.error });
        addToast({ title: 'Login Failed', description: result.error, variant: 'error' });
      } else if (result?.url) {
        router.push(result.url);
      }
    } catch (error) {
      addToast({ title: 'Error', description: 'An unexpected error occurred', variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-6">
      {errors.root && (
        <div className="p-4 bg-brand-danger text-white rounded-md text-sm">
          {errors.root.message}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <Label htmlFor="email">Email address</Label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            required
            {...register('email')}
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'email-error' : undefined}
          />
          {errors.email && (
            <p id="email-error" className="mt-1 text-sm text-brand-danger">
              {errors.email.message}
            </p>
          )}
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            {...register('password')}
            aria-invalid={!!errors.password}
            aria-describedby={errors.password ? 'password-error' : undefined}
          />
          {errors.password && (
            <p id="password-error" className="mt-1 text-sm text-brand-danger">
              {errors.password.message}
            </p>
          )}
        </div>
      </div>

      <div>
        <Button type="submit" className="w-full" disabled={!isValid || isLoading}>
          {isLoading ? 'Signing in...' : 'Sign In'}
        </Button>
      </div>
    </form>
  );
}
