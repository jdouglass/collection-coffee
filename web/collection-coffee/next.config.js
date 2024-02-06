/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack(config) {
    // Grab the existing rule that handles SVG imports
    const fileLoaderRule = config.module.rules.find((rule) =>
      rule.test?.test?.(".svg")
    );

    config.module.rules.push(
      // Reapply the existing rule, but only for svg imports ending in ?url
      {
        ...fileLoaderRule,
        test: /\.svg$/i,
        resourceQuery: /url/, // *.svg?url
      },
      // Convert all other *.svg imports to React components
      {
        test: /\.svg$/i,
        issuer: fileLoaderRule.issuer,
        resourceQuery: { not: [...fileLoaderRule.resourceQuery.not, /url/] }, // exclude if *.svg?url
        use: ["@svgr/webpack"],
      }
    );

    // Modify the file loader rule to ignore *.svg, since we have it handled now.
    fileLoaderRule.exclude = /\.svg$/i;

    return config;
  },
  env: {
    DISCORD_INVITE_URL: process.env.DISCORD_INVITE_URL,
    API_BASE_URL: process.env.API_BASE_URL,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    BUCKET_PROTOCOL: process.env.BUCKET_PROTOCOL,
    BUCKET_HOSTNAME: process.env.BUCKET_HOSTNAME,
    BUCKET_PORT: process.env.BUCKET_PORT,
  },
  images: {
    remotePatterns: [
      {
        protocol: process.env.BUCKET_PROTOCOL,
        hostname: process.env.BUCKET_HOSTNAME,
        port: process.env.BUCKET_PORT,
        pathname: "/storage/v1/object/public/product-images/**",
      },
      {
        protocol: "http",
        hostname: "127.0.0.1",
      },
    ],
  },
};

module.exports = nextConfig;
