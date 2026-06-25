# RealTimeRoomChat Frontend

A production‑ready React + Vite frontend for a real‑time chat application with persistent rooms.

## Features
- **Authentication** (JWT) with login / registration forms.
- **Room management** – sidebar lists rooms, shows unread counts.
- **Real‑time messaging** via WebSocket with optimistic UI updates.
- **State management** – React Query for server data, Zustand for UI state.
- **Accessibility** – ARIA attributes, keyboard navigation, focus management.
- **Responsive design** – mobile‑first layout using Tailwind CSS.
- **Toast notifications**, loading skeletons, error boundaries, empty states.

## Prerequisites
- Node.js >= 20
- A running backend exposing the API defined in the project plan (see backend repo).

## Getting Started
bash
# Clone the repository
git clone <repo-url>
cd realtime-room-chat/frontend

# Install dependencies
npm ci

# Copy environment example and fill values
cp .env.example .env
# Edit .env with your backend URLs

# Run the development server
npm run dev


Open <http://localhost:5173> in your browser.

## Build
bash
npm run build
# Preview the production build
npm run preview


## Testing
bash
npm run test


## Folder Structure

src/
├─ app/            # Layout components (Header, Sidebar, Footer)
├─ components/    # Feature components (Chat, Message, RoomItem, etc.)
├─ hooks/         # Custom React hooks (useWebSocket, etc.)
├─ lib/           # API client and utility functions
├─ pages/         # Route pages (Dashboard, Login, Register, 404)
├─ providers/     # Context providers (AuthProvider)
├─ store/         # Zustand stores (auth, chat)
├─ types/         # TypeScript type definitions
└─ main.tsx       # Application entry point


## License
MIT
