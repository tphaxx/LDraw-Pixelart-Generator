from PyQt5.QtGui import QImage, QColor
from Common.color import Palette, Color
from threading import Thread
import numpy as np


class Image(QImage):

    def __init__(self, image_path: str, width: int = 0, height: int = 0):
        img = QImage(image_path)

        if (width > 0) and (height > 0):
            img = img.scaled(width, height)

        super().__init__(img)
        pass

    def quantized(self, pal: Palette, thread_count: int = 1):
        count = max(1, thread_count)
        threads = []
        partition = Image.calc_height_partition(count, self.height())
        dst_vectors = []
        src_vectors = []
        y_areas = []
        src_vector = Image.get_matrix(self)
        result = None

        if (pal is None) or (len(partition) == 0):
            return self.copy()

        for n in range(len(partition)):
            x_start = 0
            x_end = self.width() - 1
            y_start = sum(partition[:n])
            y_end = y_start + partition[n] - 1
            dst_vector = src_vector[y_start:(y_end + 1)][x_start:(x_end + 1)]
            src_vectors.append(dst_vector)
            dst_vectors.append(dst_vector.copy())
            y_areas.append((y_start, y_end))
            thread = Thread(target=Image.__quantized, args=(src_vectors[-1], dst_vectors[-1],
                                                            Palette(colors=pal.colors),
                                                            0, 0,
                                                            len(dst_vector[0]) - 1,
                                                            len(dst_vector) - 1,))
            threads.append(thread)
            thread.start()

        for thread, dst_matrix, y_area in zip(threads, dst_vectors, y_areas):
            thread.join()
            if result is None:
                result = dst_matrix.copy()
            else:
                result = np.vstack((result, dst_matrix))

        return Image.get_image(result, self.format(), 0, len(result) - 1)

    @staticmethod
    def __quantized(src: list, dst: list, pal: Palette, xs: int, ys: int, xe: int, ye: int):
        for y in range(ys, ye + 1):
            for x in range(xs, xe + 1):
                pixel = src[y][x]
                dst[y][x] = Color.quantize(pixel, pal)
        pass

    @staticmethod
    def get_matrix(img: QImage):
        matrix = list()
        for y in range(img.height()):
            matrix.append(list())
            for x in range(img.width()):
                vec = Color.get_vector(QColor(img.pixel(x, y)))
                matrix[y].append(vec)
        return matrix

    @staticmethod
    def get_image(matrix, fmt, ys, ye):
        img = QImage(len(matrix[0]), len(matrix), fmt)
        for y in range(ys, ye + 1):
            for x in range(len(matrix[y])):
                color_vector = matrix[y][x]
                rgb = QColor(color_vector[0], color_vector[1], color_vector[2]).rgb()
                img.setPixel(x, y, rgb)
        return img

    @staticmethod
    def calc_height_partition(counts: int, height: int):
        if (counts == 1) or (counts == 0):
            return [height]
        if height == 0:
            return []

        partitions = []
        best_partition = None
        count = min(counts, height)
        best_max = 1e9

        for divider in range(2, count + 1):
            parts = height // divider
            remain = height % divider
            partition = [parts] * divider

            if remain > 0:
                if len(partition) < count:
                    partition.append(remain)
                else:
                    partition[-1] += remain

            partitions.append(partition)

        for partition in partitions:
            part_max = max(partition)
            if part_max < best_max:
                best_max = part_max
                best_partition = partition

        return best_partition
