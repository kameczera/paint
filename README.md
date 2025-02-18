# Paint Application - Computer Graphics Project (PUC-MG)

## Introduction
This project is part of the Computer Graphics course at PUC-MG. The goal is to develop a basic paint application that allows users to draw using geometric transformations, rasterization algorithms, and clipping techniques. The application must provide a graphical interface with mouse-based input, avoiding the use of keyboard commands.

## Features
The application implements the following features:

### 2D Geometric Transformations
- **Translation**
- **Rotation**
- **Scaling**
- **Reflections** (X, Y, and XY axes)
- **All transformations use user-defined values (no fixed values)**

### Rasterization Algorithms
- **Line Drawing**: DDA and Bresenham algorithms
- **Circle Drawing**: Bresenham's algorithm

### Clipping Algorithms
- **Cohen-Sutherland** (Region coding method)
- **Liang-Barsky** (Parametric equation method)

### Data Structure
The application supports:
- **Vertices/Points**
- **Lines**
- **Polygons**
- **Selection via rectangular region** (using mouse input)

## Requirements
- **C++ Compiler** (g++)
- **SDL2 Library**
- **Windows Operating System** (for executable and installer support)

## Compilation and Execution
### Compile:
```sh
 g++ -Isrc/Include -Lsrc/lib -o main main.cpp -lmingw32 -lSDL2main -lSDL2
```

### Run:
```sh
 main.exe
```

## Deliverables
The following items must be submitted:
1. **Fully functional source code** (well-commented, indented, and organized)
2. **Video demonstration** (showing execution and explaining features)
3. **Executable file** (or a downloadable link)
4. **Windows Installer** (with required libraries and components)

## Evaluation Criteria
- Code quality and correctness
- Clarity and organization of the presentation
- Proper use of the Portuguese language in documentation and video explanation
- **Late submissions will not be accepted**
- **The project must be complete, including the source code, otherwise it will not be graded**
