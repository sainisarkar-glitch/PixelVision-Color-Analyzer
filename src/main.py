"""
ColorScope CLI

Usage:
    python src/main.py --image data/sample_images/mona_lisa.png
    python src/main.py --folder data/sample_images
"""

from __future__ import annotations

import argparse
from pathlib import Path

from analyzer import analyze_image
from visualizer import create_bar_chart


def analyze_single_image(image_path: Path, output_dir: Path, max_size: int) -> None:
    df = analyze_image(image_path, max_size=max_size)

    chart_path = output_dir / "charts" / f"{image_path.stem}_color_distribution.png"
    csv_path = output_dir / "reports" / f"{image_path.stem}_color_report.csv"

    create_bar_chart(
        df,
        title=f"Color Distribution: {image_path.stem.replace('_', ' ').title()}",
        output_path=chart_path,
    )

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)

    print(f"\nAnalyzed: {image_path.name}")
    print(df.to_string(index=False))
    print(f"Chart saved to: {chart_path}")
    print(f"CSV saved to: {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze image color distribution.")
    parser.add_argument("--image", type=str, help="Path to one image file.")
    parser.add_argument("--folder", type=str, help="Path to a folder of images.")
    parser.add_argument("--output", type=str, default="outputs", help="Output folder.")
    parser.add_argument("--max-size", type=int, default=500, help="Max image size for processing.")

    args = parser.parse_args()

    output_dir = Path(args.output)

    if not args.image and not args.folder:
        parser.error("Please provide either --image or --folder.")

    if args.image:
        analyze_single_image(Path(args.image), output_dir, args.max_size)

    if args.folder:
        folder = Path(args.folder)
        image_files = []
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            image_files.extend(folder.glob(ext))

        if not image_files:
            raise FileNotFoundError(f"No supported image files found in {folder}")

        for image_path in sorted(image_files):
            analyze_single_image(image_path, output_dir, args.max_size)


if __name__ == "__main__":
    main()
