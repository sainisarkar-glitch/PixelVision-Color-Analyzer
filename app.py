import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colorsys
from pathlib import Path
import math

st.set_page_config(
    page_title="PixelVision Color Analyzer",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 PixelVision Color Analyzer")
st.write("Upload an image and analyze its main color distribution.")

COLOR_ORDER = [
    "Black", "Red", "Green", "Blue", "Gray",
    "Yellow", "Orange", "Brown", "Pink", "Purple", "White"
]

DISPLAY_COLORS = {
    "Black": "#111111",
    "Red": "#d62728",
    "Green": "#2ca02c",
    "Blue": "#1f77b4",
    "Gray": "#a6a6a6",
    "Yellow": "#f2c300",
    "Orange": "#ff7f0e",
    "Brown": "#8c564b",
    "Pink": "#e377c2",
    "Purple": "#9467bd",
    "White": "#ffffff"
}


def show_uploaded_image(image):
    try:
        st.image(image, caption="Uploaded Image", use_container_width=True)
    except TypeError:
        st.image(image, caption="Uploaded Image", use_column_width=True)


def classify_color(r, g, b):
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255

    h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
    h = h * 360

    if v < 0.16:
        return "Black"

    if s < 0.12 and v > 0.88:
        return "White"

    if s < 0.18:
        return "Gray"

    if 15 <= h < 50 and v < 0.60 and s < 0.75:
        return "Brown"

    if h < 15 or h >= 345:
        return "Red"
    elif 15 <= h < 40:
        return "Orange"
    elif 40 <= h < 70:
        return "Yellow"
    elif 70 <= h < 165:
        return "Green"
    elif 165 <= h < 255:
        return "Blue"
    elif 255 <= h < 295:
        return "Purple"
    elif 295 <= h < 345:
        return "Pink"

    return "Gray"


def analyze_image(image):
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    image.thumbnail((600, 600))

    pixels = np.array(image).reshape(-1, 3)

    color_counts = {color: 0 for color in COLOR_ORDER}

    for r, g, b in pixels:
        color_name = classify_color(int(r), int(g), int(b))
        color_counts[color_name] += 1

    total_pixels = len(pixels)

    results = []
    for color, count in color_counts.items():
        percentage = (count / total_pixels) * 100
        results.append(
            {
                "Color Category": color,
                "Percentage": percentage
            }
        )

    df = pd.DataFrame(results)
    df = df.sort_values(by="Percentage", ascending=False)
    return df


def plot_color_distribution(df, image_title):
    labels = df["Color Category"].tolist()
    values = df["Percentage"].tolist()

    bar_colors = [DISPLAY_COLORS.get(label, "#1f77b4") for label in labels]

    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.bar(
        labels,
        values,
        color=bar_colors,
        edgecolor="black"
    )

    ax.set_title(
        f"Color Distribution: {image_title}",
        fontsize=22,
        fontweight="bold"
    )

    ax.set_xlabel("Color Category", fontsize=13)
    ax.set_ylabel("Percentage of Image", fontsize=13)

    max_value = max(values)
    y_limit = max(40, math.ceil(max_value + 5))
    ax.set_ylim(0, y_limit)

    ax.tick_params(axis="x", labelrotation=35, labelsize=11)
    ax.tick_params(axis="y", labelsize=11)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=11
        )

    plt.tight_layout()
    return fig


uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    show_uploaded_image(image)

    if st.button("Analyze Image"):
        df = analyze_image(image)

        image_title = Path(uploaded_file.name).stem
        image_title = image_title.replace("_", " ").replace("-", " ").title()

        fig = plot_color_distribution(df, image_title)

        st.pyplot(fig)

        st.subheader("Color Percentage Table")
        st.dataframe(df)

else:
    st.info("Please upload an image to start analysis.")
