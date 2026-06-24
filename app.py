import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colorsys

st.set_page_config(
    page_title="PixelVision Color Analyzer",
    page_icon="🎨",
    layout="wide"
)

COLOR_ORDER = [
    "Black", "Brown", "Green", "Yellow", "Red",
    "Orange", "Pink", "Gray", "Purple", "White", "Blue"
]

BAR_COLORS = {
    "White": "#FFFFFF",
    "Black": "#111111",
    "Red": "#D62728",
    "Green": "#2CA02C",
    "Yellow": "#FFD000",
    "Blue": "#1F77B4",
    "Brown": "#8C564B",
    "Purple": "#9467BD",
    "Pink": "#E377C2",
    "Orange": "#FF7F0E",
    "Gray": "#7F7F7F"
}

def map_color(rgb):
    r, g, b = rgb
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255

    h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
    h = h * 360

    # Brightness-based categories
    if v < 0.18:
        return "Black"

    if s < 0.12 and v > 0.90:
        return "White"

    if s < 0.18:
        if v < 0.35:
            return "Black"
        return "Gray"

    # Brown detection
    if 10 <= h <= 45 and v < 0.65 and s > 0.25:
        return "Brown"

    # Hue-based categories
    if h < 15 or h >= 345:
        return "Red"
    elif 15 <= h < 40:
        return "Orange"
    elif 40 <= h < 70:
        return "Yellow"
    elif 70 <= h < 170:
        return "Green"
    elif 170 <= h < 250:
        return "Blue"
    elif 250 <= h < 290:
        return "Purple"
    elif 290 <= h < 345:
        return "Pink"

    return "Gray"

def analyze_image(image):
    image = image.convert("RGB")
    image = image.resize((300, 300))

    pixels = np.array(image).reshape(-1, 3)

    counts = {color: 0 for color in COLOR_ORDER}

    for pixel in pixels:
        color = map_color(pixel)
        counts[color] += 1

    total_pixels = len(pixels)

    data = []

    for color in COLOR_ORDER:
        percentage = round((counts[color] / total_pixels) * 100, 1)

        data.append({
            "Color": color,
            "Percentage": percentage
        })

    df = pd.DataFrame(data)
    df = df[df["Percentage"] > 0]
    df = df.sort_values(by="Percentage", ascending=False)

    return df

st.title("🎨 PixelVision Color Analyzer")

st.write(
    "Upload an image. The app analyzes pixels, maps similar shades into 11 color categories, "
    "and generates a percentage distribution chart."
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    image_name = uploaded_file.name
    clean_name = image_name.replace("_", " ").replace(".png", "").replace(".jpg", "").replace(".jpeg", "").title()

    left, right = st.columns(2)

    with left:
        st.subheader("Uploaded Image")
        st.image(
            image,
            caption="Input image",
            use_column_width=True
        )

    df = analyze_image(image)

    with right:
        st.subheader("Color Distribution Chart")

        fig, ax = plt.subplots(figsize=(10, 6))

        colors = [BAR_COLORS[color] for color in df["Color"]]

        bars = ax.bar(
            df["Color"],
            df["Percentage"],
            color=colors,
            edgecolor="black"
        )

        ax.set_xlabel("Color Category")
        ax.set_ylabel("Percentage of Image")
        ax.set_title(f"Color Distribution: {clean_name}")

        plt.xticks(rotation=45)

        for bar, percentage in zip(bars, df["Percentage"]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{percentage}%",
                ha="center",
                va="bottom",
                fontsize=10
            )

        plt.tight_layout()

        st.pyplot(fig)

    st.subheader("Percentage Breakdown")
    st.dataframe(df, use_container_width=True)

    st.success("Analysis complete. Take a screenshot of this result for your submission.")

else:
    st.info("Upload one image to generate the color percentage chart.")
