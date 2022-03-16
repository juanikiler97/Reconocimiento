import pickle
import os
import cv2
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

def erase_censored_images(img_folder_path:str, label_folder_path:str):
    print(img_folder_path)
    NEGRO = [0,0,0]
    raras = []
    if os.path.isfile("raras.pkl"):
        with open("raras.pkl", "rb") as f:
            raras = pickle.load(f)
        for index, rara in tqdm( enumerate(raras)):
            os.remove(os.path.join(img_folder_path, raras[index]))
            os.remove(os.path.join(label_folder_path, raras[index][:-3] + "png"))
    else:
        for file in tqdm(os.listdir(img_folder_path)):
            image = cv2.imread( os.path.join(img_folder_path, file) )
            black  = np.count_nonzero(np.all(image==NEGRO,axis=2))
            if black > 200:
                raras.append(file)
                os.remove(os.path.join(img_folder_path, file))
                os.remove(os.path.join(label_folder_path, file)[:-3] + "png")


    

