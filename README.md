# 3D Holiday Sign - Gingerbread Project

A FreeCAD Python script to create a 3D printable holiday sign with a "Happy Holidays" text piece.

## Features

- Creates a rectangular sign base: **8 inches x 6 inches x 1 inch**
- Creates a separate "Happy Holidays" text piece for 3D printing
- Exports both pieces as STL files for 3D printing
- Saves a FreeCAD document (.FCStd) for further editing

## Requirements

- [FreeCAD](https://www.freecad.org/) (version 0.19 or later recommended)
- Python 3.x (included with FreeCAD)

## Usage

### Option 1: Run from FreeCAD GUI

1. Open FreeCAD
2. Go to **View → Panels → Python Console**
3. Run the following command:
   ```python
   exec(open("/path/to/create_holiday_sign.py").read())
   ```

### Option 2: Run from Command Line

```bash
freecad -c create_holiday_sign.py
```

Or with the FreeCAD Python console:

```bash
freecadcmd create_holiday_sign.py
```

## Output Files

After running the script, you will get:

| File | Description |
|------|-------------|
| `sign_base.stl` | The 8x6x1 inch sign base for 3D printing |
| `happy_holidays_text.stl` | The "Happy Holidays" text piece for 3D printing |
| `holiday_sign.FCStd` | FreeCAD document with both objects |

## Customization

You can modify the following constants in the script:

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