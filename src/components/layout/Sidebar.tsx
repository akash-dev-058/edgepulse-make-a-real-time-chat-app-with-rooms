import React from 'react';
import { useChatStore } from '@/store/useChatStore';
import { useQuery } from '@tanstack/react-query';
import { fetchRooms } from '@/lib/api';
import { useAuthStore } from '@/store/useAuthStore';
import RoomItem from '@/components/room/RoomItem';
import LoadingSkeleton from '@/components/common/LoadingSkeleton';
import EmptyState from '@/components/common/EmptyState';

/**
 * Sidebar that lists rooms the user belongs to.
 * Shows loading, error, and empty states.
 */
const Sidebar: React.FC = () => {
  const { token } = useAuthStore();
  const { rooms, setRooms, activeRoomId, setActiveRoomId } = useChatStore();

  const { data, isLoading, isError, error } = useQuery(['rooms'], () => fetchRooms(token!), {
    enabled: !!token,
    staleTime: 1000 * 60,
  });

  React.useEffect(() => {
    if (data) {
      setRooms(data);
    }
  }, [data, setRooms]);

  if (isLoading) {
    return <LoadingSkeleton className="w-64 p-4" />;
  }

  if (isError) {
    return (
      <div className="p-4 text-red-600">
        Failed to load rooms: {(error as Error).message}
        <button
          onClick={() => window.location.reload()}
          className="ml-2 text-primary underline"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!rooms || rooms.length === 0) {
    return (
      <EmptyState
        title="No rooms"
        description="Create a room to start chatting."
        imageUrl="https://images.pexels.com/photos/37495850/pexels-photo-37495850.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
        imageAlt="A large group of people sitting outdoors under a tree, showcasing diversity and unity."
        ctaLabel="Create Room"
        onCtaClick={() => alert('Room creation not implemented')}
      />
    );
  }

  return (
    <aside className="w-64 bg-gray-100 overflow-y-auto border-r border-gray-200" aria-label="Room list">
      <nav className="p-4">
        {rooms.map((room) => (
          <RoomItem
            key={room.id}
            room={room}
            isActive={room.id === activeRoomId}
            onSelect={() => setActiveRoomId(room.id)}
          />
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
