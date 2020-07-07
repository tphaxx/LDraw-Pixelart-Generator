from typing import Final, final

from Common.color import Color, Palette
from Common.image import Image


@final
class Constants:
    META_OR_COMMENT_STRING: Final[str] = "0"
    IDENTITY: Final[list] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    RECT_DAT: Final[str] = "3024.dat"
    ROUND_DAT: Final[str] = "6141.dat"
    pass


@final
class PixelMode:
    ROUND: Final[str] = "round"
    RECT: Final[str] = "rect"
    pass


@final
class Plate1x1:

    def __init__(self, color: Color, palette: Palette, mode: PixelMode = PixelMode.RECT,
                 x: int = 0, y: int = 0, z: int = 0):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__color = color
        self.__palette = palette
        self.__dat = Constants.RECT_DAT

        if mode == PixelMode.ROUND:
            self.__dat = Constants.ROUND_DAT

        self.__matrix = Constants.IDENTITY
        self.__line_type = 1
        pass

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    @property
    def color(self):
        return self.__color

    @property
    def palette(self):
        return self.__palette

    def __str__(self):
        return "{} {} {} {} {} {} {}"\
            .format(self.__line_type, self.palette.get_id(self.color), self.x, self.z, self.y,
                    Plate1x1.get_matrix_str(self.__matrix), self.__dat)

    @staticmethod
    def get_matrix_str(matrix: list):
        try:
            return Plate1x1.__get_matrix_str(matrix)
        except:
            return Plate1x1.__get_matrix_str(Constants.IDENTITY)

    @staticmethod
    def __get_matrix_str(matrix: list):
        flat_matrix = [item for sublist in matrix for item in sublist]
        return "{} {} {} {} {} {} {} {} {}".format(*flat_matrix)
    pass


class PixelArt:

    XY_OFFSET: Final[int] = 10
    Z_OFFSET: Final[int] = 8
    XY_INC: Final[int] = 20

    def __init__(self, img: Image, palette: Palette = None, mode: PixelMode = PixelMode.RECT, z_offset: int = 0):
        self.__img = img
        self.__plates = PixelArt.generate(img, palette, mode, z_offset)
        pass

    def __str__(self):
        text = ""
        for plate in self.__plates:
            text += str(plate)
            text += '\n'
        return text

    @staticmethod
    def generate(img: Image, palette: Palette, mode: PixelMode = PixelMode.RECT, z_offset: int = None) -> list:
        if (img is None) or (palette is None):
            return []
        plates = []
        z = z_offset
        if z_offset is None:
            z = PixelArt.Z_OFFSET
        for x in range(img.width()):
            for y in range(img.height()):
                color = Color(img.pixel(x, y))
                plate = Plate1x1(color, palette, mode,
                                 PixelArt.XY_OFFSET + x * PixelArt.XY_INC,
                                 PixelArt.XY_OFFSET + y * PixelArt.XY_INC,
                                 -z)
                plates.append(plate)
        return plates
