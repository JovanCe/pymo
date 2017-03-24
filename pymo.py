import sys, os, random, argparse
from PIL import Image
import numpy as np


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


def average_rgb(image):
    image_array = np.array(image)
    w, h, d = image_array.shape
    return tuple(np.average(image_array.reshape(w * h, d), axis=0))


def tile_matrix(image, rows, cols):
    w, h = int(image.size[0] / cols), int(image.size[1] / rows)
    return [image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)) for j in range(rows) for i in range(cols)]


def shortest_distance_index(average_rgb, average_rgbs):
    avg = average_rgb
    min_index = 0
    min_dist = float("inf")
    for i, val in enumerate(average_rgbs):
        dist = ((val[0] - avg[0]) * (val[0] - avg[0]) +
                (val[1] - avg[1]) * (val[1] - avg[1]) +
                (val[2] - avg[2]) * (val[2] - avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = i
    return min_index


def create_image_grid(images, rows, cols):
    # get the maximum height and width of the images
    # don't assume they're all equal
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    grid_img = Image.new('RGB', (cols * width, rows * height))
    # paste the tile images into the image grid
    for i, image in enumerate(images):
        row = int(i / cols)
        col = i - cols * row
        grid_img.paste(image, (col * width, row * height))

    return grid_img


def create_photomosaic(target_image, input_images, grid_rows, grid_cols, reuse_images=False):
    # split the target image into tiles
    target_images = tile_matrix(target_image, grid_rows, grid_cols)
    # for each tile, pick one matching input image
    output_images = []
    # for user feedback
    count = 0
    batch_size = int(len(target_images) / 10)
    # calculate the average of the input image
    avgs = []
    for img in input_images:
        avgs.append(average_rgb(img))

    for img in target_images:
        # compute the average RGB value of the image
        avg = average_rgb(img)
        # find the matching index of closest RGB value # from a list of average RGB values
        match_index = shortest_distance_index(avg, avgs)
        output_images.append(input_images[match_index])
        # user feedback
        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print('processed %d of %d...' % (count, len(target_images)))
        count += 1
        # remove the selected image from input if flag set
        if not reuse_images:
            input_images.remove(match_index)
    # create photomosaic image from tiles
    mosaic_image = create_image_grid(output_images, grid_rows, grid_cols)
    # display the mosaic
    return mosaic_image


def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored

    # parse arguments
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    # add arguments
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-rows', dest='grid_rows', required=True)
    parser.add_argument('--grid-cols', dest='grid_cols', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)

    args = parser.parse_args()

    ###### INPUTS ######

    # target image
    target_image = Image.open(args.target_image)

    # input images
    print('reading input folder...')
    input_images = image_list(args.input_folder)

    # check if any valid input images found
    if input_images == []:
        print('No input images found in %s. Exiting.' % (args.input_folder,))
        exit()

    # shuffle list - to get a more varied output?
    random.shuffle(input_images)

    # output
    output_filename = 'mosaic.png'
    if args.outfile:
        output_filename = args.outfile

    # resize the input to fit original image size?
    resize_input = True
    reuse_images = True

    grid_rows = int(args.grid_rows)
    grid_cols = int(args.grid_cols)

    ##### END INPUTS #####

    print('starting photomosaic creation...')

    # if images can't be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_rows * grid_cols > len(input_images):
            print('grid size less than number of images')
            exit()

    # resizing input
    if resize_input:
        print('resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims = (int(target_image.size[0] / grid_cols),
                int(target_image.size[1] / grid_rows))
        print("max tile dims: %s" % (dims,))
        # resize
        for img in input_images:
            img.thumbnail(dims)

    # create photomosaic
    mosaic_image = create_photomosaic(target_image, input_images, grid_rows, grid_cols, reuse_images)

    # write out mosaic
    mosaic_image.save('%s.png' % output_filename, 'PNG')

    print("saved output to %s" % (output_filename,))
    print('done.')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
