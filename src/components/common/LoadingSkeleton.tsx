import React from 'react';
import clsx from 'clsx';

interface LoadingSkeletonProps {
  className?: string;
}

/**
 * Simple gray block skeleton used while loading content.
 */
const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ className }) => (
  <div className={clsx('animate-pulse bg-gray-300 rounded', className)} role="status" aria-label="Loading" />
);

export default LoadingSkeleton;
