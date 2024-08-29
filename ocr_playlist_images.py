import base64

import easyocr
import numpy as np
from collections import defaultdict


def ocr_data(image):
    reader = easyocr.Reader(['ko', 'en'])
    byte_image = base64_to_bytes(image)
    ocr_data = reader.readtext(byte_image)
    return extract_playlist_title_artists(ocr_data)


def base64_to_bytes(base64_string):
    # Base64 문자열에서 바이트로 디코딩
    return base64.b64decode(base64_string)


def extract_playlist_title_artists(ocr_data):
    texts = [(item[1],
              np.mean([coord[1] for coord in item[0]]),
              np.min([coord[0] for coord in item[0]]),
              np.max([coord[1] for coord in item[0]]) - np.min([coord[1] for coord in item[0]])  # 높이
              ) for item in ocr_data]

    x_coords = [int(item[2]) for item in texts]
    x_freq = defaultdict(int)
    for x in x_coords:
        for i in range(x - 10, x + 11):
            x_freq[i] += 1

    most_common_x = max(x_freq, key=x_freq.get)

    filtered_texts = [item for item in texts if abs(item[2] - most_common_x) <= 10]

    filtered_texts.sort(key=lambda x: x[1])

    i = 0
    json_result = []
    while i < len(filtered_texts):
        json_result.append({
            "songTitle": filtered_texts[i][0],
            "artistNames": filtered_texts[i + 1][0]
        })
        i = i + 2

    return json_result
