import pygame, sys
from properties import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(GRAY)

            pygame.display.update()
            self.clock.tick(fps)

Game().run()
