import { Suspense } from 'react';
import { RoomListSkeleton } from '@/components/Room/RoomListSkeleton';
import { RoomList } from '@/components/Room/RoomList';
import { CreateRoomButton } from '@/components/Room/CreateRoomButton';

export default function RoomsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Rooms</h1>
        <CreateRoomButton />
      </div>

      <Suspense fallback={<RoomListSkeleton />}>
        <RoomList />
      </Suspense>
    </div>
  );
}
