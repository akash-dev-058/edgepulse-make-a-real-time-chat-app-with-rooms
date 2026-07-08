import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';
import { Textarea } from '@/components/ui/Textarea';
import { useToast } from '@/hooks/useToast';
import { createRoom } from '@/lib/api';

const createRoomSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters').max(50, 'Name must be less than 50 characters'),
  slug: z
    .string()
    .min(3, 'Slug must be at least 3 characters')
    .max(30, 'Slug must be less than 30 characters')
    .regex(/^[a-z0-9-]+$/, 'Slug can only contain lowercase letters, numbers, and hyphens'),
  description: z.string().max(200, 'Description must be less than 200 characters').optional(),
});

type CreateRoomFormData = z.infer<typeof createRoomSchema>;

export function CreateRoomForm() {
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setError,
  } = useForm<CreateRoomFormData>({ resolver: zodResolver(createRoomSchema), mode: 'onChange' });

  const onSubmit = async (data: CreateRoomFormData) => {
    setIsLoading(true);
    try {
      await createRoom({
        name: data.name,
        slug: data.slug,
        description: data.description,
      });
      addToast({ title: 'Room Created', description: 'Your room is ready to use', variant: 'success' });
      router.push('/rooms');
    } catch (error: any) {
      setError('root', { type: 'server', message: error.message });
      addToast({ title: 'Failed to Create Room', description: error.message, variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {errors.root && (
        <div className="p-4 bg-brand-danger text-white rounded-md text-sm">
          {errors.root.message}
        </div>
      )}

      <div className="space-y-4">
        <div>
          <Label htmlFor="name">Room Name</Label>
          <Input
            id="name"
            type="text"
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
          <Label htmlFor="slug">Slug (URL-friendly)</Label>
          <div className="flex">
            <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-brand-muted bg-brand-muted text-brand-muted-foreground text-sm">
              /rooms/
            </span>
            <Input
              id="slug"
              type="text"
              required
              className="rounded-l-none"
              {...register('slug')}
              aria-invalid={!!errors.slug}
              aria-describedby={errors.slug ? 'slug-error' : undefined}
            />
          </div>
          {errors.slug && (
            <p id="slug-error" className="mt-1 text-sm text-brand-danger">
              {errors.slug.message}
            </p>
          )}
          <p className="text-xs text-brand-muted-foreground mt-1">
            Only lowercase letters, numbers, and hyphens allowed
          </p>
        </div>

        <div>
          <Label htmlFor="description">Description (optional)</Label>
          <Textarea id="description" {...register('description')} aria-describedby={errors.description ? 'description-error' : undefined} />
          {errors.description && (
            <p id="description-error" className="mt-1 text-sm text-brand-danger">
              {errors.description.message}
            </p>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <Button type="button" variant="outline" asChild>
          <a href="/rooms">Cancel</a>
        </Button>
        <Button type="submit" disabled={!isValid || isLoading}>
          {isLoading ? 'Creating...' : 'Create Room'}
        </Button>
      </div>
    </form>
  );
}
