#!/usr/bin/env python3
"""
Vintage Gingerbread House Creator

This script uses CadQuery to create a vintage gingerbread house with
individual pieces that can be 3D printed and assembled.

Pieces included:
- 4 Wall pieces: Front (with door), Back, Left Side, Right Side
- 3 Roof pieces: Left roof panel, Right roof panel, Chimney

The design is inspired by traditional Victorian-era gingerbread houses
with characteristic peaked roofs and decorative elements.

Requirements:
    pip install cadquery-ocp cadquery

Usage:
    python create_gingerbread_house.py
"""

import cadquery as cq
import math
import os

# Conversion factor: 1 inch = 25.4 mm
INCH_TO_MM = 25.4

# ============================================
# HOUSE DIMENSIONS (in inches)
# ============================================

# Wall dimensions
WALL_THICKNESS = 0.15  # inches (approx 4mm)
HOUSE_WIDTH = 4.0      # inches (front/back wall width)
HOUSE_DEPTH = 3.0      # inches (side wall depth)
WALL_HEIGHT = 3.0      # inches (wall height to roof line)
PEAK_HEIGHT = 1.5      # inches (height of roof peak above wall)

# Door and window dimensions
DOOR_WIDTH = 0.8       # inches
DOOR_HEIGHT = 1.5      # inches
DOOR_OFFSET_Y = 0.1    # inches (from bottom of wall)

WINDOW_WIDTH = 0.6     # inches
WINDOW_HEIGHT = 0.6    # inches
WINDOW_OFFSET_Y = 1.2  # inches (from bottom of wall)

# Roof dimensions
ROOF_OVERHANG = 0.3    # inches (how far roof extends past walls)
ROOF_THICKNESS = 0.15  # inches

# Chimney dimensions
CHIMNEY_WIDTH = 0.6    # inches
CHIMNEY_DEPTH = 0.5    # inches
CHIMNEY_HEIGHT = 1.0   # inches


def create_front_wall():
    """
    Create the front wall with a door cutout and decorative window.
    
    Returns:
        cq.Workplane: The front wall piece
    """
    # Convert to mm
    width = HOUSE_WIDTH * INCH_TO_MM
    height = WALL_HEIGHT * INCH_TO_MM
    thickness = WALL_THICKNESS * INCH_TO_MM
    door_w = DOOR_WIDTH * INCH_TO_MM
    door_h = DOOR_HEIGHT * INCH_TO_MM
    door_off = DOOR_OFFSET_Y * INCH_TO_MM
    window_w = WINDOW_WIDTH * INCH_TO_MM
    window_h = WINDOW_HEIGHT * INCH_TO_MM
    window_off = WINDOW_OFFSET_Y * INCH_TO_MM
    
    # Create base wall
    wall = cq.Workplane("XY").box(width, thickness, height)
    
    # Move wall so bottom is at Z=0
    wall = wall.translate((0, 0, height / 2))
    
    # Cut door opening (centered horizontally, at bottom)
    door_cutout = (
        cq.Workplane("XY")
        .box(door_w, thickness + 1, door_h)
        .translate((0, 0, door_off + door_h / 2))
    )
    wall = wall.cut(door_cutout)
    
    # Cut left window
    left_window = (
        cq.Workplane("XY")
        .box(window_w, thickness + 1, window_h)
        .translate((-width/3, 0, window_off + window_h / 2))
    )
    wall = wall.cut(left_window)
    
    # Cut right window
    right_window = (
        cq.Workplane("XY")
        .box(window_w, thickness + 1, window_h)
        .translate((width/3, 0, window_off + window_h / 2))
    )
    wall = wall.cut(right_window)
    
    return wall


def create_back_wall():
    """
    Create the back wall with decorative windows.
    
    Returns:
        cq.Workplane: The back wall piece
    """
    # Convert to mm
    width = HOUSE_WIDTH * INCH_TO_MM
    height = WALL_HEIGHT * INCH_TO_MM
    thickness = WALL_THICKNESS * INCH_TO_MM
    window_w = WINDOW_WIDTH * INCH_TO_MM
    window_h = WINDOW_HEIGHT * INCH_TO_MM
    window_off = WINDOW_OFFSET_Y * INCH_TO_MM
    
    # Create base wall
    wall = cq.Workplane("XY").box(width, thickness, height)
    
    # Move wall so bottom is at Z=0
    wall = wall.translate((0, 0, height / 2))
    
    # Cut center window
    center_window = (
        cq.Workplane("XY")
        .box(window_w, thickness + 1, window_h)
        .translate((0, 0, window_off + window_h / 2))
    )
    wall = wall.cut(center_window)
    
    return wall


def create_side_wall():
    """
    Create a side wall with peaked top for the roof.
    The peaked shape allows the roof to sit at an angle.
    
    Returns:
        cq.Workplane: The side wall piece
    """
    # Convert to mm
    depth = HOUSE_DEPTH * INCH_TO_MM
    height = WALL_HEIGHT * INCH_TO_MM
    peak = PEAK_HEIGHT * INCH_TO_MM
    thickness = WALL_THICKNESS * INCH_TO_MM
    window_w = WINDOW_WIDTH * INCH_TO_MM
    window_h = WINDOW_HEIGHT * INCH_TO_MM
    window_off = WINDOW_OFFSET_Y * INCH_TO_MM
    
    # Create pentagon shape for side wall (rectangle + triangle peak)
    # Points: bottom-left, bottom-right, top-right, peak, top-left
    points = [
        (-depth / 2, 0),
        (depth / 2, 0),
        (depth / 2, height),
        (0, height + peak),
        (-depth / 2, height),
    ]
    
    # Create the wall from the pentagon profile
    wall = (
        cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(thickness)
    )
    
    # Center the extrusion in Y
    wall = wall.translate((0, -thickness / 2, 0))
    
    # Cut window
    window = (
        cq.Workplane("XY")
        .box(window_w, thickness + 1, window_h)
        .translate((0, 0, window_off + window_h / 2))
    )
    wall = wall.cut(window)
    
    return wall


