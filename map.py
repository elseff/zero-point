import pygame


class Map:
    def __init__(self, game):
        self.game = game
        self.game_map = self.load_map('assets/map.txt')
        self.start_tile_pos = (0, 0)
        self.tile_width = 40
        self.tile_height = 40
        self.tile_margin = 0
        self.tile_padding = 0
        self.tiles = []

        self.init_tiles()

    @staticmethod
    def load_map(path):
        file = open(path, 'r')
        data = file.read()
        file.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))

        return game_map

    def init_tiles(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile != '0':
                    self.tiles.append(
                        pygame.Rect(self.start_tile_pos[0] + (x * (self.tile_width + self.tile_margin)),
                                    self.start_tile_pos[1] + (y * (self.tile_height + self.tile_margin)),
                                    self.tile_width,
                                    self.tile_height)
                    )
                x += 1
            y += 1
        return self.tiles

    def render_tiles(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                tile_color = self.game.colors.GREEN

                if tile == '1':
                    tile_color = self.game.colors.RED
                if tile == '2':
                    tile_color = self.game.colors.WHITE
                if tile_color != self.game.colors.GREEN:
                    pygame.draw.rect(self.game.display, tile_color,
                                     (self.tile_padding + (x * (self.tile_width + self.tile_margin)) - int(self.game.scroll[0]),
                                      self.tile_padding + (y * (self.tile_height + self.tile_margin)) - int(self.game.scroll[1]),
                                      self.tile_width,
                                      self.tile_height))
                x += 1
            y += 1
