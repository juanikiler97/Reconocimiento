import random
import shutil
from tqdm import tqdm
import os
import cv2

from erase_censored_images import erase_censored_images

DEST_PATH = "personal/final_dataset"

def _zelanda_la_oculta(path: str):
    for subdir in os.listdir(path):
        ext = "jpg"
        if subdir == "label":
            ext = "png"
        files = os.listdir(os.path.join(path, subdir))
        print( f"\t{subdir} - {len(files)}" )
        for i in tqdm(files):
            image = cv2.imread( os.path.join(path, subdir, i))
            cv2.imwrite(os.path.join(DEST_PATH, "train" , subdir + "s", subdir + "s", i[:-3] + ext), image)

def zelanda_la_nueva(path: str = "nueva_zelanda"):
    for i in next(os.walk(path))[1]:
        print(os.path.join(path, i))
        _zelanda_la_oculta( os.path.join(path, i) )

def sn1_func(path: str):
    for image in tqdm(os.listdir( os.path.join(path, "3band"))):
        im = cv2.imread(os.path.join(path, "3band", f'{image}'))
        cv2.imwrite(os.path.join(DEST_PATH, "train", 'images', 'images', f'{image[:-3]}jpg'), im)
        
        label = cv2.imread(os.path.join(path, "labels", f'{image[:-3]}png'))
        cv2.imwrite(os.path.join(DEST_PATH, "train", 'labels', 'labels', f'{image[:-3]}png'), label)

def my_func(path: str):
    for file in tqdm(os.listdir( f'{path}/images')):
        shutil.copy(f'{path}/images/{file}', f'{DEST_PATH}/train/images/images/{file}')
        shutil.copy(f'{path}/labels/{file[:-3] + "png"}', f'{DEST_PATH}/train/labels/labels/{file[:-3] + "png"}')

def test_function(dataset_path:str, dest_path:str, proportion:float = 0.02):
    """
    Coge imágenes de un dataset y separa un porcentaje en otra carpeta

    Recibe: 
        dataset_path: string con el path al dataset del que quitar imágenes
        dest_path: string que marca donde poner las imágenes
    """    
    images = os.listdir(dataset_path + "/images/images")
    n_images = len(images)

    random.seed(1234)
    selected = random.sample(images, round(n_images * proportion))

    print("Creando partición de Test...")
    for image in tqdm(selected):
        shutil.move(f'{dataset_path}/images/images/{image}', f'{dest_path}/images/images/{image}')
        shutil.move(f'{dataset_path}/labels/labels/{image[:-3] + "png"}', f'{dest_path}/labels/labels/{image[:-3] + "png"}')

# CUIDAO - - Pon bien el separador. En windows es \, en los que no son especialitos es /
FOLDER_FUNCTIONS = {
    "personal/nueva_zelanda": zelanda_la_nueva,
    "personal/SN1_buildings/train": sn1_func,
    "personal/train": my_func
}

if __name__ == "__main__":
    os.makedirs(DEST_PATH + "/train/images/images", exist_ok=True)
    os.makedirs(DEST_PATH + "/train/labels/labels", exist_ok=True)

    functions2use = FOLDER_FUNCTIONS.copy()
    start = False
    seleccion = []

    while not start:
        print(
            "Si quieres usar todas las carpetas, presiona enter\n"
            "Si quieres utilizar algunas en concreto, pon sus números separados por espacios\n"
            "Si no quieres usar ninguna, pon -1")
        for i, func in enumerate(functions2use):
            print(f'\t{i} - {func}')

        seleccion = input(">>> ")
        if seleccion == "-1":
            break

        seleccion = seleccion.split(" ")

        if seleccion == ['']:
            seleccion = list(range(len(functions2use)))  

        def parseInt(string:str):
            try:
                return int(string)
            except Exception as e:
                return None
        
        seleccion = [ i for i in map(lambda item: parseInt(item), seleccion) if i is not None]

        start = True

    if seleccion != "-1":
        for i in seleccion:
            key = list(functions2use.keys())[i]
            #print(key)
            functions2use[key](key)

    if input("¿Quieres limpiar el dataset de imágenes malas? s/n\n>>> ").lower() == "s":
        erase_censored_images(img_folder_path= DEST_PATH + "/train/images/images", label_folder_path= DEST_PATH + "/train/labels/labels")
        
    if input("¿Quieres separar en un conjunto de test? s/n\n>>> ").lower() == "s":
        if os.path.isdir(DEST_PATH + "/test"):
            for folder in os.listdir(DEST_PATH + "/test"):
                shutil.rmtree(DEST_PATH + "/test/" + folder)
        os.makedirs(DEST_PATH + "/test/images/images", exist_ok=True)
        os.makedirs(DEST_PATH + "/test/labels/labels", exist_ok=True)

        test_function(DEST_PATH + "/train", DEST_PATH + "/test")
    
    print("Fin del programa")


