import { useState } from 'react';
import { ShieldCheckIcon, UserMinusIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/Button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/Dialog';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';
import { useToast } from '@/hooks/useToast';
import { banUser, kickUser } from '@/lib/api';

interface ModerationActionsProps {
  /** Room ID where moderation is happening */
  roomId: string;
  /** Current user ID (must be admin/mod) */
  userId: string;
  /** Whether current user has moderation privileges */
  isModerator: boolean;
}

/**
 * Moderation actions dialog with ban and kick functionality
 * Validates user input and provides feedback
 */
export function ModerationActions({ roomId, userId, isModerator }: ModerationActionsProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [userIdToModerate, setUserIdToModerate] = useState('');
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { addToast } = useToast();

  const handleBan = async () => {
    if (!userIdToModerate.trim()) {
      setError('User ID is required');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await banUser({ userId: userIdToModerate.trim(), roomId, reason });
      addToast({
        title: 'User Banned',
        description: `User ${userIdToModerate.trim()} has been banned from the room`,
        variant: 'success'
      });
      setIsOpen(false);
      setUserIdToModerate('');
      setReason('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to ban user');
      addToast({
        title: 'Failed to ban user',
        description: 'Please try again',
        variant: 'error'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKick = async () => {
    if (!userIdToModerate.trim()) {
      setError('User ID is required');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await kickUser({ userId: userIdToModerate.trim(), roomId });
      addToast({
        title: 'User Kicked',
        description: `User ${userIdToModerate.trim()} has been kicked from the room`,
        variant: 'success'
      });
      setIsOpen(false);
      setUserIdToModerate('');
      setReason('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to kick user');
      addToast({
        title: 'Failed to kick user',
        description: 'Please try again',
        variant: 'error'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isModerator) {
    return null;
  }

  return (
    <div className="flex items-center gap-2">
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button
            variant="outline"
            size="sm"
            aria-label="Moderation actions"
            disabled={!isModerator}
          >
            <ShieldCheckIcon className="h-4 w-4" />
            Moderate
          </Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Moderation Actions</DialogTitle>
            <DialogDescription>Select a user and action to perform</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="userId">User ID</Label>
              <Input
                id="userId"
                type="text"
                value={userIdToModerate}
                onChange={(e) => setUserIdToModerate(e.target.value)}
                placeholder="Enter user ID"
                aria-invalid={!!error}
                aria-describedby={error ? 'moderation-error' : undefined}
              />
            </div>
            <div>
              <Label htmlFor="reason">Reason (optional)</Label>
              <Input
                id="reason"
                type="text"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Enter reason"
              />
            </div>
            {error && (
              <p id="moderation-error" className="text-sm text-destructive" role="alert">
                {error}
              </p>
            )}
            <div className="flex gap-2">
              <Button
                variant="destructive"
                onClick={handleBan}
                className="flex-1"
                disabled={isSubmitting}
                aria-busy={isSubmitting}
              >
                <UserMinusIcon className="h-4 w-4 mr-2" />
                Ban User
              </Button>
              <Button
                variant="destructive"
                onClick={handleKick}
                className="flex-1"
                disabled={isSubmitting}
                aria-busy={isSubmitting}
              >
                <ExclamationCircleIcon className="h-4 w-4 mr-2" />
                Kick User
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}