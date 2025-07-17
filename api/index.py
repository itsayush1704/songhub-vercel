from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
from ytmusicapi import YTMusic
import os
from dotenv import load_dotenv
import yt_dlp
import json
from datetime import datetime
import pickle
# Removed numpy and scikit-learn imports to reduce function size
from collections import defaultdict, Counter
import hashlib
import time

load_dotenv()

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
CORS(app)  # Enable CORS for all routes

# Initialize YouTube Music API
ytmusic = YTMusic()

# In-memory storage for playlists (in a real app, use a database)
playlists = {}
# In-memory storage for recently played songs with timestamps
recently_played = []
# User profiles for personalized recommendations
user_profiles = {}
# Song features for ML-based recommendations
song_features = {}
# User listening history for collaborative filtering
user_listening_history = defaultdict(list)
# Genre preferences
user_genre_preferences = defaultdict(Counter)
# Artist preferences
user_artist_preferences = defaultdict(Counter)

# Helper functions for recommendation system
def get_user_id():
    """Generate or get user ID from session"""
    if 'user_id' not in session:
        session['user_id'] = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    return session['user_id']

def extract_song_features(song):
    """Extract features from a song for ML recommendations"""
    # Safely extract artist name
    artist_name = ''
    if song.get('artists') and len(song['artists']) > 0:
        first_artist = song['artists'][0]
        if isinstance(first_artist, dict):
            artist_name = first_artist.get('name', '')
    
    features = {
        'title': song.get('title', ''),
        'artist': artist_name,
        'duration': song.get('duration_seconds', 0),
        'year': song.get('year', 0)
    }
    return features

