import os
from PIL import Image

from pymo.strategies import argb, alab


def image_list(image_dir):
    images = []
    image_files = os.listdir(image_dir)
    for file in image_files:
        path = os.path.abspath(os.path.join(image_dir, file))
        try:
            with open(path, "rb") as image_file:
                image = Image.open(image_file)
                image.load()
                images.append(image)
        except Exception as e:
            print("Invalid image %s: %s" % (path, e))
            continue

    return images


def tile_matrix(image, rows, cols):
    w, h = int(image.size[0] / cols), int(image.size[1] / rows)
    return [image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)) for j in range(rows) for i in range(cols)]


def image_grid(images, rows, cols):
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    grid_img = Image.new('RGB', (cols * width, rows * height))
    
    for i, image in enumerate(images):
        row = int(i / cols)
        col = i - cols * row
        grid_img.paste(image, (col * width, row * height))

    return grid_img


def generate_photo_mosaic(input_image, input_images, grid_rows, grid_cols, reuse_images=False, strategy=alab):
    input_tiles = tile_matrix(input_image, grid_rows, grid_cols)
    outputs = strategy(input_tiles, input_images, reuse_images)
    mosaic_image = image_grid(outputs, grid_rows, grid_cols)

    return mosaic_image





