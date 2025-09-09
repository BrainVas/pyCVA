from PIL import Image
import numpy as np

# Load image in grayscale
img = Image.open("output_masks/output_mask.png").convert("L")

# Convert to NumPy array
arr = np.array(img)

# Binarize: everything > 0 becomes 255
binary_arr = (arr > 0) * 255  # This gives values 0 or 255

# Convert back to image and save
binary_img = Image.fromarray(binary_arr.astype(np.uint8))
binary_img.save("output_masks/output_mask_bin.png")


# import cv2

# # Load image in grayscale
# img = cv2.imread("output_masks/output_mask.png", cv2.IMREAD_GRAYSCALE)

# # Apply binary threshold: 0 stays 0, >0 becomes 255
# _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

# # Save result
# cv2.imwrite("output_masks/output_mask_bin.png", binary_img)
