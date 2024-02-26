from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import os
import uuid
from PIL import Image
import io

#importing pybase64 module
import pybase64

# Setting Treshold
# mengubah dibawah nilai ini menjadi hitam
min_tresh = 50  
# diatas nilai diatas menjadi putih
max_tresh = 255

app = Flask(__name__)

def base64_to_image(base64_string, filename):
    #decode base64 string data
    decoded_data=pybase64.b64decode((base64_string))
    #write the decoded data back to original format in  file
    img_file = open(filename, 'wb')
    img_file.write(decoded_data)
    img_file.close()

@app.route('/ljkChecker', methods=['POST'])
def ljk_checker():
    try:
        data = request.json
        token = data['token']
        image_base64 = data['image']

        # Generate unique filename
        filename = str(uuid.uuid4()) + ".png"
        filepath = os.path.join("./images", filename)  # Simpan di folder "images" (pastikan folder tersebut sudah ada)

        # Save image to file using base64_to_image function
        base64_to_image(image_base64, filepath)
        print("File saved at:", filepath)
        # result_img_original = cv2.imread('./images/'+filename)
        result_img_original = cv2.imread('../LJK_Paylite_Edu.jpg')
        
        # Tampilkan hasil resize
        height, width = result_img_original.shape[:2]
        max_height = 600
        max_width = 800

        # Check if any of the dimensions exceed the maximum limits
        if height > max_height or width > max_width:
            # Get the scaling factor
            scale = max_height / height if height > width else max_width / width
            # Resize the image
            img = cv2.resize(result_img_original, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            
        # Konversi gambar ke skala abu-abu
        result_img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Thresholding untuk mengambil bentuk berwarna hitam hingga abu-abu
        _, thresh = cv2.threshold(result_img_gray, min_tresh, max_tresh, cv2.THRESH_BINARY)
        # # Tampilkan hasil resize
        # height, width = thresh.shape[:2]
        # max_height = 500
        # max_width = 700

        # # Check if any of the dimensions exceed the maximum limits
        # if height > max_height or width > max_width:
        #     # Get the scaling factor
        #     scale = max_height / height if height > width else max_width / width
        #     # Resize the image
        #     img = cv2.resize(thresh, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            
        cv2.imshow("original",img)
        cv2.imshow("Gray",result_img_gray)
        cv2.imshow("Treshold",thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Response
        response_data = {
            "token": token,
            "status": "OK",  # Atur status sesuai kebutuhan
            "image_filepath": filepath
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
