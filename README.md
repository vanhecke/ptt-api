# PTT API Web Service

A fast and simple FastAPI web service that wraps around the PTT (parsett) library for parsing torrent titles. This service provides a REST API to extract structured metadata from torrent file names.

## Features

- **Fast**: Built with FastAPI for high performance
- **Simple**: Easy-to-use REST API endpoints
- **Comprehensive**: Extracts detailed metadata from torrent titles
- **Flexible**: Supports single title parsing and batch processing
- **CORS Enabled**: Ready for web applications
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Docker Ready**: Includes Dockerfile for containerization

## Installation

### Local Installation

```bash
# Clone or download the project
cd ptt-api

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 12000 --reload
```

### Using the startup script

```bash
chmod +x start.sh
./start.sh
```

### Using Docker

```bash
# Build the image
docker build -t ptt-api .

# Run the container
docker run -p 12000:12000 ptt-api
```

## API Endpoints

### Core Endpoints

- **`GET /`** - Interactive API documentation (Swagger UI)
- **`GET /health`** - Health check endpoint
- **`GET /parse`** - Parse a single torrent title (structured response)
- **`GET /parse-simple`** - Parse a single torrent title (raw response)
- **`POST /parse-batch`** - Parse multiple torrent titles in batch
- **`GET /examples`** - Get example torrent titles and their parsed results

### Endpoint Details

#### `GET /parse`

Parse a torrent title and return structured data with success/error handling.

**Parameters:**
- `title` (required): The torrent title to parse
- `translate_languages` (optional): Whether to translate language codes to full names (default: false)

**Example:**
```bash
curl "http://localhost:12000/parse?title=The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "title": "The Simpsons",
    "seasons": [1],
    "episodes": [1],
    "languages": [],
    "resolution": "1080p",
    "quality": "BluRay",
    "codec": "hevc",
    "bit_depth": "10bit",
    "audio": ["AAC"],
    "channels": ["5.1"]
  },
  "error": null,
  "original_title": "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole"
}
```

#### `GET /parse-simple`

Parse a torrent title and return the raw parsed data directly.

**Parameters:**
- `title` (required): The torrent title to parse
- `translate_languages` (optional): Whether to translate language codes to full names (default: false)

**Example:**
```bash
curl "http://localhost:12000/parse-simple?title=The.Walking.Dead.S06E07.SUBFRENCH.HDTV.x264-AMB3R.mkv&translate_languages=true"
```

**Response:**
```json
{
  "container": "mkv",
  "quality": "HDTV",
  "codec": "avc",
  "group": "AMB3R",
  "seasons": [6],
  "episodes": [7],
  "languages": ["French"],
  "extension": "mkv",
  "title": "The Walking Dead"
}
```

#### `POST /parse-batch`

Parse multiple torrent titles in a single request.

**Request Body:**
```json
{
  "titles": [
    "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole",
    "Game.of.Thrones.S08E06.The.Iron.Throne.1080p.AMZN.WEB-DL.DDP5.1.H.264-GoT"
  ],
  "translate_languages": false
}
```

**Example:**
```bash
curl -X POST "http://localhost:12000/parse-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "titles": [
      "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole",
      "Game.of.Thrones.S08E06.The.Iron.Throne.1080p.AMZN.WEB-DL.DDP5.1.H.264-GoT"
    ],
    "translate_languages": false
  }'
```

## Supported Fields

The PTT library can extract the following fields from torrent titles:

- `title`: The main title/name
- `resolution`: Video resolution (e.g., "1080p", "720p", "2160p")
- `quality`: Source quality (e.g., "BluRay", "WEB-DL", "HDTV")
- `codec`: Video codec (e.g., "hevc", "avc", "xvid")
- `audio`: Audio formats (e.g., ["AAC"], ["Dolby Digital Plus"])
- `channels`: Audio channels (e.g., ["5.1"], ["7.1"])
- `bit_depth`: Video bit depth (e.g., "10bit", "8bit")
- `hdr`: HDR formats (e.g., ["HDR"], ["Dolby Vision"])
- `seasons`: Season numbers (e.g., [1], [1, 2, 3])
- `episodes`: Episode numbers (e.g., [1], [1, 2, 3, 4, 5])
- `year`: Release year
- `languages`: Languages (e.g., ["en"], ["French"] if translated)
- `group`: Release group
- `container`: File container (e.g., "mkv", "mp4")
- `extension`: File extension
- `network`: TV network (e.g., "Amazon", "Netflix")
- `site`: Source site
- `size`: File size
- And many more...

## Testing

Run the test suite to verify all endpoints:

```bash
python test_api.py
```

## Development

The service is built with:
- **FastAPI**: Modern, fast web framework for building APIs
- **PTT (parsett)**: Powerful torrent title parsing library
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation and serialization

## Configuration

The service runs on port 12000 by default and accepts connections from any host (0.0.0.0). CORS is enabled for all origins to support web applications.

## Production Deployment

For production deployment, consider:
- Using a reverse proxy (nginx)
- Setting up proper logging
- Configuring environment variables
- Using a process manager (systemd, supervisor)
- Setting up monitoring and health checks

## License

This project uses the PTT (parsett) library which is licensed under MIT License.