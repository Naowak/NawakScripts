import sys
import os
from PIL import Image, ImageDraw

def parse_size(size_str):
    try:
        w, h = map(int, size_str.lower().split("x"))
        return (w, h)
    except:
        raise ValueError("Format de dimension invalide. Utilise : largeurxhauteur (ex: 500x500)")

def apply_smooth_border_radius(image, radius=50, scale=4):
    width, height = image.size
    big_size = (width * scale, height * scale)
    big_radius = radius * scale

    # Masque haute résolution
    mask = Image.new("L", big_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, *big_size), radius=big_radius, fill=255)
    mask = mask.resize((width, height), Image.LANCZOS)

    # Appliquer masque
    rounded = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rounded.paste(image, (0, 0), mask)
    return rounded

def main():
    if len(sys.argv) < 3:
        print("❌ Utilisation : python round_image.py image_entree.png image_sortie.png [LARGEURxHAUTEUR]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    size = None

    if not os.path.isfile(input_path):
        print(f"❌ Le fichier d'entrée '{input_path}' n'existe pas.")
        sys.exit(1)

    if len(sys.argv) == 4:
        try:
            size = parse_size(sys.argv[3])
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)

    image = Image.open(input_path).convert("RGBA")

    if size:
        image = image.resize(size, Image.LANCZOS)

    rounded_image = apply_smooth_border_radius(image, radius=50)
    rounded_image.save(output_path, format="PNG")
    print(f"✅ Image sauvegardée : {output_path}")

if __name__ == "__main__":
    main()

