import random
import sys

from map import *
from player import *
from properties import *


class Game:
    def __init__(self):
        pygame.init()
        properties = Properties()
        self.colors = properties.colors
        self.fps = properties.fps
        self.current_fps = self.fps
        self.screen_width = properties.screen_width
        self.screen_height = properties.screen_height
        self.title = properties.title
        self.render_scale = properties.render_scale

        pygame.display.set_caption(self.title)

        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))
        self.display = pygame.Surface((self.screen_width / self.render_scale,
                                       self.screen_height / self.render_scale))
        self.clock = pygame.time.Clock()

        self.map = Map(self)

        self.scroll = [0, 0]
        self.player = Player.by_location(self, [350, 100])
        self.objects = [[[random.randint(-200, 800)
                          for a in range(2)] + [random.randint(50, 150) for d in range(2)]
                         if b != 0
                         else random.randint(10, 50) / 100
                         for b in range(2)]
                        for c in range(50)]
        print(self.objects)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill(self.colors.WHITE)

            self.scroll_update()

            for obj in self.objects:
                obj_rect = pygame.Rect(obj[1][0] - self.scroll[0] * obj[0],
                                       obj[1][1] - self.scroll[1] * obj[0],
                                       obj[1][2],
                                       obj[1][3])
                surf = pygame.Surface((obj[1][2], obj[1][3]))
                surf.set_alpha(128)
                surf.fill((45, obj[0] * 500, 78, 0.8))
                self.display.blit(surf, (obj[1][0] - self.scroll[0] * obj[0],
                                       obj[1][1] - self.scroll[1] * obj[0]))
                # pygame.draw.rect(self.display, (45, obj[0] * 500, 78, 0.5), obj_rect)

            self.map.render_tiles()

            collisions = self.player.update(events, self.map.tiles)

            self.apply_gravity(collisions)

            self.player.render()

            surface = pygame.transform.scale(self.display, (self.screen_width, self.screen_height))
            self.screen.blit(surface, (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)
            self.current_fps = self.clock.get_fps()

    def scroll_update(self):
        self.scroll[0] += (self.player.rect.x - self.scroll[0] - self.screen_width / (
                self.render_scale * 2) + self.player.image.get_width() / 2) / 10
        self.scroll[1] += (self.player.rect.y - self.scroll[1] - self.screen_height / (
                self.render_scale * 2) + self.player.image.get_height() / 2) / 10

    def apply_gravity(self, collisions):
        if not collisions['bottom'] and not collisions['top']:
            self.player.vertical_momentum += 0.2
        else:
            self.player.vertical_momentum = 0
        if self.player.vertical_momentum > 10:
            self.player.vertical_momentum = 10


if __name__ == '__main__':
    Game().run()
