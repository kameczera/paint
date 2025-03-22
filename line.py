from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QPoint
from shape import Shape
import math
import numpy as np

class Line(Shape):
    def __init__(self, start_point, end_point=None, color=QColor(255, 255, 255)):
        super().__init__(color)
        if not end_point:
            end_point = start_point
        self.start_point = start_point
        self.end_point = end_point
        self.algorithm = "DDA"

    def draw(self, painter):
        if self.algorithm == "DDA":
            self.draw_dda(painter)
        elif self.algorithm == "Bresenham":
            self.draw_bresenham(painter)

    def draw_dda(self, painter):
        pen = QPen(self.color)
        painter.setPen(pen)

        x = self.start_point.x()
        y = self.start_point.y()
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()

        xincr = 1 if dx >= 0 else -1
        yincr = 1 if dy >= 0 else -1
        dx = abs(dx)
        dy = abs(dy)

        p = 2 * dy - dx if dx > dy else 2 * dx - dy
        c1 = 2 * dy if dx > dy else 2 * dx
        c2 = 2 * (dy - dx) if dx > dy else 2 * (dx - dy)

        self.put_pixel(painter, x, y)

        if dx > dy:
            for _ in range(dx):
                x += xincr
                if p < 0:
                    p += c1
                else:
                    p += c2
                    y += yincr
                self.put_pixel(painter, x, y)
        else:
            for _ in range(dy):
                y += yincr
                if p < 0:
                    p += c1
                else:
                    p += c2
                    x += xincr
                self.put_pixel(painter, x, y)

    def draw_bresenham(self, painter):
        pen = QPen(self.color)
        painter.setPen(pen)

        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = self.end_point.x(), self.end_point.y()
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.put_pixel(painter, x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def update_end_point(self, end_point):
        self.end_point = end_point

    def is_defined(self):
        return self.start_point != self.end_point

    def translate(self, dx, dy):
        translation_matrix = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        self.start_point = self.apply_transformation(self.start_point, translation_matrix)
        self.end_point = self.apply_transformation(self.end_point, translation_matrix)

    def rotate(self, angle, pivot=None):
        if pivot is None:
            pivot = self.start_point

        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)

        translation_matrix1 = np.array([
            [1, 0, -pivot.x()],
            [0, 1, -pivot.y()],
            [0, 0, 1]
        ])

        rotation_matrix = np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])

        translation_matrix2 = np.array([
            [1, 0, pivot.x()],
            [0, 1, pivot.y()],
            [0, 0, 1]
        ])

        transformation_matrix = translation_matrix2 @ rotation_matrix @ translation_matrix1

        self.start_point = self.apply_transformation(self.start_point, transformation_matrix)
        self.end_point = self.apply_transformation(self.end_point, transformation_matrix)

    def scale(self, sx, sy, pivot=None):
        if pivot is None:
            pivot = self.start_point

        translation_matrix1 = np.array([
            [1, 0, -pivot.x()],
            [0, 1, -pivot.y()],
            [0, 0, 1]
        ])

        scale_matrix = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

        translation_matrix2 = np.array([
            [1, 0, pivot.x()],
            [0, 1, pivot.y()],
            [0, 0, 1]
        ])

        transformation_matrix = translation_matrix2 @ scale_matrix @ translation_matrix1

        self.start_point = self.apply_transformation(self.start_point, transformation_matrix)
        self.end_point = self.apply_transformation(self.end_point, transformation_matrix)

    def apply_transformation(self, point, matrix):
        point_homogeneous = np.array([point.x(), point.y(), 1])
        transformed_point = matrix @ point_homogeneous
        return QPoint(int(transformed_point[0]), int(transformed_point[1]))

    def contains(self, point, threshold=5):
        x0, y0 = self.start_point.x(), self.start_point.y()
        x1, y1 = self.end_point.x(), self.end_point.y()
        x, y = point.x(), point.y()

        if x0 == x1 and y0 == y1:
            return math.hypot(x - x0, y - y0) <= threshold

        num = abs((y1 - y0) * x - (x1 - x0) * y + x1 * y0 - y1 * x0)
        den = math.hypot(y1 - y0, x1 - x0)
        distance = num / den

        return distance <= threshold