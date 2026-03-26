# OG Image Generator — WB Hidden Gems Business Directory

`generate_og.py` creates the **Open Graph social share images** (1200×630 px JPEG) used in the `<meta property="og:image">` and `<meta name="twitter:image">` tags on each business's standalone page in `business-directory/`.

When a link to a business page is shared on Facebook, Instagram, LinkedIn, iMessage, or any other platform that reads OG tags, the platform fetches and displays that image as the preview card.

---

## Requirements

Python 3 and the **Pillow** imaging library must be installed.

```bash
pip install Pillow
```

The script uses two fonts:

| Constant | Role | Path |
|---|---|---|
| `FONT_BOLD` | Sansation Bold — all headings, labels, pills, UI text | `~/.local/share/fonts/Sansation-Bold.ttf` |
| `FONT_REGULAR` | Sansation Regular — tagline, location, URL watermark | `~/.local/share/fonts/Sansation-Regular.ttf` |
| `FONT_DESC` | FreeSans — business description lines only | `/usr/share/fonts/gnu-free/FreeSans.otf` |

Sansation is the same typeface used across the WB Hidden Gems website, keeping the images on-brand. FreeSans is kept for the description to provide a subtle visual contrast between the UI chrome and the body copy.

If the Sansation files are not present, install them by downloading from Google Fonts and placing the `.ttf` files in `~/.local/share/fonts/`, then run `fc-cache -f`. Alternatively, change the `FONT_BOLD` / `FONT_REGULAR` constants at the top of the script to any `.ttf` or `.otf` path available on your machine.

---

## How to run

From anywhere, just point Python at the script:

```bash
python3 assets/images/businesses/generate_og.py
```

Or `cd` into the folder first:

```bash
cd assets/images/businesses
python3 generate_og.py
```

Each image is written to the same folder as the script. Existing files are silently overwritten.

---

## Image layout

Every image is divided into two halves:

```
┌─────────────────────────────────────────────────────────────────────┐
│                              │                                      │
│  WB HIDDEN GEMS  (brand)     │   Business Name (bold, large)        │
│  · Local Business Directory  │   Tagline (gray, regular)            │
│                              │   Description line 1                 │
│       ┌──────────┐           │   Description line 2                 │
│       │          │           │  ─────────────────────────────────── │
│       │ Initials │           │  [Category]  ★★★★★  4.9             │
│       │  circle  │           │  [Badge]                             │
│       └──────────┘           │                                      │
│                              │   Wells Branch, TX · 78728           │
│  wbhiddengems.com/...        │                                      │
└─────────────────────────────────────────────────────────────────────┘
       Left: accent color bg          Right: white card panel
```

- The **accent color** (and two tonal variants) come from the business entry and drive the entire left-side palette.
- The **initials circle** uses two semi-transparent white overlapping ellipses to create a depth effect.
- Rating stars are drawn as polygon shapes (not Unicode characters) so they render correctly on every system regardless of font coverage.
- The business name auto-wraps to a second line if it is too wide for the panel.

---

## Adding a new business

1. Open `generate_og.py` and find the `businesses` list near the top of the file.

2. Append a new dictionary entry following this template:

```python
{
    "slug":         "my-business-og",        # output filename (without .jpg)
    "name":         "My Business Name",      # displayed large on the card
    "tagline":      "Short catchy tagline",  # one line, shown below the name
    "description":  "First line of detail\nSecond line of detail",  # use \n for line break
    "category":     "Home Services",         # shown as a pill tag
    "rating":       "4.6",                   # numeric string, e.g. "4.6"
    "initials":     "MB",                    # 2 letters shown in the logo circle
    "accent":       GREEN_D,                 # main background color (see palette below)
    "accent_mid":   (40, 107, 18),           # slightly lighter shade for decorative shapes
    "accent_light": GREEN_L,                 # used for the divider line tint
    "badge":        "Family-Owned",          # short label shown as a second pill
},
```

3. Run the script:

```bash
python3 assets/images/businesses/generate_og.py
```

   This regenerates **all** images, including the new one. Only the new file will actually look different — existing files are identical unless you changed their entry.

4. The new file will be saved as `assets/images/businesses/my-business-og.jpg`.

5. Reference it in the business's standalone HTML page (`business-directory/my-business.html`):

```html
<meta property="og:image" content="https://wbhiddengems.com/assets/images/businesses/my-business-og.jpg">
<meta name="twitter:image" content="https://wbhiddengems.com/assets/images/businesses/my-business-og.jpg">
```

---

## Accent color palette

These constants are defined at the top of the script. Use them directly as the `accent` value, or supply any custom RGB tuple.

| Constant | RGB | Use for |
|---|---|---|
| `GREEN_D` | `(32, 80, 12)` | Food, nature, farms |
| `GREEN_L` | `(170, 214, 151)` | (light variant — use for `accent_light`) |
| `RED_D` | `(138, 13, 26)` | Beauty, fashion, wellness |
| `BLUE_D` | `(8, 19, 122)` | Auto, tech, professional |
| `BLUE_L` | `(21, 34, 168)` | (light variant) |
| `YELLOW_D` | `(204, 128, 18)` | Retail, food, general |

For a custom color not in the palette, pass the RGB tuple directly:

```python
"accent":      (90, 40, 120),   # deep purple
"accent_mid":  (110, 55, 145),  # mid purple
"accent_light": (190, 150, 220), # light purple tint
```

---

## Output specs

| Property | Value |
|---|---|
| Dimensions | 1200 × 630 px |
| Format | JPEG |
| Quality | 92 (high, ~55–65 KB per image) |
| Color space | RGB |

These dimensions satisfy the minimum requirements for Facebook (600×315), Twitter/X (800×418), LinkedIn (1200×627), and iMessage link previews.
