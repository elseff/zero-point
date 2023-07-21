import pygame


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.image = pygame.image.load('assets/images/cyborg.png')
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 5
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.vertical_momentum = 0
        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}

    @classmethod
    def by_location(cls, game, player_location):
        x = player_location[0]
        y = player_location[1]
        return cls(game, x, y)

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)

        return hit_list

    def update(self, events, tiles):
        self.check_input(events)
        return self.move(tiles)

    def render(self):
        self.game.display.blit(self.image, (self.rect.x - self.game.scroll[0], self.rect.y - self.game.scroll[1]))

    def check_input(self, events):
        for event in events:
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

    def move(self, tiles):
        movement = [0, 0]
        if self.moving_right:
            movement[0] += self.speed
        if self.moving_left:
            movement[0] -= self.speed
        movement[1] += self.vertical_momentum

        self.check_jump()

        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                self.collisions['right'] = True
            if movement[0] < 0:
                self.rect.left = tile.right
                self.collisions['left'] = True
        self.rect.y += movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                self.collisions['bottom'] = True
            if movement[1] < 0:
                self.rect.top = tile.bottom
                self.collisions['top'] = True

        return self.collisions

    def check_jump(self):
        if self.jumping:
            if self.collisions['bottom']:
                self.vertical_momentum = -6
