#!/usr/bin/env python
"""
Seed script to create local sample files (PDF and Image) and create Resource objects with them.
Run with: python seed_files.py
"""
import os
import sys
import django
from pathlib import Path
from io import BytesIO

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_hub.settings')
django.setup()

from django.core.files import File
from django.core.files.base import ContentFile
from resources.models import Resource


def create_sample_pdf():
    """Create a minimal valid PDF file."""
    # Minimal PDF content (1 page, empty)
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << >> /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 24 Tf 100 700 Td (Sample PDF for Campus Hub) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000204 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
298
%%EOF"""
    return ContentFile(pdf_content, name="sample_document.pdf")


def create_sample_png():
    """Create a minimal valid PNG file (1x1 red pixel)."""
    # Minimal PNG: 1x1 red pixel
    png_content = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D,  # IHDR chunk length
        0x49, 0x48, 0x44, 0x52,  # IHDR
        0x00, 0x00, 0x00, 0x01,  # Width: 1
        0x00, 0x00, 0x00, 0x01,  # Height: 1
        0x08, 0x02, 0x00, 0x00, 0x00,  # Bit depth, color type, compression, filter, interlace
        0x90, 0x77, 0x53, 0xDE,  # CRC
        0x00, 0x00, 0x00, 0x0C,  # IDAT chunk length
        0x49, 0x44, 0x41, 0x54,  # IDAT
        0x08, 0xD7, 0x63, 0xF8, 0x0F, 0x00, 0x01, 0x01, 0x00, 0x05, 0x00, 0x1D,  # Compressed data
        0x0B, 0xFC, 0x61, 0x05,  # CRC
        0x00, 0x00, 0x00, 0x00,  # IEND chunk length
        0x49, 0x45, 0x4E, 0x44,  # IEND
        0xAE, 0x42, 0x60, 0x82   # CRC
    ])
    return ContentFile(png_content, name="sample_image.png")


def create_sample_image_larger():
    """Create a larger sample PNG (100x100 with gradient)."""
    # Create a simple 100x100 PNG programmatically
    import struct
    import zlib
    
    width, height = 100, 100
    # Create raw image data (RGB, no alpha)
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter type 0 (None)
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = 128
            raw_data.extend([r, g, b])
    
    # Compress
    compressed = zlib.compress(raw_data)
    
    # PNG chunks
    def chunk(chunk_type, data):
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
    
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit, truecolor
    idat = compressed
    iend = b''
    
    png = (
        b'\x89PNG\r\n\x1a\n' +
        chunk(b'IHDR', ihdr) +
        chunk(b'IDAT', idat) +
        chunk(b'IEND', iend)
    )
    
    return ContentFile(png, name="sample_image.png")


def seed_files():
    # Define media resources directory
    media_root = Path(__file__).resolve().parent / 'media'
    resources_dir = media_root / 'resources'
    resources_dir.mkdir(parents=True, exist_ok=True)

    print("Creating sample PDF file...")
    pdf_file = create_sample_pdf()
    
    print("Creating sample PNG image...")
    png_file = create_sample_png()  # Small 1x1 pixel
    # Or use the larger one:
    # png_file = create_sample_image_larger()

    print("\nCreating resources with generated files...")

    # Create PDF resource
    pdf_resource = Resource.objects.create(
        title="Sample PDF Document - Campus Hub Preview",
        description="A sample PDF document generated locally for testing the PDF preview feature in Campus Resource Hub. This demonstrates the inline PDF viewer using iframe.",
        subject="Computer Science",
        semester=3,
        branch="CSE",
        resource_type="Reference Material",
        tags="pdf, sample, preview, test",
        is_featured=True,
    )
    pdf_resource.file.save("sample_document.pdf", pdf_file, save=True)
    print(f"  Created: {pdf_resource.title}")

    # Create Image resource
    image_resource = Resource.objects.create(
        title="Sample Image - Campus Hub Preview",
        description="A sample PNG image generated locally for testing the image preview feature. This demonstrates the inline image viewer.",
        subject="Design",
        semester=2,
        branch="AIE",
        resource_type="Study Material",
        tags="image, png, sample, preview, test",
        is_featured=True,
    )
    image_resource.file.save("sample_image.png", png_file, save=True)
    print(f"  Created: {image_resource.title}")

    print("\nFile seeding completed successfully!")
    print(f"Total resources: {Resource.objects.count()}")
    print(f"Resources with files: {Resource.objects.exclude(file='').count()}")


if __name__ == "__main__":
    seed_files()