import numpy as np
import cv2
import imutils

# Baca gambar
img = cv2.imread('LJKKosong_page-0001.jpg')
# img = cv2.imread('miring.jpeg')
# Resizing the image to fit the window
# height, width = img.shape[:2]
# max_height = 600
# max_width = 800

# # Check if any of the dimensions exceed the maximum limits
# if height > max_height or width > max_width:
#     # Get the scaling factor
#     scale = max_height / height if height > width else max_width / width
#     # Resize the image
#     img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    
# Konversi ke HSV
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imshow("hsv",imgHSV)
# Batas warna hitam
lower_black = np.array([0, 0, 0])
upper_black = np.array([220, 220, 220])

# Filter warna
mask = cv2.inRange(imgHSV, lower_black, upper_black)
cv2.imshow("mask",mask)

# Hilangkan warna lain
img_filtered = cv2.bitwise_and(img, img, mask=mask)

# mendapatkan conturs
cnt = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt = imutils.grab_contours(cnt)

# looping jumlah contur
for c in cnt:
    area = cv2.contourArea(c)
    # cv2.drawContours(img_filtered,[c],-1,(0,255,0),2)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)  # Approximation dengan toleransi

    # Cek jika kontur memiliki 4 sisi dan mendekati bentuk persegi
    if len(approx) == 4 and cv2.isContourConvex(approx):
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:  # Cek rasio aspek untuk memastikan persegi
            # cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
            print(area)
            if area > 40 and area < 700:
                print(area)
                cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    
    
    
    # # Cek jika kontur tertutup (untuk menghindari noise)
    # if cv2.isContourConvex(approx):
    #     # Periksa bentuk berdasarkan kedekatan dengan lingkaran
    #     if len(approx) >= 5 and cv2.isContourConvex(approx):
    #         # Hitung circularity (kedekatan dengan lingkaran sempurna)
    #         circularity = 4 * np.pi * area / (peri * peri)
    #         if circularity >= 0.8:
    #             # Gambar kontur sebagai lingkaran
    #             cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    #             print(f"Lingkaran (circularity: {circularity:.2f})")
    #         else:
    #             # Bukan lingkaran sempurna, lanjutkan sebagai bentuk lain
    #             if area > 40 and area < 700:
    #                 print(f"Bentuk lain (area: {area})")
    #                 cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    #     else:
    #         # Bukan lingkaran, lanjutkan sebagai bentuk lain
    #         if area > 50:
    #             print(f"Bentuk lain (area: {area})")
    #             # cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
# Tampilkan hasil
height, width = img.shape[:2]
max_height = 600
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
cv2.imshow("Kotak Hitam", img)
cv2.waitKey(0)
cv2.destroyAllWindows()