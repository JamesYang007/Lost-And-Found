import os

# Prefix directory to append to each files
IMAGE_PREFIX_DIR = os.path.abspath("../images")

def save_image(fileobj, filename):
    filepath = os.path.join(IMAGE_PREFIX_DIR, filename)
    fileobj.save(filepath)
