import json
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import tqdm

ANNOTATION_FILE_PATH = "personal/annotation.json"
RESULT_FILE_PATH = "personal/result.json"

with open(ANNOTATION_FILE_PATH, "r") as f:
    annotations = json.load(f)

final_json = []

for image in tqdm.tqdm(annotations["images"]):
    building_borders = [np.array(i["segmentation"][0], "int32").reshape((-1,2)).tolist() for i in annotations["annotations"] if i["image_id"] == image["id"]]
    image_id = image["id"]
    image_name = image["file_name"]
    final_instance = {
        "image_id": image_id,
        "file_name": image_name,
        "coordinates": building_borders,
        "width": image["width"],
        "height": image["height"]
        }
    final_json.append(final_instance)

print(len(final_json))
with open(RESULT_FILE_PATH, "w") as f:
    json.dump(final_json, f)
