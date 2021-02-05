from pygame.sprite import Sprite
import pygame


class Brick(Sprite):
    def __init__(self, game, x, y):
        super(Brick, self).__init__()
        self.game = game
        self.display = game.display
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, game.preference.brick[0], game.preference.brick[1])

    def update(self, *args, **kwargs) -> None:
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.display, (0, 0, 0), self.rect)
