from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from shape import Shape

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

        while(x < y):
            if(p < 0): p += 4 * x + 6
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