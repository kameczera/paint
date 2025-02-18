#include <SDL2/SDL.h>
#include <stdio.h>
#include "vertice.hpp"
#include "line.hpp"
#include "rgba.hpp"

#define SCREEN_WIDTH 1280 
#define SCREEN_HEIGHT 720

void action() {

}

int main(int argc, char** argv){
    if(SDL_Init(SDL_INIT_VIDEO) < 0){
        printf("Error: SDL failed to initialize\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("SLD test", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, 0);
    if(!window){
        printf("Error: Failed to open window\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if(!renderer){
        printf("Error: Failed to create renderer\nSDL Error: '%s'\n", SDL_GetError());
        return 1;
    }

    bool running = true;
    int init;
    int end;
    while(running){
        SDL_Event event;
        while(SDL_PollEvent(&event)){
            switch(event.type){
                case SDL_QUIT:
                    running = false;
                    break;
                case SDL_MOUSEBUTTONDOWN:
                    action();
                case SDL_MOUSEBUTTONUP:
                default:
                    break;
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
        SDL_RenderClear(renderer);

        Vertice v1 = Vertice(100, 100);
        Vertice v2 = Vertice(500, 200);

        Line line = Line(v1, v2, Rgba(255, 255, 255, 255));
        line.draw_line_bresertian(renderer);
        Vertice v4 = Vertice(500, 100);
        Line line2 = Line(v4, v1, Rgba(255, 255, 255, 255));
        line2.draw_line_bresertian(renderer);
        
        SDL_RenderPresent(renderer);
    }

    return 0;
}