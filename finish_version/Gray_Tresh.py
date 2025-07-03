import cv2

def clasifier(image_crop,minimum):
    imgray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray  ", imgray)
    # kalibrasi
    ret, thresh = cv2.threshold(imgray, minimum, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Tresh ", thresh)
    
    return ret, imgray, thresh