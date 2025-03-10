#include <SDL2/SDL.h>
#include <iostream>
#include <vector>
#include "vertice.hpp"
#include "line.hpp"
#include "circumference.hpp"
#include "rgba.hpp"
#include "type.hpp"
#include "square.hpp"

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

    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);

    std::vector<Shape*> shapes;
    Shape* currentShape = nullptr;
    Type shapeType = LINE;

    while (running)
    {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (SDL_QUIT == event.type) {
                running = false;
            }
            if (SDL_MOUSEMOTION == event.type && currentShape) {
                int x, y;
                SDL_GetMouseState(&x, &y);
                currentShape->update_end_point(Vertice(x, y));
            }
            if (SDL_MOUSEBUTTONDOWN == event.type) {
                if (!currentShape) {
                    int x, y;
                    SDL_GetMouseState(&x, &y);
                    switch (shapeType) {
                        case LINE:
                            currentShape = new Line(Vertice(x, y), Vertice(x, y), Rgba(255, 255, 255, 255));
                            break;
                        case CIRCLE:
                            currentShape = new Circumference(0, Point(x, y), Rgba(255, 255, 255, 255));
                            break;
                        case SQUARE:
                            currentShape = new Square(Vertice(x, y), Rgba(255, 255, 255, 255));
                        default:
                            break;
                    }
                } else {
                    int x, y;
                    SDL_GetMouseState(&x, &y);
                    currentShape->update_end_point(Vertice(x, y));
                    currentShape->count_clicks++;
                    if(currentShape->is_defined()) {
                        shapes.push_back(currentShape);
                        currentShape = nullptr;
                    }
                }
            }
            if (event.type == SDL_KEYDOWN) {
                switch (event.key.keysym.sym) {
                    case SDLK_c:
                        shapeType = CIRCLE;
                        break;
                    case SDLK_l:
                        shapeType = LINE;
                        break;
                    case SDLK_s:
                        shapeType = SQUARE;
                        break;
                    case SDLK_t:
                        shapeType = TRIANGLE;
                        break;
                    default:
                        break;
                }
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Desenha todas as formas
        for (Shape* shape : shapes) {
            shape->draw(renderer, false);
        }

        if (currentShape) {
            currentShape->draw(renderer, false);
        }

        SDL_RenderPresent(renderer);
    }

    for (Shape* shape : shapes) {
        delete shape;
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}