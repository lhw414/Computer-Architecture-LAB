//-------------------------------------------------------------------------------------------------
// 4190.308 Computer Architecture                                                       Spring 2023
//
/// @file
/// @brief Image blending (int)
///        This module implements a function that blends two images together filter (integer
///        version)
///
/// @author Hyunwoo LEE <dlgusdn0414@snu.ac.kr>
///
/// @section changelog Change Log
/// 2023/04/30 Hyunwoo Lee : Refactor code
///
//-------------------------------------------------------------------------------------------------

#include <stdlib.h>
#include "blend.h"


struct Image blend_int(struct Image img1, struct Image img2, int overlay, int alpha)
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
        PIXEL(blended, h, w, 3) = (PIXEL(img1, h, w, 3) * (256 - alpha) + PIXEL(img2, h, w, 3) * alpha) >> 8;
        for (int c=0; c<blended.channels-1; c++) {
          PIXEL(blended, h, w, c) = (PIXEL(img1, h, w, c) * PIXEL(img1, h, w, 3) * (256 - alpha) + PIXEL(img2, h, w, c) * PIXEL(img2, h, w, 3) * alpha) >> 16;
        }
      }
    }
  }

  // Overlay Mode
  int alpha_combined;
  if (overlay == 1) {
    for (int h=0; h<blended.height; h++) {
      for (int w=0; w<blended.width; w++) {
        PIXEL(blended, h, w, 3) = PIXEL(img1, h, w, 3);
        alpha_combined = (PIXEL(img2, h, w, 3) * alpha) >> 8;
        for (int c=0; c<blended.channels-1; c++) {
          PIXEL(blended, h, w, c) = (PIXEL(img1, h, w, c) * (256 - alpha_combined) + PIXEL(img2, h, w, c) * alpha_combined) >> 8;
        }
      }
    }
  }

  return blended;
}
