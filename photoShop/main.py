from PIL import Image,ImageFilter
import os
try:
    org = os.mkdir('./org')
    psdPic = os.mkdir('./psdPic')
except FileExistsError:
    pass
files = os.listdir('./org')
for file in files:
    image = Image.open(f'./org/{file}')
    sharpedImage = image.filter(ImageFilter.SHARPEN)
    blackedImage = sharpedImage.convert('L')
    new_name = f"edited-file-{file}"
    blackedImage.save(f'./psdPic/{new_name}')