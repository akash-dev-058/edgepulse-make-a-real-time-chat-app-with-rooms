import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/useAuthStore';
import LoadingSkeleton from '@/components/common/LoadingSkeleton';
import ErrorBoundary from '@/components/common/ErrorBoundary';

// Lazy‑load route components for code‑splitting
const Dashboard = lazy(() => import('@/pages/Dashboard'));
const Login = lazy(() => import('@/pages/Login'));
const Register = lazy(() => import('@/pages/Register'));
const NotFound = lazy(() => import('@/pages/NotFound'));

/**
 * Root application component handling routing and authentication guard.
 */
const App: React.FC = () => {
  const { user, isLoading } = useAuthStore();

  if (isLoading) {
    return <LoadingSkeleton className="h-screen" />;
  }

  return (
    <ErrorBoundary>
      <Suspense fallback={<LoadingSkeleton className="h-screen" />}>
        <Routes>
          <Route
            path="/"
            element={user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
          />
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" replace />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" replace />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
};

export default App;
