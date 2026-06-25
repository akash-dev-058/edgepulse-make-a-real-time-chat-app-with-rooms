import React, { useState, useRef, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from '@/components/common/Toast';

/**
 * Validation schema for the message input.
 * - `content` must be a non‑empty string with a maximum length of 1000 characters.
 */
const schema = z.object({
  content: z.string().min(1, { message: 'Message cannot be empty' }).max(1000),
});

type FormData = z.infer<typeof schema>;

/**
 * Props for {@link MessageInput}.
 */
interface MessageInputProps {
  /**
   * Callback invoked when the user submits a message.
   * It may be synchronous or return a promise.
   */
  onSend: (content: string) => Promise<void> | void;
  /**
   * Callback invoked when the user starts typing. Used to broadcast typing
   * indicators to other participants.
   */
  onTyping: () => void;
}

/**
 * MessageInput renders a textarea with validation, optimistic UI handling and
 * typing‑indicator support. It uses `react-hook-form` together with Zod for
 * schema‑based validation, displays accessible error messages and cleans up any
 * pending timers when unmounted.
 */
const MessageInput: React.FC<MessageInputProps> = ({ onSend, onTyping }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const [isTyping, setIsTyping] = useState(false);
  // In the browser `setTimeout` returns a number, not NodeJS.Timeout.
  const typingTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  /**
   * Handles typing events. It notifies the parent via `onTyping` the first time
   * the user types and then resets a debounce timer. When the timer expires we
   * consider the user stopped typing.
   */
  const handleTyping = () => {
    if (!isTyping) {
      setIsTyping(true);
      onTyping();
    }
    if (typingTimeout.current) clearTimeout(typingTimeout.current);
    typingTimeout.current = setTimeout(() => setIsTyping(false), 1500);
  };

  /**
   * Submits the form. Errors from the `onSend` callback are caught and shown via
   * a toast notification. The form is reset on successful send.
   */
  const onSubmit = async (data: FormData) => {
    try {
      await Promise.resolve(onSend(data.content));
      reset();
    } catch (err) {
      // Log the error for debugging purposes (could be sent to Sentry later).
      console.error('Message send error:', err);
      toast.error('Failed to send message');
    }
  };

  // Cleanup any pending timeout when the component unmounts.
  useEffect(() => {
    return () => {
      if (typingTimeout.current) clearTimeout(typingTimeout.current);
    };
  }, []);

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="p-4 border-t border-gray-200"
      noValidate
      aria-label="Message input form"
    >
      <div className="flex items-center">
        <textarea
          {...register('content')}
          onKeyDown={handleTyping}
          placeholder="Type a message..."
          className="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary resize-none"
          rows={1}
          aria-invalid={!!errors.content}
          aria-describedby={errors.content ? 'content-error' : undefined}
          aria-label="Message content"
        />
        <button
          type="submit"
          disabled={isSubmitting}
          className="ml-2 px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
        >
          {isSubmitting ? 'Sending...' : 'Send'}
        </button>
      </div>
      {errors.content && (
        <p
          id="content-error"
          className="mt-1 text-sm text-red-600"
          role="alert"
        >
          {errors.content.message}
        </p>
      )}
    </form>
  );
};

export default MessageInput;
