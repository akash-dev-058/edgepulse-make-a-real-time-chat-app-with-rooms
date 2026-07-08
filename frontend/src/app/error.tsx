import { Button } from '@/components/ui/Button';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="text-center max-w-md space-y-6">
        <h1 className="text-4xl font-bold">Something went wrong!</h1>
        <p className="text-brand-muted-foreground">{error.message}</p>
        <Button onClick={() => reset()}>Try again</Button>
      </div>
    </div>
  );
}
