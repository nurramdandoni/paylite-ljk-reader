import numpy as np
import cv2
im = cv2.imread('LJK_Paylite_Edu_mark.jpg')
# Tampilkan hasil resize
height, width = im.shape[:2]
max_height = 700
max_width = 800

# Check if any of the dimensions exceed the maximum limits
if height > max_height or width > max_width:
    # Get the scaling factor
    scale = max_height / height if height > width else max_width / width
    # Resize the image
    img = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
# cv2.imshow("Original ",im)
# assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)
    # print(i, approx)
    # print(i)
    # if area < 5000:
    print(area)
    side = cv2.drawContours(img, contours, i, (0,255,0), 1)
    
    # Hitung momen dari kontur
    M = cv2.moments(c)
    # Peroleh pusat massa (centroid)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
            
    print(len(approx))
    x, y, w, h = cv2.boundingRect(approx)
    x_mid = int(x+w/3)
    y_mid = int(y + h/1.5)
        
    coord_text = (x_mid, y_mid)
    color = (0,0,255)
    font = cv2.FONT_HERSHEY_DUPLEX
    if area < 10000 and area > 150:  
        if len(approx) == 3:
            cv2.putText(img, "Segitiga",coord_text,font, 0.5, color,1)
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w)/h
            if 0.95 <= aspect_ratio <= 1.05:
                cv2.putText(img, "Kotak",coord_text,font, 0.5, color,1)
            else:
                cv2.putText(img, "Persegi",coord_text,font, 0.5, color,1)
        elif len(approx) == 5:
            cv2.putText(img, "Polygon",coord_text,font, 0.5, color,1)
        elif len(approx) == 6:
            cv2.putText(img, "Hexagon",coord_text,font, 0.5, color,1)
        else:
            cv2.putText(img, "Lingkaran",coord_text,font, 0.5, color,1)
            
    # # print(area)
    # # if area < 1000:
    # #     print(len(approx))
    # #     cv2.drawContours(im, (approx), -1, (0,255,0), 2)
cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()