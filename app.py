import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="PixelVision Color Analyzer",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 PixelVision Color Analyzer")
st.write("Upload an image and analyze its color distribution across 11 color categories.")

COLOR_CATEGORIES = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Green": (0, 128, 0),
    "Yellow": (255, 255, 0),
    "Blue": (0, 0, 255),
    "Brown": (139, 69, 19),
    "Purple": (128, 0, 128),
    "Pink": (255, 105, 180),
    "Orange": (255, 165, 0),
    "Gray": (128, 128, 128)
}

def closest_color(pixel):
    r, g, b = pixel[:3]

    min_distance = float("inf")
    closest = None

    for color_name, rgb in COLOR_CATEGORIES.items():
        distance = np.sqrt(
            (r - rgb[0])**2 +
            (g - rgb[1])**2 +
            (b - rgb[2])**2
        )

        if distance < min_distance:
            min_distance = distance
            closest = color_name

    return closest

def analyze_image(image):
    image = image.convert("RGB")
    image = image.resize((300, 300))

    pixels = np.array(image).reshape(-1, 3)

    counts = {color: 0 for color in COLOR_CATEGORIES.keys()}

    for pixel in pixels:
        color = closest_color(pixel)
        counts[color] += 1

    total_pixels = len(pixels)

    percentages = {
        color: round((count / total_pixels) * 100, 2)
        for color, count in counts.items()
        if count > 0
    }

    return percentages

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)

    if st.button("Analyze Image"):

        results = analyze_image(image)

        df = pd.DataFrame({
            "Color": list(results.keys()),
            "Percentage": list(results.values())
        })

        df = df.sort_values(
            by="Percentage",
            ascending=False
        )

        with col2:
            st.subheader("Color Distribution")

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(df["Color"], df["Percentage"])
            ax.set_xlabel("Colors")
            ax.set_ylabel("Percentage (%)")
            ax.set_title("Color Distribution Chart")
            plt.xticks(rotation=45)

            st.pyplot(fig)

        st.subheader("Percentage Breakdown")
        st.dataframe(df, use_container_width=True)
