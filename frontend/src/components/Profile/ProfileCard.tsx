import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/Avatar';
import { Button } from '@/components/ui/Button';
import { signOut } from 'next-auth/react';
import { useToast } from '@/hooks/useToast';

interface ProfileCardProps {
  user: {
    id: string;
    name?: string | null;
    email?: string | null;
    image?: string | null;
  };
}

export function ProfileCard({ user }: ProfileCardProps) {
  const { addToast } = useToast();

  const handleSignOut = async () => {
    try {
      await signOut({ redirect: false });
      addToast({ title: 'Signed Out', description: 'You have been signed out', variant: 'success' });
    } catch (error) {
      addToast({ title: 'Error', description: 'Failed to sign out', variant: 'error' });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
      <div className="flex flex-col items-center gap-4">
        <Avatar className="h-20 w-20">
          <AvatarImage src={user.image || undefined} alt={user.name || 'User'} />
          <AvatarFallback>{user.name?.charAt(0) || 'U'}</AvatarFallback>
        </Avatar>
        <div className="text-center">
          <h2 className="text-2xl font-bold">{user.name || 'Unknown User'}</h2>
          <p className="text-brand-muted-foreground">{user.email}</p>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <Button variant="outline" className="w-full" asChild>
          <a href="/rooms">Back to Rooms</a>
        </Button>
        <Button variant="destructive" className="w-full" onClick={handleSignOut}>
          Sign Out
        </Button>
      </div>
    </div>
  );
}
