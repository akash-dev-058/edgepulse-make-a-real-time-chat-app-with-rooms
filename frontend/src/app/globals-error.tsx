import { Button } from '@/components/ui/Button';

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <html lang="en">
      <body className="bg-brand-light text-brand-dark">
        <div className="flex-1 flex items-center justify-center p-4 min-h-screen">
          <div className="text-center max-w-md space-y-6">
            <h1 className="text-4xl font-bold">Global Error</h1>
            <p className="text-brand-muted-foreground">{error.message}</p>
            <Button onClick={() => reset()}>Retry Application</Button>
          </div>
        </div>
      </body>
    </html>
  );
}
