import { useEffect, useState } from 'react';
import { getSocket, disconnectSocket } from '@/lib/socket';
import { useToast } from '@/hooks/useToast';

interface UseSocketOptions {
  roomId?: string;
  onMessage?: (message: { id: string; content: string; userId: string; roomId: string; createdAt: string }) => void;
  onUserJoined?: (user: { id: string; name: string; image?: string }) => void;
  onUserLeft?: (userId: string) => void;
  onUserBanned?: (data: { userId: string; roomId: string; reason?: string }) => void;
  onUserKicked?: (data: { userId: string; roomId: string }) => void;
  onError?: (error: { message: string }) => void;
}

interface SocketState {
  isConnected: boolean;
  error: string | null;
}

export function useSocket(options: UseSocketOptions = {}) {
  const { roomId, onMessage, onUserJoined, onUserLeft, onUserBanned, onUserKicked, onError } = options;
  const [socketState, setSocketState] = useState<SocketState>({ isConnected: false, error: null });
  const { addToast } = useToast();

  useEffect(() => {
    let socket: any;
    let isMounted = true;

    async function initialize() {
      try {
        socket = await getSocket();

        socket.on('connect', () => {
          if (isMounted) {
            setSocketState({ isConnected: true, error: null });
            addToast({ title: 'Connected', description: 'Real-time connection established', variant: 'success' });
          }
        });

        socket.on('disconnect', () => {
          if (isMounted) {
            setSocketState({ isConnected: false, error: null });
            addToast({ title: 'Disconnected', description: 'Real-time connection lost', variant: 'warning' });
          }
        });

        socket.on('connect_error', (err) => {
          if (isMounted) {
            setSocketState({ isConnected: false, error: err.message });
            addToast({ title: 'Connection Error', description: err.message, variant: 'error' });
            if (onError) onError({ message: err.message });
          }
        });

        if (roomId) {
          socket.emit('joinRoom', { roomId });
        }

        socket.on('message:new', (message) => {
          if (onMessage) onMessage(message);
        });

        socket.on('user:joined', (user) => {
          if (onUserJoined) onUserJoined(user);
        });

        socket.on('user:left', (userId) => {
          if (onUserLeft) onUserLeft(userId);
        });

        socket.on('user:banned', (data) => {
          if (onUserBanned) onUserBanned(data);
        });

        socket.on('user:kicked', (data) => {
          if (onUserKicked) onUserKicked(data);
        });

      } catch (error: any) {
        if (isMounted) {
          setSocketState({ isConnected: false, error: error.message });
          addToast({ title: 'Socket Error', description: error.message, variant: 'error' });
        }
      }
    }

    initialize();

    return () => {
      isMounted = false;
      if (socket) {
        if (roomId) {
          socket.emit('leaveRoom', { roomId });
        }
        socket.offAny();
        disconnectSocket();
      }
    };
  }, [roomId, onMessage, onUserJoined, onUserLeft, onUserBanned, onUserKicked, onError, addToast]);

  return socketState;
}
