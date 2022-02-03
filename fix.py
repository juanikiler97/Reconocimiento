import json
import tqdm

ANNOTATION_FILE_PATH = "personal/result.json/"

with open(ANNOTATION_FILE_PATH, "r") as f:
    annotations = json.load(f)

for image in tqdm.tqdm(annotations):
    image["mask_name"] = image["file_name"][:-3] + "png"

with open(ANNOTATION_FILE_PATH, "w") as f:
    json.dump(annotations, f)