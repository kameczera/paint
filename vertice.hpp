#ifndef VERTICE_HPP
#define VERTICE_HPP 

class Vertice {
    // private:
    
    public:
        int e[2];
        Vertice(int x, int y) : e({x, y}) {}
        int x() { return e[0]; }
        int y() { return e[1]; }
};

using Point = Vertice;




#endif