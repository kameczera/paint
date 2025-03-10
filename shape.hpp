#ifndef SHAPE_HPP
#define SHAPE_HPP

#include "rgba.hpp"

class Shape {
    public:
        Rgba color;
        int count_clicks;
        Shape(Rgba color, int count_clicks) : color(color), count_clicks(count_clicks) {}
        virtual void draw(SDL_Renderer* renderer, bool erase) = 0;
        virtual void update_end_point(Vertice end) = 0;
        virtual bool is_defined() = 0;
        virtual ~Shape() {}
};

#endif