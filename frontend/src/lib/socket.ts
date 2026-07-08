import { io, Socket } from 'socket.io-client';
import { getSession } from 'next-auth/react';

interface SocketEventMap {
  'message:new': (message: { id: string; content: string; userId: string; roomId: string; createdAt: string }) => void;
  'user:joined': (user: { id: string; name: string; image?: string }) => void;
  'user:left': (userId: string) => void;
  'user:banned': (data: { userId: string; roomId: string; reason?: string }) => void;
  'user:kicked': (data: { userId: string; roomId: string }) => void;
  'moderation:ban': (data: { userId: string; roomId: string; reason?: string }) => void;
  'moderation:kick': (data: { userId: string; roomId: string }) => void;
  'error': (error: { message: string }) => void;
}

let socketInstance: Socket<SocketEventMap> | null = null;

let isConnecting = false;

async function getSocket(): Promise<Socket<SocketEventMap>> {
  if (socketInstance) {
    return socketInstance;
  }

  if (isConnecting) {
    await new Promise((resolve) => {
      const interval = setInterval(() => {
        if (socketInstance) {
          clearInterval(interval);
          resolve(socketInstance);
        }
      }, 100);
    });
    return socketInstance!;
  }

  isConnecting = true;
  try {
    const session = await getSession();
    const token = session?.accessToken;

    const socket = io(process.env.NEXT_PUBLIC_SOCKET_IO_BASE_URL || 'http://localhost:8000', {
      withCredentials: true,
      autoConnect: false,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      transports: ['websocket'],
      extraHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });

    socketInstance = socket;
    isConnecting = false;
    return socket;
  } catch (error) {
    isConnecting = false;
    throw new Error('Failed to initialize socket connection');
  }
}

function disconnectSocket() {
  if (socketInstance) {
    socketInstance.disconnect();
    socketInstance = null;
  }
}

export { getSocket, disconnectSocket };
