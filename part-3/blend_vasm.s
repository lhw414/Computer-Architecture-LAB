#/-------------------------------------------------------------------------------------------------
#/ 4190.308 Computer Architecture                                                       Spring 2023
#/
#// @file
#// @brief Image blending (vector operations)
#//        This module implements a function that blends two images together filter (assembly 
#//        integer vector version)
#//
#//
#// @section changelog Change Log
#// 2023/06/11 Hyunwoo LEE - Fix : optimize assembly code
#// 
#/-------------------------------------------------------------------------------------------------

    .option nopic
    .attribute unaligned_access, 0
    .attribute stack_align, 16

    .text
    .align 4
    .globl blend_asm
    .type  blend_asm, @function

# struct Image {                 Ofs
#     uint8 *data;                 0
#     int height;                  4
#     int width;                   8
#     int channels;               12
# };

# int blend_asm(                 Reg
#       struct Image *blended,    a0
#       struct Image *img1,       a1
#       struct Image *img2,       a2
#       int overlay,              a3
#       int alpha                 a4
#     )

blend_asm:
    # Check parameters
    li    t0, 1
    bne   a3, t0, .OverlayError   # if overlay != 1 goto .OverlayError

    lw    t1, 12(a1)              # t1 = img1->channels
    lw    t2, 12(a2)              # t2 = img2->channels
    li    t0, 4                   # t0 = 4
    bne   t1, t0, .ChannelError   # if img1->channels != 4 goto .ChannelError
    bne   t2, t0, .ChannelError   # if img2->channels != 4 goto .ChannelError

    # more error checks if deemed necessary


    # Initialize blended image 
    lw t0, 4(a1)                  # t0 = img1->height
    lw t1, 8(a1)                  # t1 = img1->width
    lw t2, 12(a1)                 # t2 = img1->channels
    sw t0, 4(a0)                  # blended->height = t0
    sw t1, 8(a0)                  # blended->width = t1
    sw t2, 12(a0)                 # blended->channels = t2

    # Blend
    mul t2, t0, t1                # t2 = img1->height * img1->width
    lw t0, 0(a1)                  # t0 = start address of img1->data
    lw t1, 0(a2)                  # t1 = start address of img2-> data
    lw t3, 0(a0)                  # t3 = start address of blended.data
    slli t2, t2, 2                # t2 = t2 * 4
    add t2, t3, t2                # t2 = t3 + t2 // end point
    svbrdcst a4, a4               # a4 = broadcast a4 (alpha)
    li a6, 256                    # a6 = 256
    svbrdcst a6, a6               # a6 = broadcast a6
.L1:
    lw t4, 0(t0)                  # t4 = img1.data[i] (ARGB)
    lw t5, 0(t1)                  # t5 = img2.data[i] (ARGB)
    srli a2, t4, 24               # a2 = img1.data's alpha value
    srli t6, t5, 24               # t6 = img2.data's alpha value
    svbrdcst t6, t6               # t6 = broadcast t6
    svunpack t4, t4               # unpack t4 to vector data
    svunpack t5, t5               # unpack t5 to vector data
    svmul t6, t6, a4              # t6 = alpha value(img2) * alpha
    svmul t5, t5, t6              # t5 = t5 * t6 (vector)
    svsub t6, a6, t6              # t6 = a6 - t6 (256 vector - t6)
    svmul t4, t4, t6              # t4 = t4 * t6
    svadd t5, t5, t4              # t5 = t5 + t4
    svpack t5, t5, a2             # t5 = pack(t5, alpha value(img1))
    sw t5, 0(t3)                  # store value in blended.data[i]
    addi t3, t3, 4                # t3 = t3 + 4
    addi t0, t0, 4                # t0 = t0 + 4
    addi t1, t1, 4                # t1 = t1 + 4
    bne t3, t2, .L1               # if t3 != t2, goto L1

    mv    a0, x0                  # move x0 to a0
    ret

.OverlayError:
    li    a0, -1
    ret

.ChannelError:
    li    a0, -2
    ret

