import numpy as np
import cv2

# img = cv2.imread('./ljk_miring.jpg')
# img = cv2.imread('./ljk_miring2.jpg')
img = cv2.imread('./ljk_miring3.jpg')
height, width = img.shape[:2]
max_height = 700
max_width = 600

scale = min(max_width / width, max_height / height)
im = cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

cv2.imshow("ORI : ",imgray)
cv2.imshow("TRESH : ",thresh)

# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# detected_points = []

# for c in contours:
#     area = cv2.contourArea(c)
#     if area < 100:
#         continue

#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#     sides = len(approx)

#     if 4 <= sides <= 8:
#         M = cv2.moments(c)
#         if M["m00"] == 0:
#             continue
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#         detected_points.append((cX, cY))
#         cv2.drawContours(im, [approx], -1, (0, 255, 0), 2)
#         cv2.circle(im, (cX, cY), 5, (255, 0, 0), -1)

# # Urutkan titik berdasarkan posisi spatial (kiri atas, kanan atas, kiri bawah, kanan bawah)
# def sort_points(points):
#     if len(points) != 4:
#         return None
#     points = sorted(points, key=lambda p: p[1])  # sort by y
#     top = sorted(points[:2], key=lambda p: p[0])  # sort top by x
#     bottom = sorted(points[2:], key=lambda p: p[0])  # sort bottom by x
#     return np.float32([top[0], top[1], bottom[0], bottom[1]])

# sorted_points = sort_points(detected_points)
# if sorted_points is None:
#     print("❌ Tidak berhasil mendeteksi 4 titik referensi. Periksa gambar dan threshold.")
#     exit()

# dst_pts = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
# matrix = cv2.getPerspectiveTransform(sorted_points, dst_pts)
# warp = cv2.warpPerspective(im, matrix, (max_width, max_height))

# # Tampilkan hasil
# scale_percent = 70  # persen skala dari ukuran asli
# width = int(warp.shape[1] * scale_percent / 100)
# height = int(warp.shape[0] * scale_percent / 100)
# dim = (width, height)

# # Resize
# # Tampilkan gambar yang sudah di-resize
# resized_img_ori = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
# resized_img = cv2.resize(warp, dim, interpolation=cv2.INTER_AREA)
# cv2.imshow("Hasil Foto", resized_img_ori)
# cv2.imshow("Hasil Perspective Correction", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