def update_user_preferences(user_id, song):
    """Update user preferences based on played song"""
    # Safely extract artist name
    artist_name = ''
    if song.get('artists') and len(song['artists']) > 0:
        first_artist = song['artists'][0]
        if isinstance(first_artist, dict):
            artist_name = first_artist.get('name', '')
            user_artist_preferences[user_id][artist_name] += 1
    
    # Add to listening history
    user_listening_history[user_id].append({
        'videoId': song.get('videoId'),
        'title': song.get('title'),
        'artist': artist_name,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 100 songs in history
    user_listening_history[user_id] = user_listening_history[user_id][-100:]

def get_content_based_recommendations(user_id, limit=10):
    """Get recommendations based on content similarity"""
    if user_id not in user_listening_history or not user_listening_history[user_id]:
        return []
    
    # Get user's recent songs
    recent_songs = user_listening_history[user_id][-10:]
    
    # Create feature vectors for content-based filtering
    user_artists = [song['artist'] for song in recent_songs if song.get('artist')]
    
    try:
        # Get similar songs from YouTube Music
        recommendations = []
        for artist in set(user_artists[-3:]):  # Use last 3 unique artists
            try:
                search_results = ytmusic.search(f"artist:{artist}", filter='songs', limit=5)
                for song in search_results:
                    if song.get('videoId') not in [s['videoId'] for s in recent_songs]:
                        recommendations.append(song)
            except:
                continue
        
        return recommendations[:limit]
    except Exception as e:
        print(f"Error in content-based recommendations: {e}")
        return []

def get_collaborative_recommendations(user_id, limit=10):
    """Get recommendations based on collaborative filtering"""
    if user_id not in user_listening_history:
        return []
    
    user_songs = set(song['videoId'] for song in user_listening_history[user_id])
    
    # Find similar users
    similar_users = []
    for other_user_id, other_history in user_listening_history.items():
        if other_user_id != user_id and other_history:
            other_songs = set(song['videoId'] for song in other_history)
            # Calculate Jaccard similarity
            intersection = len(user_songs.intersection(other_songs))
            union = len(user_songs.union(other_songs))
            if union > 0:
                similarity = intersection / union
                if similarity > 0.1:  # Threshold for similarity
                    similar_users.append((other_user_id, similarity))
    
    # Get recommendations from similar users
    recommendations = []
    similar_users.sort(key=lambda x: x[1], reverse=True)
    
    for similar_user_id, _ in similar_users[:5]:  # Top 5 similar users
        for song in user_listening_history[similar_user_id][-10:]:
            if song['videoId'] not in user_songs:
                recommendations.append(song)
    
    return recommendations[:limit]

def get_trending_recommendations(limit=10):
    """Get trending songs as recommendations using alternative methods"""
    try:
        # Try to get trending songs from home page instead of charts
        home = ytmusic.get_home()
        trending_songs = []
        
        # Extract songs from home sections
        for section in home:
            if section.get('contents'):
                for item in section['contents']:
                    if item.get('videoId'):
                        trending_songs.append(item)
                        if len(trending_songs) >= limit:
                            break
            if len(trending_songs) >= limit:
                break
        
        return trending_songs[:limit]
    except Exception as e:
        print(f"Error getting trending recommendations: {e}")
        # Fallback to popular searches
        try:
            popular_queries = ['pop music', 'rock songs', 'hip hop', 'electronic music', 'indie music']
            trending_songs = []
            for query in popular_queries:
                try:
                    results = ytmusic.search(query, filter='songs', limit=2)
                    trending_songs.extend(results)
                    if len(trending_songs) >= limit:
                        break
                except:
                    continue
            return trending_songs[:limit]
        except:
            return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Search for songs
        results = ytmusic.search(query, filter='songs', limit=20)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stream/<video_id>')
def stream_song(video_id):
    try:
        # Get song info
        song_info = ytmusic.get_song(video_id)
        
        # Update user preferences
        user_id = get_user_id()
        update_user_preferences(user_id, song_info['videoDetails'])
        
        # Add to recently played
        recently_played.append({
            'song': song_info['videoDetails'],
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 50 recently played songs
        if len(recently_played) > 50:
            recently_played.pop(0)
        
        return jsonify(song_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations')
def get_recommendations():
    user_id = get_user_id()
    rec_type = request.args.get('type', 'mixed')
    limit = int(request.args.get('limit', 10))
    
    try:
        if rec_type == 'content':
            recommendations = get_content_based_recommendations(user_id, limit)
        elif rec_type == 'collaborative':
            recommendations = get_collaborative_recommendations(user_id, limit)
        elif rec_type == 'trending':
            recommendations = get_trending_recommendations(limit)
        else:  # mixed
            content_recs = get_content_based_recommendations(user_id, limit//3)
            collab_recs = get_collaborative_recommendations(user_id, limit//3)
            trending_recs = get_trending_recommendations(limit//3)
            recommendations = content_recs + collab_recs + trending_recs
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recently_played')
def get_recently_played():
    return jsonify(recently_played[-10:])  # Return last 10 songs

@app.route('/playlists', methods=['GET', 'POST'])
def handle_playlists():
    user_id = get_user_id()
    
    if request.method == 'GET':
        user_playlists = playlists.get(user_id, {})
        return jsonify(user_playlists)
    
    elif request.method == 'POST':
        data = request.get_json()
        playlist_name = data.get('name')
        
        if not playlist_name:
            return jsonify({'error': 'Playlist name is required'}), 400
        
        if user_id not in playlists:
            playlists[user_id] = {}
        
        playlists[user_id][playlist_name] = {
            'songs': [],
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({'message': 'Playlist created successfully'})

@app.route('/playlists/<playlist_name>/songs', methods=['POST', 'DELETE'])
def handle_playlist_songs(playlist_name):
    user_id = get_user_id()
    
    if user_id not in playlists or playlist_name not in playlists[user_id]:
        return jsonify({'error': 'Playlist not found'}), 404
    
    if request.method == 'POST':
        data = request.get_json()
        song = data.get('song')
        
        if not song:
            return jsonify({'error': 'Song data is required'}), 400
        
        playlists[user_id][playlist_name]['songs'].append(song)
        return jsonify({'message': 'Song added to playlist'})
    
    elif request.method == 'DELETE':
        data = request.get_json()
        video_id = data.get('videoId')
        
        if not video_id:
            return jsonify({'error': 'Video ID is required'}), 400
        
        songs = playlists[user_id][playlist_name]['songs']
        playlists[user_id][playlist_name]['songs'] = [
            song for song in songs if song.get('videoId') != video_id
        ]
        
        return jsonify({'message': 'Song removed from playlist'})

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# For Vercel deployment, the Flask app is automatically detected
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8009)))