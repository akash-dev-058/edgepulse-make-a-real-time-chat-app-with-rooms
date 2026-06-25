import React from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import { loginUser } from '@/lib/api';
import { toast } from '@/components/common/Toast';

const schema = z.object({
  email: z.string().email({ message: 'Invalid email address' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
});

type FormData = z.infer<typeof schema>;

const Login: React.FC = () => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  const navigate = useNavigate();
  const { setUser, setToken } = useAuthStore();

  const onSubmit = async (data: FormData) => {
    try {
      const response = await loginUser(data.email, data.password);
      setToken(response.access_token);
      setUser(response.user);
      toast.success('Logged in successfully');
      navigate('/dashboard');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
        <h2 className="mb-6 text-2xl font-bold text-center">Login</h2>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="mb-4">
            <label htmlFor="email" className="block mb-1 font-medium">Email</label>
            <input
              id="email"
              type="email"
              {...register('email')}
              className={`w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
              aria-invalid={!!errors.email}
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {errors.email && (
              <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
                {errors.email.message}
              </p>
            )}
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block mb-1 font-medium">Password</label>
            <input
              id="password"
              type="password"
              {...register('password')}
              className={`w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
              aria-invalid={!!errors.password}
              aria-describedby={errors.password ? 'password-error' : undefined}
            />
            {errors.password && (
              <p id="password-error" className="mt-1 text-sm text-red-600" role="alert">
                {errors.password.message}
              </p>
            )}
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full px-4 py-2 font-semibold text-white bg-primary rounded hover:bg-primary/90 disabled:opacity-50"
          >
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="mt-4 text-center text-sm">
          Don\'t have an account?{' '}
          <Link to="/register" className="text-primary hover:underline">Register</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
