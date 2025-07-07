#!/usr/bin/env python3
"""Test gradient and styling options to verify they work correctly."""

import requests
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import QRCodeGenerator

def test_direct_generation():
    """Test QR generation directly with the utility class."""
    print("🔬 Testing QR generation directly...")
    
    qr_gen = QRCodeGenerator()
    test_cases = [
        ("PNG Square Solid", "png", "square", "solid"),
        ("PNG Rounded Radial", "png", "rounded", "radial"),
        ("PNG Circle Square", "png", "circle", "square"),
        ("SVG Basic", "svg", "square", "solid"),
    ]
    
    for name, fmt, style, color in test_cases:
        print(f"\n📋 Testing: {name}")
        try:
            buf, mimetype, filename = qr_gen.generate_qr_code(
                data=f"Test {name}",
                export_format=fmt,
                module_drawer=style,
                color_mask=color
            )
            
            print(f"  ✅ Generated: {filename}")
            print(f"  📄 MIME type: {mimetype}")
            print(f"  📏 Size: {len(buf.getvalue())} bytes")
            
            # Save test file
            with open(f"test_{name.lower().replace(' ', '_')}.{fmt}", "wb") as f:
                f.write(buf.getvalue())
            print(f"  💾 Saved test file")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_web_api():
    """Test via web API."""
    print("\n🌐 Testing via web API...")
    
    base_url = "http://localhost:8891"
    
    test_cases = [
        ("PNG with radial gradient", {"data": "Web Test Radial", "export_format": "png", "module_drawer": "rounded", "color_mask": "radial"}),
        ("PNG with square gradient", {"data": "Web Test Square", "export_format": "png", "module_drawer": "circle", "color_mask": "square"}),
        ("SVG format", {"data": "Web Test SVG", "export_format": "svg", "module_drawer": "square", "color_mask": "solid"}),
    ]
    
    for name, data in test_cases:
        print(f"\n📋 Testing: {name}")
        try:
            response = requests.post(f"{base_url}/generate-qr", data=data)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    print("  ✅ Redirected to preview page (expected)")
                else:
                    print(f"  📄 Content-Type: {content_type}")
                    print(f"  📏 Size: {len(response.content)} bytes")
            else:
                print(f"  ❌ Unexpected status code")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing gradient and styling options...\n")
    
    # Test direct generation first
    test_direct_generation()
    
    # Test web API
    test_web_api()
    
    print("\n✨ Testing completed! Check the generated test files to verify styling works.")