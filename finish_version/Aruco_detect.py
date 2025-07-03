import cv2

def detector(img_file):
    # Load gambar
    image = img_file

    # Setup ArUco dictionary dan detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    # Deteksi marker
    corners, ids, _ = detector.detectMarkers(image)
    
    # list kordinat
    data_shape = [[] for _ in range(4)]

    # Tampilkan hasil deteksi
    if ids is not None:
        for i in range(len(ids)):
            c = corners[i][0]
            center_x = int((c[0][0] + c[2][0]) / 2)
            center_y = int((c[0][1] + c[2][1]) / 2)
            cv2.circle(image, (center_x, center_y), 5, (0, 255, 0), -1)
            cv2.putText(image, f"ID {ids[i][0]}", (center_x + 10, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(f"✅ Detected ID: {ids[i][0]} at ({center_x}, {center_y})")
            
            marker_id = ids[i][0]
            if marker_id < len(data_shape):  # pastikan ID dalam range
                data_shape[marker_id].append((center_x, center_y))
    else:
        print("⚠️ Tidak ada ArUco marker terdeteksi.")

    # Tampilkan gambar
    resized_image = cv2.resize(image, (300, 400))
    return data_shape, resized_image

