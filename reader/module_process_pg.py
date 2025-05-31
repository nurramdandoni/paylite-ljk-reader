import numpy as np
import cv2
img = cv2.imread('../omr-doni/LJK_Paylite_Edu_v21s.jpg') # success karena lurus
# img = cv2.imread('./ljk_miring.jpg') # success karena lurus
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
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY)
cv2.imshow("Tresh ", thresh)
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
    if area > 100 :
        sides = len(approx)
        print(sides)
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
            cv2.circle(im, (cX,cY),1, (0, 255, 0),5) 
            cv2.drawContours(im, [approx], 0, (0, 255, 0), 1)  # Gambar Segitiga
            print("Area Segitiga : ",area)
        elif sides == 8:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w)/h
            if 0.95 <= aspect_ratio <= 1.05:
                kotak_centers.append(cX)
                kotak_centers.append(cY)
                cv2.circle(im, (cX,cY),1, (255, 0, 0),5) 
                cv2.drawContours(im, [approx], 0, (255, 0, 0), 1)  # Gambar kotak
                print("Area Kotak : ",area)
            else:
                persegi_centers.append(cX)
                persegi_centers.append(cY)
                cv2.circle(im, (cX,cY),1, (18, 242, 255),5) 
                cv2.drawContours(im, [approx], 0, (18, 242, 225), 1)  # Gambar persegi panjang
                print("Area Persegi : ",area)
        else:
            if area > 300:
                if sides != 4:
                    hexagon_centers.append(cX)
                    hexagon_centers.append(cY)
                    cv2.circle(im, (cX,cY),1, (0, 0, 255),5) 
                    cv2.drawContours(im, [approx], 0, (0, 0, 255), 1)  # Gambar poligon
                    print("Area Segi Enam : ",area)


# setelah dilakukan perspective akan dicrop
print("kiri atas ",hexagon_centers)
print("kanan atas ",kotak_centers)
print("kiri bawah ",persegi_centers)
print("kanan bawah ",segitiga_centers)

# awal perspektif
pts1 = np.float32([hexagon_centers, kotak_centers, persegi_centers, segitiga_centers])

pts2 = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(imgray, matrix, (max_width, max_height))
cv2.imshow("Perspektif ", result)
# selesai perspektif

all_centers = [hexagon_centers,kotak_centers,persegi_centers,segitiga_centers]
print(all_centers)
roi_crop = im[all_centers[0][1]:all_centers[3][1],all_centers[0][0]:all_centers[3][0]]
imgray_crop = cv2.cvtColor(roi_crop, cv2.COLOR_BGR2GRAY)
retCrop, threshCrop = cv2.threshold(imgray_crop, 50, 255, 0)
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

no_soal = [0 for _ in range(60)] #untuk menyimpan box/koordinat bernilai A-E

pg_look = ["","A","B","C","D","E"]
# Loop melalui setiap baris
for i in range(num_boxes_height):
    # print("ini i ke ",i)
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
              if 10 < i < 52:
                # print("Baris,Kolom ",{i},{j})
                cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 255, 0), 1)
        
        # ambil Data Jawaban dan komparasi nilai jawaban  ke array pg_look
        if 39 < i < 45:
             # assgin baris jawaban 1
            if 0 < j < 6:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[i-40] = pg_look[j]
            if 6 < j < 12:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+10] = pg_look[j-6]
            if 12 < j < 18:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+20] = pg_look[j-12]
            if 18 < j < 24:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+30] = pg_look[j-18]
            if 24 < j < 30:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+40] = pg_look[j-24]
            if 30 < j < 36:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+50] = pg_look[j-30]
                    
        if 45 < i < 51:
             # assgin baris jawaban 1
            if 0 < j < 6:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[i-41] = pg_look[j]
            if 6 < j < 12:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+10] = pg_look[j-6]
            if 12 < j < 18:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+20] = pg_look[j-12]
            if 18 < j < 24:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+30] = pg_look[j-18]
            if 24 < j < 30:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+40] = pg_look[j-24]
            if 30 < j < 36:
                if black_pixels > 55:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+50] = pg_look[j-30]




# resize window
# Resize gambar ke ukuran yang lebih kecil, misal 50% ukuran asli
scale_percent = 70  # persen skala dari ukuran asli
width = int(im.shape[1] * scale_percent / 100)
height = int(im.shape[0] * scale_percent / 100)
dim = (width, height)

# Resize

# Tampilkan gambar yang sudah di-resize
resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
cv2.imshow("Ori Foto ", resized_img)
resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
cv2.imshow("Ori", resized)
print("Jawaban Peserta")
print(no_soal)
cv2.waitKey(0)
cv2.destroyAllWindows()