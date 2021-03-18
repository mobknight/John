import os
from PIL import Image

for root, dirs, files in os.walk('./'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        print("== ", fname, " is a ", ext)
        if ext in ['.jpg', '.JPG', '.png', '.PNG', '.gif', '.GIF']:
            print("==> Processing ", fname, "...")
            im = Image.open(file)
            width, height = im.size
            crop_image = im.crop((387, 65, 1897, 920))
            # Left, Top, Right, Bottom
            crop_image.save('cropped_' + fname + '.png')
