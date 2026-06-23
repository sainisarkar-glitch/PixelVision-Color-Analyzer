"""
Color mapping engine for ColorScope.

The algorithm converts RGB pixels into HSV because HSV separates:
- Hue: actual color family
- Saturation: color intensity
- Value: brightness

This makes mapping shades like navy, burgundy, light yellow, and gray easier
than using raw RGB thresholds.
"""

from __future__ import annotations

import colorsys
from typing import Dict, Tuple

COLOR_CATEGORIES = [
    "White",
    "Black",
    "Gray",
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Purple",
    "Pink",
    "Brown",
]

CHART_COLORS: Dict[str, str] = {
    "White": "#f5f5f5",
    "Black": "#111111",
    "Gray": "#9e9e9e",
    "Red": "#d62728",
    "Orange": "#ff7f0e",
    "Yellow": "#f2c300",
    "Green": "#2ca02c",
    "Blue": "#1f77b4",
    "Purple": "#9467bd",
    "Pink": "#e377c2",
    "Brown": "#8c564b",
}


def rgb_to_hsv_degrees(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB 0-255 values to HSV where hue is 0-360 degrees."""
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h * 360, s, v


def map_rgb_to_category(r: int, g: int, b: int) -> str:
    """
    Map one RGB pixel to the closest human-readable color category.

    Priority matters:
    1. White/black/gray are detected first using brightness and saturation.
    2. Brown is detected before orange because brown is usually a dark orange.
    3. Remaining colors are mapped by hue ranges.
    """
    h, s, v = rgb_to_hsv_degrees(r, g, b)

    if v > 0.90 and s < 0.15:
        return "White"

    if v < 0.15:
        return "Black"

    if s < 0.15:
        return "Gray"

    # Brown is generally an orange/red hue with lower brightness.
    if 15 <= h < 45 and 0.20 <= s and v < 0.70:
        return "Brown"

    if h < 15 or h >= 345:
        return "Red"
    if h < 40:
        return "Orange"
    if h < 70:
        return "Yellow"
    if h < 170:
        return "Green"
    if h < 260:
        return "Blue"
    if h < 310:
        return "Purple"
    if h < 345:
        return "Pink"

    return "Gray"
