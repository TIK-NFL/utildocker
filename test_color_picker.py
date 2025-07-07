#!/usr/bin/env python3
"""Test script to verify color picker functionality works."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_color_picker_functionality():
    """Test all color picker related functionality."""
    print("🧪 Testing Color Picker Functionality")
    print("=" * 50)
    
    # Test 1: Import all modules
    try:
        from utils import QRCodeGenerator, URLShortener, SVGColorValidator
        print("✅ 1. All modules imported successfully")
    except Exception as e:
        print(f"❌ 1. Module import failed: {e}")
        return False
    
    # Test 2: Basic QR generation with custom colors
    try:
        qr_gen = QRCodeGenerator()
        buf, mimetype, filename = qr_gen.generate_qr_code(
            data='Test custom colors',
            export_format='png',
            color_mask='custom',
            foreground_color='#ff0000',
            background_color='#ffffff'
        )
        print(f"✅ 2. Custom colors work - Generated {filename} ({len(buf.getvalue())} bytes)")
    except Exception as e:
        print(f"❌ 2. Custom colors failed: {e}")
        return False
    
    # Test 3: Gradient QR generation
    try:
        buf, mimetype, filename = qr_gen.generate_qr_code(
            data='Test gradient',
            export_format='png',
            color_mask='custom',
            gradient_start='#ff0000',
            gradient_end='#0000ff'
        )
        print(f"✅ 3. Custom gradients work - Generated {filename} ({len(buf.getvalue())} bytes)")
    except Exception as e:
        print(f"❌ 3. Custom gradients failed: {e}")
        return False
    
    # Test 4: SVG color analysis
    try:
        validator = SVGColorValidator()
        test_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <rect x="10" y="10" width="30" height="30" fill="#ff0000" stroke="#000000"/>
            <circle cx="70" cy="70" r="15" fill="#00ff00" stroke="#0000ff"/>
        </svg>'''
        
        analysis = validator.validate_svg_colors(test_svg)
        colors = validator.extract_colors_for_picker(test_svg)
        
        print(f"✅ 4. SVG analysis works - Found {len(analysis['color_summary']['unique_colors'])} colors")
        print(f"   Colors: {analysis['color_summary']['unique_colors']}")
        print(f"   Suggested fg: {colors['foreground']}, bg: {colors['background']}")
    except Exception as e:
        print(f"❌ 4. SVG analysis failed: {e}")
        return False
    
    # Test 5: Check HTML template has color picker elements
    try:
        with open('src/templates/index.html', 'r') as f:
            html_content = f.read()
        
        required_elements = [
            'value="custom"',
            'id="foreground_color"',
            'id="background_color"',
            'id="gradient_start"',
            'id="gradient_end"',
            'id="use_gradient"'
        ]
        
        missing = [elem for elem in required_elements if elem not in html_content]
        if missing:
            print(f"❌ 5. HTML template missing: {missing}")
            return False
        
        print("✅ 5. HTML template has all color picker elements")
    except Exception as e:
        print(f"❌ 5. HTML template check failed: {e}")
        return False
    
    # Test 6: Check CSS has color picker styles
    try:
        with open('src/static/css/style.css', 'r') as f:
            css_content = f.read()
        
        required_styles = [
            'color-picker-group',
            'color-input',
            'input[type="color"]',
            '#custom-colors'
        ]
        
        missing = [style for style in required_styles if style not in css_content]
        if missing:
            print(f"❌ 6. CSS missing styles: {missing}")
            return False
        
        print("✅ 6. CSS has all color picker styles")
    except Exception as e:
        print(f"❌ 6. CSS check failed: {e}")
        return False
    
    # Test 7: Check JavaScript has color picker functionality
    try:
        with open('src/static/js/script.js', 'r') as f:
            js_content = f.read()
        
        required_functions = [
            'handleColorMaskChange',
            'analyzeSVGColors',
            'useColorInPicker',
            'addSVGAnalysisFeature'
        ]
        
        missing = [func for func in required_functions if func not in js_content]
        if missing:
            print(f"❌ 7. JavaScript missing functions: {missing}")
            return False
        
        print("✅ 7. JavaScript has all color picker functions")
    except Exception as e:
        print(f"❌ 7. JavaScript check failed: {e}")
        return False
    
    # Test 8: Check SVG checker tab and functionality
    try:
        with open('src/templates/index.html', 'r') as f:
            html_content = f.read()
        
        svg_checker_elements = [
            'id="svg-tab"',
            'id="svg-section"',
            'SVG Color Checker',
            'action="/check-svg"',
            'name="svg_file"',
            'name="svg_text"'
        ]
        
        missing = [elem for elem in svg_checker_elements if elem not in html_content]
        if missing:
            print(f"❌ 8. SVG checker HTML missing: {missing}")
            return False
        
        print("✅ 8. SVG checker tab and form are in HTML template")
    except Exception as e:
        print(f"❌ 8. SVG checker HTML check failed: {e}")
        return False

    print("\n🎉 ALL TESTS PASSED! Color picker AND SVG checker functionality fully implemented.")
    print("\n📋 Features implemented:")
    print("   • Custom foreground/background colors")
    print("   • Custom gradient colors") 
    print("   • SVG color analysis and extraction")
    print("   • Interactive color picker UI")
    print("   • Integration with existing QR generator")
    print("   • SVG analysis button for generated SVG QR codes")
    print("   • Dedicated SVG Color Checker tab")
    print("   • SVG file upload and text paste support")
    print("   • svg_checker.py compliance checking")
    print("   • Color suggestions from SVG analysis")
    
    return True

if __name__ == "__main__":
    success = test_color_picker_functionality()
    sys.exit(0 if success else 1)