import json
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas
from tqdm import tqdm

def _parser(items:list) -> list:
    """
    Transforma array de strings a array de integers
    """
    return [int(float(item)) for item in items]

def _get_contours(row) -> list:
    """
    Devuelve un array de arrays de numpy,uno por segmento del edificio
    """
    #print(row)
    coordenadas = row["PolygonWKT_Pix"]
    if "EMPTY" in coordenadas:
        return []
    else:
        #building_borders = [np.array(i["segmentation"][0], "int32").reshape((-1,2)).tolist() for i in annotations["annotations"] if i["image_id"] == image["id"]]
        coordenadas = coordenadas[10:-2]
        coordenadas = coordenadas.split("),(")
        coordenadas = [building.split(",") for building in coordenadas]
        coordenadas = [[_parser(i.split(" ")[0:-1])for i in building] for building in coordenadas]
    return coordenadas

def SN1(label_data:pandas.DataFrame, 
        img_folder_path:str, 
        label_folder_path:str, 
        result_label_filename:str):
    previous_image = ""
    sn1_labels = []
    last_index = -1

    for i, row in tqdm(label_data.iterrows(), total=label_data.shape[0]):
        if row["ImageId"] != previous_image:

            im = cv2.imread(os.path.join(img_folder_path, f'3band_{row["ImageId"]}.tif') )
            height, width = im.shape[0], im.shape[1]
            sn1_labels.append({"ImageId":row["ImageId"], "height":height, "width":width, "buildings":[]})
            last_index += 1
            previous_image = row["ImageId"]
            

        for building in _get_contours(row):
            sn1_labels[last_index]["buildings"].append(building)

    with open( os.path.join(label_folder_path, result_label_filename), "w")as f:
        json.dump(sn1_labels, f)
        
    #print(len(sn1_labels))
    #print(len(os.listdir(img_folder_path)))


def satellite_images_kaggle(annotation_file_path:str = "personal/annotation.json", result_file_path:str = "personal/result.json"):
    with open(annotation_file_path, "r") as f:
        annotations = json.load(f)

    final_json = []

    for image in tqdm(annotations["images"]):
        building_borders = [np.array(i["segmentation"][0], "int32").reshape((-1,2)).tolist() for i in annotations["annotations"] if i["image_id"] == image["id"]]
        image_id = image["id"]
        image_name = image["file_name"]
        final_instance = {
            "image_id": image_id,
            "file_name": image_name,
            "mask_name": image_name[:-3] + "png",
            "coordinates": building_borders,
            "width": image["width"],
            "height": image["height"]
            }
        final_json.append(final_instance)

    print(len(final_json))
    with open(result_file_path, "w") as f:
        json.dump(final_json, f)
