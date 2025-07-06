"""QR Code generation utilities."""

import qrcode
from PIL import Image
import io
import datetime
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask
from qrcode.image.svg import SvgImage


class QRCodeGenerator:
    """Handles QR code generation with various styling options."""
    
    def __init__(self):
        self.version = 1
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.box_size = 10
        self.border = 4
    
    def generate_qr_code(self, data, export_format='png', module_drawer='square', 
                        color_mask='solid', logo_image=None):
        """
        Generate a QR code with the specified parameters.
        
        Args:
            data (str): The data to encode in the QR code
            export_format (str): 'png' or 'svg'
            module_drawer (str): 'square', 'rounded', or 'circle'
            color_mask (str): 'solid', 'radial', or 'square'
            logo_image (PIL.Image): Optional logo to embed in the QR code
            
        Returns:
            tuple: (BytesIO buffer, mimetype, filename)
        """
        # Create QR code object
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Select image factory
        if export_format == 'svg':
            image_factory = SvgImage
        else:
            image_factory = StyledPilImage
        
        # Select module drawer
        drawer = None
        if module_drawer == 'rounded':
            drawer = RoundedModuleDrawer()
        elif module_drawer == 'circle':
            drawer = CircleModuleDrawer()
        
        # Select color mask
        mask = None
        if color_mask == 'radial':
            mask = RadialGradiantColorMask()
        elif color_mask == 'square':
            mask = SquareGradiantColorMask()
        
        # Create QR code image
        if export_format == 'svg':
            # SVG format has limited styling support
            # Try to apply styling if supported, fallback to basic SVG
            try:
                kwargs = {'image_factory': image_factory}
                # SVG format doesn't support all styling options
                # We can still try basic generation with some options
                qr_img = qr.make_image(**kwargs)
            except Exception:
                # Fallback to basic SVG generation
                qr_img = qr.make_image(image_factory=image_factory)
        else:
            # Only pass drawer and mask if they are not None
            kwargs = {'image_factory': image_factory}
            if drawer is not None:
                kwargs['module_drawer'] = drawer
            if mask is not None:
                kwargs['color_mask'] = mask
            qr_img = qr.make_image(**kwargs)
            
            # Add logo if provided
            if logo_image:
                logo_size = 50
                logo_image.thumbnail((logo_size, logo_size))
                pos = ((qr_img.size[0] - logo_image.size[0]) // 2, 
                       (qr_img.size[1] - logo_image.size[1]) // 2)
                qr_img.paste(logo_image, pos)
        
        # Save to buffer
        buf = io.BytesIO()
        if export_format == 'svg':
            qr_img.save(buf)
            mimetype = 'image/svg+xml'
        else:
            qr_img.save(buf, format='PNG')
            mimetype = 'image/png'
        buf.seek(0)
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_qrcode.{export_format}"
        
        return buf, mimetype, filename