import sys

import pygame

from properties import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.player_image = pygame.image.load('images/cyborg.png')
        self.player_location = [350, 50]
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.player_y_momentum = 0
        self.player_rect = pygame.Rect(self.player_location[0],
                                       self.player_location[1],
                                       self.player_image.get_width(),
                                       self.player_image.get_height())
        self.is_player_jump = False
        self.map = []
        self.tile_width = 40
        self.tile_height = 40
        self.tile_margin = 1
        self.tile_padding = 0
        self.game_map = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '2', '2', '0', '0', '0', '2', '2', '2', '0', '0', '0', '2', '2', '2', '0', ],
            ['0', '0', '0', '0', '0', '2', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '2', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ],
            ['2', '2', '2', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', ],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', ]
        ]

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)

        return hit_list

    def move(self, rect, movement, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            if movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            if movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True

        return rect, collision_types

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    if event.key == pygame.K_UP:
                        self.jumping = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.moving_right = False
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                    if event.key == pygame.K_UP:
                        self.jumping = False

            self.screen.fill(BLACK)
            y = 0
            tile_rects = []
            for row in self.game_map:
                x = 0
                for tile in row:
                    tile_color = GREEN

                    if tile == '1':
                        tile_color = RED
                    if tile == '2':
                        tile_color = WHITE
                    if tile_color != GREEN:
                        pygame.draw.rect(self.screen, tile_color,
                                         (self.tile_padding + (x * (self.tile_width + self.tile_margin)),
                                          self.tile_padding + (y * (self.tile_height + self.tile_margin)),
                                          self.tile_width,
                                          self.tile_height))
                        tile_rects.append(
                            pygame.Rect(self.tile_padding + (x * (self.tile_width + self.tile_margin)),
                                        self.tile_padding + (y * (self.tile_height + self.tile_margin)),
                                        self.tile_width,
                                        self.tile_height))
                    x += 1
                y += 1

            player_movement = [0, 0]
            if self.moving_right:
                player_movement[0] += 4
            if self.moving_left:
                player_movement[0] -= 4
            player_movement[1] += self.player_y_momentum

            self.player_rect, collisions = self.move(self.player_rect, player_movement, tile_rects)

            if self.player_rect.y > screen_height - self.player_image.get_height():
                self.player_y_momentum = 0
                self.player_rect.y = screen_height - self.player_image.get_height()

            if not collisions['bottom'] and not collisions['top']:
                self.player_y_momentum += 0.2
            else:
                self.player_y_momentum = 0

            if self.jumping:
                if collisions['bottom']:
                    self.player_y_momentum = -6

            self.screen.blit(self.player_image, (self.player_rect.x, self.player_rect.y))
            pygame.display.update()
            self.clock.tick(fps)
            pygame.display.set_caption(str(self.clock.get_fps()))


if __name__ == '__main__':
    Game().run()
