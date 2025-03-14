from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from shape import Shape
from line import Line
from circle import Circle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Drawing App")
        self.setGeometry(100, 100, 1280, 720)

        self.drawing_area = DrawingArea()
        self.setCentralWidget(self.drawing_area)
        
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        
        new_action.triggered.connect(lambda: print("New File action triggered"))
        open_action.triggered.connect(lambda: print("Open File action triggered"))
        save_action.triggered.connect(lambda: print("Save File action triggered"))
        
        self.toolbar = self.addToolBar("Shapes")
        line_action = QAction("Line", self)
        circle_action = QAction("Circle", self)
        
        line_action.triggered.connect(lambda: self.set_shape_type('line'))
        circle_action.triggered.connect(lambda: self.set_shape_type('circle'))
        
        self.toolbar.addAction(line_action)
        self.toolbar.addAction(circle_action)
    
    def set_shape_type(self, shape_type):
        self.drawing_area.shape_type = shape_type
        print(f"Shape type set to {shape_type}")

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.shape_type = 'line'
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
        
        if self.current_shape:
            self.current_shape.draw(painter)

    def mousePressEvent(self, event):
        if event.y() < 30:
            return

        if not self.current_shape:
            if self.shape_type == 'line':
                self.current_shape = Line(QPoint(event.x(), event.y()))
            elif self.shape_type == 'circle':
                self.current_shape = Circle(QPoint(event.x(), event.y()))
        else:
            self.current_shape.update_end_point(QPoint(event.x(), event.y()))
            if self.current_shape.is_defined():
                self.shapes.append(self.current_shape)
                self.current_shape = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.current_shape:
            self.current_shape.update_end_point(QPoint(event.x(), event.y()))
            self.update()