//-------------------------------------------------------------------------------------------------
// 4190.308 Computer Architecture                                                       Spring 2023
//
/// @file
/// @brief Image blurring (int)
///        This module implements a function that blurs an image with a filter (integer version)
///
/// @author Hyunwoo LEE <dlgusdn0414@snu.ac.kr>
///
/// @section changelog Change Log
/// 2023/04/30 Hyunwoo Lee : Refactor code
///
//-------------------------------------------------------------------------------------------------

#include <stdlib.h>
#include "blur.h"


struct Image blur_int(struct Image image, int kernel_size)
{
  // Make kernel
  int kernel[kernel_size][kernel_size];

  for (int y=0; y<kernel_size; y++) {
    for (int x=0; x<kernel_size; x++) {
      kernel[y][x] = 255 / (kernel_size * kernel_size);
    }
  }
  kernel[kernel_size/2][kernel_size/2] = 255 - (kernel_size * kernel_size - 1) * (255 / (kernel_size * kernel_size));

  // Initialize output image
  struct Image output = {
    .height   = image.height - kernel_size + 1,
    .width    = image.width - kernel_size + 1,
    .channels = image.channels
  };
  output.data = (uint8*) malloc(sizeof(uint8) * output.height * output.width * output.channels);
  if (output.data == NULL) abort();

  // Calculate convolution 
  int convolution;
  for (int c=0; c<output.channels; c++) {
    for (int h=0; h<output.height; h++) {
      for (int w=0; w<output.width; w++) {
        convolution = 0;
        for (int y=0; y<kernel_size; y++) {
          for (int x=0; x<kernel_size; x++) {
            convolution += PIXEL(image, h+y, w+x, c) * kernel[y][x];
          }
        }
        PIXEL(output, h, w, c) = convolution >> 8;
      }
    }
  }

  return output;
}
