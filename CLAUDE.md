# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python utility toolkit that provides QR code generation and Confluence URL shortening services through both a modern web interface and command-line tools.

**Main Components:**
1. **Flask Web Application** (`app.py`) - Unified web interface for both tools
2. **Command Line Interface** (`cli.py`) - Modern CLI for both QR generation and URL shortening
3. **Legacy CLI** (`tiny_url_wm.py`) - Original URL shortener command-line utility

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# For development dependencies
pip install -r requirements-dev.txt
```

### Running Applications

**Web Application (Primary Interface):**
```bash
python app.py
# Runs on http://127.0.0.1:8888 with both QR generation and URL shortening
```

**Modern CLI Interface:**
```bash
# QR Code generation
python cli.py qr --data "Hello World" --output qr.png

# URL shortening
python cli.py shorten --url "https://confluence.com/pages/123456"
```

**Legacy URL Shortener:**
```bash
python tiny_url_wm.py --full-url "https://example.com/pages/123456"
```

**SVG Checker Utility:**
```bash
python svg_checker.py --svg-file test_example.svg
```

### Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build

# Or with Docker directly
docker build -t utildocker .
docker run -p 8888:8888 utildocker
```

### Testing and Code Quality
```bash
# Run tests
python -m pytest tests/

# Run individual test files
python test_web_features.py
python test_ui_functionality.py

# Code formatting
black .
isort .

# Linting
flake8 .
```

## Architecture

### Modular Structure
The codebase is organized into a clean, modular structure:

- **`src/utils/`** - Core utility modules
  - `qr_generator.py` - QRCodeGenerator class with all QR code logic
  - `url_shortener.py` - URLShortener class with URL manipulation logic
  - `svg_color_validator.py` - SVGColorValidator class for SVG analysis
- **`src/templates/`** - HTML templates for the web interface
- **`src/static/`** - CSS, JavaScript, and images for the web interface
- **`config.py`** - Configuration management for different environments
- **`svg_checker.py`** - Standalone SVG color and thickness analyzer

### Web Application (`app.py`)
- Modern Flask application with proper error handling
- Responsive web interface with tabbed navigation
- Supports both QR code generation and URL shortening
- Uses modular utility classes for core functionality
- Proper file upload handling and security measures

### CLI Interface (`cli.py`)
- Comprehensive command-line interface using argparse
- Supports all features available in the web interface
- Proper error handling and help documentation
- Consistent with modern CLI design patterns

### Core Utilities
- **QRCodeGenerator**: Handles QR code creation with advanced styling options (module shapes, color masks, logo embedding)
- **URLShortener**: Manages Confluence URL shortening logic
- **SVGColorValidator**: Analyzes SVG files for color validation and shape analysis
- All utilities are designed to be reusable and testable

## Dependencies

**Production Dependencies:**
- Flask 3.1.1 - Web framework
- Pillow 11.3.0 - Image processing
- qrcode 8.2 - QR code generation with styling support
- lxml 6.0.0 - XML/SVG parsing
- webcolors 24.11.1 - Color validation
- requests 2.32.4 - HTTP requests
- playwright 1.53.0 - Web automation (for testing)

**Development Dependencies:**
- pytest - Testing framework
- pytest-flask - Flask testing utilities
- pytest-cov - Coverage reporting
- black - Code formatting
- flake8 - Code linting
- isort - Import sorting
- python-dotenv - Environment variables
- sphinx - Documentation generation

## Configuration

The application uses environment variables for configuration:
- `SECRET_KEY` - Flask secret key
- `DEBUG` - Debug mode (True/False)
- `PORT` - Application port (default: 8888)
- Logging is configured to output to both `app.log` and stdout

## Deployment

### Docker Support
The application includes Docker support with:
- `Dockerfile` - Multi-stage build for production
- `docker-compose.yml` - Development environment setup
- `Caddyfile` - Reverse proxy configuration

## File Structure

```
utildocker/
├── app.py                 # Main Flask application
├── cli.py                 # Modern CLI interface
├── tiny_url_wm.py        # Legacy URL shortener CLI
├── svg_checker.py         # SVG color and thickness analyzer
├── config.py             # Configuration management
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── Dockerfile            # Docker build configuration
├── docker-compose.yml    # Docker Compose setup
├── Caddyfile             # Reverse proxy configuration
├── README.md            # Project documentation
├── CLAUDE.md            # This file
├── src/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── qr_generator.py      # QR code generation logic
│   │   ├── url_shortener.py     # URL shortening logic
│   │   └── svg_color_validator.py # SVG validation logic
│   ├── templates/
│   │   └── index.html           # Main web interface
│   └── static/
│       ├── css/style.css        # Modern responsive styling
│       ├── js/script.js         # Interactive functionality
│       └── images/              # Example QR code images
├── tests/                       # Test files
├── docs/                        # Documentation
├── test_*.py                    # Integration test files
└── venv/                        # Virtual environment (not tracked)
```

## Development Guidelines

1. **Code Quality**: Use black for formatting, flake8 for linting, and isort for import organization
2. **Testing**: Add tests to the `tests/` directory using pytest; integration tests are in `test_*.py` files
3. **Configuration**: Use environment variables for configuration, never hardcode secrets
4. **Security**: Always validate user inputs, especially file uploads and URLs
5. **Documentation**: Update README.md and this file when adding new features
6. **Logging**: Application logs to both `app.log` and stdout with structured formatting

## Key Features

### QR Code Generation
- Supports PNG and SVG export formats
- Advanced styling options: module shapes (square, rounded, circle), color masks (solid, radial gradient, square gradient)
- Logo embedding with proper scaling and positioning
- Custom foreground/background colors and gradients

### URL Shortening
- Confluence URL shortening with automatic base URL detection
- Custom base URL support
- Pattern-based URL transformation

### SVG Analysis
- Color validation and extraction from SVG files
- Shape analysis (paths, rectangles, circles, etc.)
- Thickness measurement for vector elements
- Integration with web interface for SVG QR code validation