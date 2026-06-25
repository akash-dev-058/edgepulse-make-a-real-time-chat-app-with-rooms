import React from 'react';
import { Message } from '@/types';
import { formatDistanceToNow } from 'date-fns';
import clsx from 'clsx';

interface MessageItemProps {
  message: Message;
}

/**
 * Single chat message bubble.
 */
const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isOwn = message.isOwn;
  return (
    <li
      className={clsx(
        'max-w-xs md:max-w-md lg:max-w-lg',
        isOwn ? 'ml-auto' : 'mr-auto'
      )}
    >
      <div
        className={clsx(
          'px-3 py-2 rounded-lg shadow',
          isOwn ? 'bg-primary text-white' : 'bg-gray-200 text-gray-800'
        )}
      >
        <p>{message.content}</p>
        <span className="block text-xs text-gray-300 mt-1 text-right">
          {formatDistanceToNow(new Date(message.createdAt), { addSuffix: true })}
        </span>
      </div>
    </li>
  );
};

export default MessageItem;
