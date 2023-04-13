#include <SDL2/SDL.h>

#include <stdexcept>

int SCREEN_WIDTH = 1280;
int SCREEN_HEIGHT = 720;

void render(SDL_Renderer *renderer) {
   int row = 0, column = 0, x = 0, i = 0;
   SDL_Rect rect;

   SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
   SDL_RenderClear(renderer);

   for (; row < 8; row++) {
      column = row % 2;
      x = column;
      for (; column < 4 + (row % 2); column++) {
         SDL_SetRenderDrawColor(renderer,
                                i == 0 ? 255 : 0,
                                i == 1 ? 255 : 0,
                                i == 2 ? 255 : 0,
                                0xFF);

         rect.w = SCREEN_WIDTH / 8;
         rect.h = SCREEN_HEIGHT / 8;
         rect.x = x * rect.w;
         rect.y = row * rect.h;
         x = x + 2;
         SDL_RenderFillRect(renderer, &rect);
         i = (i + 1) % 3;
      }
   }

   SDL_RenderPresent(renderer);
}

int main(int argc, char *argv[]) {
   SDL_Window *window = nullptr;
   SDL_Renderer *renderer = nullptr;
   int done, count;
   SDL_Event event;

   SDL_LogSetAllPriority(SDL_LOG_PRIORITY_VERBOSE);

   /* initialize SDL */
   if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER | SDL_INIT_AUDIO | SDL_INIT_EVENTS) < 0) {
      SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_Init failed: %s", SDL_GetError());
      return 0;
   }

   // Fixes red screen on SGS3 and other android devices
   // https://bugzilla.libsdl.org/show_bug.cgi?id=2291k
   #if ANDROID
   SDL_GL_SetAttribute(SDL_GL_RED_SIZE, 5);
   SDL_GL_SetAttribute(SDL_GL_GREEN_SIZE, 6);
   SDL_GL_SetAttribute(SDL_GL_BLUE_SIZE, 5);
   //   SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 0);
   #endif

   /* create window and renderer */
   window = SDL_CreateWindow("cross-test",
                             SDL_WINDOWPOS_CENTERED,
                             SDL_WINDOWPOS_CENTERED,
                             SCREEN_WIDTH,
                             SCREEN_HEIGHT,
                             SDL_WINDOW_ALLOW_HIGHDPI | SDL_WINDOW_SHOWN);
   if (!window) {
      SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_CreateWindow failed: %s", SDL_GetError());
      return 1;
   }

   renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC);
   if (!renderer) {
      SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_CreateRenderer failed: %s", SDL_GetError());
      return 1;
   }

   const char *path = SDL_GetBasePath();
   if (path != nullptr) {
      SDL_LogDebug(SDL_LOG_CATEGORY_APPLICATION, "SDL_GetBasePath: %s", path);
   } else {
      SDL_LogDebug(SDL_LOG_CATEGORY_APPLICATION, "SDL_GetBasePath: null");
   }

   SDL_GetRendererOutputSize(renderer, &SCREEN_WIDTH, &SCREEN_HEIGHT);

   /* Enter render loop, waiting for user to quit */
   done = 0;
   count = 0;

   while (!done && count++ < 6000) {
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            done = 1;
         } else if (event.type == SDL_KEYUP) {
            if (event.key.keysym.sym == SDLK_AC_BACK) {
               done = 1;
            }
         }
      }
      render(renderer);
      SDL_Delay(10);
   }

   /* shutdown SDL */
   SDL_Quit();

   return 0;
}
