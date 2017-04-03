import os
from PIL import Image

from pymo.strategies import get_output_tiles


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


def tile_matrix(image, tile_height, tile_width, rows, cols):
    return [image.crop((i * tile_width, j * tile_height, (i + 1) * tile_width, (j + 1) * tile_height)) for j in
            range(rows) for i in range(cols)]


def image_grid(images, tile_height, tile_width, rows, cols):
    grid_img = Image.new('RGB', (cols * tile_width, rows * tile_height))

    for i, image in enumerate(images):
        row = int(i / cols)
        col = i - cols * row
        grid_img.paste(image, (col * tile_width, row * tile_height))

    return grid_img


def generate_photo_mosaic(target_image, input_images, grid_rows, grid_cols, reuse_images=False, strategy='lab'):
    tile_width = int(target_image.size[0] / grid_cols)
    tile_height = int(target_image.size[1] / grid_rows)

    for image in input_images:
        image.thumbnail((tile_width, tile_height))

    input_tiles = tile_matrix(target_image, tile_height, tile_width, grid_rows, grid_cols)
    outputs = get_output_tiles(input_tiles, input_images, reuse_images, strategy)
    mosaic_image = image_grid(outputs, tile_height, tile_width, grid_rows, grid_cols)

    return mosaic_image





