import { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { useToast } from '@/hooks/useToast';

interface MessageInputProps {
  /** Room ID to send message to */
  roomId: string;
  /** Callback when message is sent */
  onSend: (content: string, roomId: string) => Promise<void>;
  /** Whether socket connection is active */
  isConnected: boolean;
  /** Current user ID */
  userId?: string;
}

/**
 * Message input component with textarea and send button
 * Handles optimistic UI updates and auto-resizing
 */
export function MessageInput({ roomId, onSend, isConnected, userId }: MessageInputProps) {
  const [content, setContent] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { addToast } = useToast();

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [content]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!content.trim()) return;
    if (!isConnected) {
      setError('Connection lost. Please reconnect.');
      addToast({
        title: 'Connection Error',
        description: 'Unable to send message while disconnected',
        variant: 'error'
      });
      return;
    }

    if (!userId) {
      setError('User not authenticated');
      addToast({
        title: 'Authentication Required',
        description: 'Please log in to send messages',
        variant: 'error'
      });
      return;
    }

    try {
      setIsSending(true);
      setError(null);
      await onSend(content, roomId);
      setContent('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      addToast({
        title: 'Message Failed',
        description: 'Please try again',
        variant: 'error'
      });
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full">
      <Textarea
        ref={textareaRef}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type a message..."
        rows={1}
        className="flex-1 resize-none min-h-[44px] max-h-[200px]"
        disabled={!isConnected || !userId}
        aria-label="Message input"
        aria-invalid={!!error}
        aria-describedby={error ? 'message-error' : undefined}
      />
      <Button
        type="submit"
        size="icon"
        disabled={!content.trim() || !isConnected || !userId || isSending}
        aria-label="Send message"
        aria-busy={isSending}
      >
        {isSending ? (
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : (
          <PaperAirplaneIcon className="h-5 w-5" />
        )}
      </Button>
      {error && (
        <p id="message-error" className="text-sm text-destructive mt-1" role="alert">
          {error}
        </p>
      )}
    </form>
  );
}