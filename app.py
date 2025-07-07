#!/usr/bin/env python3
"""
Utility Tools Flask Application
Provides QR code generation and URL shortening services.
"""

import os
import sys
import logging
import io
import uuid
import tempfile
from flask import Flask, request, render_template, send_file, flash, redirect, url_for, session, Response
from PIL import Image

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import QRCodeGenerator, URLShortener, SVGColorValidator

app = Flask(__name__, 
            template_folder='src/templates',
            static_folder='src/static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize utility classes
qr_generator = QRCodeGenerator()
url_shortener = URLShortener()
svg_validator = SVGColorValidator()

# Create temp directory for QR previews
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'qr_previews')
os.makedirs(TEMP_DIR, exist_ok=True)

def cleanup_old_files():
    """Clean up old preview files (older than 1 hour)."""
    import time
    try:
        current_time = time.time()
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > 3600:  # 1 hour
                    os.remove(filepath)
                    logger.info(f"Cleaned up old preview file: {filename}")
    except Exception as e:
        logger.warning(f"Failed to cleanup old files: {e}")

def save_qr_preview(qr_data, mimetype, filename, export_format):
    """Save QR preview to temp file and return preview info."""
    # Generate unique preview ID
    preview_id = str(uuid.uuid4())
    
    # Save to temp file
    temp_filename = f"{preview_id}.{export_format}"
    temp_filepath = os.path.join(TEMP_DIR, temp_filename)
    
    if export_format == 'svg':
        # Save SVG as text
        with open(temp_filepath, 'w', encoding='utf-8') as f:
            f.write(qr_data)
    else:
        # Save PNG as binary from base64
        import base64
        qr_bytes = base64.b64decode(qr_data)
        with open(temp_filepath, 'wb') as f:
            f.write(qr_bytes)
    
    # Clean up old files periodically
    cleanup_old_files()
    
    # Return preview info (small, session-safe)
    return {
        'preview_id': preview_id,
        'filename': filename,
        'format': export_format,
        'mimetype': mimetype,
        'temp_file': temp_filename
    }


@app.route('/')
def index():
    """Main page with both QR code generator and URL shortener."""
    qr_preview = None
    show_qr = request.args.get('show_qr')
    
    if show_qr and 'qr_preview' in session:
        qr_preview = session['qr_preview']
        
    return render_template('index.html', qr_preview=qr_preview)


@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    """Generate QR code with specified parameters."""
    try:
        # Get form data
        data = request.form.get('data')
        if not data:
            flash('Please enter text or URL to encode', 'error')
            return redirect(url_for('index'))
        
        # Get optional logo image
        logo_image = None
        if 'image' in request.files and request.files['image'].filename != '':
            logo_image = Image.open(request.files['image'])
            logger.info(f"Logo image uploaded: {request.files['image'].filename}")
        
        # Get styling options
        export_format = request.form.get('export_format', 'png')
        module_drawer = request.form.get('module_drawer', 'square')
        color_mask = request.form.get('color_mask', 'solid')
        
        # Get custom color options
        foreground_color = request.form.get('foreground_color')
        background_color = request.form.get('background_color')
        gradient_start = request.form.get('gradient_start')
        gradient_end = request.form.get('gradient_end')
        use_gradient = request.form.get('use_gradient') == 'on'
        
        # Only use gradient colors if custom mode and gradient is enabled
        if color_mask == 'custom' and not use_gradient:
            gradient_start = None
            gradient_end = None
        
        if export_format == 'svg':
            logger.info(f"Generating QR code - Format: {export_format} (styling options not available for SVG)")
        else:
            if color_mask == 'custom':
                color_info = f"custom (fg: {foreground_color}, bg: {background_color}"
                if use_gradient:
                    color_info += f", gradient: {gradient_start} to {gradient_end}"
                color_info += ")"
                logger.info(f"Generating QR code - Format: {export_format}, Style: {module_drawer}, Color: {color_info}")
            else:
                logger.info(f"Generating QR code - Format: {export_format}, Style: {module_drawer}, Color: {color_mask}")
        
        # Generate QR code
        buf, mimetype, filename = qr_generator.generate_qr_code(
            data=data,
            export_format=export_format,
            module_drawer=module_drawer,
            color_mask=color_mask,
            logo_image=logo_image,
            foreground_color=foreground_color,
            background_color=background_color,
            gradient_start=gradient_start,
            gradient_end=gradient_end
        )
        
        # Save QR code for preview using file storage (not session)
        import base64
        buf.seek(0)  # Reset buffer to beginning
        
        if export_format == 'svg':
            # For SVG, get raw content
            svg_content = buf.read().decode('utf-8')
            qr_data = svg_content
            logger.info(f"Generated SVG QR code, size: {len(svg_content)} chars")
            # Re-encode for download
            buf = io.BytesIO(svg_content.encode('utf-8'))
        else:
            # For PNG, get base64 data
            qr_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            logger.info(f"Generated PNG QR code, base64 size: {len(qr_data)} chars")
            buf.seek(0)  # Reset buffer for download
        
        # Save preview to temp file and store small reference in session
        preview_info = save_qr_preview(qr_data, mimetype, filename, export_format)
        session.pop('qr_preview', None)  # Clear any existing preview
        session['qr_preview'] = preview_info
        logger.info(f"Stored QR preview: {filename} (ID: {preview_info['preview_id']})")
        
        return redirect(url_for('index', show_qr=1))
        
    except Exception as e:
        flash(f'Error generating QR code: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/clear-qr-session', methods=['POST'])
