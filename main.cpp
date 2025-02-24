#include <SDL2/SDL.h>
#include <iostream>
#include <stdio.h>
#include "vertice.hpp"
#include "line.hpp"
#include "rgba.hpp"
#include "circumference.hpp"

#define SCREEN_WIDTH 1280
#define SCREEN_HEIGHT 720

int main(int argc, char **argv)
{
    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        printf("Error: SDL failed to initialize\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("SLD test", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, 0);
    if (!window)
    {
        printf("Error: Failed to open window\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer)
    {
        printf("Error: Failed to create renderer\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    bool running = true;
    int click = false;
    Vertice* init = (Vertice*) malloc(sizeof(Vertice));
    Vertice* end = (Vertice*) malloc(sizeof(Vertice));

    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_RenderClear(renderer);
    Vertice v1 = Vertice(100, 100);
    Vertice v2 = Vertice(500, 200);
    Line line = Line(v1, v2, Rgba(255, 255, 255, 255));
    line.draw_line_bresertian(renderer);
    Vertice v4 = Vertice(500, 100);
    Line line2 = Line(v4, v1, Rgba(255, 255, 255, 255));
    line2.draw_line_bresertian(renderer);
    
    Point p = Point(500, 300);
    Circumference circ = Circumference(20, p, Rgba(255, 255, 255, 255));
    circ.draw_circumference(renderer);
    SDL_RenderPresent(renderer);

    while (running)
    {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (SDL_QUIT == event.type) {
                running = false;
            }
            if (SDL_MOUSEMOTION == event.type) {
                if(click == true) {
                }
            }
            if (SDL_MOUSEBUTTONUP == event.type) {
                click = false;
                int x, y;
                SDL_GetMouseState(&x, &y);
                *end = Vertice(x, y);
                Line l = Line(*init, *end, Rgba(255, 255, 255, 255));
                std::cout << init->e[0] << " " << init->e[1] << " " << end->e[0] << " " << end->e[1] << " ";
                l.draw_line_bresertian(renderer);
            }
            if(SDL_MOUSEBUTTONDOWN == event.type) {
                click = true;
                int x, y;
                SDL_GetMouseState(&x, &y);
                *init = Vertice(x, y);
            }
        }
        SDL_RenderPresent(renderer);
    }

    return 0;
}