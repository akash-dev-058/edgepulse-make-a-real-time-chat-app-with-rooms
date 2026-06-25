import React, { useEffect, useRef } from 'react';
import { useChatStore } from '@/store/useChatStore';
import MessageList from '@/components/chat/MessageList';
import MessageInput from '@/components/chat/MessageInput';
import { useWebSocket } from '@/hooks/useWebSocket';
import LoadingSkeleton from '@/components/common/LoadingSkeleton';

/**
 * Main chat room view that ties together message list, input, and WebSocket handling.
 */
const ChatRoom: React.FC = () => {
  const { activeRoomId, setMessages, messages } = useChatStore();
  const { sendMessage, sendTyping, connectionStatus } = useWebSocket(activeRoomId);
  const listRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  if (!activeRoomId) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Select a room to start chatting.
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <header className="flex items-center justify-between px-4 py-2 bg-white border-b border-gray-200">
        <h2 className="text-lg font-semibold">Chat Room</h2>
        <span className="text-sm text-gray-500">
          {connectionStatus === 'connected' ? 'Online' : 'Connecting...'}
        </span>
      </header>
      <div ref={listRef} className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <LoadingSkeleton className="h-48" />
        ) : (
          <MessageList messages={messages} />
        )}
      </div>
      <MessageInput onSend={sendMessage} onTyping={sendTyping} />
    </div>
  );
};

export default ChatRoom;
