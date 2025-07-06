#!/usr/bin/env python3
"""Debug web interface issues using Playwright."""

import asyncio
from playwright.async_api import async_playwright

async def debug_gradient_issue():
    """Debug why user might not see gradients working."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        page = await browser.new_page()
        
        try:
            print("🔍 Debugging gradient and SVG issues...")
            await page.goto("http://localhost:8888")  # User's port
            
            print("\n1️⃣ Testing PNG with radial gradient...")
            
            # Fill form for radial gradient
            await page.fill('#data', 'Test Radial Gradient')
            await page.click('input[name="export_format"][value="png"]')
            await page.click('input[name="module_drawer"][value="rounded"]')
            await page.click('input[name="color_mask"][value="radial"]')
            
            # Submit and wait
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)
            
            # Check if preview appears
            preview = await page.query_selector('.qr-preview')
            if preview and await preview.is_visible():
                print("  ✅ PNG radial gradient preview appeared")
                
                # Take screenshot
                await page.screenshot(path="debug_png_radial.png")
                print("  📸 Screenshot saved: debug_png_radial.png")
            else:
                print("  ❌ PNG preview did not appear")
            
            print("\n2️⃣ Testing SVG generation...")
            
            # Generate new QR code
            generate_new_btn = await page.query_selector('button.new-btn')
            if generate_new_btn:
                await generate_new_btn.click()
                await page.wait_for_timeout(1000)
            
            # Fill form for SVG
            await page.fill('#data', 'Test SVG Format')
            await page.click('input[name="export_format"][value="svg"]')
            
            # Submit and wait
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)
            
            # Check SVG preview
            svg_preview = await page.query_selector('.qr-preview')
            if svg_preview and await svg_preview.is_visible():
                print("  ✅ SVG preview container appeared")
                
                # Check if SVG content is present
                svg_element = await page.query_selector('.svg-container svg')
                if svg_element:
                    print("  ✅ SVG element found in DOM")
                    
                    # Check SVG dimensions
                    bbox = await svg_element.bounding_box()
                    if bbox:
                        print(f"  📐 SVG size: {bbox['width']}x{bbox['height']}")
                    else:
                        print("  ⚠️  SVG has no dimensions")
                else:
                    print("  ❌ SVG element not found in DOM")
                    
                    # Check raw content
                    svg_container = await page.query_selector('.svg-container')
                    if svg_container:
                        content = await svg_container.inner_html()
                        print(f"  📝 SVG container content preview: {content[:100]}...")
                
                # Take screenshot
                await page.screenshot(path="debug_svg.png")
                print("  📸 Screenshot saved: debug_svg.png")
            else:
                print("  ❌ SVG preview did not appear")
            
            print("\n3️⃣ Testing square gradient...")
            
            # Generate new QR code
            if generate_new_btn:
                await generate_new_btn.click()
                await page.wait_for_timeout(1000)
            
            # Fill form for square gradient
            await page.fill('#data', 'Test Square Gradient')
            await page.click('input[name="export_format"][value="png"]')
            await page.click('input[name="module_drawer"][value="circle"]')
            await page.click('input[name="color_mask"][value="square"]')
            
            # Submit and wait
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)
            
            # Take screenshot
            await page.screenshot(path="debug_square_gradient.png")
            print("  📸 Screenshot saved: debug_square_gradient.png")
            
            print("\n✅ Debug completed! Check the screenshots to see what user sees.")
            
            # Wait for user to examine
            print("🔍 Keeping browser open for 10 seconds for examination...")
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"\n❌ Debug failed: {e}")
            await page.screenshot(path="debug_error.png")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_gradient_issue())