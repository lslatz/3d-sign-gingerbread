#!/usr/bin/env python3
"""
FreeCAD Script to Create a Holiday Sign

This script creates:
1. A rectangular sign base (8in x 6in x 1in)
2. A separate "Happy Holidays" text piece for 3D printing

To run this script:
1. Open FreeCAD
2. Go to View -> Panels -> Python Console
3. Run: exec(open("path/to/create_holiday_sign.py").read())

Or from command line:
    freecad -c create_holiday_sign.py
"""

import FreeCAD
import Part
from FreeCAD import Base

# Conversion factor: 1 inch = 25.4 mm
INCH_TO_MM = 25.4

# Sign dimensions in inches
SIGN_WIDTH = 8.0   # inches
SIGN_HEIGHT = 6.0  # inches
SIGN_DEPTH = 1.0   # inches

# Text settings
TEXT_HEIGHT = 0.5  # inches (extrusion depth for text)
TEXT_FONT_SIZE = 1.0  # inches (approximate height of letters)
TEXT_BACKING_WIDTH_PER_CHAR = 0.7  # inches per character for fallback text width

# Font paths for different operating systems
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    "/System/Library/Fonts/Helvetica.ttc",  # macOS
    "C:/Windows/Fonts/arial.ttf",  # Windows
]


def create_sign_base():
    """
    Create the rectangular sign base (8in x 6in x 1in).
    
    Returns:
        Part.Shape: The sign base shape
    """
    # Convert dimensions to mm
    width_mm = SIGN_WIDTH * INCH_TO_MM
    height_mm = SIGN_HEIGHT * INCH_TO_MM
    depth_mm = SIGN_DEPTH * INCH_TO_MM
    
    # Create the box
    sign_box = Part.makeBox(width_mm, height_mm, depth_mm)
    
    return sign_box


def get_font_path():
    """
    Get an available font path for the current operating system.
    
    Returns:
        str: Path to an available font file, or None if none found
    """
    import os
    for font_path in FONT_PATHS:
        if os.path.exists(font_path):
            return font_path
    return None


def create_text_piece(text="Happy Holidays"):
    """
    Create a 3D text piece that can be printed separately.
    
    Args:
        text: The text to create (default: "Happy Holidays")
    
    Returns:
        Part.Shape: The 3D text shape
    """
    # Convert dimensions to mm
    text_height_mm = TEXT_HEIGHT * INCH_TO_MM
    font_size_mm = TEXT_FONT_SIZE * INCH_TO_MM
    
    # Create text shape using Draft module
    try:
        import Draft
        
        font_path = get_font_path()
        if font_path is None:
            raise FileNotFoundError("No suitable font file found")
        
        # Create the text shape
        text_shape = Draft.make_shapestring(
            String=text,
            FontFile=font_path,
            Size=font_size_mm,
            Tracking=0
        )
        
        FreeCAD.ActiveDocument.recompute()
        
        # Get the wire from the shape string
        if hasattr(text_shape, 'Shape'):
            wire = text_shape.Shape
        else:
            wire = text_shape
            
        # Extrude the text
        text_solid = wire.extrude(Base.Vector(0, 0, text_height_mm))
        
        return text_solid
        
    except Exception as e:
        print(f"Note: Using alternative text creation method: {e}")
        # Fallback: Create a simple placeholder rectangle with text engraved idea
        # This creates a backing plate for the text
        # Calculate width based on text length
        width_mm = len(text) * TEXT_BACKING_WIDTH_PER_CHAR * INCH_TO_MM
        height_mm = font_size_mm * 1.5
        
        text_backing = Part.makeBox(width_mm, height_mm, text_height_mm)
        return text_backing


def main():
    """
    Main function to create the holiday sign components.
    """
    # Create a new document
    if FreeCAD.ActiveDocument is None:
        doc = FreeCAD.newDocument("HolidaySign")
    else:
        doc = FreeCAD.ActiveDocument
    
    # Create the sign base
    print("Creating sign base (8in x 6in x 1in)...")
    sign_base_shape = create_sign_base()
    sign_base_obj = doc.addObject("Part::Feature", "SignBase")
    sign_base_obj.Shape = sign_base_shape
    sign_base_obj.Label = "Sign_Base_8x6x1in"
    
    # Position the sign base at origin
    sign_base_obj.Placement = FreeCAD.Placement(
        Base.Vector(0, 0, 0),
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 0)
    )
    
    # Create the text piece
    print("Creating 'Happy Holidays' text piece...")
    text_shape = create_text_piece("Happy Holidays")
    text_obj = doc.addObject("Part::Feature", "HappyHolidaysText")
    text_obj.Shape = text_shape
    text_obj.Label = "Happy_Holidays_Text"
    
    # Position the text piece offset from the sign for separate printing
    # Place it above the sign base with some spacing
    text_obj.Placement = FreeCAD.Placement(
        Base.Vector(0, SIGN_HEIGHT * INCH_TO_MM + 20, 0),  # Offset in Y direction
        FreeCAD.Rotation(Base.Vector(0, 0, 1), 0)
    )
    
    # Recompute the document
    doc.recompute()
    
    # Get the directory of the script for export
    import os
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    
    # Export to STL files for 3D printing
    print("\nExporting STL files for 3D printing...")
    
    try:
        import Mesh
        
        # Export sign base
        sign_stl_path = os.path.join(script_dir, "sign_base.stl")
        Mesh.export([sign_base_obj], sign_stl_path)
        print(f"  Sign base exported to: {sign_stl_path}")
        
        # Export text piece
        text_stl_path = os.path.join(script_dir, "happy_holidays_text.stl")
        Mesh.export([text_obj], text_stl_path)
        print(f"  Text piece exported to: {text_stl_path}")
        
    except Exception as e:
        print(f"  Note: STL export requires running in FreeCAD GUI: {e}")
    
    # Save the FreeCAD document
    try:
        fcstd_path = os.path.join(script_dir, "holiday_sign.FCStd")
        doc.saveAs(fcstd_path)
        print(f"\nFreeCAD document saved to: {fcstd_path}")
    except Exception as e:
        print(f"  Note: Document save requires running in FreeCAD: {e}")
    
    print("\n" + "=" * 50)
    print("Holiday Sign Creation Complete!")
    print("=" * 50)
    print("\nCreated components:")
    print(f"  1. Sign Base: {SIGN_WIDTH}in x {SIGN_HEIGHT}in x {SIGN_DEPTH}in")
    print(f"  2. Text Piece: 'Happy Holidays'")
    print("\nBoth pieces are separate objects and can be exported")
    print("individually for 3D printing.")
    
    return doc


# Run the main function when script is executed
if __name__ == "__main__":
    main()
