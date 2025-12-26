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
    
    // Initialize resolve configuration
    if (!config.resolve) {
      config.resolve = {};
    }
    
    // Set up alias
    if (!config.resolve.alias) {
      config.resolve.alias = {};
    }
    
    // Set @ alias - makes @/lib/api resolve to src/lib/api
    config.resolve.alias['@'] = srcPath;
    
    // Ensure modules array includes node_modules for proper resolution
    if (!config.resolve.modules) {
      config.resolve.modules = ['node_modules'];
    }
    
    // Also add src to modules for direct imports
    if (Array.isArray(config.resolve.modules)) {
      config.resolve.modules.push(srcPath);
    }
    
    // Ensure extensions are properly set
    if (!config.resolve.extensions) {
      config.resolve.extensions = ['.tsx', '.ts', '.jsx', '.js', '.json'];
    }
    
    return config;
  },
};

module.exports = nextConfig;
