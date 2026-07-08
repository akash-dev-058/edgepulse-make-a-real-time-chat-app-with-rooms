const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['images.pexels.com'],
  },
  experimental: {
    esmExternals: 'loose',
    serverActions: true,
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(process.cwd(), 'src'),
    };
    return config;
  },
  async redirects() {
    return [
      {
        source: '/',
        destination: '/rooms',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;
