import numpy as np
from sklearn.neighbors import KDTree


def rgb_to_lab(input_rgb):
    num = 0
    RGB = [0, 0, 0]

    for value in input_rgb:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value /= 12.92

        RGB[num] = value * 100
        num += 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value **= 0.3333333333333333
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num += 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab


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