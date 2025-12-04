# 3D Holiday Sign - Gingerbread Project

Python scripts to create 3D printable holiday decorations including a holiday sign and a vintage gingerbread house.

## Features

### Holiday Sign
- Creates a rectangular sign base: **8 inches x 6 inches x 1 inch**
- Creates a separate "Happy Holidays" text piece for 3D printing
- Exports both pieces as STL files for 3D printing

### Vintage Gingerbread House
- Creates a complete vintage-style gingerbread house with **7 separate pieces**
- **4 Wall pieces**: Front (with door & windows), Back, Left Side, Right Side
- **3 Roof pieces**: Left roof panel, Right roof panel, Chimney
- Side walls feature peaked tops for the classic gingerbread house silhouette
- **Stylish arched windows and door** with rounded tops for a Victorian look
- **Interlocking tabs** for easy assembly without glue
- All pieces export as individual STL files for easy 3D printing

## Usage Options

### Gingerbread House (CadQuery)

Create a vintage-style gingerbread house with all pieces ready for 3D printing.

**Requirements:**
```bash
pip install cadquery-ocp cadquery numpy-stl matplotlib
```

**Run:**
```bash
python create_gingerbread_house.py
```

This will generate 7 STL files:
- `gingerbread_front_wall.stl` - Front wall with door and windows
- `gingerbread_back_wall.stl` - Back wall with window
- `gingerbread_left_side.stl` - Left side wall with peaked top
- `gingerbread_right_side.stl` - Right side wall with peaked top
- `gingerbread_roof_left.stl` - Left roof panel
- `gingerbread_roof_right.stl` - Right roof panel
- `gingerbread_chimney.stl` - Chimney piece

**Preview Images:**

The script also generates PNG preview images for each STL file for validation:
- `gingerbread_front_wall.png` - Preview of front wall (validates 1 door, 2 windows)
- `gingerbread_back_wall.png` - Preview of back wall
- `gingerbread_left_side.png` - Preview of left side wall
- `gingerbread_right_side.png` - Preview of right side wall
- `gingerbread_roof_left.png` - Preview of left roof panel
- `gingerbread_roof_right.png` - Preview of right roof panel
- `gingerbread_chimney.png` - Preview of chimney

**Validation:**

The script validates that the front wall has the required features:
- 1 door (centered, arched)
- 2 windows (left and right, arched)

### Holiday Sign - Standalone Script (CadQuery)

The standalone script uses CadQuery to generate STL files directly without needing FreeCAD.

**Requirements:**
```bash
pip install cadquery-ocp cadquery
```

**Run:**
```bash
python create_holiday_sign_standalone.py
```

This will generate:
- `sign_base.stl` - The 8x6x1 inch sign base
- `happy_holidays_text.stl` - The "Happy Holidays" text piece

### Holiday Sign - FreeCAD Script (Legacy)

If you prefer using FreeCAD, you can still use the original script.

**Requirements:**
- [FreeCAD](https://www.freecad.org/) (version 0.19 or later recommended)
- Python 3.x (included with FreeCAD)

**Run from FreeCAD GUI:**
1. Open FreeCAD
2. Go to **View → Panels → Python Console**
3. Run the following command:
   ```python
   exec(open("/path/to/create_holiday_sign.py").read())
   ```

**Run from Command Line:**
```bash
freecad -c create_holiday_sign.py
```

Or with the FreeCAD Python console:
```bash
freecadcmd create_holiday_sign.py
```

## Output Files

### Gingerbread House

| File | Description |
|------|-------------|
| `gingerbread_front_wall.stl` | Front wall (4in x 3in) with arched door and windows, interlocking tabs |
| `gingerbread_back_wall.stl` | Back wall (4in x 3in) with arched window, interlocking tabs |
| `gingerbread_left_side.stl` | Left side (3in x 4.5in) with peaked top, arched window, interlocking slots |
| `gingerbread_right_side.stl` | Right side (3in x 4.5in) with peaked top, arched window, interlocking slots |
| `gingerbread_roof_left.stl` | Left roof panel with overhang and tabs |
| `gingerbread_roof_right.stl` | Right roof panel with overhang and tabs |
| `gingerbread_chimney.stl` | Chimney (0.6in x 0.5in x 1in) |

### Holiday Sign

| File | Description |
|------|-------------|
| `sign_base.stl` | The 8x6x1 inch sign base for 3D printing |
| `happy_holidays_text.stl` | The "Happy Holidays" text piece for 3D printing |
| `holiday_sign.FCStd` | FreeCAD document (only with FreeCAD script) |

## Customization

### Gingerbread House

You can modify the following constants in `create_gingerbread_house.py`:

```python
# Wall dimensions (in inches)
WALL_THICKNESS = 0.15  # approx 4mm
HOUSE_WIDTH = 4.0      # front/back wall width
HOUSE_DEPTH = 3.0      # side wall depth
WALL_HEIGHT = 3.0      # wall height to roof line
PEAK_HEIGHT = 1.5      # height of roof peak above wall

# Door and window dimensions
DOOR_WIDTH = 0.8
DOOR_HEIGHT = 1.5
WINDOW_WIDTH = 0.6
WINDOW_HEIGHT = 0.6

# Arch settings (for rounded tops)
ARCH_SEGMENTS = 16     # number of segments for smooth arches

# Tab dimensions for interlocking pieces
TAB_WIDTH = 0.3        # width of each tab
TAB_DEPTH = 0.15       # how deep tabs extend
TAB_HEIGHT = 0.3       # height of each tab
TAB_TOLERANCE = 0.01   # clearance for fitting
```

### Holiday Sign

You can modify the following constants in `create_holiday_sign_standalone.py`:

```python
# Sign dimensions in inches
SIGN_WIDTH = 8.0   # inches
SIGN_HEIGHT = 6.0  # inches
SIGN_DEPTH = 1.0   # inches

# Text settings
TEXT_HEIGHT = 0.5  # inches (extrusion depth for text)
TEXT_FONT_SIZE = 1.0  # inches (approximate height of letters)
```

## 3D Printing Tips

### Gingerbread House

1. Print all wall pieces flat on the print bed
2. Side walls should be printed with the peaked edge facing up
3. Roof panels print flat - they will be angled during assembly
4. **Interlocking tabs**: Front/back wall tabs slide into side wall slots for easy assembly
5. Tabs allow assembly without glue - adjust TAB_TOLERANCE if fit is too tight or loose
6. Attach roof panels to the peaked edges of the side walls using the roof tabs
7. Place the chimney on one of the roof panels
8. Consider using brown/tan filament for an authentic gingerbread look
9. Add white icing details with a 3D pen or printed decorations

### Holiday Sign

1. Print the sign base flat on the print bed
2. Print the text piece with the letters facing up
3. Use different colors for visual contrast
4. The text piece can be glued or press-fitted onto the sign base

## License

This project is open source and available under the MIT License