#ifndef CIRCUMFERENCE_HPP
#define CIRCUMFERENCE_HPP

#include "vertice.hpp"
#include "rgba.hpp"

class Circumference {
public:
    int radius;
    Point center;
    Rgba color;

    Circumference(int radius, Point center, Rgba color) : radius(radius), center(center), color(color) {}

    void draw_circumference(SDL_Renderer *renderer) {
        SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), color.a());
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
};

#endif