#!/usr/bin/env python3
from functools import wraps
from flask import Flask, jsonify, send_from_directory, request
from services.number_service import NumberService
from configs.config import (
    STATIC_FOLDER, STATIC_URL_PATH, AUDIO_DIR,
    API_BASE_PATH, get_api_keys_set, STATIC_DIR
)
import os

# Get API keys
API_ACCESS_KEYS = get_api_keys_set()

# Initialize Flask app with configuration from config.py
app = Flask(__name__)

# Configure static files
app.static_url_path = STATIC_URL_PATH
app.static_folder = STATIC_DIR

# Initialize the number service
number_service = NumberService()

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip auth if no API keys are configured
        if not API_ACCESS_KEYS:
            return f(*args, **kwargs)
            
        # Check for API key in Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
            
        api_key = auth_header.split(' ')[1]
        if api_key not in API_ACCESS_KEYS:
            return jsonify({"error": "Invalid API key"}), 403
            
        return f(*args, **kwargs)
    return decorated_function

@app.route(f'{API_BASE_PATH}/audio/number/<int:number>', methods=['GET'])
@require_api_key
def get_number_audio(number):
    """Get audio for a specific number"""
    if number < 0 or number > 1000000:
        return jsonify({"error": "Number must be between 0 and 1000000"}), 400
    
    number_info = number_service.get_number_info(number)
    
    if number_info:
        return jsonify(number_info)
    else:
        return jsonify({"error": "Failed to process number"}), 500

@app.route(f'{API_BASE_PATH}/health', methods=['GET'])
def health_check():
    """Health check endpoint (public)"""
    return jsonify({"status": "healthy"})

@app.route(f'{API_BASE_PATH}/audio/<path:filename>')
@require_api_key
def serve_audio(filename):
    """Serve audio files from the static/audio directory"""
    # Use NumberService to get the correct audio directory
    audio_dir = number_service.audio_dir
    return send_from_directory(audio_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)