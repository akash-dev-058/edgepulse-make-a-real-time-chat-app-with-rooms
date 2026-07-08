import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';
import { useToast } from '@/hooks/useToast';
import { registerUser } from '@/lib/api';

const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type RegisterFormData = z.infer<typeof registerSchema>;

export function RegisterForm() {
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setError,
  } = useForm<RegisterFormData>({ resolver: zodResolver(registerSchema), mode: 'onChange' });

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      await registerUser({
        email: data.email,
        name: data.name,
        password: data.password,
      });

      addToast({ title: 'Account Created', description: 'Please sign in to continue', variant: 'success' });
      router.push('/login');
    } catch (error: any) {
      setError('root', { type: 'server', message: error.message });
      addToast({ title: 'Registration Failed', description: error.message, variant: 'error' });
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
          <Label htmlFor="name">Full Name</Label>
          <Input
            id="name"
            type="text"
            autoComplete="name"
            required
            {...register('name')}
            aria-invalid={!!errors.name}
            aria-describedby={errors.name ? 'name-error' : undefined}
          />
          {errors.name && (
            <p id="name-error" className="mt-1 text-sm text-brand-danger">
              {errors.name.message}
            </p>
          )}
        </div>

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
            autoComplete="new-password"
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
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </Button>
      </div>
    </form>
  );
}
