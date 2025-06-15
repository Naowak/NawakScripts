import cv2
import numpy as np
from PIL import Image
import os
import sys

def extract_assets_from_image(image_path, output_dir):
    basename = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Erreur : impossible de lire '{image_path}' (fichier non lisible).")
        return
    if len(image.shape) < 3 or image.shape[2] < 4:
        print(f"Erreur : '{image_path}' ne contient pas de canal alpha (RGBA requis).")
        return

    alpha = image[:, :, 3]
    _, binary = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    count = 0
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 100:
            continue

        mask = (labels[y:y+h, x:x+w] == i).astype(np.uint8) * 255
        masked_region = image[y:y+h, x:x+w].copy()
        masked_region[:, :, 3] = cv2.bitwise_and(masked_region[:, :, 3], mask)

        # Générer un nom de fichier unique
        index = count
        while True:
            asset_name = f"{basename}-{index}.png"
            asset_path = os.path.join(output_dir, asset_name)
            if not os.path.exists(asset_path):
                break
            index += 1

        masked_region = cv2.cvtColor(masked_region, cv2.COLOR_BGRA2RGBA)
        im = Image.fromarray(masked_region)
        im.save(asset_path)
        print(f" -> Enregistré : {asset_name}")
        count += 1

    print(f"{count} assets extraits depuis '{image_path}' dans le dossier '{output_dir}'\n")

if len(sys.argv) < 2:
    print("Usage: python extract_assets.py <image.png> ou <dossier>")
    sys.exit(1)

input_path = sys.argv[1]
output_dir = "extraits"
os.makedirs(output_dir, exist_ok=True)

if os.path.isdir(input_path):
    for filename in os.listdir(input_path):
        if filename.lower().endswith(".png"):
            full_path = os.path.join(input_path, filename)
            extract_assets_from_image(full_path, output_dir)
else:
    extract_assets_from_image(input_path, output_dir)

