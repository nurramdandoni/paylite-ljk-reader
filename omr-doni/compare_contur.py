import cv2
import numpy as np

# Load image and templates
image = cv2.imread('LJK_Paylite_Edu_mark.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template_box = cv2.imread('./template/template_box.jpg', 0)
template_square = cv2.imread('./template/template_square.jpg', 0)
template_circle = cv2.imread('./template/template_circle.jpg', 0)
template_triangle = cv2.imread('./template/template_triangle.jpg', 0)

# Perform template matching
res_box = cv2.matchTemplate(gray_image, template_box, cv2.TM_CCOEFF_NORMED)
res_square = cv2.matchTemplate(gray_image, template_square, cv2.TM_CCOEFF_NORMED)
res_circle = cv2.matchTemplate(gray_image, template_circle, cv2.TM_CCOEFF_NORMED)
res_triangle = cv2.matchTemplate(gray_image, template_triangle, cv2.TM_CCOEFF_NORMED)

cv2.imshow("box",res_box)

# Define threshold for template matching results
threshold = 0.8

# Find locations with high correlation
loc_box = np.where(res_box >= threshold)
loc_square = np.where(res_square >= threshold)
loc_circle = np.where(res_circle >= threshold)
loc_triangle = np.where(res_triangle >= threshold)

# Iterate through locations and draw bounding box
for pt in zip(*loc_box[::-1]):
    cv2.rectangle(image, pt, (pt[0] + template_box.shape[1], pt[1] + template_box.shape[0]), (0, 255, 0), 2)
    centroid_x = pt[0] + template_box.shape[1] // 2
    centroid_y = pt[1] + template_box.shape[0] // 2
    cv2.circle(image, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
    print("Box centroid coordinates:", (centroid_x, centroid_y))

for pt in zip(*loc_square[::-1]):
    cv2.rectangle(image, pt, (pt[0] + template_square.shape[1], pt[1] + template_square.shape[0]), (0, 255, 0), 2)
    centroid_x = pt[0] + template_square.shape[1] // 2
    centroid_y = pt[1] + template_square.shape[0] // 2
    cv2.circle(image, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
    print("Square centroid coordinates:", (centroid_x, centroid_y))

for pt in zip(*loc_circle[::-1]):
    cv2.rectangle(image, pt, (pt[0] + template_circle.shape[1], pt[1] + template_circle.shape[0]), (0, 255, 0), 2)
    centroid_x = pt[0] + template_circle.shape[1] // 2
    centroid_y = pt[1] + template_circle.shape[0] // 2
    cv2.circle(image, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
    print("Circle centroid coordinates:", (centroid_x, centroid_y))

for pt in zip(*loc_triangle[::-1]):
    cv2.rectangle(image, pt, (pt[0] + template_triangle.shape[1], pt[1] + template_triangle.shape[0]), (0, 255, 0), 2)
    centroid_x = pt[0] + template_triangle.shape[1] // 2
    centroid_y = pt[1] + template_triangle.shape[0] // 2
    cv2.circle(image, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
    print("Triangle centroid coordinates:", (centroid_x, centroid_y))

# Display image
cv2.imshow('Detected Shapes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
