"""Configuration settings for the Utility Tools application."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask configuration
class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    # QR Code settings
    QR_DEFAULT_VERSION = 1
    QR_DEFAULT_ERROR_CORRECTION = 'L'  # L, M, Q, H
    QR_DEFAULT_BOX_SIZE = 10
    QR_DEFAULT_BORDER = 4
    QR_MAX_LOGO_SIZE = 50
    
    # URL shortener settings
    URL_SHORTENER_TOKEN_LENGTH = 8
    URL_SHORTENER_ALLOWED_DOMAINS = []  # Empty means all domains allowed
    
    @staticmethod
    def init_app(app):
        """Initialize the Flask app with configuration."""
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-must-be-set'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'test-secret-key'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}