# ColorScope — Image Color Percentage Analyzer

A GitHub-ready Product Management + Python prototype project that analyzes an image at pixel level and maps every pixel into 11 human-readable color categories.

This project was built for a Product Management internship assignment where the requirement was to create a simple local prototype, run it on 4 images, and explain the color-mapping logic clearly.

## Problem Statement

Users need a tool that takes an image as input, analyzes it at the pixel level, and produces a chart showing the percentage breakdown of colors across the image.

The tool maps similar shades into 11 categories:

- White
- Black
- Red
- Green
- Yellow
- Blue
- Brown
- Purple
- Pink
- Orange
- Gray

Example: navy maps to Blue, burgundy maps to Red, and light yellow maps to Yellow.

## Why This Project Stands Out

This is not just a script. It includes:

- Clean Python prototype
- Product Requirements Document
- Color-mapping algorithm explanation
- Sample image analysis
- CSV reports
- Bar chart outputs
- Recruiter-friendly documentation
- Developer handoff notes

## Project Structure

```text
colorscope-image-color-analyzer/
├── data/
│   └── sample_images/
│       ├── mona_lisa.png
│       ├── flowers_vase.png
│       ├── expressionist_landscape.png
│       └── wheat_field.png
├── docs/
│   ├── PRD.md
│   ├── PROMPTS_USED.md
│   └── VIDEO_SCRIPT.md
├── outputs/
│   ├── charts/
│   └── reports/
├── src/
│   ├── analyzer.py
│   ├── color_mapper.py
│   ├── visualizer.py
│   └── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Tech Stack

- Python
- Pillow
- NumPy
- Pandas
- Matplotlib

## How It Works

```text
Image Upload
    ↓
RGB Pixel Extraction
    ↓
RGB to HSV Conversion
    ↓
Color Mapping Engine
    ↓
Pixel Count
    ↓
Percentage Calculation
    ↓
CSV Report + Chart
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/colorscope-image-color-analyzer.git
cd colorscope-image-color-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Windows:

```bash
.venv\Scripts\activate
```

## Run the Project

Analyze one image:

```bash
python src/main.py --image data/sample_images/mona_lisa.png
```

Analyze all sample images:

```bash
python src/main.py --folder data/sample_images
```

## Output

The project generates:

```text
outputs/charts/
outputs/reports/
```

Each image gets:

- A color percentage chart
- A CSV report with pixel counts and percentages

## Algorithm Summary

The prototype converts RGB pixels into HSV format because HSV better matches how humans understand color.

### White

High brightness and low saturation.

### Black

Very low brightness.

### Gray

Low saturation and medium brightness.

### Brown

Orange/red hue with lower brightness.

### Remaining Colors

Mapped by hue ranges:

| Color | Hue Range |
|---|---|
| Red | 0°–15° and 345°–360° |
| Orange | 15°–40° |
| Yellow | 40°–70° |
| Green | 70°–170° |
| Blue | 170°–260° |
| Purple | 260°–310° |
| Pink | 310°–345° |

## Product Thinking

Important product tradeoffs considered:

- RGB vs HSV
- Fixed thresholds vs ML model
- Accuracy vs speed
- Simple local prototype vs full hosted application
- Human-readable color categories vs exact RGB values

## Future Roadmap

- Dominant color palette extraction
- Upload UI
- Batch image analysis
- Brand color matching
- Color psychology insights
- API endpoint for image-processing platforms

## Author

Saini Sarkar  
Data Science Intern | Product + AI Enthusiast
