from PyQt5.QtGui import QPainter, QColor, QPen

class Shape:
    def __init__(self, color=QColor(255, 255, 255)):
        self.color = color

    def draw(self, painter):
        pass

    def update_end_point(self, end_point):
        pass

    def put_pixel(self, painter, x, y, color=QColor("black")):
        painter.drawPoint(x, y)
    
    def translate(self, dx, dy):
        """Translada a forma em dx e dy."""
        pass

    def rotate(self, angle, pivot=None):
        """Rotaciona a forma em torno de um ponto pivot."""
        pass

    def scale(self, sx, sy, pivot=None):
        """Escala a forma em relação a um ponto pivot."""
        pass

    def contains(self, pos):
        pass