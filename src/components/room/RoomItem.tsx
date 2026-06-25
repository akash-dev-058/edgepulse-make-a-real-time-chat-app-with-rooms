import React from 'react';
import clsx from 'clsx';
import { Room } from '@/types';

interface RoomItemProps {
  room: Room;
  isActive: boolean;
  onSelect: () => void;
}

/**
 * Single room entry in the sidebar.
 */
const RoomItem: React.FC<RoomItemProps> = ({ room, isActive, onSelect }) => (
  <button
    onClick={onSelect}
    className={clsx(
      'w-full text-left px-3 py-2 rounded hover:bg-primary/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary',
      isActive ? 'bg-primary text-white' : 'text-gray-800'
    )}
    aria-current={isActive ? 'page' : undefined}
  >
    <div className="flex justify-between items-center">
      <span>{room.name}</span>
      {room.unreadCount > 0 && (
        <span className="ml-2 inline-flex items-center justify-center px-2 py-0.5 text-xs font-medium bg-accent text-white rounded-full">
          {room.unreadCount}
        </span>
      )}
    </div>
  </button>
);

export default RoomItem;
