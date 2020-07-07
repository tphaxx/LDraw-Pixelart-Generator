from typing import final
from PyQt5.QtGui import QColor, QImage, qRed, qGreen, qBlue
import math
import pandas as pd
import os


@final
class Color(QColor):

    @staticmethod
    def quantize(color_vector: tuple, palette) -> tuple:
        min_dst = 8e9
        result = None

        for dst_color in palette.colors:
            dst_vector = Color.get_vector(dst_color)
            dst = Color.calc_distance(color_vector, dst_vector)
            if dst < min_dst:
                result = dst_vector
                min_dst = dst
                if min_dst == 0:
                    return result
        return result

    @staticmethod
    def calc_distance(vec_a, vec_b):
        return math.sqrt((vec_a[0] - vec_b[0])**2
                         + (vec_a[1] - vec_b[1])**2
                         + (vec_a[2] - vec_b[2])**2)

    @staticmethod
    def get_vector(color: QColor) -> tuple:
        rgb = color.rgb()
        return qRed(rgb), qGreen(rgb), qBlue(rgb)
    pass


@final
class Palette:
    def __init__(self, image_path: str = None, colors: list = None, ids: list = None, csv_path: str = None):
        self.__colors = []
        self.__ids = []
        saved_colors = []

        if csv_path is not None:
            color_csv = pd.read_csv(csv_path, ',')
            ids = color_csv['id']
            self.__ids = ids.values
            colors = color_csv['rgb'].values
            for n in range(len(colors)):
                rgb = int(colors[n], 16)
                color = QColor(qRed(rgb), qGreen(rgb), qBlue(rgb))
                self.__colors.append(color)
        else:
            if image_path is not None:
                image = QImage(image_path)
                for x in range(image.width()):
                    for y in range(image.height()):
                        rgb = image.pixel(x, y)
                        color = QColor(qRed(rgb), qGreen(rgb), qBlue(rgb))

                        if rgb not in saved_colors:
                            self.__colors.append(color)
                            saved_colors.append(rgb)
            if colors is not None:
                self.colors = colors
            if ids is not None:
                self.__ids = ids
        pass

    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, new_colors):
        self.__colors.clear()
        for color in new_colors:
            self.append_color(QColor(color.rgb()))
        pass

    def append_color(self, color: Color):
        if color is not None:
            self.__colors.append(color)
        pass

    @property
    def ids(self):
        return self.__ids

    def get_id(self, color: Color):
        rgb = Color.quantize(Color.get_vector(color), self)
        c = QColor(rgb[0], rgb[1], rgb[2])

        if len(self.ids) != len(self.colors):
            return -1

        for n in range(len(self.colors)):
            if self.colors[n] == c:
                return self.ids[n]
        return -1

    @staticmethod
    def create(src_palette=None, path=None):
        if src_palette is not None:
            palette = Palette()
            palette.colors = src_palette.colors
            return palette
        if path is not None:
            pal_ext = os.path.splitext(path)[1]

            if pal_ext == '.csv':
                return Palette(csv_path=path)
            else:
                return Palette(image_path=path)
        return Palette()

    def __str__(self):
        colors_table = "color\n"

        for color in self.colors:
            rgb = color.rgb()
            colors_table += "{}\n".format(hex(rgb))

        colors_table += 'color count: {}'.format(len(self.colors))
        return colors_table
    pass
