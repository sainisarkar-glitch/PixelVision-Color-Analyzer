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
    "Gray": (128, 128, 128),
}

def closest_color(pixel):
    r, g, b = pixel[:3]
    min_distance = float("inf")
    closest = "Gray"

    for color_name, rgb in COLOR_CATEGORIES.items():
        distance = np.sqrt(
            (int(r) - rgb[0]) ** 2 +
            (int(g) - rgb[1]) ** 2 +
            (int(b) - rgb[2]) ** 2
        )

        if distance < min_distance:
            min_distance = distance
            closest = color_name

    return closest

def analyze_image(image):
    image = image.convert("RGB")
    image = image.resize((250, 250))

    pixels = np.array(image).reshape(-1, 3)

    counts = {color: 0 for color in COLOR_CATEGORIES.keys()}

    for pixel in pixels:
        mapped_color = closest_color(pixel)
        counts[mapped_color] += 1

    total_pixels = len(pixels)

    data = []

    for color, count in counts.items():
        percentage = round((count / total_pixels) * 100, 2)

        if percentage > 0:
            data.append({
                "Color": color,
                "Percentage": percentage
            })

    df = pd.DataFrame(data)
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

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(df["Color"], df["Percentage"])
        ax.set_xlabel("Color Category")
        ax.set_ylabel("Percentage (%)")
        ax.set_title("Image Color Distribution")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    st.subheader("Percentage Breakdown")
    st.dataframe(df)

    st.success("Analysis complete. Take a screenshot of this result for your submission.")

else:
    st.info("Upload one image to generate the color percentage chart.")     
