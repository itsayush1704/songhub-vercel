# SongHub - Vercel Deployment

🎵 A modern music streaming web application built with Flask and deployed on Vercel.

## Features

- **Music Search & Streaming**: Search and stream music using YouTube Music API
- **AI Recommendations**: Smart music suggestions based on listening history
- **Playlist Management**: Create and manage custom playlists
- **Recently Played**: Track your listening history
- **Responsive Design**: Works seamlessly on all devices
- **Serverless Architecture**: Optimized for Vercel's serverless platform

## Quick Deploy to Vercel

### Method 1: One-Click Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/songhub-vercel)

### Method 2: Vercel Dashboard
1. Fork this repository
2. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your forked repository
5. Click "Deploy"

### Method 3: Vercel CLI
```bash
npm i -g vercel
vercel login
vercel --prod
```

### Method 4: Automated Script
```bash
./deploy-vercel.sh
```

## Project Structure

```
songhub-vercel/
├── api/
│   ├── index.py          # Main Flask application
│   └── requirements.txt   # Python dependencies
├── templates/
│   └── index.html        # Frontend template
├── vercel.json           # Vercel configuration
├── .vercelignore         # Deployment exclusions
├── deploy-vercel.sh      # Automated deployment script
├── VERCEL_DEPLOYMENT.md  # Detailed deployment guide
└── README.md            # This file
```

## Technology Stack

- **Backend**: Flask (Python)
- **Music API**: YouTube Music API (ytmusicapi)
- **ML/AI**: scikit-learn for recommendations
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Vercel Serverless Functions
- **Storage**: In-memory (session-based)

## API Endpoints

- `GET /` - Main application interface
- `GET /search?q={query}` - Search for music
- `GET /stream/{video_id}` - Stream a specific song
- `GET /recommendations` - Get AI-powered recommendations
- `GET /recently_played` - Get recently played songs
- `POST /playlists` - Create a new playlist
- `POST /playlists/{name}/songs` - Add song to playlist
- `GET /health` - Health check endpoint

## Features in Detail

### 🎯 Smart Recommendations
- **Content-based filtering**: Based on your music preferences
- **Collaborative filtering**: Learn from similar users
- **Trending music**: Popular songs and artists
- **Mixed recommendations**: Combination of all methods

### 🎵 Music Streaming
- High-quality audio streaming
- Seamless playback experience
- YouTube Music integration
- Real-time search results

### 📱 Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Cross-browser compatibility
- Progressive Web App features

## Environment Variables

No environment variables required for basic functionality. The app works out of the box!

## Performance

- **Cold Start**: ~2-3 seconds
- **Response Time**: <500ms for most endpoints
- **Scalability**: Automatic scaling with Vercel
- **Global CDN**: Fast worldwide access

## Limitations

- **Session Storage**: Data is not persistent across sessions
- **Function Timeout**: 10 seconds on Hobby plan, 60 seconds on Pro
- **Memory**: 1024 MB on Hobby plan, 3008 MB on Pro
- **Concurrent Users**: Limited by Vercel plan

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development!

## Support

For deployment issues, check the [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) guide.

---

🚀 **Ready to deploy? Click the Vercel button above or follow the deployment guide!**