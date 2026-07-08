import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export function CreateRoomButton() {
  return (
    <Button asChild>
      <Link href="/rooms/create">Create Room</Link>
    </Button>
  );
}
