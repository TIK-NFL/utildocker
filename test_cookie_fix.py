#!/usr/bin/env python3
"""Test that the cookie size issue is fixed."""

import requests
import sys

def test_cookie_fix():
    """Test QR generation to ensure no cookie size warnings."""
    print("🔧 Testing cookie size fix...")
    
    base_url = "http://localhost:8888"
    
    # Test cases that previously caused large cookies
    test_cases = [
        {
            "name": "Large PNG with gradient",
            "data": {
                "data": "Testing Cookie Size Fix - This is a longer text to generate a larger QR code",
                "export_format": "png",
                "module_drawer": "rounded",
                "color_mask": "radial"
            }
        },
        {
            "name": "SVG format",
            "data": {
                "data": "Testing SVG Cookie Fix",
                "export_format": "svg",
                "module_drawer": "square",
                "color_mask": "solid"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        try:
            # Create session to track cookies
            session = requests.Session()
            
            # Submit QR generation
            response = session.post(f"{base_url}/generate-qr", data=test_case['data'])
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ Request successful")
                
                # Check cookie sizes
                cookies = session.cookies
                total_cookie_size = 0
                for cookie in cookies:
                    cookie_size = len(f"{cookie.name}={cookie.value}")
                    total_cookie_size += cookie_size
                    print(f"  🍪 {cookie.name}: {cookie_size} bytes")
                
                print(f"  📏 Total cookie size: {total_cookie_size} bytes")
                
                if total_cookie_size < 4000:  # Well under 4KB limit
                    print("  ✅ Cookie size is within browser limits")
                else:
                    print("  ⚠️  Cookie size still too large")
                    
            else:
                print(f"  ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_cookie_fix()