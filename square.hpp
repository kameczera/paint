#ifndef SQUARE_HPP
#define SQUARE_HPP

#include "vertice.hpp"
#include "shape.hpp"
#include "rgba.hpp"

class Square : public Shape {
    public:
    Vertice v[4];
    Square(Vertice v1, Rgba color) : Shape(color, 1), v({v1, v1, v1, v1}) {}

    void draw(SDL_Renderer *renderer, bool erase) override {
        if (!erase) SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), color.a());
        else SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
        for(int i = 0; i < count_clicks - 1; i++) bres(v[i], v[i + 1], renderer, erase);
        bres(v[count_clicks - 1], v[0], renderer, erase);
    }

    void update_end_point(Vertice end) override {
        v[count_clicks] = end;
    }

    bool is_defined() override {
        if(count_clicks == 4) return true;
        return false;
    }

    void bres(Vertice v1, Vertice v2, SDL_Renderer *renderer, bool erase) {
        int x = v1.x();
        int y = v1.y();

        int dx = v2.x() - v1.x();
        int dy = v2.y() - v1.y();
        int p, c1, c2, xincr, yincr;

        SDL_RenderDrawPoint(renderer, x, y);
    
        if(dx >= 0) xincr = 1;
        else {
            xincr = -1;
            dx = - dx;
        }
        if(dy >= 0) yincr = 1;
        else {
            yincr = -1;
            dy = -dy;
        }
        if(dx > dy) {
            p = 2 * dy - dx;
            c1 = 2 * dy;
            c2 = 2 * (dy - dx);

            for(int i = 0; i < dx; i++) {
                x += xincr;
                if(p < 0) p += c1;
                else {
                    p += c2;
                    y += yincr;
                }
                SDL_RenderDrawPoint(renderer, x, y);
            }
        } else {
            p = 2 * dx - dy;
            c1 = 2 * dx;
            c2 = 2 * (dx - dy);

            for(int i = 0; i < dy; i++) {
                y += yincr;
                if(p < 0) p += c1;
                else {
                    p += c2;
                    x += xincr;
                }
                SDL_RenderDrawPoint(renderer, x, y);
            }
        }
    }
    
};


#endif