import { useToast } from '@/hooks/useToast';
import { Transition } from '@headlessui/react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { useEffect, useState } from 'react';

interface ToastProps {
  id: string;
  title?: string;
  description?: string;
  variant?: 'default' | 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}

function Toast({ id, title, description, variant = 'default', duration = 5000 }: ToastProps) {
  const [isVisible, setIsVisible] = useState(false);
  const { dismissToast } = useToast();

  useEffect(() => {
    setIsVisible(true);
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => dismissToast(id), 300);
    }, duration);
    return () => clearTimeout(timer);
  }, [id, duration, dismissToast]);

  const getVariantStyles = () => {
    switch (variant) {
      case 'success':
        return 'bg-brand-success text-white border-l-4 border-l-brand-success-dark';
      case 'error':
        return 'bg-brand-danger text-white border-l-4 border-l-brand-danger-dark';
      case 'warning':
        return 'bg-brand-warning text-white border-l-4 border-l-brand-warning-dark';
      case 'info':
        return 'bg-brand-info text-white border-l-4 border-l-brand-info-dark';
      default:
        return 'bg-white text-brand-dark border border-brand-muted rounded-lg shadow-lg';
    }
  };

  return (
    <Transition
      show={isVisible}
      enter="transition-all duration-300 ease-out"
      enterFrom="opacity-0 scale-95"
      enterTo="opacity-100 scale-100"
      leave="transition-all duration-200 ease-in"
      leaveFrom="opacity-100 scale-100"
      leaveTo="opacity-0 scale-95"
    >
      <div
        className={`p-4 mb-2 rounded-md shadow-lg ${getVariantStyles()}`}
        role="status"
        aria-live="polite"
      >
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            {title && <p className="font-medium">{title}</p>}
            {description && <p className="text-sm mt-1">{description}</p>}
          </div>
          <button
            onClick={() => dismissToast(id)}
            className="text-inher-it hover:text-opacity-70 transition-colors"
            aria-label="Dismiss toast"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </Transition>
  );
}

export function Toaster() {
  const { toasts } = useToast();

  return (
    <div
      className="fixed top-4 right-4 z-50 flex flex-col gap-2 w-full max-w-sm"
      aria-label="Notifications"
    >
      {toasts.map((toast) => (
        <Toast key={toast.id} {...toast} />
      ))}
    </div>
  );
}
