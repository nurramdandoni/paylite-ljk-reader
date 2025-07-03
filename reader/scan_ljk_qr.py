import cv2
import numpy as np

# Load gambar
img = cv2.imread('LJK QR-v1.0.jpg')

# Inisialisasi QRCode detector
qr_decoder = cv2.QRCodeDetector()

# Deteksi dan decode multiple QR
retval, decoded_info, points, _ = qr_decoder.detectAndDecodeMulti(img)
print(retval)
print(decoded_info)

# Buat dict untuk menyimpan posisi QR
qr_positions = {}

if retval:
    for info, pts in zip(decoded_info, points):
        if info in ['UpLeft', 'UpRight', 'BottomLeft', 'BottomRight']:
            # Hitung titik tengah QR
            pts = pts[0]  # ambil koordinat dari QR
            center_x = int(np.mean(pts[:, 0]))
            center_y = int(np.mean(pts[:, 1]))

            qr_positions[info] = (center_x, center_y)

            # Gambar titik tengah di gambar (optional)
            cv2.circle(img, (center_x, center_y), 10, (0, 255, 0), -1)
            cv2.putText(img, info, (center_x + 10, center_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
# Tampilkan hasilnya (optional)
# cv2.imshow("QR Centers", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print koordinat pusat masing-masing QR
print("Koordinat QR Code:")
for key, val in qr_positions.items():
    print(f"{key}: {val}")