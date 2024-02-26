import numpy as np
import cv2
img = cv2.imread('LJK_Paylite_Edu_v21s.jpg')
# Tampilkan hasil resize
height, width = img.shape[:2]
max_height = 700
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    im = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
# cv2.imshow("Original ",im)
# assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Inisialisasi daftar untuk pusat (pertimbangkan menggunakan kamus untuk organisasi yang lebih baik)

hexagon_centers = []
kotak_centers = []
persegi_centers = []
segitiga_centers = []
for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.001 * peri, True)
    # cv2.drawContours(im, [approx], -1, (0,255,0), 1)
    # print(area)
    if area > 100 :
        # cv2.drawContours(im, [approx], -1, (0,255,0), 1)
        sides = len(approx)
        print(sides)
        # print("area ; ",area)
        # Hitung momen dari kontur
        M = cv2.moments(c)
        
        # Peroleh pusat massa (centroid)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # # Tentukan jenis bentuk berdasarkan jumlah sisi
        if sides == 6:
            segitiga_centers.append(cX)
            segitiga_centers.append(cY)
            cv2.circle(im, (cX,cY),1, (0, 255, 0),1) 
            cv2.drawContours(im, [approx], 0, (0, 255, 0), 1)  # Gambar Segitiga
            print("Area Segitiga : ",area)
        elif sides == 8:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w)/h
            if 0.95 <= aspect_ratio <= 1.05:
                kotak_centers.append(cX)
                kotak_centers.append(cY)
                cv2.circle(im, (cX,cY),1, (255, 0, 0),1) 
                cv2.drawContours(im, [approx], 0, (255, 0, 0), 1)  # Gambar kotak
                print("Area Kotak : ",area)
            else:
                persegi_centers.append(cX)
                persegi_centers.append(cY)
                cv2.circle(im, (cX,cY),1, (18, 242, 255),1) 
                cv2.drawContours(im, [approx], 0, (18, 242, 225), 1)  # Gambar persegi panjang
                print("Area Persegi : ",area)
        # elif sides == 5:
        #     all_centers["polygon"] = (cX, cY)
        #     cv2.drawContours(thresh, [approx], 0, (255, 255, 0), 2)  # Gambar poligon
        # elif sides == 10:
        #     print("Bintang")
        else:
            if area > 300:
                if sides != 4:
                    hexagon_centers.append(cX)
                    hexagon_centers.append(cY)
                    cv2.circle(im, (cX,cY),1, (0, 0, 255),1) 
                    cv2.drawContours(im, [approx], 0, (0, 0, 255), 1)  # Gambar poligon
                    print("Area Segi Enam : ",area)
                    # print("Segi Enam")
# kiri atas, kanan atas, kiri bawah, kanan bawah
all_centers = [hexagon_centers,kotak_centers,persegi_centers,segitiga_centers]
print(all_centers)


# setelah dilakukan perspective akan dicrop

roi_crop = im[all_centers[0][1]:all_centers[3][1],all_centers[0][0]:all_centers[3][0]]
imgray_crop = cv2.cvtColor(roi_crop, cv2.COLOR_BGR2GRAY)
retCrop, threshCrop = cv2.threshold(imgray_crop, 50, 255, 0)
cv2.imshow("Original ",im)
# cv2.imshow("croping", roi_crop)
# cv2.imshow("Original Crop ",roi_crop)
# cv2.imshow("ROI Gray :: Step 1", imgray_crop)
# cv2.imshow("Tresh :: Step 2", threshCrop)
# Ukuran gambar kerja

heightCrop, widthCrop = roi_crop.shape[:2]

# Jumlah kotak lebar
num_boxes_width = 36

# Jarak antara titik-titik untuk lebar
width_interval = widthCrop / num_boxes_width  # Pembagi lebar
# width_interval = 11  # Pembagi lebar

# Jumlah kotak tinggi
num_boxes_height = 53

# Jarak antara titik-titik untuk tinggi
height_interval = heightCrop / num_boxes_height  # Pembagi tinggi
# height_interval = 10  # Pembagi tinggi

# Inisialisasi array untuk menyimpan hasil analisis
result = np.zeros((num_boxes_height, num_boxes_width), dtype=np.int_)

# Loop melalui setiap baris
for i in range(num_boxes_height):
    # Loop melalui setiap kotak dalam baris
    for j in range(num_boxes_width):
        # Potong kotak dari gambar
        start_x = int(j * width_interval)
        # print("start_x : ",start_x)
        end_x = int((j + 1) * width_interval)
        start_y = int(i * height_interval)
        end_y = int((i + 1) * height_interval)
        # Tandai kotak sebagai hitam jika jumlah piksel hitam melebihi ambang batas
        cv2.rectangle(roi_crop, (start_x, start_y), (end_x, end_y), (150, 150, 150), 1) # garis bantu boleh dinyalakan
        # if i == 0:
        roi2 = roi_crop[start_y:end_y,start_x:end_x]
        imgray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY) 
        ret2, thresh2 = cv2.threshold(imgray2, 50, 255, 0)
            # cv2.imshow("cut",imgray2)
        black_pixels = np.sum(thresh2 == 0) #hitung jumlah pixel hitam dalam kotak thresh2
        # print(black_pixels)
        if black_pixels > 25:  # Ubah ambang batas sesuai kebutuhan
        #     result[i, j] = 1
        #     # Gambar kotak dengan warna hijau
              cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 255, 0), 1)

print("height :", height)
print("height cell :", height/53)
print("width :", width)
print("width cell :", width/36)


# print("height crop : ",heightCrop)
# print("width crop : ",widthCrop)
# cv2.imshow("Ori", im)
# cv2.imshow("ROI Gray :: Step 3", imgray_crop)
# cv2.imshow("Mapping :: Step 2", threshCrop)
cv2.imshow("ROI Crop Pixel Check :: Step 3", roi_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()