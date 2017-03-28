import numpy as np
from sklearn.neighbors import KDTree


def _average_rgb(image):
    image_array = np.array(image)
    width, height, depth = image_array.shape
    return tuple(np.average(image_array.reshape(width * height, depth), axis=0))


def argb(input_tiles, input_images, reuse_images=True):
    candidates = []
    outputs = []
    input_length = len(input_tiles)
    batch_size = int(input_length / 10)

    for img in input_images:
        candidates.append(_average_rgb(img))

    rgb_tree = KDTree(np.array(candidates))

    for i, tile in enumerate(input_tiles):
        target = _average_rgb(tile)
        match_index = rgb_tree.query(np.array(target).reshape(1, -1))
        outputs.append(input_images[match_index[1][0][0]])

        if i % batch_size is 0:
            print('Processed %d of %d...' % (i, input_length))

    return outputs
