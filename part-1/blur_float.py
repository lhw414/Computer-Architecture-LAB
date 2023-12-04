"""
4190.308 Computer Architecture                                                          Spring 2023

Image blurring (float)

This module implements a function that blurs an image with a 3x3 filter (floating point version)

@author:
    Hyunwoo Lee <dlgusdn0414@snu.ac.kr>

@changes:
    2023/04/08 Refactor code

"""


def blur(image, height, width, channels, kernel_size=5):
    """
    Blurs an image with a kernel and returns the blurred image.

    Args:
        image:        image data (multi-level list)
        height:       image height
        width:        image width
        channels:     number of channels (BGR or BGRA)
        kernel_size:  size of blurring kernel

    Returns:
        A tuple containing the following elements:
        - blurred:    blurred image data
        - bheight:    blurred image height
        - bwidth:     blurred image width
        - bchannels:  blurred image channels

    """

    # Calculate bheight, bwidth, bchannels
    bheight = height - kernel_size + 1
    bwidth = width - kernel_size + 1
    bchannels = channels

    # Make kernel
    kernel = [[1.0 / (kernel_size**2) for _ in range(kernel_size)]
              for __ in range(kernel_size)]

    # Init blurred
    blurred = [[[0.0 for _c in range(channels)]
                for _w in range(bwidth)] for _h in range(bwidth)]

    for c in range(channels):
        for h in range(bheight):
            for w in range(bwidth):
                for y in range(kernel_size):
                    for x in range(kernel_size):
                        blurred[h][w][c] += image[h+y][w+x][c] * kernel[y][x]
                blurred[h][w][c] = int(blurred[h][w][c])

    return blurred, bheight, bwidth, bchannels
