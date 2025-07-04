"""
Chifron Voice API Configuration Package

This package contains configuration settings for the Chifron Voice API.
"""
from .config import *  # noqa: F403

__all__ = [
    'STATIC_FOLDER', 'STATIC_URL_PATH', 'AUDIO_DIR',
    'API_BASE_PATH', 'get_api_keys_set', 'get_static_config'
]
