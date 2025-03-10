#ifndef CIRCUMFERENCE_HPP
#define CIRCUMFERENCE_HPP

#include "vertice.hpp"
#include "rgba.hpp"
#include "shape.hpp"
#include <cmath>

class Circumference : public Shape {
public:
    int radius;
    Point center;
    
    Circumference(int radius, Point center, Rgba color) : Shape(color, 1), radius(radius), center(center) {}

    void draw(SDL_Renderer *renderer, bool erase) override {
        if(!erase) SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), color.a());
        else SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
        int x = 0;
        int y = radius;
        int p = 3 - 2 * radius;
        plot_simetrics(x, y, center.x(), center.y(), renderer);

        while (x < y) {
            if (p < 0)
                p += 4 * x + 6;
            else {
                p += 4 * (x - y) + 10;
                y--;
            }
            x++;
            plot_simetrics(x, y, center.x(), center.y(), renderer);
        }
    }

    void update_end_point(Vertice end) override {
        radius = sqrt(pow(end.x() - center.x(), 2) + pow(end.y() - center.y(),2));
    }

    void plot_simetrics(int x, int y, int cx, int cy, SDL_Renderer *renderer) {
        SDL_RenderDrawPoint(renderer, cx + x, cy + y);
        SDL_RenderDrawPoint(renderer, cx + x, cy - y);
        SDL_RenderDrawPoint(renderer, cx - x, cy + y);
        SDL_RenderDrawPoint(renderer, cx - x, cy - y);
        SDL_RenderDrawPoint(renderer, cx + y, cy + x);
        SDL_RenderDrawPoint(renderer, cx + y, cy - x);
        SDL_RenderDrawPoint(renderer, cx - y, cy + x);
        SDL_RenderDrawPoint(renderer, cx - y, cy - x);
    }

    bool is_defined() override {
        if(count_clicks == 2) return true;
        return false;
    }
};

#endif