import { redirect } from 'next/navigation';
import { Session } from 'next-auth';
import { joinRoom, leaveRoom } from '@/lib/api';
import { ChatContainer } from '@/components/Chat/ChatContainer';
import { RoomHeader } from '@/components/Room/RoomHeader';

interface Room {
  id: string;
  name: string;
  slug: string;
  description: string;
  createdAt: string;
  isMember: boolean;
}

interface RoomViewProps {
  room: Room;
  session: Session;
}

export async function RoomView({ room, session }: RoomViewProps) {
  const isMember = room.isMember;

  if (!isMember) {
    try {
      await joinRoom(room.id);
    } catch (error) {
      redirect('/rooms');
    }
  }

  async function handleLeaveRoom() {
    'use server';
    try {
      await leaveRoom(room.id);
    } catch (error) {
      // Ignore error on leave as user will be redirected anyway
    }
  }

  return (
    <div className="flex-1 flex flex-col min-h-[calc(100vh-4rem)]">
      <RoomHeader room={room} />
      <ChatContainer roomId={room.id} userId={session.user.id} />
    </div>
  );
}
