import { Button } from '@/components/ui/Button';

export default function ProvidersError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="text-center max-w-md space-y-6">
        <h1 className="text-4xl font-bold">Providers Error</h1>
        <p className="text-brand-muted-foreground">{error.message}</p>
        <Button onClick={() => reset()}>Retry Providers</Button>
      </div>
    </div>
  );
}
