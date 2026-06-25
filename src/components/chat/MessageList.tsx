import React from 'react';
import { Message } from '@/types';
import MessageItem from '@/components/chat/MessageItem';

interface MessageListProps {
  messages: Message[];
}

/**
 * Renders a list of messages.
 */
const MessageList: React.FC<MessageListProps> = ({ messages }) => (
  <ul className="space-y-2" role="list" aria-label="Message list">
    {messages.map((msg) => (
      <MessageItem key={msg.id} message={msg} />
    ))}
  </ul>
);

export default MessageList;
