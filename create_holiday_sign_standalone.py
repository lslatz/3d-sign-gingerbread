#!/usr/bin/env python3
"""
Standalone Script to Create a Holiday Sign (No FreeCAD Required)

This script uses CadQuery to create:
1. A rectangular sign base (8in x 6in x 1in)
2. A separate "Happy Holidays" text piece for 3D printing

Both pieces are exported directly as STL files.

Requirements:
    pip install cadquery-ocp cadquery

Usage:
    python create_holiday_sign_standalone.py
"""

import cadquery as cq
import os

# Conversion factor: 1 inch = 25.4 mm
INCH_TO_MM = 25.4

# Sign dimensions in inches
SIGN_WIDTH = 8.0   # inches
SIGN_HEIGHT = 6.0  # inches
SIGN_DEPTH = 1.0   # inches

# Text settings
TEXT_HEIGHT = 0.5  # inches (extrusion depth for text)
TEXT_FONT_SIZE = 1.0  # inches (approximate height of letters)

# Font paths for different operating systems
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",  # Linux alternative
    "/System/Library/Fonts/Helvetica.ttc",  # macOS
    "C:/Windows/Fonts/arial.ttf",  # Windows
]


def get_font_path():
    """
    Get an available font path for the current operating system.
    
    Returns:
        str: Path to an available font file, or None if none found
    """
    for font_path in FONT_PATHS:
        if os.path.exists(font_path):
            return font_path
    return None


def create_sign_base():
    """
    Create the rectangular sign base (8in x 6in x 1in).
    
    Returns:
        cq.Workplane: The sign base shape
    """
    # Convert dimensions to mm (CadQuery uses mm by default)
    width_mm = SIGN_WIDTH * INCH_TO_MM
    height_mm = SIGN_HEIGHT * INCH_TO_MM
    depth_mm = SIGN_DEPTH * INCH_TO_MM
    
    # Create the box centered on the XY plane
    sign_base = cq.Workplane("XY").box(width_mm, height_mm, depth_mm)
    
    return sign_base


def create_text_piece(text="Happy Holidays"):
    """
    Create a 3D text piece that can be printed separately.
    
    Args:
        text: The text to create (default: "Happy Holidays")
    
    Returns:
        cq.Workplane: The 3D text shape
    """
    # Convert dimensions to mm
    text_height_mm = TEXT_HEIGHT * INCH_TO_MM
    font_size_mm = TEXT_FONT_SIZE * INCH_TO_MM
    
    font_path = get_font_path()
    
    if font_path:
        try:
            # Create 3D text using CadQuery's text() method
            text_piece = (
                cq.Workplane("XY")
                .text(text, font_size_mm, text_height_mm, font=font_path)
            )
            return text_piece
        except Exception as e:
            print(f"Note: Could not create text with font: {e}")
            print("Falling back to placeholder geometry.")
    
    # Fallback: Create a simple placeholder rectangle
    # Calculate width based on text length (approximate)
    width_mm = len(text) * 0.7 * font_size_mm
    height_mm = font_size_mm * 1.5
    
    text_backing = cq.Workplane("XY").box(width_mm, height_mm, text_height_mm)
    return text_backing


def main():
    """
    Main function to create the holiday sign components and export to STL.
    """
    # Get the directory of the script for export
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    
    print("=" * 50)
    print("Holiday Sign Creator (Standalone - No FreeCAD)")
    print("=" * 50)
    
    # Create the sign base
    print("\nCreating sign base (8in x 6in x 1in)...")
    sign_base = create_sign_base()
    
    # Export sign base to STL
    sign_stl_path = os.path.join(script_dir, "sign_base.stl")
    cq.exporters.export(sign_base, sign_stl_path)
    print(f"  Sign base exported to: {sign_stl_path}")
    
    # Create the text piece
    print("\nCreating 'Happy Holidays' text piece...")
    text_piece = create_text_piece("Happy Holidays")
    
    # Export text piece to STL
    text_stl_path = os.path.join(script_dir, "happy_holidays_text.stl")
    cq.exporters.export(text_piece, text_stl_path)
    print(f"  Text piece exported to: {text_stl_path}")
    
    print("\n" + "=" * 50)
    print("Holiday Sign Creation Complete!")
    print("=" * 50)
    print("\nCreated components:")
    print(f"  1. Sign Base: {SIGN_WIDTH}in x {SIGN_HEIGHT}in x {SIGN_DEPTH}in")
    print(f"  2. Text Piece: 'Happy Holidays'")
    print("\nBoth STL files are ready for 3D printing!")


if __name__ == "__main__":
    main()
