# Utility Tools

A comprehensive Flask web application and CLI toolkit providing QR code generation and Confluence URL shortening services.

## Features

### 🔳 QR Code Generator
- Generate QR codes for any text or URL
- Multiple export formats (PNG, SVG)
- Customizable styling options:
  - Module shapes: Square, Rounded, Circle
  - Color masks: Solid, Radial Gradient, Square Gradient
- Logo embedding support
- Web interface and CLI access

### 🔗 URL Shortener
- Convert long Confluence URLs to short links
- Automatic base URL detection
- Custom base URL support
- Web interface and CLI access

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd utildocker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at `http://localhost:8888`

#### Features:
- **QR Code Generator**: Enter text/URL, customize styling, optionally add a logo
- **URL Shortener**: Enter Confluence URL, get shortened version
- **Responsive Design**: Works on desktop and mobile devices

### Command Line Interface

The CLI provides command-line access to all features:

#### Generate QR Codes
```bash
# Basic QR code
python cli.py qr --data "Hello World" --output qr.png

# QR code with logo and custom styling
python cli.py qr --data "https://example.com" --logo logo.png --output qr.png --style rounded --color radial

# SVG output
python cli.py qr --data "https://example.com" --output qr.svg --format svg
```

#### Shorten URLs
```bash
# Basic URL shortening
python cli.py shorten --url "https://confluence.example.com/pages/123456"

# With custom base URL
python cli.py shorten --url "https://conf.example.com/pages/123" --base "https://short.example.com"
```

### Legacy CLI (tiny_url_wm.py)

The original URL shortener CLI is still available:
```bash
python tiny_url_wm.py --full-url "https://confluence.example.com/pages/123456"
```

## Project Structure

```
utildocker/
├── app.py                 # Main Flask application
├── cli.py                 # Command-line interface
├── tiny_url_wm.py        # Legacy URL shortener CLI
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── CLAUDE.md             # Claude Code guidance
├── src/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── qr_generator.py    # QR code generation logic
│   │   └── url_shortener.py   # URL shortening logic
│   ├── templates/
│   │   └── index.html         # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css      # Styling
│       ├── js/
│       │   └── script.js      # JavaScript functionality
│       └── images/            # Example images
├── tests/                     # Test files (future)
├── docs/                      # Documentation (future)
└── venv/                      # Virtual environment
```

## Configuration

### Environment Variables

The application supports these environment variables:

- `SECRET_KEY`: Flask secret key (default: dev key)
- `PORT`: Port number (default: 8888)
- `DEBUG`: Debug mode (default: True)

### Production Deployment

For production deployment:

1. Set environment variables:
   ```bash
   export SECRET_KEY="your-secure-secret-key"
   export DEBUG="False"
   export PORT="80"
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

## API Endpoints

### Web Interface
- `GET /` - Main page with both tools
- `POST /generate-qr` - Generate QR code
- `POST /shorten-url` - Shorten URL

## Dependencies

- **Flask 3.1.1** - Web framework
- **Pillow 11.3.0** - Image processing
- **qrcode 8.2** - QR code generation

## Development

### Running Tests
```bash
# Tests will be added in future versions
python -m pytest tests/
```

### Code Structure
- `src/utils/qr_generator.py` - QR code generation logic
- `src/utils/url_shortener.py` - URL shortening logic
- `src/templates/index.html` - Web interface template
- `src/static/` - CSS, JavaScript, and images

## License

This project is provided as-is for utility purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Changelog

### v2.0.0
- Integrated QR code generator and URL shortener into single Flask app
- Added modern web interface with responsive design
- Created modular code structure
- Added CLI interface for both tools
- Improved error handling and user feedback