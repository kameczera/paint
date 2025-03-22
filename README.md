# 2D Graphics Algorithms Implementation

## Introduction
This project is a practical implementation of fundamental 2D computer graphics algorithms, developed as part of the Computer Graphics course at PUC Minas. The application provides a graphical interface for drawing and manipulating geometric shapes, implementing essential transformations, rasterization techniques, and clipping algorithms.

## Features
The application includes the following functionalities:

### **Geometric Transformations (2D)**
- Translation
- Rotation
- Scaling
- Reflections (X, Y, XY)

### **Rasterization Algorithms**
- Line Drawing: DDA and Bresenham
- Circle Drawing: Bresenham

### **Clipping Algorithms**
- Cohen-Sutherland (Region Coding)
- Liang-Barsky (Parametric Equation)

## Data Structure
The data structure supports:
- **Points/Vertices**
- **Lines**
- **Polygons**

These elements can be selected using a rectangular region indicated via the graphical interface.

## User Interaction
To enhance usability, keyboard input is avoided. Instead, user input is handled through mouse clicks or similar interaction events in the Drawing Area.

---

## Installation and Execution

### **Prerequisites**
Ensure you have Python installed on your system (version 3.8+ recommended).

### **Setup Instructions**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/computer-graphics.git
   cd computer-graphics
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### **Usage**
- Use the buttons to select different shapes (Line, Circle, Polygon).
- Apply transformations (Translation, Rotation, Scaling, Reflection) with user-defined values.
- Use clipping options to crop elements within the defined regions.
- The graphical interface provides an interactive Drawing Area to manipulate elements visually.

## Technologies Used
- **Python** (Main language)
- **PyQt5** (GUI framework)
- **NumPy** (Mathematical operations)

## Author
Developed as part of the **Computer Graphics** course at **PUC Minas**.

## License
This project is open-source and available under the MIT License.

