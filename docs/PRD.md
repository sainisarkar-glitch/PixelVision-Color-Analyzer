# Product Requirements Document: ColorScope

## 1. Executive Summary

ColorScope is a lightweight image-analysis tool that allows users to upload an image and receive a percentage breakdown of colors across the image.

The product analyzes pixels and maps every color into one of 11 categories:

White, Black, Red, Green, Yellow, Blue, Brown, Purple, Pink, Orange, and Gray.

## 2. Target Users

### Designer
Needs to understand dominant colors in artwork, moodboards, or brand assets.

### E-commerce Seller
Needs quick color analysis for product images.

### Marketing Team
Needs to understand visual themes in creative campaigns.

### Researcher
Needs structured color data from images for analysis.

## 3. User Problem

Most image tools show exact RGB/HEX values, but non-technical users need human-readable color categories.

A user should not need to manually inspect pixels or understand color theory to know what percentage of an image is blue, green, brown, etc.

## 4. Goals

- Accept standard image formats.
- Analyze image pixels.
- Group shades under 11 primary color categories.
- Produce a percentage chart.
- Export structured CSV output.

## 5. Non-Goals

- Full production web app.
- Image editing.
- AI-generated image creation.
- Perfect scientific color classification.
- Object detection.

## 6. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR1 | User can provide one image path | Must Have |
| FR2 | User can provide a folder of images | Should Have |
| FR3 | System extracts RGB pixels | Must Have |
| FR4 | System maps pixels to 11 categories | Must Have |
| FR5 | System generates percentage chart | Must Have |
| FR6 | System exports CSV report | Should Have |
| FR7 | Transparent pixels are handled safely | Should Have |

## 7. Input Requirements

Supported image formats:

- PNG
- JPG
- JPEG
- WEBP

Recommended maximum file size:

- 20 MB

## 8. Processing Flow

```text
Input Image
    ↓
Open with Pillow
    ↓
Convert to RGB
    ↓
Resize for performance
    ↓
Extract pixels using NumPy
    ↓
Convert RGB to HSV
    ↓
Map each pixel to category
    ↓
Count category frequency
    ↓
Calculate percentages
    ↓
Generate chart and CSV
```

## 9. Color Mapping Algorithm

The system uses HSV because it separates hue, saturation, and brightness.

### Priority Rules

1. White, black, and gray are detected first.
2. Brown is detected before orange.
3. Remaining colors are mapped using hue ranges.

### Thresholds

| Category | Logic |
|---|---|
| White | Value > 0.90 and Saturation < 0.15 |
| Black | Value < 0.15 |
| Gray | Saturation < 0.15 |
| Brown | Hue 15°–45°, medium/high saturation, Value < 0.70 |
| Red | Hue 0°–15° or 345°–360° |
| Orange | Hue 15°–40° |
| Yellow | Hue 40°–70° |
| Green | Hue 70°–170° |
| Blue | Hue 170°–260° |
| Purple | Hue 260°–310° |
| Pink | Hue 310°–345° |

## 10. Output Requirements

For each image, the system generates:

1. A bar chart showing color percentage distribution.
2. A CSV report containing:
   - Color category
   - Pixel count
   - Percentage

## 11. Edge Cases

| Edge Case | Expected Behavior |
|---|---|
| Very dark image | Most pixels map to Black |
| Grayscale image | Pixels map to White, Gray, or Black |
| Transparent image | Transparency is composited over white |
| Large image | Image is resized for performance |
| Low quality image | System still returns approximate distribution |

## 12. Success Metrics

| Metric | Target |
|---|---|
| Processing Time | Under 2 seconds for standard images |
| Upload Success | 99% for supported formats |
| Color Category Coverage | 100% pixels assigned |
| User Interpretability | Output understandable without technical knowledge |

## 13. Tradeoffs

### RGB vs HSV

RGB is easy to extract but difficult for human color classification. HSV is better because hue directly represents the color family.

### Fixed Thresholds vs ML

Fixed thresholds are simple, explainable, and enough for the assignment. ML can improve accuracy but adds complexity and requires labeled training data.

### Bar Chart vs Pie Chart

Bar chart is easier to compare when there are 11 categories. Pie chart becomes crowded.

## 14. Future Roadmap

### V1
Local prototype with CLI, CSV, and charts.

### V2
Simple Streamlit UI for image uploads.

### V3
Dominant color palette extraction.

### V4
Brand color comparison.

### V5
AI-generated insights such as: "This image is warm-toned and dominated by brown and yellow."
