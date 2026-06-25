import React, { useEffect } from 'react';
import { useChatStore } from '@/store/useChatStore';
import { useAuthStore } from '@/store/useAuthStore';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import ChatRoom from '@/components/chat/ChatRoom';
import { useQuery } from '@tanstack/react-query';
import { fetchRooms } from '@/lib/api';
import LoadingSkeleton from '@/components/common/LoadingSkeleton';
import EmptyState from '@/components/common/EmptyState';

/**
 * Dashboard page that displays the chat interface.
 * It loads the user's rooms and selects the first one by default.
 */
const Dashboard: React.FC = () => {
  const { token, logout } = useAuthStore();
  const { rooms, setRooms, activeRoomId, setActiveRoomId } = useChatStore();

  const { data, isLoading, isError, error } = useQuery(['rooms'], () => fetchRooms(token!), {
    enabled: !!token,
    staleTime: 1000 * 60,
  });

  useEffect(() => {
    if (data) {
      setRooms(data);
      if (!activeRoomId && data.length > 0) {
        setActiveRoomId(data[0].id);
      }
    }
  }, [data, activeRoomId, setRooms, setActiveRoomId]);

  if (isLoading) {
    return <LoadingSkeleton className="h-screen" />;
  }

  if (isError) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-red-600">Failed to load rooms: {(error as Error).message}</p>
        <button
          onClick={() => window.location.reload()}
          className="ml-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary/80"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!rooms || rooms.length === 0) {
    return (
      <EmptyState
        title="No rooms yet"
        description="Create a room to start chatting with your team."
        imageUrl="https://images.pexels.com/photos/33688258/pexels-photo-33688258.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
        imageAlt="A lively outdoor gathering with people interacting in a vibrant community setting."
        ctaLabel="Create Room"
        onCtaClick={() => alert('Room creation UI not implemented in this demo')}
      />
    );
  }

  return (
    <div className="flex flex-col h-screen">
      <Header onLogout={logout} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-4">
          <ChatRoom />
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