def create_roof_panel():
    """
    Create a single roof panel.
    Two of these make up the main roof.
    
    Returns:
        cq.Workplane: The roof panel piece
    """
    # Convert to mm
    width = HOUSE_WIDTH * INCH_TO_MM
    peak = PEAK_HEIGHT * INCH_TO_MM
    depth = (HOUSE_DEPTH / 2) * INCH_TO_MM
    overhang = ROOF_OVERHANG * INCH_TO_MM
    thickness = ROOF_THICKNESS * INCH_TO_MM
    
    # Calculate roof panel length (hypotenuse of the triangle)
    roof_length = math.sqrt(depth ** 2 + peak ** 2) + overhang
    
    # Roof is wider than house for overhang
    roof_width = width + (2 * overhang)
    
    # Create flat roof panel
    roof = cq.Workplane("XY").box(roof_width, roof_length, thickness)
    
    # Move roof so bottom edge is at Z=0 (will be positioned during assembly)
    roof = roof.translate((0, 0, thickness / 2))
    
    return roof


def create_chimney():
    """
    Create a chimney piece for the roof.
    
    Returns:
        cq.Workplane: The chimney piece
    """
    # Convert to mm
    width = CHIMNEY_WIDTH * INCH_TO_MM
    depth = CHIMNEY_DEPTH * INCH_TO_MM
    height = CHIMNEY_HEIGHT * INCH_TO_MM
    wall_thick = WALL_THICKNESS * INCH_TO_MM / 2  # Thinner walls for chimney
    
    # Create outer box
    outer = cq.Workplane("XY").box(width, depth, height)
    
    # Create inner hollow
    inner = cq.Workplane("XY").box(
        width - 2 * wall_thick,
        depth - 2 * wall_thick,
        height + 1  # Slightly taller to ensure complete cutout
    )
    
    # Hollow out the chimney
    chimney = outer.cut(inner)
    
    # Move so bottom is at Z=0
    chimney = chimney.translate((0, 0, height / 2))
    
    return chimney


def export_piece(piece, filename, script_dir):
    """
    Export a piece to STL file.
    
    Args:
        piece: CadQuery workplane object
        filename: Name of the output file
        script_dir: Directory to save the file
    """
    filepath = os.path.join(script_dir, filename)
    cq.exporters.export(piece, filepath)
    print(f"  Exported: {filename}")
    return filepath


def main():
    """
    Main function to create all gingerbread house pieces and export to STL.
    """
    # Get the directory of the script for export
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    
    print("=" * 60)
    print("Vintage Gingerbread House Creator")
    print("=" * 60)
    print("\nCreating gingerbread house pieces...")
    print(f"\nHouse dimensions: {HOUSE_WIDTH}in x {HOUSE_DEPTH}in x {WALL_HEIGHT + PEAK_HEIGHT}in")
    print(f"Wall thickness: {WALL_THICKNESS}in")
    print()
    
    # Create all pieces
    print("Creating wall pieces...")
    front_wall = create_front_wall()
    back_wall = create_back_wall()
    left_side = create_side_wall()
    right_side = create_side_wall()  # Same as left, will be mirrored during assembly
    
    print("Creating roof pieces...")
    roof_left = create_roof_panel()
    roof_right = create_roof_panel()  # Same as left panel
    chimney = create_chimney()
    
    # Export all pieces
    print("\nExporting STL files...")
    export_piece(front_wall, "gingerbread_front_wall.stl", script_dir)
    export_piece(back_wall, "gingerbread_back_wall.stl", script_dir)
    export_piece(left_side, "gingerbread_left_side.stl", script_dir)
    export_piece(right_side, "gingerbread_right_side.stl", script_dir)
    export_piece(roof_left, "gingerbread_roof_left.stl", script_dir)
    export_piece(roof_right, "gingerbread_roof_right.stl", script_dir)
    export_piece(chimney, "gingerbread_chimney.stl", script_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("Gingerbread House Creation Complete!")
    print("=" * 60)
    print("\nPieces created (7 total):")
    print("\n  WALLS (4 pieces):")
    print(f"    1. Front Wall    - {HOUSE_WIDTH}in x {WALL_HEIGHT}in (with door & windows)")
    print(f"    2. Back Wall     - {HOUSE_WIDTH}in x {WALL_HEIGHT}in (with window)")
    print(f"    3. Left Side     - {HOUSE_DEPTH}in x {WALL_HEIGHT + PEAK_HEIGHT}in (peaked)")
    print(f"    4. Right Side    - {HOUSE_DEPTH}in x {WALL_HEIGHT + PEAK_HEIGHT}in (peaked)")
    print("\n  ROOF (3 pieces):")
    print(f"    5. Left Roof     - Angled panel with overhang")
    print(f"    6. Right Roof    - Angled panel with overhang")
    print(f"    7. Chimney       - {CHIMNEY_WIDTH}in x {CHIMNEY_DEPTH}in x {CHIMNEY_HEIGHT}in")
    print("\nAll STL files are ready for 3D printing!")
    print("\nAssembly Tips:")
    print("  - Print walls flat on the print bed")
    print("  - Glue side walls to front/back walls at 90 degrees")
    print("  - Roof panels attach at the peaked edges of side walls")
    print("  - Chimney sits on one of the roof panels")


if __name__ == "__main__":
    main()
