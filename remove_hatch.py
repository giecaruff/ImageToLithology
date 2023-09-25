import cv2
import numpy as np
# pip install opencv-python

def remove_hatches(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use morphological operations to remove thin lines
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=2)

    # Blur the image to reduce noise
    blurred = cv2.GaussianBlur(opening, (5, 5), 0)

    # Threshold the image to create a mask of the hatches
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Inpainting the original image using the mask
    inpainted = cv2.inpaint(img, thresh, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

    # Save the result
    cv2.imwrite(output_path, inpainted)

# Call the function
remove_hatches("C:\\Users\\mario\\Desktop\\3-BRSA-1195-RJS_PC_lito.png", "C:\\Users\\mario\\Desktop\\3-BRSA-1195-RJS_PC_lito_clean.png")