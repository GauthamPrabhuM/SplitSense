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
  webpack: (config) => {
    // Get absolute path to src directory
    // Use __dirname (location of next.config.js) as base
    const srcPath = path.resolve(__dirname, 'src');
    
    // Initialize resolve and alias objects
    config.resolve = config.resolve || {};
    config.resolve.alias = {
      ...config.resolve.alias, // Preserve existing aliases
      '@': srcPath, // Add our @ alias pointing to src directory
    };
    
    return config;
  },
};

module.exports = nextConfig;
