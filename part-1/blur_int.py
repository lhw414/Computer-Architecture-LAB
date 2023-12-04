"""
4190.308 Computer Architecture                                                          Spring 2023

Image blurring (int)

This module implements a function that blurs an image with a filter (integer version)

@author:
    Hyunwoo Lee <dlgusdn0414@snu.ac.kr>

@changes:
    2023/04/09 Refactor code

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
    kernel = [[255 // kernel_size ** 2 for _ in range(kernel_size)]
              for __ in range(kernel_size)]
    kernel[kernel_size//2][kernel_size//2] = 255 - \
        (kernel_size ** 2 - 1) * (255 // kernel_size ** 2)

    # Init blurred
    blurred = [[[0 for _c in range(channels)]
                for _w in range(bwidth)] for _h in range(bwidth)]

    for c in range(channels):
        for h in range(bheight):
            for w in range(bwidth):
                for y in range(kernel_size):
                    for x in range(kernel_size):
                        blurred[h][w][c] += image[h+y][w+x][c] * kernel[y][x]
                blurred[h][w][c] = blurred[h][w][c] >> 8

    return blurred, bheight, bwidth, bchannels
