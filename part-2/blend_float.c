//-------------------------------------------------------------------------------------------------
// 4190.308 Computer Architecture                                                       Spring 2023
//
/// @file
/// @brief Image blending (float)
///        This module implements a function that blends two images together filter (floating-point
///        version). Note that CPython uses the 'double' data type for floating point numbers, 
///        so one may observe small differences in the output if the 'float' data type is used.
///
/// @author Hyunwoo LEE <dlgusdn0414@snu.ac.kr>
///
/// @section changelog Change Log
/// 2023/04/30 Hyunwoo Lee : Refactor code
///
//-------------------------------------------------------------------------------------------------

#include <stdlib.h>
#include "blend.h"


struct Image blend_float(struct Image img1, struct Image img2, int overlay, double alpha)
{
  if (img1.channels != 4) abort();


  // Initialize blended image
  struct Image blended = {
    .height   = img1.height,
    .width    = img1.width,
    .channels = img1.channels
  };
  blended.data = malloc(blended.height*blended.width*blended.channels*sizeof(uint8));
  if (blended.data == NULL) abort();

  // Merge Mode
  if (overlay == 0) {
    for (int h=0; h<blended.height; h++) {
      for (int w=0; w<blended.width; w++) {
        PIXEL(blended, h, w, 3) = (uint8) (((PIXEL(img1, h, w, 3) / 255.0) * (1.0 - alpha) + (PIXEL(img2, h, w, 3) / 255.0) * alpha) * 255.0);
        for (int c=0; c<blended.channels-1; c++) {
          PIXEL(blended, h, w, c) = (uint8) (((PIXEL(img1, h, w, c) / 255.0) * (PIXEL(img1, h, w, 3) / 255.0) * (1.0 - alpha) + (PIXEL(img2, h, w, c) / 255.0) * (PIXEL(img2, h, w, 3) / 255.0) * alpha) * 255.0);
        }
      }
    }
  }

  // Overlay Mode
  double alpha_combined;
  if (overlay == 1) {
    for (int h=0; h<blended.height; h++) {
      for (int w=0; w<blended.width; w++) {
        PIXEL(blended, h, w, 3) = PIXEL(img1, h, w, 3);
        alpha_combined = (PIXEL(img2, h, w, 3) / 255.0) * alpha;
        for (int c=0; c<blended.channels-1; c++) {
          PIXEL(blended, h, w, c) = (uint8) (((PIXEL(img1, h, w, c) / 255.0) * (1.0 - alpha_combined) + (PIXEL(img2, h, w, c) / 255.0) * alpha_combined) * 255.0);
        }
      }
    }
  }


  return blended;
}
