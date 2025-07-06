"""URL shortening utilities for Confluence pages."""

import re
import struct
import base64
import urllib.parse


class URLShortener:
    """Handles URL shortening for Confluence pages."""
    
    @staticmethod
    def extract_base_url(full_url: str) -> str:
        """Extract base URL from a full URL."""
        p = urllib.parse.urlparse(full_url)
        base = f"{p.scheme}://{p.hostname}"
        if p.port:
            base += f":{p.port}"
        return base
    
    @staticmethod
    def extract_page_id(url: str) -> int:
        """Extract page ID from Confluence URL."""
        u = urllib.parse.unquote(url)
        
        # Try different Confluence URL patterns
        patterns = [
            r'/pages/(\d+)(?:/|$)',  # /pages/123456 or /pages/123456/title
            r'[?&]pageId=(\d+)',     # ?pageId=123456 or &pageId=123456
            r'/viewpage\.action\?pageId=(\d+)',  # viewpage.action?pageId=123456
            r'/display/[^/]+/.*\?pageId=(\d+)',  # display/SPACE/title?pageId=123456
        ]
        
        for pattern in patterns:
            m = re.search(pattern, u)
            if m:
                return int(m.group(1))
        
        raise ValueError(f"No pageId found in Confluence URL: {url}. Supported formats: /pages/ID, ?pageId=ID, viewpage.action?pageId=ID")
    
    @staticmethod
    def create_tiny_token(page_id: int) -> str:
        """Create a tiny token from page ID."""
        packed = struct.pack('<L', page_id)
        return base64.b64encode(packed, altchars=b'_-').rstrip(b'=').decode('ascii')
    
    @classmethod
    def create_short_url(cls, base_url: str, full_url: str) -> str:
        """Create a short URL from a full Confluence URL."""
        page_id = cls.extract_page_id(full_url)
        token = cls.create_tiny_token(page_id)
        return base_url.rstrip('/') + '/x/' + token
    
    @classmethod
    def shorten_url(cls, full_url: str, custom_base_url: str = None) -> str:
        """
        Shorten a Confluence URL.
        
        Args:
            full_url (str): The full Confluence URL
            custom_base_url (str): Optional custom base URL
            
        Returns:
            str: The shortened URL
        """
        base_url = custom_base_url or cls.extract_base_url(full_url)
        return cls.create_short_url(base_url, full_url)