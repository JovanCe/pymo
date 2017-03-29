import numpy as np
from sklearn.neighbors import KDTree


def rgb_to_lab(input_rgb):
    rgb = [0, 0, 0]

    for i, value in enumerate(input_rgb):
        value = float(value) / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value /= 12.92
        rgb[i] = value * 100

    xyz = []
    # ref_X =  95.047   Observer= 2°, Illuminant= D65
    xyz[0] = float(round(rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805, 4)) / 95.047
    # ref_Y = 100.000
    xyz[1] = float(round(rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722, 4)) / 100.0
    # ref_Z = 108.883
    xyz[2] = float(round(rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505, 4)) / 108.883

    for i, value in enumerate(xyz):
        if value > 0.008856:
            value **= 0.3333333333333333
        else:
            value = (7.787 * value) + (16 / 116)
        xyz[i] = value

    return [round(116 * xyz[1] - 16, 4), round(500 * (xyz[0] - xyz[1]), 4), round(200 * (xyz[1] - xyz[2]), 4)]


def _average_lab(image):
    image_array = np.array(image)
    width, height, depth = image_array.shape
    image_array = np.apply_along_axis(rgb_to_lab, 1, image_array.reshape(width * height, depth))
    return tuple(np.average(image_array, axis=0))


def alab(input_tiles, input_images, reuse_images=True):
    candidates = []
    outputs = []
    input_length = len(input_tiles)
    batch_size = int(input_length / 10)

    for img in input_images:
        candidates.append(_average_lab(img))

    rgb_tree = KDTree(np.array(candidates))

    for i, tile in enumerate(input_tiles):
        target = _average_lab(tile)
        match_index = rgb_tree.query(np.array(target).reshape(1, -1))
        outputs.append(input_images[match_index[1][0][0]])

        if i % batch_size is 0:
            print('Processed %d of %d...' % (i, input_length))

    return outputs