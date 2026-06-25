import React, { useEffect } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { useNavigate } from 'react-router-dom';

/**
 * Provider that checks token validity on mount and redirects accordingly.
 */
export const AuthProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const { token, setUser, logout } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        navigate('/login');
        return;
      }
      try {
        // Simple token decode to extract user info (no verification on client)
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUser({ id: payload.sub, email: payload.email, name: payload.name } as any);
      } catch {
        logout();
        navigate('/login');
      }
    };
    verifyToken();
  }, [token, setUser, logout, navigate]);

  return <>{children}</>;
};
