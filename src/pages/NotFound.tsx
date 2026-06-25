import React from 'react';
import { Link } from 'react-router-dom';
import { FaExclamationTriangle } from 'react-icons/fa';

const NotFound: React.FC = () => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <FaExclamationTriangle className="text-6xl text-primary mb-4" aria-hidden="true" />
    <h1 className="text-3xl font-bold mb-2">Page Not Found</h1>
    <p className="mb-6 text-gray-600">The page you are looking for does not exist.</p>
    <Link to="/" className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90">
      Go Home
    </Link>
  </div>
);

export default NotFound;
