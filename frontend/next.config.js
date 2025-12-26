/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Use 'standalone' for Railway, remove for Vercel/Netlify
  output: process.env.NEXT_OUTPUT || undefined,
  async rewrites() {
    // Use environment variable for API URL, fallback to localhost for development
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Only add rewrites if API URL is set (for Vercel/Netlify)
    if (apiUrl && apiUrl !== 'http://localhost:8000') {
      return [
        {
          source: '/api/:path*',
          destination: `${apiUrl}/api/:path*`,
        },
        {
          source: '/auth/:path*',
          destination: `${apiUrl}/auth/:path*`,
        },
      ];
    }
    
    // For local development, use localhost
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
      {
        source: '/auth/:path*',
        destination: 'http://localhost:8000/auth/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
