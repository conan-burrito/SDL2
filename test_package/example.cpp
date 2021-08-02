#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef __EMSCRIPTEN__
#include <emscripten.h>
#include <emscripten/html5.h>
#endif

#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 480

SDL_Renderer *renderer;
SDL_Event event;
int done = 0;
int count;

int randomInt(int min, int max) {
    return min + rand() % (max - min + 1);
}

void render(SDL_Renderer *renderer) {
    SDL_Rect rect;
    Uint8 r, g, b;

    /* Clear the screen */
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    /*  Come up with a random rectangle */
    rect.w = randomInt(64, 128);
    rect.h = randomInt(64, 128);
    rect.x = randomInt(0, SCREEN_WIDTH);
    rect.y = randomInt(0, SCREEN_HEIGHT);

    /* Come up with a random color */
    r = randomInt(50, 255);
    g = randomInt(50, 255);
    b = randomInt(50, 255);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);

    /*  Fill the rectangle in the color */
    SDL_RenderFillRect(renderer, &rect);

    /* update screen */
    SDL_RenderPresent(renderer);
}

void loop_iteration() {
  while (SDL_PollEvent(&event)) {
      if (event.type == SDL_QUIT) {
          done = 1;
      }
   }

   render(renderer);
   return ;
}

int main(int argc, char *argv[]) {
    SDL_Window *window;

    /* initialize SDL */
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("Could not initialize SDL: %s\n", SDL_GetError());
        /* Still return 0 - we want to be able to test on headless machines */
        return 0;
    }

    /* seed random number generator */
    srand(time(NULL));

    /* create window and renderer */
    window = SDL_CreateWindow(NULL, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_OPENGL);
    if (!window) {
        printf("Could not initialize Window: %s\n", SDL_GetError());
        return 1;
    }

    renderer = SDL_CreateRenderer(window, -1, 0);
    if (!renderer) {
        printf("Could not create renderer: %s\n", SDL_GetError());
        return 1;
    }

    /* Enter render loop, waiting for user to quit */
    count = 0;

#ifdef __EMSCRIPTEN__
    emscripten_set_main_loop(loop_iteration, 0, true);
#else
    while (!done && count++ < 5000) {
       loop_iteration();
       SDL_Delay(1);
    }
#endif

    /* shutdown SDL */
    SDL_Quit();

    return 0;
}
