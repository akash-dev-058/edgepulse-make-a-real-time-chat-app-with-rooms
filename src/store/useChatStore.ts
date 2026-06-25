import { create } from 'zustand';
import { Room, Message } from '@/types';

interface ChatState {
  rooms: Room[];
  activeRoomId: string | null;
  messages: Message[];
  setRooms: (rooms: Room[]) => void;
  setActiveRoomId: (id: string) => void;
  setMessages: (msgs: Message[]) => void;
  addMessage: (msg: Message) => void;
  clearChat: () => void;
}

/**
 * Zustand store for chat UI state.
 */
export const useChatStore = create<ChatState>((set) => ({
  rooms: [],
  activeRoomId: null,
  messages: [],
  setRooms: (rooms) => set({ rooms }),
  setActiveRoomId: (id) => set({ activeRoomId: id, messages: [] }),
  setMessages: (msgs) => set({ messages: msgs }),
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  clearChat: () => set({ messages: [] }),
}));
