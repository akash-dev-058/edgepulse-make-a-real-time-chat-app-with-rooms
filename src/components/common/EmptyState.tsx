import React from 'react';

interface EmptyStateProps {
  title: string;
  description: string;
  imageUrl: string;
  imageAlt: string;
  ctaLabel: string;
  onCtaClick: () => void;
}

/**
 * Friendly empty state with illustration and call‑to‑action.
 */
const EmptyState: React.FC<EmptyStateProps> = ({ title, description, imageUrl, imageAlt, ctaLabel, onCtaClick }) => (
  <div className="flex flex-col items-center justify-center py-12 text-center">
    <img src={imageUrl} alt={imageAlt} className="w-64 h-64 object-cover mb-6" />
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="mb-4 text-gray-600">{description}</p>
    <button
      onClick={onCtaClick}
      className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90"
    >
      {ctaLabel}
    </button>
  </div>
);

export default EmptyState;
