import React from 'react';
import { Toaster } from 'react-hot-toast';

/**
 * Global toast container placed once at the root of the app.
 */
export const ToastContainer: React.FC = () => (
  <Toaster
    toastOptions={{
      style: {
        borderRadius: '8px',
        background: '#333',
        color: '#fff',
      },
    }}
  />
);
