import numpy as np
import cv2

# Read the image
img = cv2.imread('LJKKosong_page-0001.jpg')

# Resizing the image to fit the window
height, width = img.shape[:2]
max_height = 600
max_width = 800

if height > max_height or width > max_width:
    scale = max_height / height if height > width else max_width / width
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# Split the image into its BGR components
b, g, r = cv2.split(img)

# Reduce intensity of blue channel
b = np.clip(b - 50, 0, 255)  # Decrease blue intensity by 50 (adjust as needed)

# Merge the channels back together
img_without_blue = cv2.merge((b, g, r))

# Convert the image to grayscale
imgGrey = cv2.cvtColor(img_without_blue, cv2.COLOR_BGR2GRAY)

# Thresholding to create a binary image of black areas
_, binary_img = cv2.threshold(imgGrey, 1, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get bounding boxes of the contours
black_boxes = [cv2.boundingRect(contour) for contour in contours]

# Print the coordinates of black boxes
for i, box in enumerate(black_boxes):
    x, y, w, h = box
    print("Black Box {}: x={}, y={}, width={}, height={}".format(i+1, x, y, w, h))

# Display the result
cv2.imshow("Image without Blue", img_without_blue)
cv2.waitKey(0)
cv2.destroyAllWindows()
