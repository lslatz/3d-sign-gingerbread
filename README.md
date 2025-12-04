# 3D Holiday Sign - Gingerbread Project

Python scripts to create a 3D printable holiday sign with a "Happy Holidays" text piece.

## Features

- Creates a rectangular sign base: **8 inches x 6 inches x 1 inch**
- Creates a separate "Happy Holidays" text piece for 3D printing
- Exports both pieces as STL files for 3D printing

## Usage Options

### Option 1: Standalone Script (Recommended - No FreeCAD Required)

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

### Option 2: FreeCAD Script (Legacy)

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

After running either script, you will get:

| File | Description |
|------|-------------|
| `sign_base.stl` | The 8x6x1 inch sign base for 3D printing |
| `happy_holidays_text.stl` | The "Happy Holidays" text piece for 3D printing |
| `holiday_sign.FCStd` | FreeCAD document (only with FreeCAD script) |

## Customization

You can modify the following constants in either script:

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

1. Print the sign base flat on the print bed
2. Print the text piece with the letters facing up
3. Use different colors for visual contrast
4. The text piece can be glued or press-fitted onto the sign base

## License

This project is open source and available under the MIT License