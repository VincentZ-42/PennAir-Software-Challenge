import cv2
import numpy as np

# Load the image
image = cv2.imread("Static.png")
if image is None:
    raise ValueError("Image not found!")

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create masks for colors

# Green (grass + green shapes)
lower_green = np.array([35, 40, 40])
upper_green = np.array([85, 255, 255])
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# Non-green (all other shapes)
mask_non_green = cv2.bitwise_not(mask_green)

# Low-texture check for green shapes
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Compute local variance (sliding window)
kernel_size = 9
mean = cv2.blur(gray.astype(np.float32), (kernel_size, kernel_size))
sq_mean = cv2.blur((gray.astype(np.float32)**2), (kernel_size, kernel_size))
local_variance = sq_mean - mean**2

# Adjust these to match the texture of the grass in the background
variance_thresh = 100
low_texture_mask = (local_variance < variance_thresh).astype(np.uint8) * 255

# Combine green mask with low-texture mask
mask_green_shapes = cv2.bitwise_and(mask_green, low_texture_mask)

# Combine masks (non-green + green shapes)
combined_mask = cv2.bitwise_or(mask_non_green, mask_green_shapes)

# Clean masks
kernel = np.ones((5,5), np.uint8)
mask_clean = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

# Find contours and draw
contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
output = image.copy()
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 500:
        # Draw contour with red outline
        cv2.drawContours(output, [cnt], -1, (0,0,255), 2)
        
        # Compute center of shape
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Draw center as a small red dot
            cv2.circle(output, (cX, cY), 2, (0, 0, 255), 2)

# Save the result as a new image
output_filename = "Detected_Static_Shapes.png"
cv2.imwrite(output_filename, output)
print(f"Processing complete...detected shapes stored in {output_filename}")
