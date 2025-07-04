# Chifron Voice API

<a href='https://ko-fi.com/X8X61HDXIO' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi6.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

A production-ready REST API for converting numbers to French text and generating audio files using gTTS (Google Text-to-Speech). The API includes rate limiting, API key authentication, and efficient audio file caching.



## Features

- Convert numbers to French text
- Generate audio files for numbers using gTTS
- Audio file caching for improved performance
- API key authentication
- Rate limiting
- Health check endpoint
- Docker support

## Related Projects

- **[Chifron Flutter App](https://github.com/vbuyakov/chifron-flutter-app)** - Mobile application built with Flutter for learning French numbers by listening to audio and typing the correct numbers.

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Using Docker Compose (Recommended)

```bash
# Start the API in development mode
docker-compose -f docker-compose.dev.yml up --build

# Or for production:
docker-compose -f docker-compose.prod.yml up --build

# The API will be available at http://localhost:5000
```

### Local Development

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   python app.py
   ```

## API Documentation

### Authentication
All endpoints except `/api/health` require an API key in the `Authorization` header using Bearer token format.

### Security Configuration
The API requires a `configs/security.json` file with the following structure:

```json
{
  "api_keys": ["your-secure-api-key-here"]
}
```

**Important Security Notes:**
- The `security.json` file is listed in `.gitignore` and should never be committed to version control
- Use strong, unique API keys in production
- Multiple API keys can be added to the `api_keys` array
- The API key must be included in the `Authorization: Bearer <api-key>` header for all authenticated requests

### Endpoints

#### Health Check
```
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "Chifron Voice API",
  "version": "1.0.0"
}
```

#### Convert Number to Speech
```
GET /api/speak?number=<number>
```
**Parameters:**
- `number` (required): The number to convert to speech (0-999,999,999)

**Response:**
```json
{
  "text": "cent vingt-trois",
  "audio_url": "/static/audio/123.mp3"
}
```

## Configuration

Edit `configs/config.json` to configure the API:

```json
{
  "static": {
    "folder": "static",
    "audio_subfolder": "audio",
    "url_path": "/static"
  },
  "api": {
    "base_path": "/api",
    "access_keys": []
  }
}
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Environment Variables

- `PORT`: Port to run the API on (default: 5000)
- `CONFIG_PATH`: Path to config file (default: `/app/configs/config.json` in Docker)
- `DOCKER_CONTAINER`: Set to `true` when running in Docker

## License

MIT
}
## Testing with cURL

### Health Check
```bash
curl -X GET "http://localhost:5000/api/health"
```

### Get Number Audio
```bash
# Get audio for number 123
curl -X GET "http://localhost:5000/api/audio/number/123" \
  -H "Authorization: Bearer your-api-key"
```

### Get Audio File
After getting the audio URL from the previous request:
```bash
# Example - replace with actual URL from the response
curl -X GET "http://localhost:5000/static/audio/abc123.mp3" \
  -H "Authorization: Bearer your-api-key" \
  --output number_audio.mp3
```

## Features

- ✅ **Number to French Text**: Convert any number to French words up to 1000000
- ✅ **Audio Generation**: Generate MP3 files using gTTS
- ✅ **Audio Caching**: Efficient file-based caching for performance
- ✅ **API Key Authentication**: Secure access control
- ✅ **Health Monitoring**: Built-in health check endpoint
- ✅ **Docker Ready**: Easy deployment with Docker Compose

## Audio Files

- Audio files are generated on-demand using gTTS
- Files are cached in `/app/static/audio/` directory in the container
- Unique filenames based on number hashes prevent conflicts
- Cache directory persists across container restarts

## Production Considerations

1. **Configuration**:
   - Set up API keys in `configs/security.json`
   - Configure Nginx as a reverse proxy (see DEPLOYMENT.md)

2. **Security**:
   - Always use HTTPS in production
   - Rotate API keys regularly
   - Monitor API usage and logs

3. **Performance**:
   - The application is stateless and can be horizontally scaled
   - Consider adding a CDN for audio file delivery
   - Monitor disk usage for the audio cache

4. **Monitoring**:
   - Check the health endpoint: `GET /api/health`
   - Monitor Docker container logs
   - Set up alerts for failed health checks

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input or missing parameters)
- `401`: Unauthorized (missing or invalid API key)
- `404`: Not Found (invalid endpoint or resource)
- `500`: Internal server error

Error responses include a descriptive message:
```json
{
  "error": "Invalid number format"
}
``` 