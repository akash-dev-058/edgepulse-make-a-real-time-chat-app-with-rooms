import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/Avatar';

interface NavLink {
  href: string;
  label: string;
}

const navLinks: NavLink[] = [
  { href: '/rooms', label: 'Rooms' },
  { href: '/rooms/create', label: 'Create Room' },
];

export function Navbar() {
  const { data: session } = useSession();
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <header className="bg-brand-primary text-white shadow-md sticky top-0 z-30">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold tracking-wider">
          RealTimeChatApp
        </Link>

        <nav className="hidden md:flex items-center gap-6">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hover:text-brand-light transition-colors font-medium"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          {session ? (
            <div className="hidden md:flex items-center gap-4">
              <Avatar className="h-8 w-8">
                <AvatarImage src={session.user?.image || undefined} alt={session.user?.name || 'User'} />
                <AvatarFallback>{session.user?.name?.charAt(0) || 'U'}</AvatarFallback>
              </Avatar>
              <span className="hidden md:inline font-medium">{session.user?.name}</span>
              <Button variant="ghost" asChild>
                <Link href="/profile">Profile</Link>
              </Button>
              <Button variant="outline" asChild>
                <Link href="/api/auth/signout">Sign Out</Link>
              </Button>
            </div>
          ) : (
            <div className="hidden md:flex items-center gap-2">
              <Button variant="outline" asChild>
                <Link href="/login">Sign In</Link>
              </Button>
              <Button asChild>
                <Link href="/register">Sign Up</Link>
              </Button>
            </div>
          )}

          <button
            className="md:hidden p-2 rounded-md hover:bg-brand-primary-dark transition-colors"
            onClick={toggleMenu}
            aria-label={isOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={isOpen}
          >
            {isOpen ? (
              <XMarkIcon className="h-6 w-6" />
            ) : (
              <Bars3Icon className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-brand-primary-dark px-4 pb-4">
          <nav className="flex flex-col gap-4">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="py-2 font-medium hover:text-brand-light transition-colors"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            {session ? (
              <>
                <div className="flex items-center gap-3 py-2">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={session.user?.image || undefined} alt={session.user?.name || 'User'} />
                    <AvatarFallback>{session.user?.name?.charAt(0) || 'U'}</AvatarFallback>
                  </Avatar>
                  <span>{session.user?.name}</span>
                </div>
                <Button variant="ghost" size="sm" asChild>
                  <Link href="/profile" onClick={() => setIsOpen(false)}>Profile</Link>
                </Button>
                <Button variant="outline" size="sm" asChild>
                  <Link href="/api/auth/signout" onClick={() => setIsOpen(false)}>Sign Out</Link>
                </Button>
              </>
            ) : (
              <>
                <Button variant="outline" size="sm" asChild>
                  <Link href="/login" onClick={() => setIsOpen(false)}>Sign In</Link>
                </Button>
                <Button size="sm" asChild>
                  <Link href="/register" onClick={() => setIsOpen(false)}>Sign Up</Link>
                </Button>
              </>
            )}
          </nav>
        </div>
      )}
    </header>
  );
}
