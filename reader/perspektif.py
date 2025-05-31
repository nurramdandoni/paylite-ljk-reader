import cv2
import numpy as np

img = cv2.imread("../omr-doni/miring.jpeg")
# mengubah ukuran
height, width = img.shape[:2]
print("tinggi : ",height)
print("lebar : ",width)
max_height = 600
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    print("skala : ",scale)
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# kiri atas
cv2.circle(img, (200, 150), 5, (0, 0, 255), -1) 
# kanan atas
cv2.circle(img, (310, 185), 5, (0, 0, 255), -1)
# kiri bawah
cv2.circle(img, (8, 295), 5, (0, 0, 255), -1)
# kanan bawah
cv2.circle(img, (140, 370), 5, (0, 0, 255), -1)

pts1 = np.float32([[200, 150], [310, 185], [8, 295], [140, 370]])

pts2 = np.float32([[0, 0], [350, 0], [0, 600], [350, 600]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (350, 600))

cv2.imshow("Image", img)
cv2.imshow("Perspective transformation", result)
cv2.waitKey(0)
cv2.destroyAllWindows()