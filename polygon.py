from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QPoint
from shape import Shape
import numpy as np
from line import Line

class Polygon(Shape):
    def __init__(self, point, color=QColor(255, 255, 255)):
        super().__init__(color)
        self.vertices = [point]
        print(color)

    def update_end_point(self, point):
        self.vertices.append(point)
        
    def is_defined(self):
        return len(self.vertices) == 3

    def draw(self, painter):
        for i in range(len(self.vertices)):
            start_point = self.vertices[i]
            end_point = self.vertices[(i + 1) % len(self.vertices)] if i + 1 < len(self.vertices) else self.vertices[0]
            new_line = Line(start_point, end_point, self.color)
            new_line.draw(painter)

    def translate(self, dx, dy):
        for i in range(len(self.vertices)):
            self.vertices[i] = QPoint(self.vertices[i].x() + dx, self.vertices[i].y() + dy)

    def rotate(self, angle, pivot=None):
        if pivot is None:
            pivot = self.vertices[0]

        rad = np.radians(angle)
        cos_a, sin_a = np.cos(rad), np.sin(rad)

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

        self.vertices = [self.apply_transformation(v, transformation_matrix) for v in self.vertices]
    
    def scale(self, sx, sy, pivot=None):
        if pivot is None:
            pivot = self.vertices[0]

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

        self.vertices = [self.apply_transformation(v, transformation_matrix) for v in self.vertices]

    def apply_transformation(self, point, matrix):
        point_homogeneous = np.array([point.x(), point.y(), 1])
        transformed_point = matrix @ point_homogeneous
        return QPoint(int(transformed_point[0]), int(transformed_point[1]))

    def contains(self, point, threshold=5):
        for i in range((len(self.vertices))):
            start_point = self.vertices[i]
            end_point = self.vertices[(i + 1) % len(self.vertices)] if i + 1 < len(self.vertices) else self.vertices[0]
            new_line = Line(start_point, end_point, self.color)
            if(new_line.contains(point)): return True
        return False