/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/:path*',
      },
      {
        source: '/health',
        destination: 'http://127.0.0.1:8000/health',
      },
      {
        source: '/ready',
        destination: 'http://127.0.0.1:8000/ready',
      },
    ];
  },
};

export default nextConfig;
