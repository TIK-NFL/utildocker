#!/usr/bin/env python3
"""Test form data submission to debug gradient/styling issues."""

import requests
import os

base_url = "http://localhost:8891"

print("🔍 Testing form data submission...")

# Test different combinations
test_cases = [
    {
        "name": "PNG with square solid",
        "data": {
            "data": "Test PNG Square Solid",
            "export_format": "png", 
            "module_drawer": "square",
            "color_mask": "solid"
        }
    },
    {
        "name": "PNG with rounded radial",
        "data": {
            "data": "Test PNG Rounded Radial",
            "export_format": "png",
            "module_drawer": "rounded", 
            "color_mask": "radial"
        }
    },
    {
        "name": "PNG with circle square gradient", 
        "data": {
            "data": "Test PNG Circle Square",
            "export_format": "png",
            "module_drawer": "circle",
            "color_mask": "square"
        }
    },
    {
        "name": "SVG with square solid",
        "data": {
            "data": "Test SVG Square Solid", 
            "export_format": "svg",
            "module_drawer": "square",
            "color_mask": "solid"
        }
    }
]

for test_case in test_cases:
    print(f"\n📝 Testing: {test_case['name']}")
    print(f"   Data: {test_case['data']}")
    
    response = requests.post(f"{base_url}/generate-qr", data=test_case['data'])
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        # Check if we got a redirect (which means success)
        if 'text/html' in response.headers.get('Content-Type', ''):
            print("   ✅ Success - got HTML response (likely redirected to preview)")
        else:
            print(f"   📁 Got file - Content-Type: {response.headers.get('Content-Type')}")
            print(f"   📏 Size: {len(response.content)} bytes")
    else:
        print(f"   ❌ Error: {response.status_code}")
        if response.text:
            print(f"   Error details: {response.text[:200]}...")

print("\n✨ Form data tests completed!")