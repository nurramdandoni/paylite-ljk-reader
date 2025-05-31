from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import json
from .process import proses_ljk

@csrf_exempt
def proses(request):
    if request.method == 'POST':
        file = request.FILES['gambar']
        titik = json.loads(request.POST['titik'])
        kunci = request.POST['kunci'].split(',')

        img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        hasil = proses_ljk(img, titik, kunci)
        return JsonResponse(hasil)

