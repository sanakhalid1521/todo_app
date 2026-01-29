#!/bin/sh
# Remove any existing lockfiles that might cause permission issues
rm -f .next/cache/lock*

# Start the Next.js development server
npm run dev