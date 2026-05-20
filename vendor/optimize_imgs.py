#!/usr/bin/env python3
"""
optimize_imgs.py — Resize and convert images for web delivery.

Produces PNG and WebP variants at multiple widths from a single source image.
Requires ImageMagick 7+ (magick).
"""

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_SIZES = [800, 1200, 1800]
# WebP is generated for every size; PNG only up to this width (large PNGs are heavy).
PNG_MAX_WIDTH = 1200


def check_magick():
    try:
        subprocess.run(["magick", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        sys.exit("Error: ImageMagick 7 (magick) is not installed or not on PATH.")


def build_output_path(source: Path, width: int, fmt: str, out_dir: Path) -> Path:
    stem = source.stem
    return out_dir / f"{stem}-{width}.{fmt}"


def convert(source: Path, dest: Path, width: int, quality: int):
    cmd = [
        "magick",
        str(source),
        "-resize", f"{width}x",
        "-quality", str(quality),
        str(dest),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}", file=sys.stderr)
        return False
    return True


def optimize(
    source: Path,
    sizes: list[int],
    out_dir: Path,
    png_quality: int,
    webp_quality: int,
    png_max_width: int,
    dry_run: bool,
):
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for width in sorted(sizes):
        # WebP — every size
        dest_webp = build_output_path(source, width, "webp", out_dir)
        results.append(("webp", width, dest_webp))

        # PNG — only up to png_max_width
        if width <= png_max_width:
            dest_png = build_output_path(source, width, "png", out_dir)
            results.append(("png", width, dest_png))

    if dry_run:
        print("Dry run — files that would be created:")
        for fmt, width, dest in results:
            print(f"  {dest}")
        return

    success = 0
    for fmt, width, dest in results:
        quality = webp_quality if fmt == "webp" else png_quality
        print(f"  → {dest.name} ({width}px, q{quality})", end=" ", flush=True)
        ok = convert(source, dest, width, quality)
        if ok:
            size_kb = dest.stat().st_size // 1024
            print(f"[{size_kb} KB]")
            success += 1
        else:
            print("[FAILED]")

    print(f"\n{success}/{len(results)} files written to {out_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Resize and convert images to PNG and WebP at multiple widths.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python optimize_imgs.py assets/images/photo.png
  python optimize_imgs.py assets/images/photo.png --sizes 600 900 1400
  python optimize_imgs.py assets/images/photo.png --out assets/images/resized
  python optimize_imgs.py assets/images/photo.png --dry-run
        """,
    )
    parser.add_argument("source", type=Path, help="Source image file")
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=DEFAULT_SIZES,
        metavar="PX",
        help=f"Output widths in pixels (default: {DEFAULT_SIZES})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        metavar="DIR",
        help="Output directory (default: same directory as source)",
    )
    parser.add_argument(
        "--png-quality",
        type=int,
        default=90,
        metavar="Q",
        help="PNG quality 1-100 (default: 90)",
    )
    parser.add_argument(
        "--webp-quality",
        type=int,
        default=85,
        metavar="Q",
        help="WebP quality 1-100 (default: 85)",
    )
    parser.add_argument(
        "--png-max-width",
        type=int,
        default=PNG_MAX_WIDTH,
        metavar="PX",
        help=f"Skip PNG output above this width (default: {PNG_MAX_WIDTH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing any files",
    )

    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists():
        sys.exit(f"Error: source file not found: {source}")

    out_dir = args.out.resolve() if args.out else source.parent

    check_magick()

    print(f"Source : {source} ({source.stat().st_size // 1024} KB)")
    print(f"Output : {out_dir}")
    print(f"Sizes  : {args.sizes}")
    print()

    optimize(
        source=source,
        sizes=args.sizes,
        out_dir=out_dir,
        png_quality=args.png_quality,
        webp_quality=args.webp_quality,
        png_max_width=args.png_max_width,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
