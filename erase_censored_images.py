import pickle
import os
import cv2
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

LABEL_FILE_PATH = "personal/final_dataset/labels/"
IMAGE_FILE_PATH = "personal/final_dataset/images/"

NEGRO = [0,0,0]

if __name__ == "__main__":

    raras = []
    if os.path.isfile("raras.pkl"):
        with open("raras.pkl", "rb") as f:
            raras = pickle.load(f)
        for index, rara in tqdm( enumerate(raras)):
        #print(os.path.join(IMAGE_FILE_PATH, raras[index]))
            os.remove(os.path.join(IMAGE_FILE_PATH, raras[index]))
            os.remove(os.path.join(LABEL_FILE_PATH, raras[index][:-3] + "png"))
    else:
        for file in tqdm(os.listdir(IMAGE_FILE_PATH)):
            image = cv2.imread( os.path.join(IMAGE_FILE_PATH, file) )
            #image = cv2.imread( "personal/train/images/000000000590.jpg" )
            #label = cv2.imread( "personal/train/labels/000000000590.png" )
            #print(np.unique(label))
            black  = np.count_nonzero(np.all(image==NEGRO,axis=2))
            #plot_multiple_images([image, label * 255])
            if black > 200:
                raras.append(file)
                os.remove(os.path.join(IMAGE_FILE_PATH, os.path.join(IMAGE_FILE_PATH, file)))
                os.remove(os.path.join(LABEL_FILE_PATH, os.path.join(IMAGE_FILE_PATH, file)[:-3] + "png"))

        with open("raras.pkl", "wb") as f:
            pickle.dump(raras, f)

    

