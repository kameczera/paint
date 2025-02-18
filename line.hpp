#ifndef LINE_HPP
#define LINE_HPP

#include <cmath>
#include "vertice.hpp"
#include "rgba.hpp"

class Line {
    public:
        Vertice v[2];
        Rgba color;
        Line(Vertice v1, Vertice v2, Rgba color) : v({v1, v2}), color(color) {}

        void draw_line_DDA(SDL_Renderer *renderer) {
            SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), color.a());
            float dx = v[1].x() - v[0].x();
            float dy = v[1].y() - v[0].y();

            float xincr, yincr, x, y, step;
            
            x = v[0].x();
            y = v[0].y();

            if(std::abs(dx) > std::abs(dy)) step = std::abs(dx);
            else step = std::abs(dy);

            xincr = dx / step;
            yincr = dy / step;

            for(int i = 0; i < step; i++) {
                x += xincr;
                y += yincr;
                SDL_RenderDrawPoint(renderer, std::round(x), std::round(y));
            }
        }

        void draw_line_bresertian(SDL_Renderer *renderer) {
            SDL_SetRenderDrawColor(renderer, color.r(), color.g(), color.b(), color.a());
            int x = v[0].x();
            int y = v[0].y();

            int dx = v[1].x() - v[0].x();
            int dy = v[1].y() - v[0].y();

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