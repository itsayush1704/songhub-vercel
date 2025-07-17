# Vercel Deployment Guide for SongHub

This guide will help you deploy your SongHub music streaming application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Vercel CLI** (optional): Install with `npm i -g vercel`

## Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect GitHub Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your `songhub1` repository from GitHub

2. **Configure Project Settings**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r api/requirements.txt`

3. **Environment Variables** (if needed):
   - Add any environment variables in the Vercel dashboard
   - Go to Project Settings → Environment Variables

4. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy your app

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from Project Root**:
   ```bash
   cd /path/to/songhub1
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N` (for first deployment)
   - Project name: `songhub1` or your preferred name
   - Directory: `./`

## Project Structure for Vercel

```
songhub1/
├── api/
│   ├── index.py          # Main Flask app for Vercel
│   └── requirements.txt   # Python dependencies
├── templates/
│   └── index.html        # Frontend template
├── vercel.json           # Vercel configuration
├── .vercelignore         # Files to ignore during deployment
└── README.md
```

## Key Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "./api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### api/requirements.txt
- Contains all Python dependencies with specific versions
- Optimized for Vercel's Python runtime

## Environment Variables

If your app uses environment variables, add them in Vercel:

1. Go to your project dashboard
2. Navigate to Settings → Environment Variables
3. Add variables like:
   - `SECRET_KEY`: Your Flask secret key
   - Any API keys or configuration values

## Deployment Features

✅ **Automatic Deployments**: Every push to main branch triggers deployment
✅ **Preview Deployments**: Pull requests get preview URLs
✅ **Custom Domains**: Add your own domain
✅ **HTTPS**: Automatic SSL certificates
✅ **Global CDN**: Fast worldwide access
✅ **Serverless Functions**: Automatic scaling

## Post-Deployment

1. **Test Your App**:
   - Visit the provided Vercel URL
   - Test all endpoints: search, streaming, playlists
   - Check browser console for any errors

2. **Monitor Performance**:
   - Use Vercel Analytics
   - Monitor function execution times
   - Check error logs in Vercel dashboard

3. **Custom Domain** (optional):
   - Go to Project Settings → Domains
   - Add your custom domain
   - Configure DNS settings

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check the build logs in Vercel dashboard
   - Ensure all dependencies are in `api/requirements.txt`
   - Verify Python version compatibility

2. **Function Timeouts**:
   - Vercel has a 10-second timeout for Hobby plan
   - Optimize slow operations
   - Consider caching strategies

3. **Import Errors**:
   - Ensure all imports are available in the serverless environment
   - Some packages might not work in serverless functions

4. **File System Issues**:
   - Vercel functions are read-only
   - Use external storage for persistent data
   - Consider using Vercel KV or external databases

## Limitations

- **Function Timeout**: 10 seconds (Hobby), 60 seconds (Pro)
- **Memory Limit**: 1024 MB (Hobby), 3008 MB (Pro)
- **File System**: Read-only, no persistent storage
- **Cold Starts**: Functions may have startup delay

## Next Steps

1. **Database Integration**: Consider adding a database for persistent storage
2. **Caching**: Implement Redis or similar for better performance
3. **Monitoring**: Set up error tracking and performance monitoring
4. **Custom Domain**: Add your own domain for branding

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Flask on Vercel**: [vercel.com/guides/using-flask-with-vercel](https://vercel.com/guides/using-flask-with-vercel)

---

🚀 **Your SongHub app is now ready for Vercel deployment!**

Simply push your changes to GitHub and deploy via the Vercel dashboard or CLI.