import Link from 'next/link';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import { listRooms } from '@/lib/api';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/Avatar';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Skeleton } from '@/components/ui/Skeleton';

interface Room {
  id: string;
  name: string;
  slug: string;
  description: string;
  createdAt: string;
  memberCount: number;
}

async function RoomList() {
  const session = await getServerSession(authOptions);
  const data = await listRooms();
  const rooms = data.rooms || [];

  if (rooms.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold mb-2">No rooms yet</h2>
        <p className="text-brand-muted-foreground mb-4">
          Be the first to create a room and start chatting!
        </p>
        <Button asChild>
          <Link href="/rooms/create">Create Room</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {rooms.map((room) => (
        <Card key={room.id} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Avatar className="h-8 w-8">
                <AvatarFallback>{room.name.charAt(0)}</AvatarFallback>
              </Avatar>
              {room.name}
            </CardTitle>
            <CardDescription>{room.description}</CardDescription>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <div className="text-sm text-brand-muted-foreground">
              <p>Members: {room.memberCount}</p>
              <p>Created: {new Date(room.createdAt).toLocaleDateString()}</p>
            </div>
            <Button variant="outline" asChild>
              <Link href={`/rooms/${room.slug}`}>Join</Link>
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export { RoomList };
