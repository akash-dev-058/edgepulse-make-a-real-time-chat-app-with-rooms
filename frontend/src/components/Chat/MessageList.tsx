import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/Avatar';
import { formatTime } from '@/lib/utils';

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

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">No messages yet</h2>
          <p className="text-brand-muted-foreground">Start the conversation!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {messages.map((message) => (
        <div key={message.id} className="flex gap-3">
          <Avatar className="h-8 w-8 flex-shrink-0">
            <AvatarImage src={message.user.image} alt={message.user.name} />
            <AvatarFallback>{message.user.name.charAt(0)}</AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <div className="flex items-baseline gap-2">
              <p className="font-medium truncate">{message.user.name}</p>
              <time className="text-xs text-brand-muted-foreground whitespace-nowrap" dateTime={message.createdAt}>
                {formatTime(message.createdAt)}
              </time>
            </div>
            <p className="mt-1 text-sm break-words">{message.content}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
