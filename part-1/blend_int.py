"""
4190.308 Computer Architecture                                                          Spring 2023

Image blending (int)

This module implements a function that blends two images together (integer version)

@author:
    Hyunwoo Lee <dlgusdn0414@snu.ac.kr>

@changes:
    2023/04/09 Refactor code

"""


def blend(img1, img2, height, width, channels, overlay, alpha):
    """
    Alpha-blends two images of size heightxwidth. The image data must contain an alpha
    channel, i.e., 'channels' must be four

    Args:
        img1:         image 1 data (multi-level list), BGRA
        img2:         image 2 data (multi-level list), BGRA
        height:       image height
        width:        image width
        channels:     number of channels (must be 4)
        overlay:      if 1, overlay the second image over the first
                      if 0, merge the two images
        alpha:        alpha blending factor (0-255)

    Returns:
        A tuple containing the following elements:
        - blended:    blended image data (multi-level list), BGRA
        - bheight:    blended image height (=height)
        - bwidth:     blended image width (=width)
        - bchannels:  blended image channels (=channels)

    """

    if channels != 4:
        raise ValueError('Invalid number of channels')

    # Init bheight, bwidth, bchannels, blended
    bheight = height
    bwidth = width
    bchannels = channels
    blended = [[[0 for _c in range(channels)]
                for _w in range(bwidth)] for _h in range(bwidth)]

    # Merge Mode
    if (overlay == 0):
        for h in range(bheight):
            for w in range(bwidth):
                blended[h][w][3] = (img1[h][w][3] *
                                    (256 - alpha) + img2[h][w][3] * alpha) >> 8
                for c in range(bchannels-1):
                    blended[h][w][c] = (img1[h][w][c]*img1[h][w][3] *
                                        (256 - alpha) + img2[h][w][c]*img2[h][w][3] * alpha) >> 16

    # Overlay Mode
    if (overlay == 1):
        for h in range(bheight):
            for w in range(bwidth):
                blended[h][w][3] = img1[h][w][3]
                alpha_combined = (img2[h][w][3] * alpha) >> 8
                for c in range(bchannels-1):
                    blended[h][w][c] = (img1[h][w][c] *
                                        (256-alpha_combined) + img2[h][w][c] * alpha_combined) >> 8

    return blended, bheight, bwidth, bchannels
