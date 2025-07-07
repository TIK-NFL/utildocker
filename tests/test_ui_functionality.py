#!/usr/bin/env python3
"""Test UI functionality using Playwright."""

import asyncio
from playwright.async_api import async_playwright

async def test_form_functionality():
    """Test that radio buttons and styling work correctly."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()
        
        try:
            print("🔍 Testing form functionality...")
            await page.goto("http://localhost:8891")
            
            # Test initial state
            print("📋 Testing initial form state...")
            png_radio = await page.query_selector('input[name="export_format"][value="png"]')
            is_checked = await png_radio.is_checked()
            print(f"  PNG radio initially checked: {is_checked}")
            
            # Test clicking different options
            print("🎨 Testing styling options...")
            
            # Click SVG format
            await page.click('input[name="export_format"][value="svg"]')
            await page.wait_for_timeout(100)
            svg_checked = await page.is_checked('input[name="export_format"][value="svg"]')
            print(f"  SVG radio checked after click: {svg_checked}")
            
            # Click rounded style
            await page.click('input[name="module_drawer"][value="rounded"]')
            await page.wait_for_timeout(100)
            rounded_checked = await page.is_checked('input[name="module_drawer"][value="rounded"]')
            print(f"  Rounded module checked: {rounded_checked}")
            
            # Click radial gradient
            await page.click('input[name="color_mask"][value="radial"]')
            await page.wait_for_timeout(100)
            radial_checked = await page.is_checked('input[name="color_mask"][value="radial"]')
            print(f"  Radial gradient checked: {radial_checked}")
            
            # Fill in data and submit
            await page.fill('#data', 'Test Form Functionality')
            print("  Filled text input")
            
            # Submit form
            await page.click('button[type="submit"]')
            print("  Submitted form")
            
            # Wait for redirect and check if preview appears
            await page.wait_for_timeout(2000)
            preview = await page.query_selector('.qr-preview')
            preview_visible = await preview.is_visible() if preview else False
            print(f"  QR preview visible: {preview_visible}")
            
            if preview_visible:
                # Test "Generate New" button
                await page.click('button.new-btn')
                await page.wait_for_timeout(500)
                
                # Check if form is visible again
                form = await page.query_selector('#qr-form')
                form_visible = await form.is_visible() if form else False
                print(f"  Form visible after 'Generate New': {form_visible}")
                
                # Check if radio selections are preserved
                svg_still_checked = await page.is_checked('input[name="export_format"][value="svg"]')
                rounded_still_checked = await page.is_checked('input[name="module_drawer"][value="rounded"]')
                radial_still_checked = await page.is_checked('input[name="color_mask"][value="radial"]')
                
                print(f"  SVG still selected: {svg_still_checked}")
                print(f"  Rounded still selected: {rounded_still_checked}")
                print(f"  Radial still selected: {radial_still_checked}")
                
                # Test generating with different settings
                await page.click('input[name="export_format"][value="png"]')
                await page.click('input[name="module_drawer"][value="circle"]')
                await page.click('input[name="color_mask"][value="square"]')
                
                await page.fill('#data', 'Test Different Settings')
                await page.click('button[type="submit"]')
                
                print("  ✅ Second generation test completed")
            
            print("\n✨ Form functionality test completed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            raise
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_form_functionality())