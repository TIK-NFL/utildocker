#!/usr/bin/env python3
"""Test web features directly."""

import requests
import os

base_url = "http://localhost:8889"

# Test QR code generation
print("🔍 Testing QR Code Generation...")
response = requests.post(f"{base_url}/generate-qr", data={
    "data": "Hello from Web Test",
    "export_format": "png",
    "module_drawer": "rounded",
    "color_mask": "radial"
})
print(f"  Status Code: {response.status_code}")
print(f"  Content Type: {response.headers.get('Content-Type')}")
print(f"  File Size: {len(response.content)} bytes")

if response.status_code == 200:
    with open("web_test_qr.png", "wb") as f:
        f.write(response.content)
    print("  ✅ QR code saved as web_test_qr.png")

# Test URL shortening
print("\n🔗 Testing URL Shortening...")
response = requests.post(f"{base_url}/shorten-url", data={
    "full_url": "https://confluence.example.com/pages/123456789",
    "base_url": ""
})
print(f"  Status Code: {response.status_code}")

if response.status_code == 200:
    # Look for the short URL in the response
    if "short-url-input" in response.text:
        import re
        match = re.search(r'value="(https://[^"]+)"', response.text)
        if match:
            short_url = match.group(1)
            print(f"  ✅ Short URL: {short_url}")
        else:
            print("  ❌ Could not find short URL in response")
    else:
        print("  ✅ Response received (may have redirected)")

print("\n✨ Web feature tests completed!")