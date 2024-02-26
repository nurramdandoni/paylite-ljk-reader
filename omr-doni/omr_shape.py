import cv2

def detect_and_draw_boxes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to extract black regions
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw bounding boxes around black regions
    for contour in contours:
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw the bounding box on the original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)
    
    return image

# Read the image
image = cv2.imread('LJK2.jpg')

# Detect and draw bounding boxes around black regions
result_image = detect_and_draw_boxes(image)

# Display the result
cv2.imshow('Detected Boxes', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
