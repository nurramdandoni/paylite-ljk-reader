import cv2
import numpy as np
import imutils

# Baca citra
img = cv2.imread('LJK_Paylite_Edu_v10.jpg')

# Tampilkan hasil resize
height, width = img.shape[:2]
max_height = 600
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
cv2.imshow('Original', img)           
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grey', gray)           

# Lakukan thresholding
_, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
cv2.imshow('Tresh', thresh)           

# Temukan kontur
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnt = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# contours = imutils.grab_contours(cnt)
cv2.drawContours(img, contours, -1, (0,255,0), 3)
print("jumlah kontur ",contours)

# Inisialisasi list untuk menyimpan pusat dari setiap bentuk
circle_centers = []
rectangle_centers = []
square_centers = []
polygon_centers = []

# # Loop melalui setiap kontur
# for contour in contours:
#     # Hitung jumlah sisi dari kontur
#     approx = cv2.approxPolyDP(contour,0.01* cv2.arcLength(contour, True), True)
#     sides = len(approx)
    
#     # Hitung momen dari kontur
#     M = cv2.moments(contour)
    
#     # Peroleh pusat massa (centroid)
#     if M["m00"] != 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#     else:
#         cX, cY = 0, 0
    
#     # Tentukan jenis bentuk berdasarkan jumlah sisi
#     if sides == 3:
#         # circle_centers.append((cX, cY))
#         cv2.drawContours(thresh, [contour], 0, (0, 255, 0), 2)  # Gambar Segitiga
#     elif sides == 4:
#         x, y, w, h = cv2.boundingRect(contour)
#         aspect_ratio = float(w)/h
#         if 0.95 <= aspect_ratio <= 1.05:
#             square_centers.append((cX, cY))
#             cv2.drawContours(thresh, [contour], 0, (0, 0, 255), 2)  # Gambar kotak
#         else:
#             rectangle_centers.append((cX, cY))
#             cv2.drawContours(thresh, [contour], 0, (255, 0, 0), 2)  # Gambar persegi panjang
#     elif sides == 5:
#         polygon_centers.append((cX, cY))
#         cv2.drawContours(thresh, [contour], 0, (255, 255, 0), 2)  # Gambar poligon
#     elif sides == 10:
#         print("Bintang")
#     else:
#         circle_centers.append((cX, cY))
#         print("lingkaran")

# Tampilkan citra dengan bentuk-bentuk yang ditemukan
cv2.imshow('Shapes', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Tampilkan pusat dari setiap bentuk
print("Circle Centers:", circle_centers)
print("Square Centers:", square_centers)
print("Rectangle Centers:", rectangle_centers)
print("Polygon Centers:", polygon_centers)