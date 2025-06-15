import cv2
import numpy as np
from PIL import Image
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python extract_assets.py image.png")
    sys.exit(1)

image_path = sys.argv[1]
if not os.path.exists(image_path):
    print(f"Erreur : le fichier '{image_path}' n'existe pas.")
    sys.exit(1)

output_dir = "extraits"
os.makedirs(output_dir, exist_ok=True)

# Charger l'image avec canal alpha
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

if image is None or image.shape[2] < 4:
    print("Erreur : image introuvable ou sans canal alpha.")
    sys.exit(1)

# On récupère uniquement le canal alpha pour détecter les zones opaques
alpha = image[:, :, 3]

# Créer une image binaire où les pixels opaques sont blancs
_, binary = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)

# Étiquetage des composantes connexes (chaque "amat" de pixels)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

count = 0
for i in range(1, num_labels):  # Ignorer le fond (label 0)
    x, y, w, h, area = stats[i]
    if area < 10:  # ignorer les très petits amas (bruit)
        continue

    # Masquer uniquement l'amat de pixels courant
    mask = (labels[y:y+h, x:x+w] == i).astype(np.uint8) * 255
    masked_region = image[y:y+h, x:x+w].copy()

    # Appliquer le masque à l'alpha pour ne garder que l'objet courant
    masked_region[:, :, 3] = cv2.bitwise_and(masked_region[:, :, 3], mask)

    im = Image.fromarray(masked_region)
    im.save(os.path.join(output_dir, f"asset_{count}.png"))
    count += 1

print(f"{count} assets extraits depuis '{image_path}' dans le dossier '{output_dir}'")

