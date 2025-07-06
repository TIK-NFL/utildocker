#!/usr/bin/env python3
"""
Command-line interface for utility tools.
Provides CLI access to QR code generation and URL shortening.
"""

import argparse
import sys
import os
from PIL import Image

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import QRCodeGenerator, URLShortener


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Utility Tools CLI - QR Code Generator & URL Shortener",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate QR code
  %(prog)s qr --data "Hello World" --output qr.png
  
  # Generate QR code with logo
  %(prog)s qr --data "https://example.com" --logo logo.png --output qr.png
  
  # Shorten Confluence URL
  %(prog)s shorten --url "https://confluence.com/pages/123456"
  
  # Shorten URL with custom base
  %(prog)s shorten --url "https://conf.com/pages/123" --base "https://short.com"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # QR Code generation subcommand
    qr_parser = subparsers.add_parser('qr', help='Generate QR codes')
    qr_parser.add_argument('--data', '-d', required=True, help='Data to encode in QR code')
    qr_parser.add_argument('--output', '-o', required=True, help='Output file path')
    qr_parser.add_argument('--logo', '-l', help='Logo image file to embed')
    qr_parser.add_argument('--format', '-f', choices=['png', 'svg'], default='png', help='Output format')
    qr_parser.add_argument('--style', '-s', choices=['square', 'rounded', 'circle'], default='square', help='Module style')
    qr_parser.add_argument('--color', '-c', choices=['solid', 'radial', 'square'], default='solid', help='Color mask')
    
    # URL shortening subcommand
    url_parser = subparsers.add_parser('shorten', help='Shorten Confluence URLs')
    url_parser.add_argument('--url', '-u', required=True, help='Full Confluence URL to shorten')
    url_parser.add_argument('--base', '-b', help='Custom base URL for shortened link')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'qr':
            generate_qr_cli(args)
        elif args.command == 'shorten':
            shorten_url_cli(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def generate_qr_cli(args):
    """Generate QR code via CLI."""
    qr_generator = QRCodeGenerator()
    
    # Load logo if provided
    logo_image = None
    if args.logo:
        try:
            logo_image = Image.open(args.logo)
        except Exception as e:
            raise ValueError(f"Could not load logo image: {e}")
    
    # Generate QR code
    buf, mimetype, _ = qr_generator.generate_qr_code(
        data=args.data,
        export_format=args.format,
        module_drawer=args.style,
        color_mask=args.color,
        logo_image=logo_image
    )
    
    # Save to file
    with open(args.output, 'wb') as f:
        f.write(buf.read())
    
    print(f"QR code generated: {args.output}")


def shorten_url_cli(args):
    """Shorten URL via CLI."""
    url_shortener = URLShortener()
    
    try:
        short_url = url_shortener.shorten_url(args.url, args.base)
        print(short_url)
    except ValueError as e:
        raise ValueError(f"Invalid URL: {e}")


if __name__ == '__main__':
    main()