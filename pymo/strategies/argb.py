import numpy as np


def average_rgb(image):
    image_array = np.array(image)
    width, height, depth = image_array.shape
    return tuple(np.average(image_array.reshape(width * height, depth), axis=0))
