import cv2

def detect_square_shapes(image):
    # Konversi gambar ke skala abu-abu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Thresholding untuk mengambil bentuk berwarna hitam hingga abu-abu
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    # Temukan kontur
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Inisialisasi list untuk menyimpan koordinat bentuk kotak
    square_shapes_coords = []

    for contour in contours:
        # Hitung jumlah sisi bentuk
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
        # Jika bentuk memiliki 4 sisi (kotak)
        if len(approx) == 4:
            # Dapatkan kotak pembatas untuk bentuk
            x, y, w, h = cv2.boundingRect(approx)
            # Tambahkan koordinat kotak ke list
            square_shapes_coords.append((x, y, x + w, y + h))

    return square_shapes_coords

# Baca gambar
image = cv2.imread('LJKKosong_page-0001.jpg')

# Deteksi bentuk kotak
square_shapes_coords = detect_square_shapes(image)

# Gambar kotak pada gambar asli
if square_shapes_coords:
    for box in square_shapes_coords:
        x1, y1, x2, y2 = box
        # Tandai kotak dengan garis biru tebal 3 pt
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)

# Tampilkan gambar hasil
cv2.imshow('Square Shapes Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
