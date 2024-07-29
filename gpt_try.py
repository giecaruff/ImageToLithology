from collections import Counter
from PIL import Image
import pandas as pd
from collections import Counter
import math
import numpy as np

##############################################################
top_depth = 2075.0
bottom_depth = 2114.2
step = False
path_color = "C:\\Users\\mario\\Desktop\\lito_conversor\\colors.csv"
image_path = "C:\\Users\\mario\\Desktop\\lito_conversor\\3-BRSA-1195-RJS_PC_possal.png"
##############################################################

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def euclidean_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def closest_color_code(rgb, color_data):
    min_dist = float('inf')
    closest_code = None
    
    for _, row in color_data.iterrows():
        color = hex_to_rgb(row['COR'])
        dist = euclidean_distance(rgb, color)
        if dist < min_dist:
            min_dist = dist
            closest_code = row['CODIGO']
            
    return closest_code

def is_dark_color(rgba, threshold=50):
    """
    Check if the color is dark or fully transparent.
    A color is considered dark if its r, g, and b values are all below the threshold.
    """
    r, g, b, a = rgba
    return a == 0 or (r < threshold and g < threshold and b < threshold)

def most_common_color_in_row(image_path):
    """
    Extract the most common color in each row of a PNG image, excluding black, dark grey tones, and transparent pixels.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        colors_per_row = []

        for y in range(height):
            row_colors = [img.getpixel((x, y)) for x in range(width)]
            row_colors = [color for color in row_colors if not is_dark_color(color)]
            counter = Counter(row_colors)
            most_common = counter.most_common(1)
            if most_common:
                colors_per_row.append(most_common[0][0][:3])  # Take only RGB, ignore alpha
            else:
                # In case all colors are dark or the row is empty, you might want to append a default color or None
                colors_per_row.append(None)
        return colors_per_row

color_data = pd.read_csv(path_color)

# Usage:

dominant_row_colors = most_common_color_in_row(image_path)

# Initialize the last valid color
last_valid_color = None

# Get CODIGO for each row color
codes_for_rows = []
for color in dominant_row_colors:
    if color is None and last_valid_color:
        color = last_valid_color
    if color:
        last_valid_color = color
    code = closest_color_code(color, color_data) if color else None
    codes_for_rows.append(code)

# Print the results

interval = (bottom_depth - top_depth) / len(codes_for_rows)
depths = [top_depth + i * interval for i in range(len(codes_for_rows))]

if step:
    print("Step")
    new_depth = np.arrange(top_depth, bottom_depth, step)
    new_code = np.interp(new_depth, depths, codes_for_rows)

    df = pd.DataFrame({
    'Depth': new_depth,
    'Code': new_code
    }) 

else:
    print("No Step")
    df = pd.DataFrame({
    'Depth': depths,
    'Code': codes_for_rows
    })

df.to_csv("C:\\Users\\mario\\Desktop\\3-BRSA-1195-RJS_possal_PC_lito.csv", index=False)