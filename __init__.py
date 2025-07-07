"""
Utility Tools Package

A comprehensive Python utility toolkit that provides QR code generation 
and Confluence URL shortening services through both a modern web interface 
and command-line tools.
"""

__version__ = "2.0.0"
__author__ = "Utility Tools Team"
__description__ = "QR Code Generator and URL Shortener Toolkit"

# Import main components for easy access
from src.utils.qr_generator import QRCodeGenerator
from src.utils.url_shortener import URLShortener
from src.utils.svg_color_validator import SVGColorValidator

__all__ = [
    'QRCodeGenerator',
    'URLShortener', 
    'SVGColorValidator'
]