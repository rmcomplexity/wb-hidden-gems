# vendor/

Third-party scripts and utilities used by this project.

---

## optimize_imgs.py

Resizes a source image to multiple widths and saves both PNG and WebP variants — ready to drop into a `<picture>` element for responsive images.

### Requirements

- Python 3.10+
- [ImageMagick 7](https://imagemagick.org/) (`magick` must be on your PATH)

Install ImageMagick on Arch Linux:
```bash
sudo pacman -S imagemagick
```

### Usage

```bash
python vendor/optimize_imgs.py <source-image> [options]
```

#### Basic — uses all defaults

```bash
python vendor/optimize_imgs.py assets/images/my-photo.png
```

Produces in the same directory as the source:
```
my-photo-800.png
my-photo-1200.png
my-photo-800.webp
my-photo-1200.webp
my-photo-1800.webp
```

PNG is skipped above 1200px by default (large PNGs are heavy; WebP covers the wider sizes).

#### Custom sizes

```bash
python vendor/optimize_imgs.py assets/images/my-photo.png --sizes 600 900 1400
```

#### Custom output directory

```bash
python vendor/optimize_imgs.py assets/images/my-photo.png --out assets/images/resized
```

#### Preview without writing files

```bash
python vendor/optimize_imgs.py assets/images/my-photo.png --dry-run
```

### All options

| Option | Default | Description |
|---|---|---|
| `--sizes PX [PX ...]` | `800 1200 1800` | Output widths in pixels |
| `--out DIR` | Same dir as source | Output directory |
| `--png-quality Q` | `90` | PNG quality (1–100) |
| `--webp-quality Q` | `85` | WebP quality (1–100) |
| `--png-max-width PX` | `1200` | Skip PNG output above this width |
| `--dry-run` | off | Print files that would be created without writing |

### Using the output in HTML

```html
<picture>
    <source
        type="image/webp"
        srcset="assets/images/my-photo-800.webp 800w,
                assets/images/my-photo-1200.webp 1200w,
                assets/images/my-photo-1800.webp 1800w"
        sizes="(max-width: 860px) 100vw, 960px">
    <source
        type="image/png"
        srcset="assets/images/my-photo-800.png 800w,
                assets/images/my-photo-1200.png 1200w"
        sizes="(max-width: 860px) 100vw, 960px">
    <img
        src="assets/images/my-photo-1200.png"
        alt="Description"
        width="1200"
        height="900"
        loading="lazy"
        decoding="async">
</picture>
```
