from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from shape import Shape

class Line(Shape):
    def __init__(self, start_point, color=QColor(255, 255, 255)):
        super().__init__(color)
        self.start_point = start_point
        self.end_point = start_point
    
    def draw(self, painter):
        pen = QPen(self.color)
        painter.setPen(pen)

        x = self.start_point.x()
        y = self.start_point.y()

        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        
        xincr = 0
        yincr = 0
        p = 0
        c1 = 0
        c2 = 0

        self.put_pixel(painter, x, y)
        
        if(dx >= 0): xincr = 1
        else:
            xincr = -1
            dx = -dx
        if(dy >= 0): yincr = 1
        else:
            yincr = -1
            dy = -dy

        if(dx > dy):
            p = 2 * dy - dx
            c1 = 2 * dy
            c2 = 2 * (dy - dx)
            for i in range(dx):
                x += xincr
                if(p < 0): p += c1
                else:
                    p += c2
                    y += yincr
                self.put_pixel(painter, x, y)
        else:
            p = 2 * dx - dy
            c1 = 2 * dx
            c2 = 2 * (dx - dy)
            for i in range(dy):
                y += yincr
                if(p < 0): p += c1
                else:
                    p += c2
                    x += xincr
                self.put_pixel(painter, x, y)
        
    
    def update_end_point(self, end_point):
        self.end_point = end_point
    
    def is_defined(self):
        return self.start_point != self.end_point