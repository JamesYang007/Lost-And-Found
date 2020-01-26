import os
import hashlib
import threading

# Prefix directory to append to each files
IMAGE_PREFIX_DIR = "./images"

# Save file using given filename
def process_image(fileobj):
    filepath = os.path.join(IMAGE_PREFIX_DIR, "__tmp" + str(threading.current_thread().ident) + "__")
    fileobj.save(filepath)
    unique_filepath = IMAGE_PREFIX_DIR + "/" + ''.join([hash_file(filepath), '.jpg'])
    os.rename(filepath, unique_filepath)
    return filepath

# MD5 hash file content to name file
def hash_file(filepath):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()

if __name__ == "__main__":
    print(hash_file(os.path.join(IMAGE_PREFIX_DIR, 'IMG_0626.jpeg')))
