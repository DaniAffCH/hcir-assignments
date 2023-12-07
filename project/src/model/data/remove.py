from PIL import Image
import os

def is_monochannel(image_path):
    try:
        img = Image.open(image_path)
        channels = img.getbands()
        return len(channels) == 1
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def remove_monochannel_images(directory):
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        if is_monochannel(image_path):
            os.remove(image_path)
            print(f"Removed monochannel image: {filename}")

if __name__ == "__main__":
    directory_path = "negatives/"
    remove_monochannel_images(directory_path)
