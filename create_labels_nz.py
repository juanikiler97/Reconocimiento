import os
import cv2
import numpy as np
from tqdm import tqdm

LABELS_PATHS = [
    "personal/nueva_zelanda/test",
    "personal/nueva_zelanda/train",
    "personal/nueva_zelanda/val"
]

if __name__ == "__main__":
    for path in LABELS_PATHS:
        print(f"Cambiando: {path}:")
        for label in tqdm(os.listdir(os.path.join(path, "label"))):
            #print(label)
            im = cv2.imread( os.path.join(path, "label", label) )
            cv2.imwrite( os.path.join(path, "label", label), im // 255)
            
