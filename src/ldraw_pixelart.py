#!/usr/bin/env python
import time
import datetime

import Common
from Common.ldraw import Constants
from Common.color import Palette
from Common.image import Image
from Common.ldraw import PixelArt
from Common.options import CmdLineParser


if __name__ == '__main__':
    cmdline = CmdLineParser(Common.__version__)
    commands = cmdline.parse_args()

    # required commands
    in_pal = Palette.create(path=commands.in_pal_path[0])
    out_pal = in_pal
    img = Image(commands.src_path[0], commands.size[0], commands.size[1])

    # optional commands
    if commands.out_pal_path is not None:
        out_pal = Palette.create(path=commands.out_pal_path[0])

    # start processing
    print("{} start processing..".format(Constants.META_OR_COMMENT_STRING))

    # measuring time
    start_time = time.time()

    # quantize image
    quantized_img = img.quantized(in_pal, commands.thread_count).mirrored(False, commands.mirrored)
    end_time = time.time()

    # print time
    elapsed_time = end_time - start_time
    qt = datetime.timedelta(seconds=elapsed_time)
    print("{} elapsed quantization time is {}".format(Constants.META_OR_COMMENT_STRING, qt))

    # measuring time
    start_time = time.time()

    # save quantized image
    if commands.dst_path is not None:
        quantized_img.save(commands.dst_path[0])

    # create pixel art
    pixel_art = PixelArt(img=quantized_img, palette=out_pal, mode=commands.pixel_mode, z_offset=commands.z_offset)

    # stream pixel art
    if commands.ldr_path is not None:
        ldr_file = open(commands.ldr_path[0], "w")
        ldr_file.write(str(pixel_art))
        ldr_file.close()
    else:
        print(str(pixel_art))

    end_time = time.time()

    # print time
    elapsed_time = end_time - start_time
    gt = datetime.timedelta(seconds=elapsed_time)
    print("{} elapsed pixel art creation time is {}".format(Constants.META_OR_COMMENT_STRING, gt))

    ct = qt + gt
    print("{} ..end of processing. Complete time is {}".format(Constants.META_OR_COMMENT_STRING, ct))
    pass
