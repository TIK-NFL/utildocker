#!/usr/bin/env python3
"""Test to create visually distinct QR codes to verify styling works."""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import QRCodeGenerator

def create_comparison_qr_codes():
    """Create QR codes with different styles for visual comparison."""
    print("🎨 Creating QR codes with different styles for comparison...")
    
    qr_gen = QRCodeGenerator()
    
    # Test data
    test_data = "TESTING VISUAL DIFFERENCES"
    
    styles = [
        ("solid_square", "png", "square", "solid"),
        ("radial_square", "png", "square", "radial"),
        ("square_gradient", "png", "square", "square"),
        ("rounded_radial", "png", "rounded", "radial"),
        ("circle_square", "png", "circle", "square"),
    ]
    
    for name, fmt, style, color in styles:
        print(f"\n📸 Creating: {name}")
        try:
            buf, mimetype, filename = qr_gen.generate_qr_code(
                data=test_data,
                export_format=fmt,
                module_drawer=style,
                color_mask=color
            )
            
            # Save with descriptive name
            output_name = f"comparison_{name}.{fmt}"
            with open(output_name, "wb") as f:
                f.write(buf.getvalue())
            
            size = len(buf.getvalue())
            print(f"  ✅ Saved: {output_name}")
            print(f"  📏 Size: {size:,} bytes")
            
            # Analyze file size to detect if styling is applied
            if color in ['radial', 'square'] and size > 10000:
                print(f"  🎨 ✅ Gradient detected (large file size)")
            elif style in ['rounded', 'circle'] and size > 5000:
                print(f"  🔷 ✅ Shape styling detected")
            elif color == 'solid' and style == 'square' and size < 5000:
                print(f"  📦 ✅ Basic style (small file)")
            else:
                print(f"  ⚠️  Unexpected file size for this style combination")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n📋 Comparison files created! Check the visual differences:")
    print(f"   - comparison_solid_square.png (baseline)")
    print(f"   - comparison_radial_square.png (should have gradient)")
    print(f"   - comparison_square_gradient.png (should have gradient)")
    print(f"   - comparison_rounded_radial.png (rounded + gradient)")
    print(f"   - comparison_circle_square.png (circle + gradient)")

if __name__ == "__main__":
    create_comparison_qr_codes()