import cv2
import numpy as np

# --- CONFIG ---
total_soal = 40
kunci_jawaban = [
    'B', 'D', 'B', 'C', 'A', 'D', 'D', 'D', 'B', 'C',
    'A', 'B', 'A', 'B', 'C', 'D', 'C', 'B', 'C', 'C',
    'B', 'C', 'B', 'A', 'A', 'A', 'B', 'C', 'B', 'A',
    'D', 'D', 'B', 'D', 'A', 'D', 'C', 'B', 'A', 'D'
    ]
preview_max_width = 400  # Lebar maksimum saat preview (biar nggak kegedean di layar)
output_width, output_height = 250, 400  # Ukuran hasil crop

# --- LOAD GAMBAR ---
original = cv2.imread('./ljk_miring.jpg')
# original = cv2.imread('./ljk_miring2.jpg')
# original = cv2.imread('../omr-doni/LJK_Paylite_Edu_v21s.jpg')
if original is None:
    print("Gambar tidak ditemukan!")
    exit()

# Hitung rasio scaling preview
h, w = original.shape[:2]
scale = preview_max_width / w if w > preview_max_width else 1.0
preview = cv2.resize(original, (int(w * scale), int(h * scale)))

# --- PILIH TITIK MANUAL DI GAMBAR YANG DIRESIZE ---
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        cv2.circle(preview, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Klik 4 titik: kiri atas, kanan atas, kanan bawah, dan kiri bawah", preview)
        # Simpan titik dalam skala asli (supaya crop akurat)
        real_x = int(x / scale)
        real_y = int(y / scale)
        points.append((real_x, real_y))

cv2.imshow("Klik 4 titik: kiri atas, kanan atas, kanan bawah, dan kiri bawah", preview)
cv2.namedWindow("Klik 4 titik: kiri atas, kanan atas, kanan bawah, dan kiri bawah", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Klik 4 titik: kiri atas, kanan atas, kanan bawah, dan kiri bawah", preview_max_width, int(h * scale))
cv2.setMouseCallback("Klik 4 titik: kiri atas, kanan atas, kanan bawah, dan kiri bawah", click_event)

print("Klik 4 titik: kiri atas → kanan atas → kanan bawah → kiri bawah...")

# Tunggu klik titik
while True:
    if len(points) == 4:
        break
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cv2.destroyAllWindows()

if len(points) != 4:
    print("Kamu belum klik 4 titik.")
    exit()

# --- TRANSFORMASI PERSPEKTIF ---
pts1 = np.float32(points)
pts2 = np.float32([
    [0, 0],
    [output_width, 0],
    [output_width, output_height],
    [0, output_height]
])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
hasilCrop = cv2.warpPerspective(original, matrix, (output_width, output_height))

# --- TAMPILKAN HASIL ---
cv2.imshow("Foto", preview)
cv2.imshow("Hasil Transformasi", hasilCrop)
cv2.imwrite("hasil_crop.jpg", hasilCrop)

imgray = cv2.cvtColor(hasilCrop, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Gray  ", imgray)
# kalibrasi
minimum = 125 # diatas 150 akan menjadi putih
ret, thresh = cv2.threshold(imgray, minimum, 255, cv2.THRESH_BINARY)
cv2.imshow("Tresh ", thresh)



# PROSES JAWABAN
all_centers = [[0, 0],
    [output_width, 0],
    [output_width, output_height],
    [0, output_height]]
print(all_centers)
# # roi_crop = thresh[all_centers[0][1]:all_centers[3][1],all_centers[0][0]:all_centers[3][0]]
# # roi_crop_gray = hasilCrop[all_centers[0][1]:all_centers[3][1],all_centers[0][0]:all_centers[3][0]]
roi_crop = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
heightCrop, widthCrop = roi_crop.shape[:2]
# Jumlah kotak lebar
num_boxes_width = 36

# Jarak antara titik-titik untuk lebar
width_interval = output_width / num_boxes_width  # Pembagi lebar
# width_interval = 11  # Pembagi lebar

# Jumlah kotak tinggi
num_boxes_height = 53

# Jarak antara titik-titik untuk tinggi
height_interval = output_height / num_boxes_height  # Pembagi tinggi
# height_interval = 10  # Pembagi tinggi

# Inisialisasi array untuk menyimpan hasil analisis
result = np.zeros((num_boxes_height, num_boxes_width), dtype=np.int_)

no_soal = [0 for _ in range(60)] #untuk menyimpan box/koordinat bernilai A-E
pixel_opsi_soal = [[0 for _ in range(5)] for _ in range(60)]  #untuk menyimpan jumlah pixel setiap opsi dalam 1 nomor

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
        # imgray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY) 
        ret2, thresh2 = cv2.threshold(roi2, minimum, 255, 0)
            # cv2.imshow("cut",imgray2)
        black_pixels = np.sum(thresh2 == 0) #hitung jumlah pixel hitam dalam kotak thresh2
        # print("piksel",black_pixels)
        param_piksel_count = 25
        if black_pixels > param_piksel_count:  # Ubah ambang batas sesuai kebutuhan
        #     # Gambar kotak dengan warna hijau
              if 10 < i < 52:
                cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 255, 0), 1)
        
        # ambil Data Jawaban dan komparasi nilai jawaban  ke array pg_look
        if 39 < i < 45:
             # assgin baris jawaban 1
            if 0 < j < 6:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[i-40] = pg_look[j]
                    pixel_opsi_soal[i-40][j-1] = black_pixels
            if 6 < j < 12:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+10] = pg_look[j-6]
                    pixel_opsi_soal[(i-40)+10][j-7] = black_pixels
            if 12 < j < 18:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+20] = pg_look[j-12]
                    pixel_opsi_soal[(i-40)+20][j-13] = black_pixels
            if 18 < j < 24:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+30] = pg_look[j-18]
                    pixel_opsi_soal[(i-40)+30][j-19] = black_pixels
            if 24 < j < 30:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+40] = pg_look[j-24]
                    pixel_opsi_soal[(i-40)+40][j-25] = black_pixels
            if 30 < j < 36:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-40)+50] = pg_look[j-30]
                    pixel_opsi_soal[(i-40)+50][j-31] = black_pixels
                    
        if 45 < i < 51:
             # assgin baris jawaban 1
            if 0 < j < 6:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[i-41] = pg_look[j]
                    pixel_opsi_soal[i-41][j-1] = black_pixels
            if 6 < j < 12:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+10] = pg_look[j-6]
                    pixel_opsi_soal[(i-41)+10][j-7] = black_pixels
            if 12 < j < 18:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+20] = pg_look[j-12]
                    pixel_opsi_soal[(i-41)+20][j-13] = black_pixels
            if 18 < j < 24:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+30] = pg_look[j-18]
                    pixel_opsi_soal[(i-41)+30][j-19] = black_pixels
            if 24 < j < 30:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+40] = pg_look[j-24]
                    pixel_opsi_soal[(i-41)+40][j-25] = black_pixels
            if 30 < j < 36:
                if black_pixels > param_piksel_count:
                    cv2.rectangle(roi_crop, (start_x+2, start_y+2), (end_x-2, end_y-2), (0, 0, 255), 1)
                    no_soal[(i-41)+50] = pg_look[j-30]
                    pixel_opsi_soal[(i-41)+50][j-31] = black_pixels
# print("height :", height)
# print("height cell :", height/53)
# print("width :", width)
# print("width cell :", width/36)


# print("height crop : ",output_height)
# print("width crop : ",output_width)
# cv2.imshow("Ori", im)
# cv2.imshow("Mapping :: Step 2", threshCrop)
# cv2.imshow("ROI Gray :: Step 3", imgray_crop)
cv2.imshow("ROI Crop Pixel Check :: Step 3", roi_crop)
print("Jumlah Pixel Opsi")
print(pixel_opsi_soal)
print("Jawaban Peserta")
benar = 0
salah = 0
for i in range(len(kunci_jawaban)):
    data = pixel_opsi_soal[i]
    index_jawaban = data.index(max(data))
    no_soal[i] = pg_look[index_jawaban+1]
    if no_soal[i] == kunci_jawaban[i]:
        benar += 1
    else:
        salah += 1
print(no_soal)
print("total Benar : ",benar)
print("total Salah : ",salah)
# AKHIR PROSES JAWABAN
cv2.waitKey(0)
cv2.destroyAllWindows()
