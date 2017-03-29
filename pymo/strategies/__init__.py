import numpy as np
from sklearn.neighbors import KDTree

from .argb import average_rgb
from .alab import average_lab


def get_output_tiles(input_tiles, input_images, reuse_images=True, strategy='lab'):
    # check manually for now
    if strategy == 'lab':
        strategy_func = average_lab
    else:
        strategy_func = average_rgb

    candidates = []
    outputs = []
    input_length = len(input_tiles)
    batch_size = int(input_length / 10)

    for img in input_images:
        candidates.append(strategy_func(img))

    rgb_tree = KDTree(np.array(candidates))

    for i, tile in enumerate(input_tiles):
        target = strategy_func(tile)
        match_index = rgb_tree.query(np.array(target).reshape(1, -1))
        outputs.append(input_images[match_index[1][0][0]])

        if i % batch_size is 0:
            print('Processed %d of %d...' % (i, input_length))

    return outputs