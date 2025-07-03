import cv2
from Aruco_detect import detector
from Image_perspective import transform
from Gray_Tresh import clasifier
from Corrector_data import correction


total_soal = 40
kunci_jawaban = [
    'B', 'D', 'B', 'C', 'A', 'D', 'D', 'D', 'B', 'C',
    'A', 'B', 'A', 'B', 'C', 'D', 'C', 'B', 'C', 'C',
    'B', 'C', 'B', 'A', 'A', 'A', 'B', 'C', 'B', 'A',
    'D', 'D', 'B', 'D', 'A', 'D', 'C', 'B', 'A', 'D'
    ]

file = cv2.imread("Backup_of_LJK_ArUco.jpg")

# # panggil Detector Marker
position, image = detector(img_file=file)

print("Marker Possition : ",position)
cv2.imshow("Detected ArUco", image)

# # Panggil Perspector
croping = transform(image=file,position=position,out_width=300,out_height=400)
cv2.imshow("Croped", croping)

# croping = cv2.imread("hasil_crop.jpg")

# Panggil GrayScale dan Treshhold
ret, imgray, tresh = clasifier(image_crop=croping,minimum=125)
cv2.imshow("Tresh", tresh)

# Panggil Korentor
jawaban, benar, salah, grid = correction(imgray=imgray,output_width=300,output_height=400,minimum=125,kunci_jawaban=kunci_jawaban)
cv2.imshow("Grid", grid)

cv2.waitKey(0)
cv2.destroyAllWindows()