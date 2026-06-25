/**
 * Shared TypeScript types for the frontend.
 */
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Room {
  id: string;
  name: string;
  unreadCount: number;
}

export interface Message {
  id: string;
  content: string;
  createdAt: string;
  isOwn?: boolean; // set on client for optimistic messages
}
