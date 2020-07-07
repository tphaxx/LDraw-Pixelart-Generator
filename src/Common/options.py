import argparse
from typing import final

from Common.ldraw import PixelMode, PixelArt
from Common.csv_example import CsvExample


class CsvPrintAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest,
                 nargs=0,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        argparse.Action.__init__(self,
                                 option_strings=option_strings,
                                 dest=dest,
                                 nargs=nargs,
                                 const=const,
                                 default=default,
                                 type=type,
                                 choices=choices,
                                 required=required,
                                 help=help,
                                 metavar=metavar,
                                 )
        pass

    def __call__(self, parser, namespace, values, option_string=None):
        print(CsvExample.show_csv())
        parser.exit(0)
        pass
    pass


@final
class CmdLineParser(argparse.ArgumentParser):

    def __init__(self, version: str):
        super().__init__(description='This tool generates a pixel art for LDraw or '
                                     'a derivate like LeoCAD from an image. '
                                     'The output stream is the in LDraw file format.',
                         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                         epilog=
                         'Small pixel art constructions (until 256x256) elapsed max 30s.'
                         'Tested pixel art construction with 160x90 needs 5s.'.format(version))
        self.__version = version
        self.add_options()
        self.add_actions()
        pass

    def add_options(self):
        # source image
        self.add_argument('--src_image', nargs=1, required=True, dest='src_path',
                          help='Path of source image file. Possible file formats: BMP, GIF, JPG, PNG')
        # pixel art size
        self.add_argument('--size', nargs=2, required=False, dest='size', type=int, metavar=('width', 'height'),
                          default=(0, 0),
                          help='Size of final pixel art image. Size in pixel, also bricks.')
        # destination image
        self.add_argument('--dst_image', nargs=1, required=False, dest='dst_path',
                          help='Path of destination image file. See also source file formats.')
        # input palette
        self.add_argument('--input_palette', nargs=1, required=True, dest='in_pal_path',
                          help='The input palette is for transformation the colors. '
                               'This colors are the first instance of possible brick colors.')
        # output palette
        self.add_argument('--output_palette', nargs=1, required=False, dest='out_pal_path',
                          help='The output palette is for transformation the previous '
                               'transformed colors from input palette. This second instance is '
                               'the final color palette for the bricks.')
        # ldr path
        self.add_argument('--ldr_path', nargs=1, required=False, dest='ldr_path',
                          help='If the output file is given then the output stream is closed.')
        # thread count
        self.add_argument('--thread_count', nargs=1, required=False, type=int, dest='thread_count', default=1,
                          help='This is experimental. The source code has an unknown issue. '
                               'So more threads don\'t speed up the generation.')
        # pixel mode
        self.add_argument('--pixel_mode', nargs=1, required=False, choices=[PixelMode.ROUND, PixelMode.RECT],
                          default=PixelMode.RECT, help='(Pixel-) Plate 1x1 in rectangle or rounded shape.')
        # z offset
        self.add_argument('--z_offset', nargs=1, required=False, type=int, default=PixelArt.Z_OFFSET,
                          help='The offset for coordinate z. This is useful for '
                               'own picture frame creation under the generated pixel art.')
        # don't mirror
        self.add_argument('--not_mirrored', action='store_const', dest='mirrored', const=False, default=True,
                          help="The LDraw coordinate system is right handed -y up. "
                               "Monitor screens (also images) are left handed. Mirroring solve the problem.")
        pass

    def add_actions(self):
        # show csv file format example
        self.add_argument('--show_csv_example', action=CsvPrintAction,
                          help='Show a csv file format example and exit program.')
        # version
        self.add_argument('--version', action='version',
                          version='LDraw PixelArt Generator {version}'.format(version=self.__version))
        pass
