import json
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import tqdm

ANNOTATION_FILE_PATH = "personal/result.json/"
RESULT_FILE_PATH = "personal/train/labels/"
IMAGE_FILE_PATH = "personal/train/images/"

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