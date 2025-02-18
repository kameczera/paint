#ifndef RGBA_HPP
#define RGBA_HPP

class Rgba {
    public:
        int color[4];
        Rgba(int r, int g, int b, int a) : color({r, g, b, a}) {}
        int r() { return color[0]; }
        int g() { return color[1]; }
        int b() { return color[2]; }
        int a() { return color[3]; }
};


#endif