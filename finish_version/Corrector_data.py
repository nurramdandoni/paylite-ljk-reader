import cv2
import numpy as np

def correction(imgray,output_width,output_height, minimum, kunci_jawaban):
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
    
    # cv2.imshow("ROI Crop Pixel Check :: Step 3", roi_crop)
    print("Jumlah Pixel Opsi")
    print(pixel_opsi_soal)
    print("Jawaban Peserta")
    benar = 0
    salah = 0
    for i in range(len(kunci_jawaban)):
        data = pixel_opsi_soal[i]
        index_jawaban = data.index(max(data))
        # if index_jawaban > 0:
        no_soal[i] = pg_look[index_jawaban+1]
        if no_soal[i] == kunci_jawaban[i]:
            benar += 1
        else:
            salah += 1
        # else:
        #     no_soal[i] = "-"
    print(no_soal)
    print("total Benar : ",benar)
    print("total Salah : ",salah)
    
    return no_soal, benar, salah, roi_crop