def clear_qr_session():
    """Clear QR preview from session."""
    session.pop('qr_preview', None)
    logger.info("Cleared QR preview from session")
    return {'status': 'success'}


@app.route('/preview/<preview_id>')
def serve_preview(preview_id):
    """Serve QR preview file."""
    qr_preview = session.get('qr_preview')
    if not qr_preview or qr_preview['preview_id'] != preview_id:
        return "Preview not found", 404
    
    temp_filepath = os.path.join(TEMP_DIR, qr_preview['temp_file'])
    if not os.path.exists(temp_filepath):
        return "Preview file not found", 404
    
    return send_file(
        temp_filepath,
        mimetype=qr_preview['mimetype']
    )


@app.route('/download-qr')
def download_qr():
    """Download the generated QR code."""
    qr_preview = session.get('qr_preview')
    if not qr_preview:
        flash('No QR code to download. Please generate one first.', 'error')
        return redirect(url_for('index'))
    
    temp_filepath = os.path.join(TEMP_DIR, qr_preview['temp_file'])
    if not os.path.exists(temp_filepath):
        flash('Preview file not found. Please generate a new QR code.', 'error')
        return redirect(url_for('index'))
    
    return send_file(
        temp_filepath,
        mimetype=qr_preview['mimetype'],
        as_attachment=True,
        download_name=qr_preview['filename']
    )


@app.route('/check-svg', methods=['POST'])
def check_svg():
    """Check SVG file based on svg_checker.py functionality."""
    try:
        svg_content = None
        
        # Get SVG content from either file upload or text input
        if 'svg_file' in request.files and request.files['svg_file'].filename != '':
            svg_file = request.files['svg_file']
            svg_content = svg_file.read().decode('utf-8')
        elif request.form.get('svg_text'):
            svg_content = request.form.get('svg_text')
        
        if not svg_content:
            flash('Please provide an SVG file or paste SVG content', 'error')
            return render_template('index.html')
        
        # Get check options
        check_red = request.form.get('check_red') == 'on'
        check_width = request.form.get('check_width') == 'on'
        check_opacity = request.form.get('check_opacity') == 'on'
        
        # Analyze SVG
        analysis = svg_validator.validate_svg_colors(svg_content)
        color_suggestions = svg_validator.extract_colors_for_picker(svg_content)
        
        logger.info(f"SVG analysis completed: {analysis['total_shapes']} shapes, {len(analysis['color_summary']['unique_colors'])} colors")
        
        return render_template('index.html', 
                             svg_analysis=analysis,
                             color_suggestions=color_suggestions,
                             check_red=check_red,
                             check_width=check_width,
                             check_opacity=check_opacity,
                             show_svg=True)
        
    except Exception as e:
        logger.error(f"Error checking SVG: {str(e)}")
        flash(f'Error analyzing SVG: {str(e)}', 'error')
        return render_template('index.html')


@app.route('/analyze-svg-colors', methods=['POST'])
def analyze_svg_colors():
    """Analyze colors in SVG content."""
    try:
        data = request.get_json()
        if not data or 'svg_content' not in data:
            return {'error': 'No SVG content provided'}, 400
        
        svg_content = data['svg_content']
        analysis = svg_validator.validate_svg_colors(svg_content)
        color_suggestions = svg_validator.extract_colors_for_picker(svg_content)
        
        return {
            'analysis': analysis,
            'color_suggestions': color_suggestions
        }
        
    except Exception as e:
        logger.error(f"Error analyzing SVG colors: {str(e)}")
        return {'error': f'Error analyzing SVG: {str(e)}'}, 500


@app.route('/shorten-url', methods=['POST'])
def shorten_url():
    """Shorten a Confluence URL."""
    try:
        full_url = request.form.get('full_url')
        base_url = request.form.get('base_url')
        
        if not full_url:
            flash('Please enter a Confluence URL', 'error')
            return redirect(url_for('index'))
        
        # Generate short URL
        short_url = url_shortener.shorten_url(full_url, base_url)
        
        return render_template('index.html', short_url=short_url)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error shortening URL: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html'), 500


if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 8888))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)