import cv2
import numpy as np

print(cv2.__version__)

# img = cv2.imread("./UpLeft.png")
img = cv2.imread("./UpRight.png")
# img = cv2.imread("./BottomRight.png")
# img = cv2.imread("./BottomLeft.png")
# # img = cv2.imread("./LJK-QR-v1.0.jpg")
# height, width = img.shape[:2]
# max_height = 800
# scaling_factor = max_height / height
# new_width = int(width * scaling_factor)
# new_height = int(height * scaling_factor)
# img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# cv2.imshow("Original : ",img_rgb)

qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
print(retval)
print(decoded_info)
print(points)
# [0] = top-left (UpLeft)
# [1] = top-right (UpRight)
# [2] = bottom-right (BottomRight)
# [3] = bottom-left (BottomLeft)
print("==========")
qr_position = {}

if retval:
  for i, (info, pts) in enumerate(zip(decoded_info, points)):

      center_calculate = np.array(points[i])
      center = center_calculate.mean(axis=0)
      cx, cy = center

      qr_position[info] = [cx, cy]


else:
  print("QR Tidak terdeteksi, Pastikan foto dengan jelas")
  
print(qr_position)

# img = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 3)

# for s, p in zip(decoded_info, points):
#     img = cv2.putText(img, s, p[0].astype(int),
#                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

# cv2.imshow("Hasil : ",img)