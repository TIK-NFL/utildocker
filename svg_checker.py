from lxml import etree
import argparse
import webcolors

def check_svg(svg_file):
    """
    Parses an SVG file and checks the color and thickness of vector lines.

    Args:
        svg_file: The path to the SVG file.
    """
    try:
        tree = etree.parse(svg_file)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"Error parsing SVG file: {e}")
        return
    except FileNotFoundError:
        print(f"Error: File not found at {svg_file}")
        return

    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    shapes = root.xpath(
        '//svg:path | //svg:rect | //svg:circle | //svg:ellipse | //svg:line | //svg:polyline',
        namespaces=namespaces
    )

    if not shapes:
        shapes = root.xpath(
            '//path | //rect | //circle | //ellipse | //line | //polyline'
        )

    if not shapes:
        print("No shape elements found in the SVG file.")
        return

    print(f"Found {len(shapes)} shape element(s).\n")
    
    for i, shape in enumerate(shapes):
        tag_name = etree.QName(shape).localname
        shape_id = shape.get('id', f"{tag_name}_{i+1}")
        print(f"--- Checking Shape '{shape_id}' ({tag_name}) ---")

        # Check stroke width
        stroke_width = shape.get('stroke-width')
        if stroke_width == "1mm":
            print(f"  - Stroke width: {stroke_width} (OK)")
        else:
            print(f"  - Stroke width: {stroke_width} (Warning: Should be 1mm)")

        # Check stroke color
        stroke_color = shape.get('stroke')
        try:
            rgb_color = webcolors.name_to_rgb(stroke_color) if stroke_color.isalpha() else webcolors.hex_to_rgb(stroke_color)
            if rgb_color == (255, 0, 0):
                print(f"  - Stroke color: {stroke_color} (OK)")
            else:
                print(f"  - Stroke color: {stroke_color} (Warning: Should be 100% red)")
        except (ValueError, AttributeError):
            print(f"  - Stroke color: {stroke_color} (Warning: Could not determine color)")

        # Check stroke opacity
        stroke_opacity = shape.get('stroke-opacity', '1') # Default to 1 if not present
        if stroke_opacity == "1":
            print(f"  - Stroke opacity: {stroke_opacity} (OK)")
        else:
            print(f"  - Stroke opacity: {stroke_opacity} (Warning: Should be 1)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check SVG file for line color and thickness.')
    parser.add_argument('svg_file', help='The path to the SVG file to check.')
    args = parser.parse_args()

    check_svg(args.svg_file)