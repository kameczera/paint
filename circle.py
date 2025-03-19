from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from shape import Shape
import math
import numpy as np

class Circle(Shape):
    def __init__(self, center, color=QColor(255, 255, 255)):
        super().__init__(color)
        self.center = center
        self.radius = 0
    
    def draw(self, painter):
        pen = QPen(self.color)
        painter.setPen(pen)
        x = 0
        y = self.radius
        p = 3 - 2 * self.radius
        self.plot_simetrics(x, y, self.center.x(), self.center.y(), painter)

        while x < y:
            if p < 0:
                p += 4 * x + 6
            else:
                p += 4 * (x - y) + 10
                y -= 1
            x += 1
            self.plot_simetrics(x, y, self.center.x(), self.center.y(), painter)
    
    def plot_simetrics(self, x, y, cx, cy, painter):
        self.put_pixel(painter, cx + x, cy + y)
        self.put_pixel(painter, cx + x, cy - y)
        self.put_pixel(painter, cx - x, cy + y)
        self.put_pixel(painter, cx - x, cy - y)
        self.put_pixel(painter, cx + y, cy + x)
        self.put_pixel(painter, cx + y, cy - x)
        self.put_pixel(painter, cx - y, cy + x)
        self.put_pixel(painter, cx - y, cy - x)

    def update_end_point(self, end_point):
        self.radius = int(((end_point.x() - self.center.x())**2 + (end_point.y() - self.center.y())**2) ** 0.5)
    
    def is_defined(self):
        return self.radius > 0

    def contains(self, point):
        distance = math.hypot(point.x() - self.center.x(), point.y() - self.center.y())
        return distance <= self.radius

    def translate(self, dx, dy):
        """Translada a forma em dx e dy."""
        self.center = QPoint(self.center.x() + dx, self.center.y() + dy)

    def rotate(self, angle, pivot=None):
        """Rotaciona a forma em torno de um ponto pivot."""
        if pivot is None:
            pivot = self.center

        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)

        # Translação para a origem
        x, y = self.center.x() - pivot.x(), self.center.y() - pivot.y()

        # Aplicação da matriz de rotação
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a

        # Translação de volta
        self.center = QPoint(int(new_x + pivot.x()), int(new_y + pivot.y()))

    def scale(self, sx, sy, pivot=None):
        """Escala a forma em relação a um ponto pivot."""
        if pivot is None:
            pivot = self.center

        # Translação para a origem
        x, y = self.center.x() - pivot.x(), self.center.y() - pivot.y()

        # Aplicação da matriz de escala
        new_x = x * sx
        new_y = y * sy

        # Translação de volta
        self.center = QPoint(int(new_x + pivot.x()), int(new_y + pivot.y()))

        # Escala o raio
        self.radius = int(self.radius * sx)