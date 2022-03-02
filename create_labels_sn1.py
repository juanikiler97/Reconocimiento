import os
import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd
import json

from helper_functions import plot_single_image, plot_multiple_images
from big_ann2less_big_ann import SN1

DATASET_PATH = "personal/SN1_buildings/train/"
IMAGE_FOLDER_PATH = "personal/SN1_buildings/train/3band"

LABEL_FOLDER_PATH = "personal/SN1_buildings/train/summarydata/"
BIG_LABEL_FILE_NAME = "AOI_1_RIO_polygons_solution_3band.csv"
LABEL_FILE_NAME = "sn1_labels.json"

if __name__ == "__main__":
    label_data = None
    if not os.path.isfile( os.path.join(LABEL_FOLDER_PATH, LABEL_FILE_NAME) ):
        with open( LABEL_FOLDER_PATH + BIG_LABEL_FILE_NAME, "r") as f:
            label_data = pd.read_csv(f)
        print(f"AVISO - No se ha detectado el fichero {LABEL_FILE_NAME}, creando nuevo fichero.")
        SN1(label_data=label_data, img_folder_path = IMAGE_FOLDER_PATH, label_folder_path = LABEL_FOLDER_PATH, result_label_filename=LABEL_FILE_NAME)    

    with open(os.path.join(LABEL_FOLDER_PATH, LABEL_FILE_NAME), "r") as f:
        label_data = json.load(f)

    print("Creando labels...")
    os.makedirs( os.path.join(DATASET_PATH, "labels") , exist_ok=True)

    for label in tqdm(label_data):
        mask = np.zeros( (label["height"], label["width"]), dtype="int32")
        coordenadas = [np.array( b, dtype="int32") for b in label["buildings"]]
        cv2.drawContours(mask, coordenadas, -1, 1, thickness=cv2.FILLED)
        cv2.imwrite(os.path.join( DATASET_PATH, "labels", f'3band_{label["ImageId"]}.png' ), mask)