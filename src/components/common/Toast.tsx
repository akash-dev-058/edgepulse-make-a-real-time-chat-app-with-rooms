import { toast as hotToast } from 'react-hot-toast';

/**
 * Wrapper around react-hot-toast to provide typed helpers.
 */
export const toast = {
  success: (msg: string) => hotToast.success(msg, { duration: 3000, position: 'top-right' }),
  error: (msg: string) => hotToast.error(msg, { duration: 5000, position: 'top-right' }),
  warning: (msg: string) => hotToast('⚠️ ' + msg, { duration: 4000, position: 'top-right' }),
  info: (msg: string) => hotToast(msg, { duration: 3000, position: 'top-right' }),
};
