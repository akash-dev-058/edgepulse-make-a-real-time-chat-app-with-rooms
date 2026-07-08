# RealTimeChatApp Frontend

A production-grade real-time multi-room chat application frontend built with Next.js 14, TypeScript, and Tailwind CSS.


## Features

- User authentication (register, login, logout)
- Room management (create, join, leave, list)
- Real-time messaging with Socket.io
- Message history with pagination
- Moderation tools (ban, kick)
- Responsive design (mobile, tablet, desktop)
- Accessibility-first components
- Error boundaries and loading states
- Type-safe API client with Zod validation


## Environment Variables

Create a `.env.local` file in the root directory with the following variables:



NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SOCKET_IO_BASE_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=next-auth-secret-min-32-chars-change-in-production
NEXTAUTH_URL_INTERNAL=http://frontend:3000
JWT_SECRET=min-32-char-secret-for-rs256-change-in-production
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
SOCKET_IO_SECRET=socket-io-secret-min-32-chars-change-in-production
NODE_ENV=development


## Development

### Prerequisites
- Node.js >= 18.0.0
- npm >= 9.0.0

### Installation
bash
npm install


### Running the Development Server
bash
npm run dev


The app will be available at `http://localhost:3000`.


### Building for Production
bash
npm run build
npm run start


### Linting and Formatting
bash
npm run lint
npm run format


### Testing
bash
npm run test
npm run test:watch


## Project Structure

frontend/
├── src/
│   ├── app/                  # App Router pages and layouts
│   ├── components/           # Reusable components
│   ├── lib/                  # Utility functions and API client
│   ├── hooks/                # Custom hooks
│   ├── types/                # TypeScript types
│   └── styles/              # Global styles
├── public/                  # Static assets
├── package.json             # Project dependencies and scripts
└── tailwind.config.js       # Tailwind CSS configuration


## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query, Zustand
- **Forms**: React Hook Form + Zod
- **Real-time**: Socket.io-client
- **Authentication**: NextAuth.js
- **Testing**: Vitest
- **Linting**: ESLint + Prettier


## Accessibility
- All interactive elements have ARIA labels
- Keyboard navigation support
- Focus management
- Skip navigation link
- Color contrast >= 4.5:1

## Performance
- Code splitting with Next.js dynamic imports
- Lazy loading for non-critical components
- Optimized images with Next.js Image
- Efficient state management with React Query

## Security
- Input validation with Zod and Pydantic
- Secure authentication with JWT
- Security headers via middleware
- Rate limiting on API endpoints
- CSRF protection with HTTP-only cookies

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License
MIT
