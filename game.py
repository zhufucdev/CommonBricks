import pygame

from brick import Brick
from bullet import Bullet
from preference import Preference
from wall import Wall


class Game:
    def __init__(self, preference):
        self.preference = preference
        self.display = pygame.display.set_mode(preference.display)
        pygame.display.set_caption("Bricks")
        # Game Properties
        self.running = True
        self.bricks = pygame.sprite.Group()
        self.wall = Wall(self)
        self.bullet = Bullet(self)

        pygame.init()

        self.start()
        self.main_loop()

    def main_loop(self):
        def update():
            self._update()
            self._flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP and event.key == pygame.K_r:
                    self.start()
            update()

    def start(self):
        brick = self.preference.brick
        margin = self.preference.margin

        self.bricks = pygame.sprite.Group()
        self.wall = Wall(self)
        self.bullet = Bullet(self)
        for x in range(self.preference.army[0]):
            for y in range(self.preference.army[1]):
                b = Brick(self, x * (brick[0] + margin[0]) + margin[0], y * (brick[1] + margin[1]) + margin[1])
                self.bricks.add(b)

    def _update(self):
        self.wall.update()
        self.bricks.update()
        self.bullet.update()

    def _flip(self):
        self.display.fill((255, 255, 255))

        self.wall.draw()
        self.bullet.draw()
        for brick in self.bricks:
            brick.draw()
        pygame.display.flip()


if __name__ == '__main__':
    instance = Game(Preference())
