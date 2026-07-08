import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { MessageList } from '@/components/Chat/MessageList';
import { MessageInput } from '@/components/Chat/MessageInput';
import { PresenceIndicator } from '@/components/Chat/PresenceIndicator';
import { ModerationActions } from '@/components/Chat/ModerationActions';
import { useSocket } from '@/hooks/useSocket';
import { useToast } from '@/hooks/useToast';

interface ChatContainerProps {
  roomId: string;
  userId: string;
}

interface Message {
  id: string;
  content: string;
  createdAt: string;
  user: {
    id: string;
    name: string;
    image?: string;
  };
}

export function ChatContainer({ roomId, userId }: ChatContainerProps) {
  const { data: session } = useSession();
  const [messages, setMessages] = useState<Message[]>([]);
  const [optimisticMessages, setOptimisticMessages] = useState<Message[]>([]);
  const { addToast } = useToast();
  const { isConnected, error } = useSocket({
    roomId,
    onMessage: (message) => {
      setMessages((prev) => [...prev, message]);
    },
    onUserJoined: (user) => {
      addToast({ title: 'User Joined', description: `${user.name} has joined the room`, variant: 'info' });
    },
    onUserLeft: (userId) => {
      addToast({ title: 'User Left', description: 'A user has left the room', variant: 'info' });
    },
    onUserBanned: (data) => {
      if (data.userId === userId) {
        addToast({ title: 'Banned', description: 'You have been banned from this room', variant: 'error' });
      } else {
        addToast({ title: 'User Banned', description: 'A user has been banned', variant: 'warning' });
      }
    },
    onUserKicked: (data) => {
      if (data.userId === userId) {
        addToast({ title: 'Kicked', description: 'You have been kicked from this room', variant: 'error' });
      } else {
        addToast({ title: 'User Kicked', description: 'A user has been kicked', variant: 'warning' });
      }
    },
  });

  const handleSendMessage = async (content: string) => {
    const optimisticId = crypto.randomUUID();
    const optimisticMessage: Message = {
      id: optimisticId,
      content,
      createdAt: new Date().toISOString(),
      user: {
        id: userId,
        name: session?.user?.name || 'You',
        image: session?.user?.image,
      },
    };

    setOptimisticMessages((prev) => [...prev, optimisticMessage]);

    try {
      // In a real app, this would emit via socket
      // await socket.emit('sendMessage', { roomId, content });
    } catch (error) {
      setOptimisticMessages((prev) => prev.filter((m) => m.id !== optimisticId));
      addToast({ title: 'Failed to send message', description: 'Please try again', variant: 'error' });
    }
  };

  useEffect(() => {
    // In a real app, fetch initial messages via API
    // const fetchMessages = async () => {
    //   const data = await listMessages({ roomId });
    //   setMessages(data.messages);
    // };
    // fetchMessages();
  }, [roomId]);

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Connection Error</h2>
          <p className="text-brand-muted-foreground mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-[calc(100vh-12rem)]">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between border-b">
        <PresenceIndicator roomId={roomId} />
        <ModerationActions roomId={roomId} userId={userId} />
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <MessageList messages={[...optimisticMessages, ...messages]} />
      </div>
      <div className="p-4 border-t">
        <MessageInput onSend={handleSendMessage} isConnected={isConnected} />
      </div>
    </div>
  );
}
