#!/bin/bash

# Vercel Deployment Script for SongHub
# This script helps deploy your SongHub app to Vercel

echo "🚀 SongHub Vercel Deployment Script"
echo "===================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
else
    echo "✅ Vercel CLI found"
fi

# Check if user is logged in to Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "🔑 Please log in to Vercel:"
    vercel login
else
    echo "✅ Already logged in to Vercel"
fi

# Ensure we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Make sure you're in the songhub1 directory."
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "📋 Project structure:"
ls -la api/ templates/ vercel.json 2>/dev/null || echo "⚠️  Some files missing"

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your SongHub app is now live on Vercel!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Test your deployed app"
    echo "   2. Set up custom domain (optional)"
    echo "   3. Configure environment variables if needed"
    echo "   4. Monitor performance in Vercel dashboard"
else
    echo "❌ Deployment failed. Check the error messages above."
    echo "💡 Common solutions:"
    echo "   - Ensure all files are committed to Git"
    echo "   - Check api/requirements.txt for correct dependencies"
    echo "   - Verify vercel.json configuration"
    exit 1
fi

echo ""
echo "🎉 Happy streaming with SongHub!"