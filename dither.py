from PIL import Image
import numpy as np


def dither_floyd_steinberg(rgb_range: int = 2, path: str = "data/lenna.jpg", save_path: str = None,
                           show_original: bool = False, show_result: bool = True):
    """
    Floyd-Steinberg-dithers image of a specified path and has the option to save it.
    :param rgb_range: The number of colors to quantize into. Returns unexpected results if the input isn't a power of 2.
    :param path: the Path that reaches the image being dithered.
    :param save_path: Place where the new image will be saved, the image will only be shown if not specified.
    :param show_original: Indicates whether the original image will be shown upon running the function.
    :param show_result: Indicates whether the dithered image will be shown after finnish.
    :return: None
    """
    smallest_val = 512 // rgb_range
    img = Image.open(path)
    pixels = img.load()
    quant_modifiers = np.zeros((img.width + 1, img.height + 1, 3))
    for y in range(img.height):
        for x in range(img.width):
            original_values = pixels[x, y]

            # TODO: add quant_modifiers value to the pixels value calculation down here

            pixels[x, y] = int(smallest_val * (pixels[x, y][0] // smallest_val)
                           + (pixels[x, y][0] % smallest_val <= (smallest_val / 2)) * smallest_val), \
 \
                           int(smallest_val * (pixels[x, y][1] // smallest_val)
                           + (pixels[x, y][0] % smallest_val <= (smallest_val / 2)) * smallest_val), \
 \
                           int(smallest_val * (pixels[x, y][2] // smallest_val)
                           + (pixels[x, y][0] % smallest_val <= (smallest_val / 2)) * smallest_val)
            # I don't know how to comment multi line code, so the explanation for this monster goes here:
            # pixels[x, y] is a 3-tuple, the values for which are computed in the three almost identical blocks
            # the first line of a block computes the closest smaller match
            # the second line of a block might increase the result depending on the proximity of the original value
            quant_error = np.zeros(3)
            quant_error[0] = pixels[x, y][0] - original_values[0]
            quant_error[1] = pixels[x, y][1] - original_values[1]
            quant_error[2] = pixels[x, y][2] - original_values[2]

            quant_modifiers[x + 1, y] += quant_error[0] * 7 / 16, \
                                         quant_error[1] * 7 / 16, \
                                         quant_error[2] * 7 / 16
            quant_modifiers[x - 1, y + 1] += quant_error[0] * 3 / 16, \
                                             quant_error[1] * 3 / 16, \
                                             quant_error[2] * 3 / 16
            quant_modifiers[x, y + 1] += quant_error[0] * 5 / 16, \
                                         quant_error[1] * 5 / 16, \
                                         quant_error[2] * 5 / 16
            quant_modifiers[x + 1, y + 1] += quant_error[0] * 1 / 16, \
                                             quant_error[0] * 1 / 16, \
                                             quant_error[0] * 1 / 16

            # ^^^^ adding modifiers to where they belong ^^^^

    # TODO: implement additional functionality

    img.show()


dither_floyd_steinberg()
