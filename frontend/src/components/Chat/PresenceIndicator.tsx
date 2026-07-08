import { useEffect, useState } from 'react';
import { UserGroupIcon } from '@heroicons/react/24/outline';
import { useSocket } from '@/hooks/useSocket';

interface PresenceIndicatorProps {
  roomId: string;
}

interface PresenceState {
  onlineCount: number;
}

export function PresenceIndicator({ roomId }: PresenceIndicatorProps) {
  const [presence, setPresence] = useState<PresenceState>({ onlineCount: 0 });
  const { isConnected } = useSocket({
    roomId,
    onUserJoined: () => setPresence((prev) => ({ onlineCount: prev.onlineCount + 1 })),
    onUserLeft: () => setPresence((prev) => ({ onlineCount: Math.max(0, prev.onlineCount - 1) })),
  });

  useEffect(() => {
    // In a real app, fetch initial count via API
    // const fetchPresence = async () => {
    //   const data = await getPresence(roomId);
    //   setPresence(data);
    // };
    // fetchPresence();
  }, [roomId]);

  return (
    <div className="flex items-center gap-2 text-sm text-brand-muted-foreground">
      <UserGroupIcon className="h-5 w-5" />
      <span>{presence.onlineCount} online</span>
      {!isConnected && <span className="text-brand-warning">(disconnected)</span>}
    </div>
  );
}
