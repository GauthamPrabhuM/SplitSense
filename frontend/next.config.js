const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Static export for simple serving from FastAPI
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Skip type checking and linting during build (faster builds)
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Webpack config to resolve @ alias - MUST work for Docker
  webpack: (config, { isServer }) => {
    // Get absolute path - critical for Docker builds
    const srcPath = path.resolve(__dirname, 'src');
    
    // Initialize resolve and alias
    config.resolve = config.resolve || {};
    config.resolve.alias = config.resolve.alias || {};
    
    // Set @ alias - makes @/lib/api resolve to src/lib/api
    config.resolve.alias['@'] = srcPath;
    
    return config;
  },
};

module.exports = nextConfig;
