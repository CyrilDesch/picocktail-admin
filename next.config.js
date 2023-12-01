/** @type {import('next').NextConfig} */

const nextConfig = {
  swcMinify: true,
  images: {
    domains: [
      'images.unsplash.com',
      'i.ibb.co',
      'scontent.fotp8-1.fna.fbcdn.net',
    ],
    // Make ENV
    unoptimized: true,
  },
};

// module.exports = withTM(nextConfig);
module.exports = nextConfig;
