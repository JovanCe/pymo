import argparse, random
from PIL import Image

from pymo.mosaic import image_list, generate_photo_mosaic

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a photo mosaic from input images')
    parser.add_argument('--input-image', dest='input_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-rows', dest='grid_rows', required=True)
    parser.add_argument('--grid-cols', dest='grid_cols', required=True)
    parser.add_argument('--output', dest='output', required=True)
    parser.add_argument('--strategy', dest='strategy', required=True, default='argb')

    args = parser.parse_args()

    target_image = Image.open(args.input_image)
    print('reading input folder...')
    input_images = image_list(args.input_folder)

    if not input_images:
        print('No images found in %s. Exiting.' % args.input_folder)
        exit()

    random.shuffle(input_images)

    # resize the input to fit original image size
    resize_input = True
    reuse_images = True

    grid_rows = int(args.grid_rows)
    grid_cols = int(args.grid_cols)

    output = '%s.png' % args.output

    # which algorithm to use
    strategy = args.strategy

    print('Creating photo mosaic...')

    if not reuse_images:
        if grid_rows * grid_cols > len(input_images):
            print('Insufficient number of images.')
            exit()

    if resize_input:
        print('Resizing images...')
        dims = (int(target_image.size[0] / grid_cols),
                int(target_image.size[1] / grid_rows))

        for img in input_images:
            img.thumbnail(dims)

    mosaic_image = generate_photo_mosaic(target_image, input_images, grid_rows, grid_cols, reuse_images)
    mosaic_image.save(output, 'PNG')

    print("Saved mosaic to %s" % output)
