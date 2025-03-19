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
        clipping_menu = menu_bar.addMenu("Recorte")

        criation_action = QAction("Criação", self)
        translate_action = QAction("Translação", self)
        rotate_action = QAction("Rotação", self)
        scale_action = QAction("Escala", self)
        
        circle_action = QAction("Circulo", self)
        line_action = QAction("Reta", self)
        polygon_action = QAction("Polígono", self)

        cohen_action = QAction("Cohen", self)
        liang_action = QAction("Liang", self)
        exit_clipping_action = QAction("Sair do modo de recorte", self)

        line_action.triggered.connect(lambda: self.set_shape_type("line"))
        circle_action.triggered.connect(lambda: self.set_shape_type("circle"))
        polygon_action.triggered.connect(lambda: self.set_shape_type("polygon"))

        criation_action.triggered.connect(lambda: self.set_transformation_mode(None))
        translate_action.triggered.connect(lambda: self.set_transformation_mode("translate"))
        rotate_action.triggered.connect(lambda: self.set_transformation_mode("rotate"))
        scale_action.triggered.connect(lambda: self.set_transformation_mode("scale"))
        
        cohen_action.triggered.connect(lambda: self.set_clipping_mode("cohen"))
        liang_action.triggered.connect(lambda: self.set_clipping_mode("liang"))
        exit_clipping_action.triggered.connect(lambda: self.set_clipping_mode(None))

        transform_menu.addAction(criation_action)
        transform_menu.addAction(translate_action)
        transform_menu.addAction(rotate_action)
        transform_menu.addAction(scale_action)

        shapes_menu.addAction(line_action)
        shapes_menu.addAction(circle_action)
        shapes_menu.addAction(polygon_action)

        clipping_menu.addAction(cohen_action)
        clipping_menu.addAction(liang_action)
        clipping_menu.addAction(exit_clipping_action)

    def set_transformation_mode(self, mode):
        self.drawing_area.transformation_mode = mode
        self.drawing_area.clipping_mode = None
    
    def set_clipping_mode(self, mode):
        if mode is None:
            self.drawing_area.clip_window = None
        self.drawing_area.clipping_mode = mode
        self.drawing_area.transformation_mode = None

    def set_shape_type(self, shape_type):
        self.drawing_area.shape_type = shape_type

class CohenSutherland:
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def compute_code(self, x, y):
        code = self.INSIDE
        if x < self.x_min:
            code |= self.LEFT
        elif x > self.x_max:
            code |= self.RIGHT
        if y < self.y_min:
            code |= self.BOTTOM
        elif y > self.y_max:
            code |= self.TOP
        return code

    def clip_line(self, line):
        x1, y1 = line.start_point.x(), line.start_point.y()
        x2, y2 = line.end_point.x(), line.end_point.y()
        code1 = self.compute_code(x1, y1)
        code2 = self.compute_code(x2, y2)
        accept = False

        while True:
            if code1 == 0 and code2 == 0:
                accept = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                x, y = 0, 0
                out_code = code1 if code1 != 0 else code2
                if out_code & self.TOP:
                    x = x1 + (x2 - x1) * (self.y_max - y1) / (y2 - y1)
                    y = self.y_max
                elif out_code & self.BOTTOM:
                    x = x1 + (x2 - x1) * (self.y_min - y1) / (y2 - y1)
                    y = self.y_min
                elif out_code & self.RIGHT:
                    y = y1 + (y2 - y1) * (self.x_max - x1) / (x2 - x1)
                    x = self.x_max
                elif out_code & self.LEFT:
                    y = y1 + (y2 - y1) * (self.x_min - x1) / (x2 - x1)
                    x = self.x_min
                
                if out_code == code1:
                    x1, y1 = x, y
                    code1 = self.compute_code(x1, y1)
                else:
                    x2, y2 = x, y
                    code2 = self.compute_code(x2, y2)
        
        if accept:
            return Line(QPoint(int(x1), int(y1)), QPoint(int(x2), int(y2)))
        return None

class LiangBarsky:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def clip_line(self, line):
        x1, y1 = line.start_point.x(), line.start_point.y()
        x2, y2 = line.end_point.x(), line.end_point.y()
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - self.x_min, self.x_max - x1, y1 - self.y_min, self.y_max - y1]
        u1, u2 = 0, 1

        for i in range(4):
            if p[i] == 0 and q[i] < 0:
                return None
            if p[i] != 0:
                t = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, t)
                else:
                    u2 = min(u2, t)
        
        if u1 > u2:
            return None

        x1_clip = x1 + u1 * dx
        y1_clip = y1 + u1 * dy
        x2_clip = x1 + u2 * dx
        y2_clip = y1 + u2 * dy

        return Line(QPoint(int(x1_clip), int(y1_clip)), QPoint(int(x2_clip), int(y2_clip)))

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.click_points = []
        self.current_shape = None
        self.shape_type = 'line'
        self.transformation_mode = None
        self.clipping_mode = None
        self.selected_shape = None
        self.last_mouse_pos = None
        self.clipped_shapes = []
        self.clip_window = None 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        
        if self.clip_window:
            for shape in self.clipped_shapes:
                shape.draw(painter)
        else:
            for shape in self.shapes:
                shape.draw(painter)
        self.update()

    def mousePressEvent(self, event):
        if event.y() < 30:
            return

        if self.transformation_mode:
            print(self.transformation_mode)
            if not self.selected_shape:
                self.selected_shape = self.get_shape_at(event.pos())
                self.last_mouse_pos = event.pos()
            else:
                self.selected_shape = None
        elif self.clipping_mode in ["cohen", "liang"]:
            self.click_points.append(QPoint(event.x(), event.y()))
            if len(self.click_points) == 2:
                x_min = min(self.click_points[0].x(), self.click_points[1].x())
                y_min = min(self.click_points[0].y(), self.click_points[1].y())
                x_max = max(self.click_points[0].x(), self.click_points[1].x())
                y_max = max(self.click_points[0].y(), self.click_points[1].y())
                if self.clipping_mode == "cohen":
                    self.clip_window = CohenSutherland(x_min, y_min, x_max, y_max)
                elif self.clipping_mode == "liang":
                    self.clip_window = LiangBarsky(x_min, y_min, x_max, y_max)
                self.apply_clipping()
                self.click_points.clear()
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

    def apply_clipping(self):
        if self.clip_window:
            self.clipped_shapes = []
            for shape in self.shapes:
                if isinstance(shape, Line):
                    clipped_line = self.clip_window.clip_line(shape)
                    if clipped_line:
                        self.clipped_shapes.append(clipped_line)
        self.update()