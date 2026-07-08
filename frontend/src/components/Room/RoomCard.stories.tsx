import type { Meta, StoryObj } from '@storybook/react';
import { RoomCard } from './RoomCard';

const meta = {
  title: 'Components/Room/RoomCard',
  component: RoomCard,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof RoomCard>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    room: {
      id: 'room-1',
      name: 'General Chat',
      slug: 'general-chat',
      description: 'A general discussion room for all users',
      createdAt: new Date().toISOString(),
      memberCount: 42,
    },
  },
};

export const LongDescription: Story = {
  args: {
    room: {
      id: 'room-2',
      name: 'Development Room',
      slug: 'dev-room',
      description: 'A dedicated space for developers to discuss technical topics and share code snippets. This room is perfect for collaborative problem-solving and knowledge sharing.',
      createdAt: new Date().toISOString(),
      memberCount: 128,
    },
  },
};
