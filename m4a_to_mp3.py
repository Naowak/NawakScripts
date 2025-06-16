import sys
import os
from pydub import AudioSegment

def convert_m4a_to_mp3(input_path):
    if not os.path.isfile(input_path):
        print(f"Fichier introuvable : {input_path}")
        return

    if not input_path.lower().endswith(".m4a"):
        print("Le fichier doit avoir une extension .m4a")
        return

    output_path = os.path.splitext(input_path)[0] + ".mp3"

    try:
        audio = AudioSegment.from_file(input_path, format="m4a")
        audio.export(output_path, format="mp3")
        print(f"Conversion réussie : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python convert_m4a_to_mp3.py fichier.m4a")
    else:
        convert_m4a_to_mp3(sys.argv[1])

