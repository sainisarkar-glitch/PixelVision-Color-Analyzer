"""
Core image analysis functions for ColorScope.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from PIL import Image

from color_mapper import COLOR_CATEGORIES, map_rgb_to_category


def load_image_pixels(image_path: str | Path, max_size: int = 500) -> np.ndarray:
    """
    Load an image and return RGB pixels as a NumPy array.

    The image is resized while keeping aspect ratio to improve performance.
    Transparent pixels are composited over white.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path)

    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        background.alpha_composite(img.convert("RGBA"))
        img = background.convert("RGB")
    else:
        img = img.convert("RGB")

    img.thumbnail((max_size, max_size))
    pixels = np.array(img).reshape(-1, 3)
    return pixels


def analyze_image(image_path: str | Path, max_size: int = 500) -> pd.DataFrame:
    """
    Analyze an image and return color category counts and percentages.
    """
    pixels = load_image_pixels(image_path, max_size=max_size)

    counts: Dict[str, int] = {color: 0 for color in COLOR_CATEGORIES}

    for r, g, b in pixels:
        category = map_rgb_to_category(int(r), int(g), int(b))
        counts[category] += 1

    total_pixels = sum(counts.values())

    data = []
    for category in COLOR_CATEGORIES:
        count = counts[category]
        percentage = round((count / total_pixels) * 100, 2)
        data.append(
            {
                "color_category": category,
                "pixel_count": count,
                "percentage": percentage,
            }
        )

    return pd.DataFrame(data).sort_values("percentage", ascending=False)
