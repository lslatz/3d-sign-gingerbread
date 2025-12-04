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

Features:
- Stylish arched windows and door with rounded tops
- Interlocking tabs for easy assembly without glue

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

# Arch dimensions (for rounded tops)
ARCH_SEGMENTS = 16     # number of segments for smooth arches

# Roof dimensions
ROOF_OVERHANG = 0.3    # inches (how far roof extends past walls)
ROOF_THICKNESS = 0.15  # inches

# Chimney dimensions
CHIMNEY_WIDTH = 0.6    # inches
CHIMNEY_DEPTH = 0.5    # inches
CHIMNEY_HEIGHT = 1.0   # inches

# Tab dimensions for interlocking pieces
TAB_WIDTH = 0.3        # inches (width of each tab)
TAB_DEPTH = 0.15       # inches (how deep tabs extend)
TAB_HEIGHT = 0.3       # inches (height of each tab)
TAB_TOLERANCE = 0.01   # inches (clearance for fitting)


def create_arched_opening(width, height, depth, arch_height=None):
    """
    Create an arched opening (rectangle with semicircular top).
    
    Args:
        width: Width of the opening in mm
        height: Total height of the opening in mm (including arch)
        depth: Depth/thickness of the opening in mm
        arch_height: Height of the arch portion (defaults to width/2 for semicircle)
    
    Returns:
        cq.Workplane: The arched opening shape
    """
    if arch_height is None:
        arch_height = width / 2  # Semicircular arch
    
    # Ensure arch height doesn't exceed total height
    if arch_height > height:
        arch_height = height
    
    # The rectangular portion height
    rect_height = max(0, height - arch_height)
    
    # Create the arched profile on XZ plane
    # Start from bottom-left, go around the arch
    points = []
    
    # Bottom left
    points.append((-width / 2, 0))
    # Top left (start of arch) - only add if there's a rectangular portion
    if rect_height > 0:
        points.append((-width / 2, rect_height))
    
    # Create arch points (semicircle from left to right)
    # Skip the first point (already added) and last point (will be added separately)
    for i in range(1, ARCH_SEGMENTS):
        angle = math.pi - (math.pi * i / ARCH_SEGMENTS)
        x = (width / 2) * math.cos(angle)
        z = rect_height + arch_height * math.sin(angle)
        points.append((x, z))
    
    # Top right (end of arch) - only add if there's a rectangular portion
    if rect_height > 0:
        points.append((width / 2, rect_height))
    # Bottom right
    points.append((width / 2, 0))
    
    # Create the shape
    opening = (
        cq.Workplane("XZ")
        .polyline(points)
        .close()
        .extrude(depth)
    )
    
    # Center the extrusion in Y
    opening = opening.translate((0, -depth / 2, 0))
    
    return opening


def create_tab(width, depth, height, is_slot=False):
    """
    Create a single tab or slot for interlocking pieces.
    
    Args:
        width: Width of the tab in mm
        depth: Depth of the tab in mm
        height: Height of the tab in mm
        is_slot: If True, add tolerance for fitting
    
    Returns:
        cq.Workplane: The tab shape
    """
    tolerance = TAB_TOLERANCE * INCH_TO_MM if is_slot else 0
    
    tab = cq.Workplane("XY").box(
        width + tolerance * 2,
        depth + tolerance * 2,
        height + tolerance * 2
    )
    
    return tab


def add_wall_tabs(wall, wall_width, wall_height, thickness, is_front_back=True):
    """
    Add interlocking tabs to a wall piece.
    
    For front/back walls: Add tabs on left and right edges (protruding outward)
    For side walls: Add slots at front and back edges to receive tabs from front/back walls
    
    Args:
        wall: The wall workplane
        wall_width: Width of the wall in mm
        wall_height: Height of the wall in mm  
        thickness: Wall thickness in mm
        is_front_back: True for front/back walls (tabs), False for side walls (slots)
    
    Returns:
        cq.Workplane: Wall with tabs/slots
    """
    tab_w = TAB_WIDTH * INCH_TO_MM
    tab_d = TAB_DEPTH * INCH_TO_MM
    tab_h = TAB_HEIGHT * INCH_TO_MM
    
    # Position tabs at 1/4 and 3/4 of wall height
    tab_positions_z = [wall_height * 0.25, wall_height * 0.75]
    
    if is_front_back:
        # Add protruding tabs on left and right edges
        for z_pos in tab_positions_z:
            # Left tab - protrudes outward from left edge
            left_tab = create_tab(tab_w, tab_d, tab_h, is_slot=False)
            left_tab = left_tab.translate((-wall_width / 2 - tab_d / 2, 0, z_pos))
            wall = wall.union(left_tab)
            
            # Right tab - protrudes outward from right edge
            right_tab = create_tab(tab_w, tab_d, tab_h, is_slot=False)
            right_tab = right_tab.translate((wall_width / 2 + tab_d / 2, 0, z_pos))
            wall = wall.union(right_tab)
    else:
        # Create slots at front and back edges of side walls
        # These slots cut into the wall edges where front/back walls connect
        for z_pos in tab_positions_z:
            # Front slot - at the +X edge of side wall
            front_slot = create_tab(tab_w, tab_d, tab_h, is_slot=True)
            front_slot = front_slot.translate((wall_width / 2, 0, z_pos))
            wall = wall.cut(front_slot)
            
            # Back slot - at the -X edge of side wall
            back_slot = create_tab(tab_w, tab_d, tab_h, is_slot=True)
            back_slot = back_slot.translate((-wall_width / 2, 0, z_pos))
            wall = wall.cut(back_slot)
    
    return wall


