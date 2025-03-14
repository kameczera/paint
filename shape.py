from PyQt5.QtGui import QPainter, QColor, QPen

class Shape:
    def __init__(self, color=QColor(255, 255, 255)):
        self.color = color

    def draw(self, painter):
        pass

    def update_end_point(self, end_point):
        pass

    def is_defined(self):
        return False

    def put_pixel(self, painter, x, y, color=QColor("black")):
        painter.drawPoint(x, y)