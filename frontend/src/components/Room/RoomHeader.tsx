import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ArrowLeftIcon } from '@heroicons/react/24/outline';

interface Room {
  id: string;
  name: string;
  slug: string;
  description: string;
  createdAt: string;
}

interface RoomHeaderProps {
  room: Room;
}

export function RoomHeader({ room }: RoomHeaderProps) {
  return (
    <header className="bg-white shadow-sm sticky top-0 z-20">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/rooms" aria-label="Back to rooms">
              <ArrowLeftIcon className="h-5 w-5" />
            </Link>
          </Button>
          <div>
            <h1 className="text-xl font-bold">{room.name}</h1>
            <p className="text-sm text-brand-muted-foreground">{room.description}</p>
          </div>
        </div>
        <Button variant="outline" size="sm" asChild>
          <Link href={`/rooms/${room.slug}`}>Share</Link>
        </Button>
      </div>
    </header>
  );
}
