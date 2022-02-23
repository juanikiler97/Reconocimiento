import pickle
import os
import cv2
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

LABEL_FILE_PATH = "personal/final_dataset/labels/"
IMAGE_FILE_PATH = "personal/final_dataset/images/"

NEGRO = [0,0,0]

def plot_single_image(img, title=None, size=(8, 8), cmap='viridis'):
	plt.figure(figsize=size)
	plt.xticks([])
	plt.yticks([])
	plt.grid(False)
	plt.imshow(img, cmap=cmap)
	if title:
		plt.title(title)
	plt.show()

def plot_multiple_images(imgs, size=(28, 18), cols=None, cmap='viridis', titles=None):
  plt.figure(figsize=size)
  count = len(imgs)
  if cols is None:
    cols = count
  rows = count // cols
  
  if count % cols != 0:
    rows += 1

  for index, img in enumerate(imgs):
    plt.subplot(rows, cols, index + 1)
    if titles:
      title = plt.title(titles[index], )
      plt.setp(title, color="white")
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(img, cmap=cmap)
  plt.show()

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

    

