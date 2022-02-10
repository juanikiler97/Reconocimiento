import shutil
from tqdm import tqdm
import os
import cv2
from matplotlib import pyplot as plt
DEST_PATH = "personal/final_dataset"

def plot_single_image(img, title=None, size=(8, 8), cmap='viridis'):
	plt.figure(figsize=size)
	plt.xticks([])
	plt.yticks([])
	plt.grid(False)
	plt.imshow(img, cmap=cmap)
	if title:
		plt.title(title)
	plt.show()

def _zelanda_la_oculta(path: str):
    for subdir in os.listdir(path):
        ext = "jpg"
        if subdir == "label":
            ext = "png"
        files = os.listdir(os.path.join(path, subdir))
        print( f"\t{subdir} - {len(files)}" )
        for i in tqdm(files):
            image = cv2.imread( os.path.join(path, subdir, i))
            cv2.imwrite(os.path.join(DEST_PATH, subdir + "s", i[:-3] + ext), image)

def zelanda_la_nueva(path: str = "nueva_zelanda"):
    for i in next(os.walk(path))[1]:
        print(os.path.join(path, i))
        _zelanda_la_oculta( os.path.join(path, i) )


def sn1_func(path: str):
    pass

def my_func(path: str):
    shutil.copytree(path, DEST_PATH, dirs_exist_ok=True)

# CUIDAO - - Pon bien el separador. En windows es \, en los que no son especialitos es /
folder_functions = {
    "personal\\nueva_zelanda": zelanda_la_nueva,
    "personal\\SN1_buildings\\train": sn1_func,
    "personal\\train": my_func
}

if __name__ == "__main__":
    os.makedirs(DEST_PATH + "/images", exist_ok=True)
    os.makedirs(DEST_PATH + "/labels", exist_ok=True)
    for f in folder_functions:
        folder_functions[f](f)