def add_roof_tabs(roof, roof_width, roof_length, thickness, side_wall_thickness):
    """
    Add tabs to roof panels for connecting to walls.
    
    Args:
        roof: The roof panel workplane
        roof_width: Width of the roof in mm
        roof_length: Length of the roof in mm
        thickness: Roof thickness in mm
        side_wall_thickness: Thickness of side walls in mm
    
    Returns:
        cq.Workplane: Roof with tabs
    """
    tab_w = TAB_WIDTH * INCH_TO_MM
    tab_d = TAB_DEPTH * INCH_TO_MM
    tab_h = TAB_HEIGHT * INCH_TO_MM
    
    # Add tabs on the bottom edge (along the length) for connecting to walls
    # Position tabs at 1/4 and 3/4 of the width
    tab_positions_x = [-roof_width * 0.25, roof_width * 0.25]
    
    for x_pos in tab_positions_x:
        # Tab on one side - create_tab(width, depth, height)
        tab = create_tab(tab_w, tab_d, tab_h, is_slot=False)
        tab = tab.translate((x_pos, -roof_length / 2 - tab_d / 2, -thickness / 2 - tab_h / 2))
        roof = roof.union(tab)
    
    return roof


def create_front_wall():
    """
    Create the front wall with an arched door cutout and stylish arched windows.
    Includes interlocking tabs on left and right edges.
    
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
    
    # Cut arched door opening (centered horizontally, at bottom)
    door_cutout = create_arched_opening(door_w, door_h, thickness + 1)
    door_cutout = door_cutout.translate((0, 0, door_off))
    wall = wall.cut(door_cutout)
    
    # Cut left arched window
    left_window = create_arched_opening(window_w, window_h, thickness + 1)
    left_window = left_window.translate((-width/3, 0, window_off))
    wall = wall.cut(left_window)
    
    # Cut right arched window
    right_window = create_arched_opening(window_w, window_h, thickness + 1)
    right_window = right_window.translate((width/3, 0, window_off))
    wall = wall.cut(right_window)
    
    # Add interlocking tabs
    wall = add_wall_tabs(wall, width, height, thickness, is_front_back=True)
    
    return wall


def create_back_wall():
    """
    Create the back wall with a stylish arched window.
    Includes interlocking tabs on left and right edges.
    
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
    
    # Cut center arched window
    center_window = create_arched_opening(window_w, window_h, thickness + 1)
    center_window = center_window.translate((0, 0, window_off))
    wall = wall.cut(center_window)
    
    # Add interlocking tabs
    wall = add_wall_tabs(wall, width, height, thickness, is_front_back=True)
    
    return wall


def create_side_wall():
    """
    Create a side wall with peaked top for the roof and arched window.
    Includes interlocking slots on front and back edges to receive tabs from front/back walls.
    
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
    
    # Cut arched window
    window = create_arched_opening(window_w, window_h, thickness + 1)
    window = window.translate((0, 0, window_off))
    wall = wall.cut(window)
    
    # Add interlocking slots (to receive tabs from front/back walls)
    wall = add_wall_tabs(wall, depth, height, thickness, is_front_back=False)
    
    return wall


def create_roof_panel():
    """
    Create a single roof panel with interlocking tabs.
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
    side_wall_thickness = WALL_THICKNESS * INCH_TO_MM
    
    # Calculate roof panel length (hypotenuse of the triangle)
    roof_length = math.sqrt(depth ** 2 + peak ** 2) + overhang
    
    # Roof is wider than house for overhang
    roof_width = width + (2 * overhang)
    
    # Create flat roof panel
    roof = cq.Workplane("XY").box(roof_width, roof_length, thickness)
    
    # Move roof so bottom edge is at Z=0 (will be positioned during assembly)
    roof = roof.translate((0, 0, thickness / 2))
    
    # Add interlocking tabs
    roof = add_roof_tabs(roof, roof_width, roof_length, thickness, side_wall_thickness)
    
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
    print("\nFeatures:")
    print("  - Stylish arched windows and door with rounded tops")
    print("  - Interlocking tabs for easy assembly")
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
    print(f"    1. Front Wall    - {HOUSE_WIDTH}in x {WALL_HEIGHT}in (with arched door & windows, tabs)")
    print(f"    2. Back Wall     - {HOUSE_WIDTH}in x {WALL_HEIGHT}in (with arched window, tabs)")
    print(f"    3. Left Side     - {HOUSE_DEPTH}in x {WALL_HEIGHT + PEAK_HEIGHT}in (peaked, with slots)")
    print(f"    4. Right Side    - {HOUSE_DEPTH}in x {WALL_HEIGHT + PEAK_HEIGHT}in (peaked, with slots)")
    print("\n  ROOF (3 pieces):")
    print(f"    5. Left Roof     - Angled panel with overhang and tabs")
    print(f"    6. Right Roof    - Angled panel with overhang and tabs")
    print(f"    7. Chimney       - {CHIMNEY_WIDTH}in x {CHIMNEY_DEPTH}in x {CHIMNEY_HEIGHT}in")
    print("\nAll STL files are ready for 3D printing!")
    print("\nAssembly Tips:")
    print("  - Print walls flat on the print bed")
    print("  - Tabs on front/back walls slide into slots on side walls")
    print("  - Roof panels attach at the peaked edges of side walls")
    print("  - Chimney sits on one of the roof panels")
    print("  - Interlocking tabs allow assembly without glue!")


if __name__ == "__main__":
    main()
