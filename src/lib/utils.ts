import { format } from 'date-fns';

/**
 * Formats a Date object to a readable string.
 */
export const formatDate = (date: Date | string, pattern = 'PPP p') => {
  return format(new Date(date), pattern);
};

/**
 * Simple debounce implementation.
 */
export const debounce = <F extends (...args: any[]) => any>(func: F, wait: number) => {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<F>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * Truncate a string to a maximum length, adding ellipsis if needed.
 */
export const truncate = (str: string, max = 100) => {
  return str.length > max ? str.slice(0, max) + '…' : str;
};
