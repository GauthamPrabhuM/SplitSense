const path = require('path');
const fs = require('fs');

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
  webpack: (config, { isServer, dir }) => {
    // Use the 'dir' parameter provided by Next.js (guaranteed to be correct)
    // This is the absolute path to the Next.js project root
    const projectRoot = dir || __dirname;
    const srcPath = path.resolve(projectRoot, 'src');
    
    // Ensure resolve and alias are properly initialized
    config.resolve = config.resolve || {};
    config.resolve.alias = config.resolve.alias || {};
    
    // CRITICAL: Set @ alias to src directory
    // This makes @/lib/api resolve to src/lib/api
    config.resolve.alias['@'] = srcPath;
    
    // Ensure extensions include TypeScript files
    config.resolve.extensions = config.resolve.extensions || [];
    if (!config.resolve.extensions.includes('.tsx')) {
      config.resolve.extensions.push('.tsx', '.ts', '.jsx', '.js');
    }
    
    return config;
  },
};

module.exports = nextConfig;
