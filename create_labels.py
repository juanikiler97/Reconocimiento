import json
import cv2
import numpy as np
import os
import tqdm

from helper_functions import plot_single_image, plot_multiple_images

ANNOTATION_FILE_PATH = "personal/result.json/"
RESULT_FILE_PATH = "personal/train/labels/"
IMAGE_FILE_PATH = "personal/train/images/"



with open( ANNOTATION_FILE_PATH, "r") as f:
    annotations = json.load(f)

os.makedirs(RESULT_FILE_PATH, exist_ok=True)
for image in tqdm.tqdm(annotations):
    #print(image)
    coordenadas = [np.array(i, dtype="int32") for i in image["coordinates"]]
    mask = np.zeros((image["width"], image["height"]), dtype="int32")
    #print(mask.shape)
    cv2.drawContours(mask, coordenadas, -1, 1, thickness=cv2.FILLED)
    cv2.imwrite(RESULT_FILE_PATH + image["mask_name"], mask)

test_path = (annotations[0]["file_name"], annotations[0]['mask_name'])
test_image = cv2.imread(f"{IMAGE_FILE_PATH}/{test_path[0]}")[:,:,::-1]
test_label = np.float32(cv2.imread(f"{RESULT_FILE_PATH}/{test_path[1]}", cv2.IMREAD_GRAYSCALE))
plot_multiple_images([test_image, test_label])