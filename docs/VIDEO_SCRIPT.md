# Explainer Video Script

Hi, my name is Saini Sarkar.

For this assignment, I built ColorScope, a lightweight image color analysis prototype.

The product solves a simple but useful problem: users often need to understand the color composition of an image, but most tools only show technical RGB or HEX values. This tool converts image pixels into human-readable color percentages.

The input is an image. The system opens the image, converts it into RGB pixels, then converts those RGB values into HSV.

I chose HSV because it separates hue, saturation, and brightness. This makes it easier to identify colors the way humans understand them. For example, navy can still be mapped to blue, light yellow can be mapped to yellow, and burgundy can be mapped to red.

The algorithm first checks for white, black, and gray using brightness and saturation. Then it detects brown as a darker orange or red tone. After that, the remaining pixels are mapped based on hue ranges into red, orange, yellow, green, blue, purple, and pink.

Once every pixel is categorized, the system counts how many pixels belong to each color and converts those counts into percentages. The final output is a CSV report and a bar chart for each image.

From a product point of view, I kept the prototype simple, explainable, and fast because the assignment requires a local working prototype, not a full hosted app.

Future versions could include a Streamlit upload interface, dominant color palette extraction, brand color matching, and AI-generated insights.

Thank you.
