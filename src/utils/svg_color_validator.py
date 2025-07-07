"""SVG Color Validation utilities based on svg_checker.py functionality."""

import tempfile
import os
from lxml import etree
import webcolors


class SVGColorValidator:
    """Handles SVG color validation and analysis."""
    
    def __init__(self):
        self.namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    def validate_svg_colors(self, svg_content):
        """
        Validate SVG colors and return analysis.
        
        Args:
            svg_content (str): SVG content as string
            
        Returns:
            dict: Analysis results with color information
        """
        try:
            # Parse SVG content
            root = etree.fromstring(svg_content.encode('utf-8'))
            
            # Find shape elements
            shapes = root.xpath(
                '//svg:path | //svg:rect | //svg:circle | //svg:ellipse | //svg:line | //svg:polyline',
                namespaces=self.namespaces
            )
            
            if not shapes:
                shapes = root.xpath(
                    '//path | //rect | //circle | //ellipse | //line | //polyline'
                )
            
            analysis = {
                'total_shapes': len(shapes),
                'shapes': [],
                'color_summary': {
                    'unique_colors': set(),
                    'has_gradients': False,
                    'stroke_colors': set(),
                    'fill_colors': set()
                },
                'compliance': {
                    'red_strokes': 0,
                    'correct_width': 0,
                    'correct_opacity': 0,
                    'total_with_stroke': 0
                }
            }
            
            for i, shape in enumerate(shapes):
                tag_name = etree.QName(shape).localname
                shape_id = shape.get('id', f"{tag_name}_{i+1}")
                
                shape_info = {
                    'id': shape_id,
                    'tag': tag_name,
                    'stroke': self._analyze_color(shape.get('stroke')),
                    'fill': self._analyze_color(shape.get('fill')),
                    'stroke_width': shape.get('stroke-width'),
                    'stroke_opacity': shape.get('stroke-opacity', '1')
                }
                
                # Check compliance for original svg_checker.py requirements
                if shape_info['stroke']['color']:
                    analysis['compliance']['total_with_stroke'] += 1
                    
                    # Check for red stroke (100% red)
                    stroke_color = shape_info['stroke']['color'].lower()
                    if stroke_color in ['red', '#ff0000', '#f00', 'rgb(255,0,0)']:
                        analysis['compliance']['red_strokes'] += 1
                
                # Check stroke width (1mm)
                if shape_info['stroke_width'] == '1mm':
                    analysis['compliance']['correct_width'] += 1
                
                # Check stroke opacity (1)
                if shape_info['stroke_opacity'] == '1':
                    analysis['compliance']['correct_opacity'] += 1
                
                # Add colors to summary
                if shape_info['stroke']['color']:
                    analysis['color_summary']['stroke_colors'].add(shape_info['stroke']['color'])
                    analysis['color_summary']['unique_colors'].add(shape_info['stroke']['color'])
                
                if shape_info['fill']['color']:
                    analysis['color_summary']['fill_colors'].add(shape_info['fill']['color'])
                    analysis['color_summary']['unique_colors'].add(shape_info['fill']['color'])
                
                analysis['shapes'].append(shape_info)
            
            # Convert sets to lists for JSON serialization
            analysis['color_summary']['unique_colors'] = list(analysis['color_summary']['unique_colors'])
            analysis['color_summary']['stroke_colors'] = list(analysis['color_summary']['stroke_colors'])
            analysis['color_summary']['fill_colors'] = list(analysis['color_summary']['fill_colors'])
            
            return analysis
            
        except Exception as e:
            return {
                'error': f"Error analyzing SVG: {str(e)}",
                'total_shapes': 0,
                'shapes': [],
                'color_summary': {
                    'unique_colors': [],
                    'has_gradients': False,
                    'stroke_colors': [],
                    'fill_colors': []
                }
            }
    
    def _analyze_color(self, color_value):
        """
        Analyze a color value and extract information.
        
        Args:
            color_value (str): Color value from SVG attribute
            
        Returns:
            dict: Color analysis information
        """
        if not color_value:
            return {'color': None, 'rgb': None, 'valid': False, 'type': 'none'}
        
        try:
            # Handle special values
            if color_value.lower() in ['none', 'transparent']:
                return {'color': color_value, 'rgb': None, 'valid': True, 'type': 'special'}
            
            # Try to parse as named color
            if color_value.replace('-', '').replace('_', '').isalpha():
                try:
                    rgb_color = webcolors.name_to_rgb(color_value)
                    return {
                        'color': color_value,
                        'rgb': rgb_color,
                        'valid': True,
                        'type': 'named',
                        'hex': webcolors.rgb_to_hex(rgb_color)
                    }
                except ValueError:
                    pass
            
            # Try to parse as hex color
            if color_value.startswith('#'):
                try:
                    rgb_color = webcolors.hex_to_rgb(color_value)
                    return {
                        'color': color_value,
                        'rgb': rgb_color,
                        'valid': True,
                        'type': 'hex',
                        'hex': color_value
                    }
                except ValueError:
                    pass
            
            # Check for RGB/RGBA patterns
            if color_value.startswith(('rgb(', 'rgba(')):
                return {
                    'color': color_value,
                    'rgb': None,
                    'valid': True,
                    'type': 'rgb_function'
                }
            
            # Check for URL references (gradients, patterns)
            if color_value.startswith('url('):
                return {
                    'color': color_value,
                    'rgb': None,
                    'valid': True,
                    'type': 'url_reference'
                }
            
            # Unknown format
            return {
                'color': color_value,
                'rgb': None,
                'valid': False,
                'type': 'unknown'
            }
            
        except Exception:
            return {
                'color': color_value,
                'rgb': None,
                'valid': False,
                'type': 'error'
            }
    
    def extract_colors_for_picker(self, svg_content):
        """
        Extract colors from SVG that can be used to populate color picker.
        
        Args:
            svg_content (str): SVG content as string
            
        Returns:
            dict: Extracted colors for color picker initialization
        """
        analysis = self.validate_svg_colors(svg_content)
        
        colors = {
            'foreground': '#000000',  # Default
            'background': '#ffffff',  # Default
            'suggested_colors': []
        }
        
        # Try to determine foreground/background from analysis
        if analysis['color_summary']['stroke_colors']:
            colors['foreground'] = analysis['color_summary']['stroke_colors'][0]
        
        if analysis['color_summary']['fill_colors']:
            # If we have a fill color that's not the same as stroke, use it as background
            fill_colors = [c for c in analysis['color_summary']['fill_colors'] 
                          if c != colors['foreground']]
            if fill_colors:
                colors['background'] = fill_colors[0]
        
        # Add all unique colors as suggestions
        for color in analysis['color_summary']['unique_colors']:
            if color and color.startswith('#'):
                colors['suggested_colors'].append(color)
        
        return colors