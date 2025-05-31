import cv2
import numpy as np

def proses_ljk(img, titik, kunci):
    print(titik)
    pts1 = np.float32(titik)
    pts2 = np.float32([[0,0], [600,0], [0,800], [600,800]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_crop = cv2.warpPerspective(img, matrix, (600, 800))

    abu = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    _, binar = cv2.threshold(abu, 127, 255, cv2.THRESH_BINARY_INV)

    hasil = []
    jawaban_user = []

    # asumsi posisi LJK 5 kolom x 10 baris
    for i in range(len(kunci)):
        x = (i % 5) * 100 + 10
        y = (i // 5) * 80 + 10
        kotak = binar[y:y+60, x:x+80]
        total = cv2.countNonZero(kotak)

        if total > 500:  # threshold isian hitam
            jawaban_user.append(chr(65 + (i % 5)))  # A, B, C, D, E
        else:
            jawaban_user.append('-')

    benar = sum(1 for i, j in zip(jawaban_user, kunci) if i == j)
    salah = len(kunci) - benar

    return {
        'jawaban_user': jawaban_user,
        'benar': benar,
        'salah': salah,
        'skor': round((benar / len(kunci)) * 100, 2)
    }
