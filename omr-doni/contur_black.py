import numpy as np
import cv2

# Read the image
img = cv2.imread('LJKKosong_page-0001.jpg')

# Resizing the image to fit the window
height, width = img.shape[:2]
max_height = 600
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# Convert the image to grayscale
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find contours of black areas
_, thrash = cv2.threshold(imgGrey, 30, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Draw red rectangles around the contours
for contour in contours:
    # Calculate contour area
    area = cv2.contourArea(contour)
    # Filter contours with a certain area (adjust this threshold as needed)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
    # if area > 1000:
    #     # Get the bounding box of the contour
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # Draw the bounding box (rectangle) on the image
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)

# Display the result
cv2.imshow("Red Rectangles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
