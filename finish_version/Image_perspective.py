import cv2
import numpy as np

def transform(image, position, out_width, out_height):
    # --- TRANSFORMASI PERSPEKTIF ---
    pts1 = np.float32(position) # Kiri Atas, Kanan Atas, Kanan Bawah dan Kiri Bawah
    pts2 = np.float32([
        [0, 0],
        [out_width - 1, 0],
        [out_width - 1, out_height - 1],
        [0, out_height - 1]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    hasilCrop = cv2.warpPerspective(image, matrix, (out_width, out_height))
    
    return hasilCrop