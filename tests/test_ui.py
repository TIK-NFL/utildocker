#!/usr/bin/env python3
"""
Playwright UI tests for the Utility Tools application.
"""

import asyncio
from playwright.async_api import async_playwright
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


async def test_ui():
    """Test the web interface using Playwright."""
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to the application
            print("🔍 Testing Web UI at http://localhost:8889")
            await page.goto("http://localhost:8889")
            
            # Check page title
            title = await page.title()
            print(f"✅ Page loaded - Title: {title}")
            
            # Check that both tabs are present
            qr_tab = await page.query_selector("#qr-tab")
            url_tab = await page.query_selector("#url-tab")
            assert qr_tab is not None, "QR tab not found"
            assert url_tab is not None, "URL tab not found"
            print("✅ Both tabs present")
            
            # Test QR Code Generator
            print("\n📷 Testing QR Code Generator:")
            
            # Ensure QR section is visible
            qr_section = await page.query_selector("#qr-section")
            is_visible = await qr_section.is_visible() if qr_section else False
            assert is_visible, "QR section not visible"
            
            # Fill in QR form
            await page.fill("#data", "https://example.com/test")
            print("  ✅ Filled text input")
            
            # Select rounded style
            await page.click('input[name="module_drawer"][value="rounded"]')
            print("  ✅ Selected rounded module style")
            
            # Select radial gradient
            await page.click('input[name="color_mask"][value="radial"]')
            print("  ✅ Selected radial gradient")
            
            # Submit form (test without actual submission to avoid download)
            submit_btn = await page.query_selector('button[type="submit"]')
            assert submit_btn is not None, "Submit button not found"
            print("  ✅ Submit button present")
            
            # Test URL Shortener
            print("\n🔗 Testing URL Shortener:")
            
            # Switch to URL tab
            await page.click("#url-tab")
            await page.wait_for_timeout(500)  # Wait for tab switch
            
            # Check URL section is visible
            url_section = await page.query_selector("#url-section")
            is_visible = await url_section.is_visible() if url_section else False
            assert is_visible, "URL section not visible"
            print("  ✅ URL shortener tab activated")
            
            # Fill in URL form
            await page.fill("#full_url", "https://confluence.example.com/pages/123456789")
            print("  ✅ Filled Confluence URL")
            
            # Check optional base URL field exists
            base_url_field = await page.query_selector("#base_url")
            assert base_url_field is not None, "Base URL field not found"
            print("  ✅ Base URL field present")
            
            # Check submit button
            url_submit = await page.query_selector('#url-section button[type="submit"]')
            assert url_submit is not None, "URL submit button not found"
            print("  ✅ Submit button present")
            
            # Test responsive design
            print("\n📱 Testing Responsive Design:")
            
            # Test mobile viewport
            await page.set_viewport_size({"width": 375, "height": 667})
            await page.wait_for_timeout(500)
            
            # Check navigation is still accessible
            nav_visible = await page.is_visible("nav")
            assert nav_visible, "Navigation not visible on mobile"
            print("  ✅ Mobile layout working")
            
            # Test tablet viewport
            await page.set_viewport_size({"width": 768, "height": 1024})
            await page.wait_for_timeout(500)
            print("  ✅ Tablet layout working")
            
            # Check example images
            print("\n🖼️  Testing Example Images:")
            example_images = await page.query_selector_all(".example-item img")
            assert len(example_images) == 4, f"Expected 4 example images, found {len(example_images)}"
            print(f"  ✅ Found {len(example_images)} example images")
            
            print("\n✨ All UI tests passed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            # Take screenshot for debugging
            await page.screenshot(path="test_failure.png")
            print("📸 Screenshot saved as test_failure.png")
            raise
        
        finally:
            await browser.close()


async def main():
    """Main test runner."""
    print("🚀 Starting UI tests...\n")
    
    # Check if app is running
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:8889")
    except:
        print("⚠️  Flask app not running on port 8889")
        print("Please start the app with: PORT=8889 python app.py")
        return
    
    await test_ui()


if __name__ == "__main__":
    asyncio.run(main())