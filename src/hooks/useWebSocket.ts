import { useEffect, useRef, useState, useCallback } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { useChatStore } from '@/store/useChatStore';
import { Message } from '@/types';
import { toast } from '@/components/common/Toast';

/**
 * Custom hook that manages a WebSocket connection for a given room.
 * Handles reconnection with exponential backoff and provides send functions.
 */
export const useWebSocket = (roomId: string | null) => {
  const { token } = useAuthStore();
  const { addMessage } = useChatStore();
  const wsRef = useRef<WebSocket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  const reconnectAttempts = useRef(0);

  const connect = useCallback(() => {
    if (!roomId || !token) return;
    const wsUrl = `${import.meta.env.VITE_WS_URL}?token=${encodeURIComponent(token)}&room_id=${roomId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;
    setConnectionStatus('connecting');

    ws.onopen = () => {
      setConnectionStatus('connected');
      reconnectAttempts.current = 0;
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as { type: string; payload: any };
        if (data.type === 'message') {
          const msg: Message = data.payload;
          addMessage(msg);
        } else if (data.type === 'typing') {
          // Handle typing indicator if needed
        }
      } catch (err) {
        console.error('WebSocket message parse error', err);
      }
    };

    ws.onerror = (err) => {
      console.error('WebSocket error', err);
    };

    ws.onclose = () => {
      setConnectionStatus('disconnected');
      // Exponential backoff reconnection
      const timeout = Math.min(10000, 1000 * 2 ** reconnectAttempts.current);
      reconnectAttempts.current += 1;
      setTimeout(() => {
        connect();
      }, timeout);
    };
  }, [roomId, token, addMessage]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  const sendMessage = useCallback(
    (content: string) => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        const payload = { type: 'message', payload: { content } };
        wsRef.current.send(JSON.stringify(payload));
        // Optimistic UI: add message locally with temporary ID
        const optimisticMsg: Message = {
          id: `temp-${Date.now()}`,
          content,
          createdAt: new Date().toISOString(),
          isOwn: true,
        } as Message;
        addMessage(optimisticMsg);
      } else {
        toast.error('Connection not ready. Message not sent.');
      }
    },
    [addMessage]
  );

  const sendTyping = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'typing' }));
    }
  }, []);

  return { sendMessage, sendTyping, connectionStatus };
};
