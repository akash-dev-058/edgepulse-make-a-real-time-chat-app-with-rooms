import { Button } from '@/components/ui/Button';
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="text-center max-w-md space-y-6">
        <h1 className="text-4xl font-bold">404 - Page Not Found</h1>
        <p className="text-brand-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Button asChild>
          <Link href="/rooms">Return to Rooms</Link>
        </Button>
      </div>
    </div>
  );
}
