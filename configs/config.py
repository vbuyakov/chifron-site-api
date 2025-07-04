import json
import os
from pathlib import Path
from typing import Dict, Any, List, Set

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Default configuration
DEFAULT_CONFIG = {
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

def load_config() -> Dict[str, Any]:
    """Load configuration from JSON files or use defaults."""
    config = DEFAULT_CONFIG.copy()
    config_path = os.getenv('CONFIG_PATH') or str(BASE_DIR / 'config.json')
    security_path = os.path.join(os.path.dirname(config_path), 'security.json')
    
    # Load main config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            file_config = json.load(f)
            # Deep merge with defaults
            for key, value in file_config.items():
                if key in config and isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if os.path.exists(config_path):
            print(f"Warning: Could not load config from {config_path}: {e}")
    
    # Load security config (API keys)
    try:
        with open(security_path, 'r', encoding='utf-8') as f:
            security_config = json.load(f)
            if 'api' in security_config and 'access_keys' in security_config['api']:
                config['api']['access_keys'] = security_config['api']['access_keys']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if os.path.exists(security_path):
            print(f"Warning: Could not load security config from {security_path}: {e}")
    
    # Ensure required API keys are set
    if not config["api"].get("access_keys"):
        print("Warning: No API access keys configured. The API will be unsecured!")
    
    return config

# Load configuration
config = load_config()

# Helper functions
def get_api_keys() -> List[str]:
    """Get list of valid API keys."""
    return config["api"].get("access_keys", [])

def get_api_keys_set() -> Set[str]:
    """Get set of valid API keys for O(1) lookups."""
    return set(get_api_keys())

def get_static_config() -> Dict[str, str]:
    """Get static files configuration."""
    return config["static"]

def get_api_base_path() -> str:
    """Get the base API path."""
    return config["api"].get("base_path", "/api").rstrip('/')

# Static files configuration
static_config = get_static_config()
STATIC_FOLDER = static_config['folder']
AUDIO_SUBFOLDER = static_config['audio_subfolder']
STATIC_URL_PATH = static_config['url_path']

# API configuration
API_BASE_PATH = get_api_base_path()
API_ACCESS_KEYS = get_api_keys_set()

# Define static paths - use /app/static in container, relative path for local development
IS_DOCKER = os.environ.get('DOCKER_CONTAINER', 'false').lower() == 'true'
STATIC_DIR = f"/app/{STATIC_FOLDER}" if IS_DOCKER else str(Path(__file__).parent.parent / STATIC_FOLDER)
AUDIO_DIR = str(Path(STATIC_DIR) / AUDIO_SUBFOLDER)

# Ensure directories exist
try:
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
except OSError as e:
    print(f"Warning: Could not create directories: {e}")
    print(f"STATIC_DIR: {STATIC_DIR}")
    print(f"AUDIO_DIR: {AUDIO_DIR}")
