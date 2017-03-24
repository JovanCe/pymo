import numpy as np


def _shortest_distance_index(average_rgb, average_rgbs):
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


def _average_rgb(image):
    image_array = np.array(image)
    w, h, d = image_array.shape
    return tuple(np.average(image_array.reshape(w * h, d), axis=0))


def argb(input_tiles, input_images, reuse_images=True):
    avgs = []
    outputs = []
    input_length = len(input_tiles)
    batch_size = int(input_length / 10)

    for img in input_images:
        avgs.append(_average_rgb(img))

    for i, tile in enumerate(input_tiles):
        avg = _average_rgb(tile)
        match_index = _shortest_distance_index(avg, avgs)
        outputs.append(input_images[match_index])

        if i % batch_size is 0:
            print('processed %d of %d...' % (i, input_length))

        if not reuse_images:
            input_images.remove(match_index)

    return outputs
