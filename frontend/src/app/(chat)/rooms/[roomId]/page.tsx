import { notFound } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import { RoomView } from '@/components/Room/RoomView';
import { getRoom } from '@/lib/api';

interface RoomPageProps {
  params: { roomId: string };
}

export default async function RoomPage({ params }: RoomPageProps) {
  const session = await getServerSession(authOptions);
  if (!session) {
    return notFound();
  }

  try {
    const room = await getRoom(params.roomId);
    if (!room) {
      return notFound();
    }

    return <RoomView room={room} session={session} />;
  } catch (error) {
    return notFound();
  }
}
