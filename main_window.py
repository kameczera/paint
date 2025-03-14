from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from shape import Shape
from line import Line
from circle import Circle
from polygon import Polygon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Drawing App")
        self.setGeometry(100, 100, 1280, 720)

        self.drawing_area = DrawingArea()
        self.setCentralWidget(self.drawing_area)

        self.create_menu()
    
    def create_menu(self):
        menu_bar = self.menuBar()
        transform_menu = menu_bar.addMenu("Transformações")
        shapes_menu = menu_bar.addMenu("Formas")

        criation_action = QAction("Criação", self)
        translate_action = QAction("Translação", self)
        rotate_action = QAction("Rotação", self)
        scale_action = QAction("Escala", self)
        
        circle_action = QAction("Circulo", self)
        line_action = QAction("Reta", self)
        polygon_action = QAction("Polígono", self)

        line_action.triggered.connect(lambda: self.set_shape_type("line"))
        circle_action.triggered.connect(lambda: self.set_shape_type("circle"))
        polygon_action.triggered.connect(lambda: self.set_shape_type("polygon"))

        criation_action.triggered.connect(lambda: self.set_transformation_mode(None))
        translate_action.triggered.connect(lambda: self.set_transformation_mode("translate"))
        rotate_action.triggered.connect(lambda: self.set_transformation_mode("rotate"))
        scale_action.triggered.connect(lambda: self.set_transformation_mode("scale"))
        
        transform_menu.addAction(criation_action)
        transform_menu.addAction(translate_action)
        transform_menu.addAction(rotate_action)
        transform_menu.addAction(scale_action)

        shapes_menu.addAction(line_action)
        shapes_menu.addAction(circle_action)
        shapes_menu.addAction(polygon_action)

    def set_transformation_mode(self, mode):
        self.drawing_area.transformation_mode = mode

    def set_shape_type(self, shape_type):
        self.drawing_area.shape_type = shape_type


class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.shape_type = 'line'
        self.transformation_mode = None
        self.selected_shape = None
        self.last_mouse_pos = None
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        
        for shape in self.shapes:
            shape.draw(painter)

    def mousePressEvent(self, event):
        if event.y() < 30:
            return

        if self.transformation_mode:
            if(not self.selected_shape):
                self.selected_shape = self.get_shape_at(event.pos())
                self.last_mouse_pos = event.pos()
            else:
                self.selected_shape = None
        else:
            if not self.current_shape:
                if self.shape_type == 'line':
                    self.current_shape = Line(QPoint(event.x(), event.y()))
                elif self.shape_type == 'circle':
                    self.current_shape = Circle(QPoint(event.x(), event.y()))
                else:
                    self.current_shape = Polygon(QPoint(event.x(), event.y()))
            elif isinstance(self.current_shape, Polygon) and not self.current_shape.is_defined():
                self.current_shape.update_end_point(QPoint(event.x(), event.y()))
            else:
                self.current_shape.update_end_point(QPoint(event.x(), event.y()))
                self.shapes.append(self.current_shape)
                self.current_shape = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.transformation_mode and self.selected_shape:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()

            if self.transformation_mode == "translate":
                self.selected_shape.translate(dx, dy)
            elif self.transformation_mode == "rotate":
                self.selected_shape.rotate(dx)
            elif self.transformation_mode == "scale":
                self.selected_shape.scale(1 + dx / 100.0, 1 + dy / 100.0)

            self.last_mouse_pos = event.pos()

    def get_shape_at(self, pos):
        for shape in self.shapes:
            if shape.contains(pos):
                return shape
        return None